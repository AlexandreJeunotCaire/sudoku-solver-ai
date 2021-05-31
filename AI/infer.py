import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
from cv2 import cv2

def main():
    model = tf.keras.models.load_model("models/model4_new_ds.model")
    images = [f"datasets/inference/sodoku_white/image{i}.jpg" for i in range(81)]
    for image in images:
        cv2.imshow(image, cv2.imread(image))
        img = tf.keras.preprocessing.image.load_img(image, target_size=(28, 28), color_mode='grayscale')
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        prediction = model.predict(img_array)
        score = tf.nn.softmax(prediction[0])
        s = sum(score)
        class_names= ["0", "1", "2", "3", "4", "5", "6", '7', '8', '9']
        #print(score)
        print( "This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], (100 * np.max(score))/s))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
if __name__ == '__main__':
    main()