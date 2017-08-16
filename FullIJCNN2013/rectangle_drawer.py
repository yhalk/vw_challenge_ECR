import cv2
import random

class Recta:
  def __init__(self, allowed_width, allowed_height):
    self.allowed_width=allowed_width
    self.allowed_height=allowed_height

  def randomRect(self):
    x=random.randint(0,self.allowed_width)
    y=random.randint(0,self.allowed_height)
    
    w=-1
    if(self.allowed_width-x > 0):
      w=random.randrange(0,self.allowed_width-x)
    else:
      x=random.randint(0,self.allowed_width)
      w=random.randrange(0,self.allowed_width-x)

    if(self.allowed_height-y > 0):
      h=random.randrange(0,self.allowed_height-y)
    else:
      y=random.randint(0,self.allowed_height)
      h=random.randrange(0,self.allowed_height-y)

    return x,y,w,h

def intersect(X1,Y1,W1,H1, X2,Y2,W2,H2):
  if (X1+W1<X2 or X2+W2<X1 or Y1+H1<Y2 or Y2+H2<Y1):
    return False
  else:
    return True

with open("gt.txt") as f:
  content = f.readlines()

content = [x.strip() for x in content]

for idx, item in enumerate(content):
  if True:#idx < 3:
    filename = item.split(";")[0]
    x1=int(item.split(";")[1])
    y1=int(item.split(";")[2])
    x2=int(item.split(";")[3])
    y2=int(item.split(";")[4])
    
    filename_jpg = filename.split(".")[0]+".jpg"
    img = cv2.imread("jpgs/"+filename_jpg)

    #cv2.rectangle(img, (x1,y1), (x2, y2), (0,0,255), 2)
    
    background_list = []

    for i in range(0,10):
      rect=Recta(img.shape[1], img.shape[0])
      (random_rect_x, random_rect_y, random_rect_width, random_rect_height) = rect.randomRect()
      if not intersect(x1,y1,x2-x1,y2-y1, random_rect_x,random_rect_y,random_rect_width,random_rect_height):
        #cv2.rectangle(img, (random_rect_x,random_rect_y), (random_rect_x+random_rect_width,random_rect_y+random_rect_height), (0,255,0), 2)
        background_list.append((filename, random_rect_x, random_rect_y, random_rect_x+random_rect_width, random_rect_y+random_rect_height, 'bg'))
      

    #cv2.imwrite("results/"+filename_jpg,img)
    with open("background.txt", "a") as f:
      for item in background_list:
        #print str(item[0])+";"+str(item[1])+";"+str(item[2])+";"+str(item[3])+";"+str(item[4])+";bg"
        f.write(str(item[0])+";"+str(item[1])+";"+str(item[2])+";"+str(item[3])+";"+str(item[4])+";bg\n")
