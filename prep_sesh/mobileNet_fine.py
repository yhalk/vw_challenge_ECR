from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.models import Model,Sequential
from keras.layers import Dense, GlobalAveragePooling2D,Conv2D
from keras import backend as K
import shapesorter as ss
import tensorflow as tf
from keras.datasets import cifar10
from keras.utils import to_categorical
import numpy as np
import sys

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
print('x_train shape:', x_train.shape)

batch_size = 32
num_classes = 10
epochs = 2
# Convert class vectors to binary class matrices.
y_train = to_categorical(y_train, num_classes)[1:1,:]
y_test = to_categorical(y_test, num_classes)[1:1,:]
x_train = x_train.astype('float32')[1:1,:,:,:]
x_test = x_test.astype('float32')[1:1,:,:,:]
x_train /= 255
x_test /= 255

print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')



img_width, img_height = 32, 32
base_model = MobileNet(include_top=False,weights='imagenet', classes=num_classes)

input = Input(shape=(img_width, img_height,3))
out = Conv2D(224,(5,5))(input)
m1 = Model(input,out)

input = Input(shape=(3, img_width, img_height))
x = vgg16_model(input)
predict = top_model(x)
model = Model(input, predict)




# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(10, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')



# train the model on the new data for a few epochs
model.fit(x_train,y_train,batch_size=batch_size,validation_data=(x_test, y_test),epochs=epochs,shuffle=True)

# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.
"""
# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)


# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 249 layers and unfreeze the rest:
for layer in model.layers[:249]:
   layer.trainable = False
for layer in model.layers[249:]:
   layer.trainable = True


# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
model.fit_generator(...)
"""
