# vision_model.py

import sys
from PIL import Image
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
from BLIP.models.blip_vqa import blip_vqa

def load_image(path, image_size, device):
    raw_image = Image.open(path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ])
    image = transform(raw_image).unsqueeze(0).to(device)
    return image

def get_answer(img_path, device, img_size):
    image = load_image(img_path, img_size, device)
    model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth'
    model = blip_vqa(pretrained=model_url, image_size=img_size, vit='base')
    model.eval()
    model = model.to(device)
    question = 'what kind of damage done in the structure/house, give answer ?'
    with torch.no_grad():
        answer = model(image, question, train=False, inference='generate') 
    print(answer[0])
    return answer
