# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 20:41:53 2019

@author: 周义青
"""
import torch.optim as optim
import torch
import os
import torch.nn as nn
import numpy as np
from PIL import Image
from torchvision import transforms as T
from torch.utils.data import DataLoader, Dataset
import cv2
import torchvision.models as models

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

transform = T.Compose([
    T.Resize(100),
    T.ToTensor(),
    T.Normalize((0.5, 0.5, 0.5), (0.4, 0.4, 0.4))
])


# 对训练集和测试集分别进行图片分割(垂直切割5等分)
def get_crop_imgs(mdir, imgName):
    img = cv2.imread(os.path.join(mdir, imgName))
    img = np.array(img)
    h = img.shape[0]
    img = Image.fromarray(img)
    childImages = []
    if mdir == 'train':
        childLabels = [x for x in imgName[-9:-4]]
    for i in range(5):
        childImg = img.crop((i * 30, 0, i * 30 + 30, 0 + h))
        childImages.append(childImg)
    if mdir == 'train':
        return (childImages, childLabels)
    else:
        return childImages


# 将图片转换成字符数据和标签分开
def data_convert():
    # trainImages = [get_crop_imgs('train', imgName)[0] for imgName in os.listdir('train')]
    # trainLabels = [get_crop_imgs('train', imgName)[-1] for imgName in os.listdir('train')]
    # trainLabels, trainImages = sum(trainLabels, []), sum(trainImages, [])
    # newLabels = []
    # print(1)
    # for label in trainLabels:
    #     if 48 <= ord(label) <= 57:
    #         newLabels.append((ord(label) - 48))
    #     elif 65 <= ord(label) <= 90:
    #         newLabels.append((ord(label) - 55))
    #     else:
    #         newLabels.append((ord(label) - 61))
    # torch.save(trainImages, 'trainImages.txt')
    # torch.save(trainLabels, 'trainLabels.txt')
    # torch.save(newLabels, 'newLabels.txt')

    # testDir = [str(x) + '.jpg' for x in sorted([int(x.split('.')[0]) for x in os.listdir('test')])]
    # testImages = [get_crop_imgs('test', imgName) for imgName in testDir]
    testImages = [get_crop_imgs('./', '1.jpg') ]
    testImages = sum(testImages, [])
    torch.save(testImages, 'testImages.txt')

    return ( testImages)


# data_convert()

# 将每张图片构建为一个对象(含读取方法，总数据长度等方法)
class dataSet(Dataset):
    def __init__(self, images, labels=None, transforms=None):
        #        super().__init__()
        self.images = images
        if labels != None:
            self.labels = labels
        self.transforms = transforms

    def __getitem__(self, index):
        image = self.images[index]
        try:
            label = self.labels[index]
        except:
            pass
        if self.transforms:
            data = self.transforms(image)
        else:
            imageArray = np.asarray(image)
            data = torch.from_numpy(imageArray)
        try:
            return (data, label)
        except:
            return data

    def __len__(self, ):
        return len(self.images)


# 定义resnet18模型
def initialize_model(num_classes=62, use_pretrained=False):
    model_ft = models.resnet18(pretrained=use_pretrained)  # pretrained（bool）–如果为True，则返回在ImageNet上进行预训练的模型
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, num_classes)  # 输出层（512,1000） -> (512,62)
    return model_ft


# 进行resNet18模型的训练
def train():
    trainImages, newLabels = torch.load('trainImages.txt'), torch.load('newLabels.txt')
    trainSet = dataSet(trainImages, newLabels, transform)
    trainLoader = DataLoader(trainSet, batch_size=128, shuffle=True)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(device)
    model = initialize_model(num_classes=62, use_pretrained=False)
    model.to(device)
    model.train()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss = 0.0
    epoch = 0
    while epoch < 20:
        runningLoss = 0.0
        for i, data in enumerate(trainLoader):
            inputs, labels = data[0].to(device), data[1].to(device)
            optimizer.zero_grad()
            outs = model(inputs)
            loss = criterion(outs, labels)
            loss.backward()
            optimizer.step()
            runningLoss += loss.item()
            print('epoch %5d: batch: %5d, loss: %f' % (epoch, i, runningLoss))
            runningLoss = 0.0
        print('Save checkpoint...')
        torch.save({'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'loss': loss}, 'm.pth')
        epoch += 1


# train()

# 对模型进行测试(预测)
def predict_test():
    testImages = torch.load('testImages.txt')
    testSet = dataSet(testImages, None, transform)
    testLoader = DataLoader(testSet, batch_size=5, shuffle=False)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(device)
    model = initialize_model(num_classes=62, use_pretrained=False)
    model.to(device)
    checkpoint = torch.load('m.pth')
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    predictions = []
    print(2)
    for i, data in enumerate(testLoader):
        inputs = data.to(device)
        outputs = model(inputs)
        _, predict = torch.max(outputs.data, 1)
        predict = np.array(predict.cpu())
        predict = list(predict)
        predictions.append(predict)
        print(3)
    newPredictions = []
    for i in range(len(predictions)):
        newPredict = []
        for j in range(len(predictions[0])):
            if 0 <= predictions[i][j] <= 9:
                newPredict.append(chr(predictions[i][j] + 48))
            elif 10 <= predictions[i][j] <= 35:
                newPredict.append(chr(predictions[i][j] + 55))
            elif 36 <= predictions[i][j] <= 61:
                newPredict.append(chr(predictions[i][j] + 61))
        strPredict = ''.join(newPredict)
        print(strPredict)
        newPredictions.append(strPredict)

    #torch.save(newPredictions, 'newPredictions.txt')
    return newPredictions


# 将预测结果写入excel文件
def write_excel(newPredictions):
    #    newPredictions=torch.load('newPredictions.txt')
    answer = []
    answer.append(['id', 'y'])
    for i in range(len(newPredictions)):
        answer.append([i, newPredictions[i]])
    np.savetxt("jingsai3_7.csv", answer, delimiter=',', fmt="%s")


def main():
    testImages = data_convert()
    newPredictions = predict_test()
    return newPredictions

