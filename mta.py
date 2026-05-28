import torch
import torch.nn.functional as F
import torchvision.transforms as transforms


def make_views(image, n_views):
    """return one original image + RandomResizedCrop n_views"""
    normalize = transforms.Normalize(
        mean=[0.48145466, 0.4578275, 0.40821073],
        std=[0.26862954, 0.26130258, 0.27577711]
    )
    base_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        normalize,
    ])
    crop_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.ToTensor(),
        normalize,
    ])

    original = base_transform(image).unsqueeze(0)
    crops = torch.stack([crop_transform(image) for _ in range(n_views)])
    return torch.cat([original, crops], dim=0)
    

def gaussian_kernel(mu, bandwidth, datapoints):
    """estimate gaussian kernel density"""
    dist = torch.norm(datapoints - mu, dim=-1, p=2)
    return torch.exp(-dist ** 2 / (2 * bandwidth ** 2))


def solve_mta(model, inputs, args):
    """MTA: compute inlierness score and return robust mode m*"""
    with torch.no_grad():
        with torch.cuda.amp.autocast():
            image_features = model.encode_image(inputs)

    image_features = image_features.float()
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    lambda_y = args.lambda_y
    lambda_q = args.lambda_q
    max_iter = 5
    temperature = 1

    batch_size = image_features.shape[0]

    # compute bandwidth based on KNN
    dist = torch.cdist(image_features, image_features)
    sorted_dist, _ = torch.sort(dist, dim=1)
    k = max(1, int(0.3 * (image_features.shape[0] - 1)))
    selected_distances = sorted_dist[:, 1:k + 1] ** 2
    mean_distance = torch.mean(selected_distances, dim=1)
    bandwidth = torch.sqrt(0.5 * mean_distance)

    affinity_matrix = (image_features @ image_features.t() / temperature).softmax(1)

    # initialization
    y = torch.ones(batch_size, device=image_features.device) / batch_size
    mode = image_features[0]

    convergence = False
    th = 1e-6
    iter_count = 0

    while not convergence:
        density = gaussian_kernel(mode, bandwidth, image_features)

        # inlierness step
        conv_inlierness = False
        i = 0
        while not conv_inlierness:
            i += 1
            old_y = y
            weighted_affinity = affinity_matrix * y.unsqueeze(0)
            y = F.softmax(
                1 / lambda_y * (density + lambda_q * torch.sum(weighted_affinity, dim=1)),
                dim=-1
            )
            if torch.norm(old_y - y) < th or i >= max_iter:
                conv_inlierness = True

        # mode step
        conv_mode = False
        i = 0
        while not conv_mode:
            i += 1
            old_mode = mode
            density = gaussian_kernel(mode, bandwidth, image_features)
            weighted_density = density * y
            mode = torch.sum(weighted_density.unsqueeze(1) * image_features, dim=0) / torch.sum(weighted_density)
            mode /= mode.norm(p=2, dim=-1)
            if torch.norm(old_mode - mode) < th or i >= max_iter:
                conv_mode = True

        iter_count += 1
        if iter_count >= max_iter:
            convergence = True

    return mode
