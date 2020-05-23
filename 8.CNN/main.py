# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
 

def loadDataSet():
    np.random.seed(25)
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    #each image has 28X28 resolution
    # plot first few images
    print("Here are the first images from the data set:\n")
    for i in range(9):
    	# define subplot
    	plt.subplot(330 + 1 + i)
    	# plot raw pixel data
    	plt.imshow(x_train[i], cmap=plt.get_cmap('gray'))
    # show the figure
    plt.show()
    #reshape the input
    #because the images are in grayscale, the number of channels is 1
    x_train = x_train.reshape(x_train.shape[0],28,28,1)
    x_test = x_test.reshape(x_test.shape[0],28,28,1)
    
    #preparing the pixels:
    #convert to floats
    x_train  =x_train.astype('float32')
    x_test = x_test.astype('float32')
    #each pixels is in the interval [0,1]:
    x_train = x_train/ 255.0
    x_test = x_test/ 255.0
    
    numberOfClasses = 10
    y_train = np_utils.to_categorical(y_train,numberOfClasses)
    y_test = np_utils.to_categorical(y_test,numberOfClasses)
    return x_train,y_train,x_test,y_test
    
def defineModel():
    # Three steps to create a CNN
    # 1. Convolution
    # 2. Activation
    # 3. Pooling
    # Repeat these steps for adding more hidden layers
    # 4. After that make a fully connected network
    
    model = Sequential()
    #first layer : 32 filters of size (3,3)
    model.add(Conv2D(32,(3,3), input_shape =(28,28,1))) #convolutional layer
    model.add(BatchNormalization(axis=-1)) #for better performance
    model.add(Activation('relu')) #activation layer
    model.add(Conv2D(32,(3,3)))
    model.add(BatchNormalization(axis=-1))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2))) #pooling layer
 
    #second layer: 64 filters of size (3,3)
    model.add(Conv2D(64,(3, 3)))#convolutional layer
    model.add(BatchNormalization(axis=-1))
    model.add(Activation('relu'))#activation layer
    model.add(Conv2D(64, (3, 3)))
    model.add(BatchNormalization(axis=-1))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))#pooling layer
    
    #we need to flatten the convolutional layers, so that we can use them as Dense layers
    model.add(Flatten())
    
    # Fully connected layer
    model.add(Dense(512))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.2)) #reduce overfitting
    #second layer
    model.add(Dense(10))
    
    model.add(Activation('softmax'))
    
    #compiling the model
    model.compile(loss='categorical_crossentropy',optimizer=Adam(),metrics=['accuracy'])
    return model
    
def load_image(filename):
	# load the image
	img = load_img(filename, target_size=(28, 28),color_mode='grayscale')
	# convert to array
	img = img_to_array(img)
	# reshape into a single sample with 1 channel
	img = img.reshape(1, 28, 28, 1)
	# prepare the pixels
	img = img.astype('float32')
	img = img / 255.0
	return img

def makePrediction():
    # load the image
    img= load_image('image7.png')
    model = load_model('final_model.h5')
    # predict the class
    digit = model.predict_classes(img)
    print(digit[0])
 
def main():
    xTrain, yTrain, xTest, yTest = loadDataSet()
    model = defineModel()
    
    #to reduce overfitting: Data Augmentation
    #it rotates, zooms, shear the image so that the model learns to generalize and not remember specific data
    gen = ImageDataGenerator(rotation_range=8, width_shift_range=0.08, shear_range=0.3,
                         height_shift_range=0.08, zoom_range=0.08)
    test_gen = ImageDataGenerator()
    
    #creating batches to train faster
    train_generator = gen.flow(xTrain, yTrain, batch_size=64)
    test_generator = test_gen.flow(xTest, yTest, batch_size=64)

    #training
    model.fit_generator(train_generator, steps_per_epoch=60000//64, epochs=5, 
                    validation_data=test_generator, validation_steps=10000//64)
    
    #testing the model
    score = model.evaluate(xTest, yTest)
    print()
    print('Test accuracy: ', score[1])
    predictions = model.predict_classes(xTest)

    predictions = list(predictions)
    actuals = list(yTest)
    
    #saving the predictions in a csv file
    sub = pd.DataFrame({'Actual': actuals, 'Predictions': predictions})
    sub.to_csv('./output_cnn.csv', index=False)
    #save the model for further use
    model.save('final_model.h5')

    
   
    
main()
makePrediction()