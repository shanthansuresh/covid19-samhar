import cv2
from nnmodel import NNModel
#import matplotlib.pyplot as plt
import numpy as np
from pyheatmap.heatmap import HeatMap

MYVIDEO='crowd.mp4'
#MYVIDEO='crowd_5fps.avi'
SCALING_FACTOR=8

def video_init(video_file_path):
  cap = cv2.VideoCapture(video_file_path)

  if (cap.isOpened() == False):
    print("Error opening video stream or file")
    return -1

  return cap

def video_deinit(cap):
  cap.release()
  cv2.destroyAllWindows()

def plot_output(output):
  out_cpu = output.cpu().detach()
  print('out_numpy shape={}'.format(out_cpu.shape))
  #x = out_numpy[0].permute(1, 2, 0)
  x = out_cpu[0].permute(1, 2, 0).numpy()
  x_sh = x.shape
  print('x shape1={}'.format(x.shape))
  x = x.reshape(x_sh[0], x_sh[1])
  print('x shape2={}'.format(x.shape))
  #plt.imshow(x, cmap='gray')
  cv2.imshow('Output', 255*x)

def count_people(output):
  num_ppl = output.detach().cpu().sum().numpy()

  return (int)(num_ppl)

def write_text(img, text_val):
  BLACK = (0, 0, 255)
  font = cv2.FONT_HERSHEY_SIMPLEX
  font_size = 1.1 
  font_color = BLACK
  font_thickness = 2 
  text = "count = " + str(text_val)
  x,y = 30,30
  img_text = cv2.putText(img, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)

  return img_text
 
def dump_output(img, i, num_ppl):
  #BLACK = (0, 0, 255)
  #font = cv2.FONT_HERSHEY_SIMPLEX
  #font_size = 1.1
  #font_color = BLACK
  #font_thickness = 2
  #text = "count = " + str(num_ppl)
  #x,y = 30,30
  #img_text = cv2.putText(img, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
  out_img_path = "out/" + str(i) + ".jpg"

  img_text = write_text(img, num_ppl)
  cv2.imwrite(out_img_path, img_text)

def heatmap(img, output, img_num, num_ppl):
    print('generating heat map for img', img_num)
    out_cpu = output.cpu().detach()
    den = out_cpu[0].permute(1, 2, 0).numpy()
    den = den[:, :, 0]
    print('output shape:{}'.format(den.shape))

    den_resized = np.zeros((den.shape[0] * SCALING_FACTOR, den.shape[1] * SCALING_FACTOR))
    for i in range(den_resized.shape[0]):
      for j in range(den_resized.shape[1]):
        den_resized[i][j] = den[int(i / SCALING_FACTOR)][int(j / SCALING_FACTOR)] / (SCALING_FACTOR*SCALING_FACTOR)
    den = den_resized
    den = den * 10 / np.max(den)

    img_text = write_text(img, num_ppl)
    img_path = "out/" + str(img_num) + ".jpg"
    cv2.imwrite(img_path, img_text);

    w = img.shape[1]
    h = img.shape[0]

    data = []
    for j in range(len(den)):
        for i in range(len(den[0])):
            for k in range(int(den[j][i])):
                data.append([i + 1, j + 1])
    hm = HeatMap(data, base = img_path)
    hm.heatmap(save_as = 'out/' + 'heat_' + '_' + str(img_num) + '_' + str(int(num_ppl)) + '.jpg')

def process_loop(video_file_path):
  #Initialize the video capture pipeline
  cap = video_init(video_file_path)
  if (cap == -1):
    print("Failed in video_init. Exiting the process_loop")

  #Initialize the nn model
  model = NNModel()
  model.init()

  i = 0
  while(cap.isOpened()):
    ret, img = cap.read()
    if ret == True:
      cv2.imshow('Frame', img)

      img_orig = img
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      output = model.run(img)
      #plot_output(output)
      num_ppl = count_people(output)
      #print("num_ppl={}".format(num_ppl))
      #dump_output(img, i, num_ppl)

      heatmap(img_orig, output, i, num_ppl)

      i = i + 1 

      #if cv2.waitKey(25) & 0xFF == ord('q'):
      if cv2.waitKey(200) & 0xFF == ord('q'):
        break
    else:
      break

  video_deinit(cap)

if __name__ == '__main__':
  process_loop(MYVIDEO)
