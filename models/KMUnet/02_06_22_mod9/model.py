from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization,AveragePooling2D
from keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from keras.regularizers import l2
from keras.utils import np_utils

num_labels = 7
batch_size = 64
epochs = 100 # изменить
width, height = 48, 48


model = Sequential()


model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(X_train.shape[1:])))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(3,3), strides=(2, 2)))
model.add(Dropout(0.25))



model.add(Conv2D(96, kernel_size=(3, 3), activation='relu'))
model.add(Conv2D(96, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(3,3), strides=(2, 2)))
model.add(Dropout(0.3))


model.add(Conv2D(112, (3, 3), activation='relu'))
model.add(AveragePooling2D(pool_size=(3,3), strides=(1, 1)))
model.add(Dropout(0.3))

model.add(Flatten())

model.add(Dense(464, activation='relu'))
model.add(Dropout(0.4))

model.add(Dense(384, activation='relu'))
model.add(Dropout(0.35))

model.add(Dense(num_labels, activation='softmax'))

model.summary()

model.compile(loss=categorical_crossentropy,
              optimizer=Adam(),
              metrics=['accuracy', Precision()])

model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(X_val, y_val),
          shuffle=True)


fer_json = model.to_json()
with open("fer.json", "w") as json_file:
    json_file.write(fer_json)
model.save_weights("fer.h5")