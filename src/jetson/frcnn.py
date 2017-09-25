from __future__ import division
import os
import cv2
import numpy as np
import sys
import pickle
from optparse import OptionParser
import time
from keras_frcnn import config
from keras import backend as K
from keras.layers import Input
from keras.models import Model
from keras_frcnn import roi_helpers
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

import math
import keras_frcnn.resnet as nn
import datetime

KNOWN_CLASSES = ["blue", "green", "grey", "multicolor", "white", "yellow"]


class ObjectPredictor:
        #os.environ['CUDA_VISIBLE_DEVICES'] = ''

        def ret_detected_objects(detected_objects):
            return detected_objects

        def image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
                # initialize the dimensions of the image to be resized and
                # grab the image size
                dim = None
                (h, w) = image.shape[:2]

                # if both the width and height are None, then return the
                # original image
                if width is None and height is None:
                   return image

                # check to see if the width is None
                if width is None:
                        # calculate the ratio of the height and construct the
                        # dimensions
                        r = height / float(h)
                        dim = (int(w * r), height)

                        # otherwise, the height is None
                else:
		        # calculate the ratio of the width and construct the
                        # dimensions
                        r = width / float(w)
                        dim = (width, int(h * r))

                # resize the image
                resized = cv2.resize(image, dim, interpolation = inter)

                # return the resized image
                return resized

        def angle_between(self, p1, p2):
            ang1 = np.arctan2(*p1[::-1])
            ang2 = np.arctan2(*p2[::-1])
            return np.rad2deg((ang1 - ang2) % (2 * np.pi))
	
        def distance(self, p0, p1):
            return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

        def format_img_size(self, img, C):
                """ formats the image size based on config """
                img_min_side = float(C.im_size)
                (height,width,_) = img.shape

                if width <= height:
                        ratio = img_min_side/width
                        new_height = int(ratio * height)
                        new_width = int(img_min_side)
                else:
                        ratio = img_min_side/height
                        new_width = int(ratio * width)
                        new_height = int(img_min_side)
                img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
                return img, ratio	


        def format_img_channels(self, img, C):
                """ formats the image channels based on config """
                img = img[:, :, (2, 1, 0)]
                img = img.astype(np.float32)
                img[:, :, 0] -= C.img_channel_mean[0]   
                img[:, :, 1] -= C.img_channel_mean[1]
                img[:, :, 2] -= C.img_channel_mean[2]
                img /= C.img_scaling_factor
                img = np.transpose(img, (2, 0, 1))
                img = np.expand_dims(img, axis=0)
                return img
	
        def format_img(self, img, C):
                """ formats an image for model prediction based on config """
                img, ratio = self.format_img_size(img, C)
                img = self.format_img_channels(img, C)
                return img, ratio
	
        # Method to transform the coordinates of the bounding box to its original size
        def get_real_coordinates(self, ratio, x1, y1, x2, y2):

                real_x1 = int(round(x1 // ratio))
                real_y1 = int(round(y1 // ratio))        
                real_x2 = int(round(x2 // ratio))
                real_y2 = int(round(y2 // ratio))
	 
                return (real_x1, real_y1, real_x2 ,real_y2)
	
	
        def __init__(self):
          gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)

          sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

          config = tf.ConfigProto()
          config.gpu_options.allow_growth=True
          sess = tf.Session(config=config)

          sys.setrecursionlimit(40000)

          self.num_features = 1024

          self.input_shape_img = (None, None, 3)
          self.input_shape_features = (None, None, self.num_features)
          self.C = None
          self.model_rpn = None
          self.model_classifier_only = None
          self.bbox_threshold = 0.5
          with open("config.pickle", 'rb') as f_in:
               self.C = pickle.load(f_in)

          self.class_mapping = self.C.class_mapping
          if 'bg' not in self.class_mapping:
              self.class_mapping['bg'] = len(self.class_mapping)

          self.class_mapping = {v: k for k, v in self.class_mapping.items()}
          print(self.class_mapping)
          class_to_color = {self.class_mapping[v]: np.random.randint(0, 255, 3) for v in self.class_mapping}
          self.C.num_rois = int(128) #32 num of rois

          img_input = Input(shape=self.input_shape_img)
          roi_input = Input(shape=(self.C.num_rois, 4))
          feature_map_input = Input(shape=self.input_shape_features)

          # define the base network (resnet here, can be VGG, Inception, etc)
          shared_layers = nn.nn_base(img_input, trainable=True)
 

          # define the RPN, built on the base layers
          num_anchors = len(self.C.anchor_box_scales) * len(self.C.anchor_box_ratios)
          rpn_layers = nn.rpn(shared_layers, num_anchors)
          classifier = nn.classifier(feature_map_input, roi_input, self.C.num_rois, nb_classes=len(self.class_mapping), trainable=True)
          self.model_rpn = Model(img_input, rpn_layers)
          self.model_classifier_only = Model([feature_map_input, roi_input], classifier)

          model_classifier = Model([feature_map_input, roi_input], classifier)
          print('Loading weights from {}'.format(self.C.model_path))
          self.model_rpn.load_weights(self.C.model_path, by_name=True)
          model_classifier.load_weights(self.C.model_path, by_name=True)

          self.model_rpn.compile(optimizer='sgd', loss='mse')
          model_classifier.compile(optimizer='sgd', loss='mse')


        #for idx, img_name in enumerate(sorted(os.listdir(img_path))):
        def detect_known_objects(self, img):
                print ("HELLLOOOOOO")
                img = self.image_resize(img, height=int(img.shape[0]/3.0))
                X, ratio = self.format_img(img, self.C)
                if K.image_dim_ordering() == 'tf':
                   X = np.transpose(X, (0, 2, 3, 1))
                
                # get the feature maps and output from the RPN
                [Y1, Y2, F] = self.model_rpn.predict(X)
	        #print Y1, Y2, F
		
                a = datetime.datetime.now()
                R = roi_helpers.rpn_to_roi(Y1, Y2, self.C, K.image_dim_ordering(), overlap_thresh=0.7)
                b = datetime.datetime.now()
                delta = b - a
                print("roi_helpers.rpn_to_roi took:", int(delta.total_seconds() * 1000)) # milliseconds
                #print R
                #for i in R:
                #    cv2.rectangle(img,(i[0],i[1]),(i[2],i[3]),(0,255,0),3)
	        # convert from (x1,y1,x2,y2) to (x,y,w,h)
                R[:, 2] -= R[:, 0]    
                R[:, 3] -= R[:, 1]
	
                # apply the spatial pyramid pooling to the proposed regions
                bboxes = {}
                probs = {}
                for idx, jk in enumerate(range(R.shape[0]//self.C.num_rois + 1)):                
                        ROIs = np.expand_dims(R[self.C.num_rois*jk:self.C.num_rois*(jk+1), :], axis=0)
                        if ROIs.shape[1] == 0:
                                break
                         
                        if jk == R.shape[0]//self.C.num_rois:
                                #pad R
                                curr_shape = ROIs.shape
                                target_shape = (curr_shape[0],self.C.num_rois,curr_shape[2]) 
                                ROIs_padded = np.zeros(target_shape).astype(ROIs.dtype)
                                ROIs_padded[:, :curr_shape[1], :] = ROIs
                                ROIs_padded[0, curr_shape[1]:, :] = ROIs[0, 0, :]
                                ROIs = ROIs_padded
                                print("ROIs shape", np.array(ROIs).shape)
                                print("F", np.array(F).shape)
                        a = datetime.datetime.now()
                        [P_cls, P_regr] = self.model_classifier_only.predict([F, ROIs])
                        b = datetime.datetime.now()
                        delta = b - a
                        print("prediction of roi took: :", int(delta.total_seconds() * 1000)) # milliseconds
                        #print P_cls, P_regr
                        #print P_cls.shape, P_regr.shape
                        for ii in range(P_cls.shape[1]):
                                #print P_cls[0,ii,:]
                                if np.max(P_cls[0, ii, :]) < self.bbox_threshold or np.argmax(P_cls[0, ii, :]) == (P_cls.shape[2] - 1):
                                   continue
                                cls_name = self.class_mapping[np.argmax(P_cls[0, ii, :])]
                                if cls_name not in bboxes: 
                                        bboxes[cls_name] = []
                                        probs[cls_name] = []
                                (x, y, w, h) = ROIs[0, ii, :]
	                        #print x, y, w, h
                                cls_num = np.argmax(P_cls[0, ii, :])
	                        #print "something", cls_num
                                try:
                                        (tx, ty, tw, th) = P_regr[0, ii, 4*cls_num:4*(cls_num+1)]
                                        tx /= self.C.classifier_regr_std[0]
                                        ty /= self.C.classifier_regr_std[1]
                                        tw /= self.C.classifier_regr_std[2]
                                        th /= self.C.classifier_regr_std[3]
                                        x, y, w, h = roi_helpers.apply_regr(x, y, w, h, tx, ty, tw, th)
                                except:
                                        print("exception")          
                                        pass
                                bboxes[cls_name].append([self.C.rpn_stride*x, self.C.rpn_stride*y, self.C.rpn_stride*(x+w), self.C.rpn_stride*(y+h)])
                                probs[cls_name].append(np.max(P_cls[0, ii, :]))
               
                all_dets = []
	
                detected_objects = []
                for key in bboxes:
                        key_bbox = []
                        bbox = np.array(bboxes[key])
                        new_boxes, new_probs = roi_helpers.non_max_suppression_fast(bbox, np.array(probs[key]), overlap_thresh=0.5)
                        for jk in range(new_boxes.shape[0]):
                                (x1, y1, x2, y2) = new_boxes[jk,:]
                                (real_x1, real_y1, real_x2, real_y2) = self.get_real_coordinates(ratio, x1, y1, x2, y2)
                                key_bbox.append((real_x1, real_y1, real_x2, real_y2))
	                        #print ("object width", self.distance([real_x1,real_y1], [real_x2,real_y1]))
	                        #print "drawing detected rect at:", (real_x1, real_y1), (real_x2, real_y2)
                                #cv2.rectangle(img,(real_x1, real_y1), (real_x2, real_y2), (int(class_to_color[key][0]), int(class_to_color[key][1]), int(class_to_color[key][2])),5)
	   
                                #textLabel = '{}: {}'.format(key,int(100*new_probs[jk]))
	                        #all_dets.append((key,100*new_probs[jk]))

                                #(retval,baseLine) = cv2.getTextSize(textLabel,cv2.FONT_HERSHEY_COMPLEX,1,1)
                                #textOrg = (real_x1-20, real_y1-20)

                                #cv2.rectangle(img, (textOrg[0] - 5, textOrg[1]+baseLine - 5), (textOrg[0]+retval[0] +5, textOrg[1]-retval[1] +5), (0, 0, 0), 2)
                                #cv2.rectangle(img, (textOrg[0] -5,textOrg[1]+baseLine - 5), (textOrg[0]+retval[0] +5, textOrg[1]-retval[1] +5), (255, 255, 255), -1)
	                        #cv2.putText(img, textLabel, textOrg, cv2.FONT_HERSHEY_DUPLEX, 0.3, (0, 0, 0), 1)
                                height, width, channels = img.shape
	                        #FOV horizontal = 62 degrees   (from 90 on right to 33 on left)
                                angle_between_robot_centre_and_detected_object = self.angle_between((real_x1,(real_y1+real_y2)/2.0), (width/2.0,0))-62
                                focal_length_mm = 1.0
                                average_real_object_height_mm = 1.0
                                image_height_px = height
                                object_height_px = self.distance([real_x1,real_y1], [real_x1,real_y2])      
                                sensor_height_mm = 314.2
                                distance_between_robot_centre_and_detected_object = (51.525 * 123) / self.distance([real_x1,real_y1], [real_x2,real_y1])  #(focal_length_mm * average_real_object_height_mm * image_height_px) / float(object_height_px * sensor_height_mm)
                                distance_between_robot_centre_and_detected_object = distance_between_robot_centre_and_detected_object * 1.5
	
                                detected_objects.append((key, key_bbox, distance_between_robot_centre_and_detected_object, angle_between_robot_centre_and_detected_object))
	
                #print(detected_objects)
                #self.ret_detected_objects(detected_objects)
                return detected_objects
                
