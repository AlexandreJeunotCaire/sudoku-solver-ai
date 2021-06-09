import tensorflow as tf

image_height = 28
image_width = 28
seed = 456789

def load_dataset(datasetPath, batch_size):
    ds_train = tf.keras.preprocessing.image_dataset_from_directory(
        datasetPath,
        labels='inferred',
        label_mode='int',
        color_mode='grayscale',
        batch_size=batch_size,
        image_size=(image_height, image_width),
        shuffle=True,
        seed=seed,
        validation_split=0.1,
        subset='training'
    )

    ds_validation = tf.keras.preprocessing.image_dataset_from_directory(
        datasetPath,
        labels='inferred',
        label_mode='int',
        color_mode='grayscale',
        batch_size=batch_size,
        image_size=(image_height, image_width),
        shuffle=True,
        seed=seed,
        validation_split=0.1,
        subset='validation'
    )
    return ds_train, ds_validation