import tensorflow as tf
import tensorflow.keras.layers as tfl

from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from keras.regularizers import l2
from keras.utils import np_utils
from tensorflow.keras.metrics import Precision 

num_labels = 6
batch_size = 64
epochs = 100 # изменить
width, height = 48, 48

model = tf.keras.Sequential([
    tfl.Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(X_train.shape[1:])),
    tfl.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    tfl.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
    tfl.Dropout(0.35),

    tfl.Conv2D(96, kernel_size=(3, 3), activation='relu'),
    tfl.Conv2D(96, kernel_size=(3, 3), activation='relu'),
    tfl.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
    tfl.Dropout(0.35),

    tfl.Conv2D(112, kernel_size=(3, 3), activation='relu', padding = 'same'),
    tfl.Conv2D(112, kernel_size=(3, 3), activation='relu'),
    tfl.AveragePooling2D(pool_size=(3, 3), strides=(1, 1)),

    tfl.Flatten(),
    tfl.Dropout(0.45),

    tfl.Dense(430, activation='relu'),
    tfl.Dropout(0.4),

    tfl.Dense(200, activation='relu'),
    tfl.Dropout(0.35),

    tfl.Dense(100, activation='relu'),
    tfl.Dropout(0.35),

    tfl.Dense(num_labels, activation='softmax'),
])
    
"""
model.summary()

model.compile(loss=categorical_crossentropy,
              optimizer=Adam(),
              metrics=['accuracy', Precision()])

history = model.fit(X_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(X_val, y_val),
                    shuffle=True)
"""