import numpy as np
import pandas as pd

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

import torchvision
import imageio
import torch.utils.data as Data

import datetime
import matplotlib.pyplot as plt
import add_noise as an
import create_noises as cn

#vasatie tedade chanel hast k baraye ma aval yeke
#bad b tedad node haye hidden mishe
#k = 10 #number of patches that we want to generate
m = 5 #m is the dimension of filter
d = 50 # d is the dimension of input
k = d/m  #check the paper!
k = int(k)

print("main2")
data = np.random.normal(0, 1, (3, 50, 50))
data = data.astype("float32")
data = torch.from_numpy(data)
data = data.reshape((3, 1, 50, 50))
y = np.random.normal(0, 1, 3)
y = y.astype("float32")
y = torch.from_numpy(y)
y = y.reshape((3, 1))


class Net(nn.Module):
    def __init__(self, num_hidden, num_input=1, kernel=1):
        super(Net, self).__init__()
        self.hiddenLayer = nn.Conv2d(in_channels=num_input, out_channels=num_hidden, kernel_size=kernel, stride=kernel)
        self.outPut = nn.AvgPool2d(kernel_size=num_hidden)
        self.outPut2 = nn.Linear(num_hidden, 1)

    def forward(self, x):
        print(x.size())
        x = self.hiddenLayer(x)
        print(x.size())
        x = F.relu(x)
        #print(x)
        print("here")
        x = self.outPut(x)
        print(x)
        x = x.view(x.size(0), -1)
        x = self.outPut2(x)
        print(x)

        return x


t_net = Net(num_hidden=k, num_input=1, kernel=m) #Creating teacher network


optimizer = torch.optim.SGD(t_net.parameters(), lr=0.2)
loss_func = nn.MSELoss()

o = 0
print("meeeeeeeee")
for name, param in t_net.state_dict().items():
    if name == "outPut.weight":
        print("out1")
        print(param)
    o = o + 1
    print(name)
print("hhhhhhh")
print(o)


# train the network
for t in range(1):
    prediction = t_net(data)  # input x and predict based on x
    print(prediction.size())
    loss = loss_func(prediction, y)  # must be (1. nn output, 2. target)

    optimizer.zero_grad()  # clear gradients for next train
    loss.backward()  # backpropagation, compute gradients
    optimizer.step()  # apply gradients
