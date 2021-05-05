# -*- coding: utf-8 -*-
import torch
from torch import nn, optim
from TestModels.app_test import place
from PIL import Image
from torchvision import transforms
import torchvision
import os


def inference(image_path, model_path):
    # 获取输入
    image = Image.open(image_path)
    image = image.convert('RGB')
    tf = transforms.Compose([
        # transforms.CenterCrop([800, 800]),
        transforms.Resize([224, 224]),
        transforms.ToTensor(),
        # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = tf(image)
    image = image.unsqueeze(dim=0).cuda()
    # 下载模型
    net = torchvision.models.resnet18(pretrained=True)
    num_fc_ftr = net.fc.in_features
    net.fc = torch.nn.Linear(num_fc_ftr, 6)
    # 加载训练权重
    device = place.get_default_device()
    place.to_device(net, device)
    net.load_state_dict(torch.load(model_path, map_location=device))
    net.eval()
    # 预测
    output = net(image)
    pre = output.argmax(dim=1).item()
    return pre

