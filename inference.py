import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
from cv2 import cv2

def load():
    return tf.keras.models.load_model("AI/final.model")

def find_digit(model, image):
        #img = tf.keras.preprocessing.image.load_img(image, target_size=(28, 28), color_mode='grayscale')
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)
        prediction = model.predict(img_array)
        class_names= ["0", "1", "2", "3", "4", "5", "6", '7', '8', '9']
        return class_names[np.argmax(tf.nn.softmax(prediction[0]))]