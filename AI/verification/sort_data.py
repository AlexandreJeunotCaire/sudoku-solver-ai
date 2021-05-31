import os
import cv2
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
import shutil

path = 'tosort/'
model = tf.keras.models.load_model('../models/model4_new_ds.model')
class_names= ["0", "1", "2", "3", "4", "5", "6", '7', '8', '9']

for c in class_names:
    p = os.path.join(f'sorted/{c}')
    try:
        os.mkdir(p)
    except FileExistsError:
        shutil.rmtree(p)
        os.mkdir(p)

for root, directories, files in os.walk(path, topdown=False):
    for name in files:
        f_path = os.path.join(root, name)

        img = tf.keras.preprocessing.image.load_img(f_path, target_size=(28, 28), color_mode='grayscale')
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        prediction = model.predict(img_array)
        score = tf.nn.softmax(prediction[0])
        s = sum(score)
        
        class_n = class_names[np.argmax(score)]
        confidence = np.max(score)
        print(f'{class_n} {confidence}')

        if(confidence > 0.2):
            cv2.imwrite(os.path.join(f'sorted/{class_n}/', name), cv2.imread(f_path))
            os.remove(f_path)