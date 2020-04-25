import cv2

MYVIDEO='crowd.mp4'
#MYVIDEO='crowd_5fps.avi'

def video_loop(video_file_path):
  cap = cv2.VideoCapture(video_file_path)

  if (cap.isOpened() == False):
    print("Error opening video stream or file")

  while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
      cv2.imshow('Frame', frame)

      #if cv2.waitKey(25) & 0xFF == ord('q'):
      if cv2.waitKey(200) & 0xFF == ord('q'):
        break
    else:
      break

  cap.release()

  cv2.destroyAllWindows()

if __name__ == '__main__':
  video_loop(MYVIDEO)
