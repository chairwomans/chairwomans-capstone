import torch
from types import SimpleNamespace
from PIL import Image
import clip
from domain_prompts import domain_prompts
from mta import make_views, solve_mta


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, _ = clip.load("ViT-B/32", device=device)
model.eval()


def _build_domain_features():
    features = {}
    for domain, prompts in domain_prompts.items():
        tokens = clip.tokenize(prompts).to(device)
        with torch.no_grad():
            embeds = model.encode_text(tokens)
            embeds = embeds / embeds.norm(dim=1, keepdim=True)
        features[domain] = embeds.mean(dim=0)

    domain_features = torch.stack(list(features.values()))
    domain_names = list(features.keys())
    return domain_features, domain_names

domain_features, domain_names = _build_domain_features()


def estimate_domain(
    image: Image.Image,
    n_views: int = 127,
    top_k: int = 5,
) -> dict:
    
    inputs = make_views(image, n_views).to(device)

    args = SimpleNamespace(lambda_y=0.2, lambda_q=4)
    mode = solve_mta(model, inputs, args)

    df = domain_features.float()
    df = df / df.norm(dim=1, keepdim=True)
    logit_scale = model.logit_scale.exp()
    similarity = mode @ df.t() * logit_scale
    domain_weights = similarity.softmax(dim=-1)

    result = {
        name: round(weight.item(), 4)
        for name, weight in zip(domain_names, domain_weights)
    }
    sorted_result = dict(
        sorted(result.items(), key=lambda x: x[1], reverse=True)
    )
    return dict(list(sorted_result.items())[:top_k])
