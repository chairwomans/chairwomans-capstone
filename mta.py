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
