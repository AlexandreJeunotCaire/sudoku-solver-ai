import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import agrumentparsers as ap
import numpy as np

def main():
    args = ap.inference_args.parse_args()
    model = tf.keras.models.load_model(args.model)

    if args.image is not None:
        img = tf.keras.preprocessing.image.load_img(args.image, target_size=(28, 28), color_mode='grayscale')
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        prediction = model.predict(img_array)
        score = tf.nn.softmax(prediction[0])
        s = sum(score)
        class_names= ["0", "1", "2", "3", "4", "5", "6", '7', '8', '9']
        print(score)
        print( "This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], (100 * np.max(score))/s))

    elif args.folder is not None:
        ds_test = tf.keras.preprocessing.image_dataset_from_directory(
        args.folder,
        labels='inferred',
        label_mode='int',
        color_mode='grayscale',
        batch_size=64,
        image_size=(28, 28),
        shuffle=True,
        seed=548465
    )

        r = model.evaluate(ds_test, batch_size=64)
        print("test loss and test accuracy:", r)

if __name__ == '__main__':
    main()