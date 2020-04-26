#import torch.nn as nn
import torch
from torchvision import datasets, transforms
from csrnet import CSRNet

class NNModel():
  def __init__(self, trained_model_path='model_files/model_best.pth.tar'):
    self.trained_model_path = trained_model_path

  def init(self):
    self.model = CSRNet()
    self.model = self.model.cuda()

    #Load the checkpoint
    checkpoint = torch.load(self.trained_model_path)

    self.model.load_state_dict(checkpoint['state_dict'])

    #Prepare the transform
    #TODO: THE MEAN AND STD NEED TO BE CHANGED FOR DIFFERENT DATASET.
    self.transform=transforms.Compose([transforms.ToTensor(),
                                  transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                       std=[0.229, 0.224, 0.225]),
                                ])

  def run(self, img_array):
    img = self.transform(img_array).cuda()
    output = self.model(img.unsqueeze(0))
    
    return output 
