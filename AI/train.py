import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import dataset
import agrumentparsers as ap
import datetime

model = tf.keras.Sequential([
    tf.keras.layers.Input((dataset.image_height, dataset.image_width, 1)),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(32, (5,5), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.4),

    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(64, (5,5), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.4),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(10, activation='softmax')
])

def save(filePath):
    model.save(filePath)

def train(epochs, datasetPath, batch_size):
    ds_train, ds_validation = dataset.load_dataset(datasetPath, batch_size)

    log_dir = "logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_cb = tf.keras.callbacks.TensorBoard(log_dir = log_dir, histogram_freq=0)

    model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.0001), loss=[tf.keras.losses.SparseCategoricalCrossentropy()], metrics=['accuracy'])
    model.fit(ds_train, epochs=epochs, validation_data=ds_validation, workers=32, callbacks=[tensorboard_cb])

    #loss, accuracy = model.evaluate(dataset.ds_validation)

    #print(f'test: {loss}')
    #print(f'accuracy: {accuracy}')


def main():
    args = ap.train_args.parse_args()
    epochs = args.epochs
    filePath = args.savepath
    datasetpath = args.dataset
    batch_size = args.batchsize
    train(epochs, datasetpath, batch_size)
    save(filePath)

if __name__ == '__main__':
    main() 