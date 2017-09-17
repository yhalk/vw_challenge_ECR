# Calculate Intersect over union between boxes b1 and b2, here each box is defined with 2 points
# box(startX, startY, endX, endY), there are other definitions ie box(x,y,width,height)
def calc_iou(b1, b2):
 # determine the (x, y)-coordinates of the intersection rectangle
 xA = max(b1[0], b2[0])
 yA = max(b1[1], b2[1])
 xB = min(b1[2], b2[2])
 yB = min(b1[3], b2[3])

 # compute the area of intersection rectangle
 area_intersect = (xB - xA + 1) * (yB - yA + 1)

 # Calculate area of boxes
 area_b1 = (b1[2] - b1[0] + 1) * (b1[3] - b1[1] + 1)
 area_b2 = (b2[2] - b2[0] + 1) * (b2[3] - b2[1] + 1)

 # compute the intersection over union by taking the intersection
 # area and dividing it by the sum of prediction + ground-truth
 # areas - the intersection area
 iou = area_intersect / float(area_b1 + area_b2 - area_intersect)

 # return the intersection over union value
 return iou

###########################################################################

import numpy as np

def calc_iou(xy_min1, xy_max1, xy_min2, xy_max2):
    # Get areas
    areas_1 = np.multiply.reduce(xy_max1 - xy_min1)
    areas_2 = np.multiply.reduce(xy_max2 - xy_min2)

    # determine the (x, y)-coordinates of the intersection rectangle
    _xy_min = np.maximum(xy_min1, xy_min2) 
    _xy_max = np.minimum(xy_max1, xy_max2)
    _wh = np.maximum(_xy_max - _xy_min, 0)

    # compute the area of intersection rectangle
    _areas = np.multiply.reduce(_wh)

    # return the intersection over union value
    return _areas / np.maximum(areas_1 + areas_2 - _areas, 1e-10)
