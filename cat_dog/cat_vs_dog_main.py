from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping


model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(150, 150,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64,(3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))


model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    'data/train',  # this is the target directory
    target_size=(150, 150),  # all images will be resized to 150x150
    batch_size=32,
    class_mode='binary',
    classes=['dog','cat'])  # since we use binary_crossentropy loss, we need binary labels

# this is a similar generator, for validation data
validation_generator = test_datagen.flow_from_directory(
    'data/validation',
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary')


early_stopping = EarlyStopping(monitor='val_loss', patience=2)
model.fit_generator(
        train_generator,
        steps_per_epoch=2000,
        epochs=100,
        validation_data=validation_generator,
        validation_steps=100,
        callbacks=[early_stopping])
model.save('cat_dog_model2.h5')
model.save_weights('cat_dog_weights2.h5')

# loss是训练集损失值. acc是训练集准确率。val_loss是测试集上的损失值,val_acc是测试集上的准确率。