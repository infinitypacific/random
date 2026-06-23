import torch
import torch.nn as nn
class FunnyNN(nn.Module):
  def __init__(self):
    super(FunnyNN,self).__init__()
    self.fc1 = nn.Linear(20,40)
    self.fc2 = nn.Linear(40,20)
    self.fc3 = nn.Linear(20,1)
    self.activation = nn.ReLU()
  def forward(self,v):
    v = self.fc1(v)
    v = self.activation(v)
    v = self.fc2(v)
    v = self.activation(v)
    v = self.fc3(v)
    return v
