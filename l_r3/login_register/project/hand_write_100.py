# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:59:30 2019

@author: 周义青
"""

import os
import torch
import torch.nn as nn
import torch.nn.functional as  F
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import numpy as np
from torchvision import transforms as T
import cv2

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

transform=T.Compose([
    T.Resize((64,64)),
    T.Grayscale(),
    T.ToTensor(),
])

newLabels={0:'一', 1:'丁', 2:'七', 3:'万', 4:'杖', 5:'三', 6:'上', 7:'下', 8:'不', 9:'与', 
           10:'丑',11:'专', 12:'且', 13:'世', 14:'丘', 15:'丙', 16:'业', 17:'丛', 18:'东', 19:'丝',
           20:'丢', 21:'两', 22:'严', 23:'丧', 24:'个', 25:'丫', 26:'中', 27:'丰', 28:'串', 29:'临',
           30:'丸', 31:'丹', 32:'为', 33:'主', 34:'丽', 35:'举', 36:'乃', 37:'久', 38:'么', 39:'义',
           40:'之', 41:'乌', 42:'乍', 43:'乎', 44:'乏', 45:'乐', 46:'乒', 47:'乓', 48:'乔', 49:'乖', 
           50:'乘', 51:'乙', 52:'九', 53:'乞', 54:'也', 55:'习', 56:'乡', 57:'书', 58:'买', 59:'乱',
           60:'乳', 61:'乾', 62:'了', 63:'予', 64:'争', 65:'事', 66:'二', 67:'于', 68:'亏', 69:'云',
           70:'互', 71:'五', 72:'井', 73:'亚', 74:'些', 75:'亡', 76:'亢', 77:'交', 78:'亥', 79:'亦', 
           80:'产', 81:'亨', 82:'亩', 83:'享', 84:'京', 85:'亭', 86:'亮', 87:'亲', 88:'人', 89:'亿', 
           90:'什', 91:'仁', 92:'仅', 93:'仆', 94:'仇', 95:'今', 96:'介', 97:'仍', 98:'从', 99:'仑'
        }

#定义LeNet模型
class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(2704, 512)
        self.fc2 = nn.Linear(512, 84)
        self.fc3 = nn.Linear(84,100)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    @staticmethod
    def num_flat_features(x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
  
#将训练集图片、测试集图片路径分别写入train.txt,test.txt中(可以找到每张图片的标签及数据)
def classes_txt(root,txtName,numClass=None):
    dirs = os.listdir(root)
    numClass=len(dirs)
    with open(txtName, 'w+') as f:
        dirs.sort()
        dirs=dirs[0:numClass]
        for xdir in dirs:
            files = os.listdir(os.path.join(root, xdir))
            for file in files:
                f.write(os.path.join(root, xdir, file) + '\n')

    
#构造数据对象
class MyDataset(Dataset):
    def __init__(self, txtPath, numClass,transforms):
        super(MyDataset, self).__init__()
        images,labels = [],[]
        with open(txtPath, 'r') as f:
            for line in f:
                if int(line.split('.')[-2])>=numClass:  # just get images of the first #num_class
                    break
                line = line.strip('\n')
                images.append(line)
                labels.append(int(line.split('.')[-2]))
#        print(labels)
        self.images = images
        self.labels = labels
        self.transforms = transforms

    def __getitem__(self, index):
        image = Image.open(self.images[index])
        label = self.labels[index]
        if self.transforms is not None:
            image = self.transforms(image)
        return (image, label)

    def __len__(self):
        return len(self.labels)
    
    
#训练模型
# def train():
#     trainSet = MyDataset('data/train.txt', numClass=100,transforms=transform)
#     trainLoader = DataLoader(trainSet, batch_size=32, shuffle=True)
#
#     device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
#     print(device)
#
#     model = LeNet()
#     model.to(device)
#     model.train()
#     criterion = nn.CrossEntropyLoss()
#     optimizer = optim.Adam(model.parameters(), lr=0.001)
#     loss = 0.0
#     epoch = 0
#
#     while epoch <50:
#         runningLoss = 0.0
#         for i, data in enumerate(trainLoader):
#             inputs, labels = data[0].to(device), data[1].to(device)
#             optimizer.zero_grad()
#             outs = model(inputs)
#             loss = criterion(outs,labels)
#             loss.backward()
#             optimizer.step()
#             runningLoss += loss.item()
#             print('epoch %5d: batch: %5d, loss: %f'%(epoch,i,runningLoss))
#             runningLoss=0.0
#         torch.save({'epoch': epoch,
#                     'model_state_dict': model.state_dict(),
#                     'optimizer_state_dict': optimizer.state_dict(),
#                     'loss': loss},
#                     'LeNet.pth')
#         epoch += 1
#     print('Finish training')

#测试模型正确率
def accuracy_test():
    testSet = MyDataset('data/test.txt', numClass=100, transforms=transform)
    testLoader = DataLoader(testSet,batch_size=32)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(device)
    model = LeNet()
    model.to(device)
    checkpoint = torch.load('LeNet.pth')
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()

    total = 0.0
    correct = 0.0
    with torch.no_grad():
        for i, data in enumerate(testLoader):
            inputs, labels = data[0].to(device), data[1].to(device)
            outputs = model(inputs)
            _, predict = torch.max(outputs.data, 1)
            print(predict)
            total += labels.size(0)
            predict=np.array(predict.cpu())
            labels=np.array(labels.cpu())
            correct += sum(predict == labels).item()
            
            if i % 10 == 0:
                print('batch: %5d,\t acc: %f' % (i + 1, correct / total))
    print('Accuracy: %.2f%%' % (correct / total * 100))

#预测函数
def predict_test():
    testSet = MyDataset('test.txt', numClass=100, transforms=transform)
    testLoader = DataLoader(testSet,batch_size=32)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(device)
    model = LeNet()
    model.to(device)
    checkpoint = torch.load('LeNet.pth')
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    predictions=[]
    with torch.no_grad():
        for i, data in enumerate(testLoader):
            inputs= data[0].to(device)
            outputs = model(inputs)
            _, predict = torch.max(outputs.data, 1)
            predict=np.array(predict.cpu())
            predict=[newLabels[x] for x in predict ]
            predictions.append(predict)
        predictions=sum(predictions,[])
    print(predictions)
    return predictions
    
#if __name__ == '__main__':
    
#    classes_txt('data/train', 'data/train.txt', numClass=100)
#    classes_txt('data/test' , 'data/test.txt', numClass=100)
#    train()
#    accuracy_test()
    #predict_test()