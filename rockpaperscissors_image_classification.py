# -*- coding: utf-8 -*-
"""RockPaperScissors-Image-Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AdVI2JuQJbbLdkjYQH0l4UgO_RVgPndG

Nama: Timotius Haniel

Username Dicoding: Timotius Haniel

Domisili Asal: Bandung, Jawa Barat

Pekerjaan: Mahasiswa Institut Teknologi Harapan Bangsa, Bandung
"""

import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import os

print(tf.__version__)
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))

"""**Men-download dataset dalam bentuk zip**"""

# melakukan download file dalam bentuk zip
!wget --no-check-certificate \
https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip \
  -O /tmp/rockpaperscissors.zip

"""**Meng-ekstrak file zip data set**"""

import zipfile

local_zip = '/tmp/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip,'r')
zip_ref.extractall('/tmp')
zip_ref.close()

"""**Membuat split data set menjadi train dan validation, lalu membuat direktori split data set tersebut**"""

# Membuat folder untuk dataset
base_dir = '/tmp/rockpaperscissors'
dataset = os.path.join(base_dir,'dataset')

os.mkdir(dataset)

# Split dataset menjadi train dir dan validation dir
base_dir = '/tmp/rockpaperscissors/dataset'
train_dir = os.path.join(base_dir,'train')
validation_dir = os.path.join(base_dir, 'val')

os.mkdir(train_dir)
os.mkdir(validation_dir)

# Membuat split untuk tipe dataset train dan validation untuk setiap kategori rock, paper, dan scissors
train_rock = os.path.join(train_dir, 'rock')
train_paper = os.path.join(train_dir, 'paper')
train_scissors = os.path.join(train_dir, 'scissors')

val_rock = os.path.join(validation_dir, 'rock')
val_paper = os.path.join(validation_dir, 'paper')
val_scissors = os.path.join(validation_dir, 'scissors')

# Membuat folder untuk split data yang telah dibuat untuk setiap kategori rock, paper, dan scissors
os.mkdir(train_rock)
os.mkdir(train_paper)
os.mkdir(train_scissors)

os.mkdir(val_rock)
os.mkdir(val_paper)
os.mkdir(val_scissors)

"""**Menghitung list foto pada direktori untuk setiap kategori rock, paper, dan scissors**"""

#Rock
len(os.listdir('/tmp/rockpaperscissors/rock'))

#Paper
len(os.listdir('/tmp/rockpaperscissors/paper'))

#Scissors
len(os.listdir('/tmp/rockpaperscissors/scissors'))

"""**Memecah direktori rock, paper, dan scissors menjadi data train dan data validation sebesar 40% dari total data set**"""

base_dir = '/tmp/rockpaperscissors'

rock_dir = os.path.join(base_dir,'rock')
paper_dir = os.path.join(base_dir,'paper')
scissors_dir = os.path.join(base_dir,'scissors')

# Rock
train_rock_dir, val_rock_dir = train_test_split(os.listdir(rock_dir), test_size = 0.40)

# Paper
train_paper_dir, val_paper_dir = train_test_split(os.listdir(paper_dir), test_size = 0.40)

# Scissors
train_scissors_dir, val_scissors_dir = train_test_split(os.listdir(scissors_dir), test_size = 0.40)

train_rock = os.path.join(train_dir, 'rock')
train_paper = os.path.join(train_dir, 'paper')
train_scissors = os.path.join(train_dir, 'scissors')

val_rock = os.path.join(validation_dir, 'rock')
val_paper = os.path.join(validation_dir, 'paper')
val_scissors = os.path.join(validation_dir, 'scissors')

"""**Meng-copy data train dan data validation ke directory dataset (direktori baru)**"""

import shutil

for file in train_rock_dir:
  shutil.copy(os.path.join(rock_dir, file), os.path.join(train_rock, file))
for file in train_paper_dir:
  shutil.copy(os.path.join(paper_dir,file), os.path.join(train_paper,file))
for file in train_scissors_dir:
  shutil.copy(os.path.join(scissors_dir,file), os.path.join(train_scissors,file))
for file in val_rock_dir:
  shutil.copy(os.path.join(rock_dir, file), os.path.join(val_rock,file))
for file in val_paper_dir:
  shutil.copy(os.path.join(paper_dir,file), os.path.join(val_paper,file))
for file in val_scissors_dir:
  shutil.copy(os.path.join(scissors_dir,file), os.path.join(val_scissors,file))

"""**Menghitung list foto pada direktori train data untuk setiap kategori rock, paper, dan scissors**"""

#Rock (Train Data)
len(os.listdir('/tmp/rockpaperscissors/dataset/train/rock'))

#Paper (Train Data)
len(os.listdir('/tmp/rockpaperscissors/dataset/train/paper'))

#Scissors (Train Data)
len(os.listdir('/tmp/rockpaperscissors/dataset/train/scissors'))

"""**Menghitung list foto pada direktori validation data untuk setiap kategori rock, paper, dan scissors**"""

#Rock (Validation Data)
len(os.listdir('/tmp/rockpaperscissors/dataset/val/rock'))

#Paper (Validation Data)
len(os.listdir('/tmp/rockpaperscissors/dataset/val/paper'))

#Scissors (Validation Data)
len(os.listdir('/tmp/rockpaperscissors/dataset/val/scissors'))

"""**Mengimplementasikan augmentasi gambar untuk menggambarkan data-data baru dari datasets**"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator
 
train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    horizontal_flip=True,
                    vertical_flip = True,
                    zoom_range = 0.2,
                    shear_range = 0.2,
                    fill_mode = 'nearest')
 
test_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    horizontal_flip=True,
                    vertical_flip = True,
                    zoom_range = 0.2,
                    shear_range = 0.2,
                    fill_mode = 'nearest')

"""**Mengimplementasikan image data generator untuk menyiapkan data latih yang digunakan oleh model untuk dipelajari**"""

train_generator = train_datagen.flow_from_directory(
        train_dir,  # direktori data latih
        target_size=(150, 150),  # mengubah resolusi seluruh gambar menjadi 256x256 piksel
        batch_size=32,
        # karena kita merupakan masalah klasifikasi 2 kelas maka menggunakan class_mode = 'binary'
        class_mode='categorical',
        seed=39)
 
validation_generator = test_datagen.flow_from_directory(
        validation_dir, # direktori data validasi
        target_size=(150, 150), # mengubah resolusi seluruh gambar menjadi 256x256 piksel
        batch_size=32, # karena kita merupakan masalah klasifikasi 2 kelas maka menggunakan class_mode = 'binary'
        class_mode='categorical',
        seed=39)

"""**Membangun arsitektur Convolutional Neural Network untuk mempercepat proses pelatihan Muti Layer Perceptron**"""

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

# Data Model Summary
model.summary()

# compile model dengan 'adam' optimizer loss function 'categorical_crossentropy' 
model.compile(loss='categorical_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy', 'mean_absolute_error'])

"""**Melatih model dengan model fi dengan menggunakan Callback (Menghentikan training setelah akurasi melebihi 96 %)**"""

# Penggunaan Callback untuk menghindari overfitting dan menghentikan data training apabila akurasi telah melebihi 98 %
class callbackClass(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy') > 0.98) and (logs.get('val_accuracy') > 0.98):
      print("\nAkurasi sudah mencukupi (melebihi 98%), Stop Data Training!")
      print(
            "Average Loss pada epoch {} adalah {:7.2f} "
            "& Mean Absolute Error nya adalah {:7.2f}.".format(
                epoch, logs["loss"], logs["mean_absolute_error"]
            )
        )
      self.model.stop_training = True

dataModelHistory = model.fit(
    train_generator,
    steps_per_epoch = 40, # Total batch yang dieksekusi pada setiap epoch
    epochs = 30, # Tambahkan nilai epochs jika akurasi model belum sesuai dengan yang diinginkan
    validation_data = validation_generator, # Menampilkan akurasi pengujian data yang sudah divalidasi
    validation_steps = 20, # Total Batch yang dieksekusi pada setiap epoch
    verbose = 2,
    callbacks=[callbackClass()]
)

"""**Gambar / Plot Model Accuracy, Model Loss, dan Mean Absolute Error dari Training Data and Validation Data**"""

import matplotlib.pyplot as plt

#Model Accuracy Ploting
accuracy = dataModelHistory.history['accuracy']
validationAccuracy = dataModelHistory.history['val_accuracy']

plt.figure()
plt.plot(accuracy, color='green')
plt.plot(validationAccuracy, color='red')
plt.title('Data Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

#Model Loss Plotting
loss = dataModelHistory.history['loss']
validationLoss = dataModelHistory.history['val_loss']

plt.figure()
plt.plot(loss, color='green')
plt.plot(validationLoss, color='red')
plt.title('Data Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.show()

#Mean Absolute Error Plotting
meanAbsError = dataModelHistory.history['mean_absolute_error']
valMeanAbsError = dataModelHistory.history['val_loss']

plt.figure()
plt.plot(meanAbsError, color='green')
plt.plot(valMeanAbsError, color='red')
plt.title('Mean Absolute Error (MAE)')
plt.ylabel('MAE')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.show()

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
 
uploadedData = files.upload()
 
for data in uploadedData.keys():
  # predicting images
  path = data
  img = image.load_img(path, target_size=(150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
 
  pics = np.vstack([x])
  classes = model.predict(pics, batch_size=32)

  if classes[0,0]!=0:
    print('Paper')
  elif classes[0,1]!=0:
    print('Rock')
  elif classes[0,2]!=0:
    print('Scissors')
  else:
    print("Klasifikasi Gambar tidak dikenali")