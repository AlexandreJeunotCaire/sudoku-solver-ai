import numpy as np
from numpy import random
from cv2 import cv2

for i in range(0,6000):
    my_img_1 = np.zeros((28, 28, 1), dtype = "uint8")
    cv2.randn(my_img_1, 0, 1)

    if np.random.randint(0, 100) < 20:
        for j in range(0, 3):
            # Random center point
            center_x = np.random.randint(0, 28)
            center_y = np.random.randint(0, 28)

            # Random radius and color
            radius = np.random.randint(2, 28/5)
            color = np.random.randint(150, 256)

            cv2.circle(my_img_1, (center_x, center_y), radius, (color, color, color), -1)
    cv2.imwrite("training\\0\\" + str(i)+".jpg", my_img_1)
