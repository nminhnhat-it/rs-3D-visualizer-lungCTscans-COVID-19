import numpy as np
import cv2
import tensorflow as tf
import tensorflow.keras as k
import tensorflow.keras.backend as K
from classification_models.tfkeras import Classifiers

from keras.regularizers import l2
from tensorflow.keras.layers import (BatchNormalization, Conv2D, Dense, Lambda,
                                     GlobalAveragePooling2D, GlobalMaxPooling2D,
                                     MaxPooling2D, Input, LeakyReLU, concatenate, add)

from .utils import reshape_image


def build_model(input_shape,
                num_classes,
                encoder,):
  model = unet3plus(input_shape, num_classes, encoder, False)
  return model


def resnet(input_shape,
           fine_tune_at=False):
  """ Resnet model """
  filters = [64, 256, 512, 1024, 2048]

  resnet, _ = Classifiers.get('resnet50')
  resnet_model = resnet(include_top=False, input_shape=input_shape, weights='imagenet')

  resnet_model.trainable = True

  fine_tune_at = round(len(resnet_model.layers) * fine_tune_at)
  if fine_tune_at != False:
    for layer in resnet_model.layers[:fine_tune_at]:
      layer.trainable = False

  return resnet_model, filters


def seresnext(input_shape,
              fine_tune_at=False):
  """ Resnet model """
  filters = [64, 256, 512, 1024, 2048]

  seresnext, preprocess_input = Classifiers.get('seresnext50')
  seresnext_model = seresnext(include_top=False, input_shape=input_shape, weights='imagenet')

  seresnext_model.trainable = True
  print("Number of layers in the base model: ", len(seresnext_model.layers))
  fine_tune_at = round(len(seresnext_model.layers) * fine_tune_at)
  if fine_tune_at != False:
    for layer in seresnext_model.layers[:fine_tune_at]:
      layer.trainable = False

  return seresnext_model, filters


def conv_block(x, kernels, kernel_size=(3, 3), strides=(1, 1), padding='same',
               is_bn=True, is_relu=True, n=2):
  """ Custom function for conv2d:
      Apply  3*3 convolutions with BN and relu.
  """
  for i in range(1, n + 1):
    x = k.layers.Conv2D(filters=kernels, kernel_size=kernel_size,
                        padding=padding, strides=strides,
                        kernel_regularizer=tf.keras.regularizers.l2(1e-4),
                        kernel_initializer=k.initializers.he_normal(seed=5))(x)
    if is_bn:
      x = k.layers.BatchNormalization()(x)
    if is_relu:
      x = k.activations.relu(x)

  return x


def unet3plus(input_shape,
              num_classes,
              encoder=False,
              fine_tune_at=False):
  """ UNet3+ model """

  """ Encoder """
  if encoder == 'resnet':
    resnet_model, filters = resnet(input_shape, fine_tune_at)

    input_layer = resnet_model.get_layer('data').output

    # block 1
    e1 = resnet_model.get_layer('relu0').output

    # block 2
    e2 = resnet_model.get_layer('stage2_unit1_relu1').output

    # block 3
    e3 = resnet_model.get_layer('stage3_unit1_relu1').output

    # block 4
    e4 = resnet_model.get_layer('stage4_unit1_relu1').output

    # block 5
    # bottleneck layer
    e5 = resnet_model.get_layer('relu1').output

  if encoder == 'seresnext':

    seresnext_model, filters = seresnext(input_shape, fine_tune_at)

    input_layer = seresnext_model.get_layer('input').output

    # block 1
    e1 = seresnext_model.get_layer('activation').output

    # block 2
    e2 = seresnext_model.get_layer('activation_15').output

    # block 3
    e3 = seresnext_model.get_layer('activation_35').output

    # block 4
    e4 = seresnext_model.get_layer('activation_65').output

    # block 5
    # bottleneck layer
    e5 = seresnext_model.get_layer('activation_80').output

  if encoder == False:
    filters = [64, 128, 256, 512, 1024]

    input_layer = k.layers.Input(
        shape=input_shape,
        name="input_layer"
    )

    # block 1
    e1 = conv_block(input_layer, filters[0])

    # block 2
    e2 = k.layers.MaxPool2D(pool_size=(2, 2))(e1)
    e2 = conv_block(e2, filters[1])

    # block 3
    e3 = k.layers.MaxPool2D(pool_size=(2, 2))(e2)
    e3 = conv_block(e3, filters[2])

    # block 4
    e4 = k.layers.MaxPool2D(pool_size=(2, 2))(e3)
    e4 = conv_block(e4, filters[3])

    # block 5
    # bottleneck layer
    e5 = k.layers.MaxPool2D(pool_size=(2, 2))(e4)
    e5 = conv_block(e5, filters[4])

  """ Decoder """
  cat_channels = filters[0]
  cat_blocks = len(filters)
  upsample_channels = cat_blocks * cat_channels

  """ d4 """
  e1_d4 = k.layers.MaxPool2D(pool_size=(8, 8))(e1)
  e1_d4 = conv_block(e1_d4, cat_channels, n=1, is_bn=False, is_relu=False)

  e2_d4 = k.layers.MaxPool2D(pool_size=(4, 4))(e2)
  e2_d4 = conv_block(e2_d4, cat_channels, n=1, is_bn=False, is_relu=False)

  e3_d4 = k.layers.MaxPool2D(pool_size=(2, 2))(e3)
  e3_d4 = conv_block(e3_d4, cat_channels, n=1, is_bn=False, is_relu=False)

  e4_d4 = conv_block(e4, cat_channels, n=1, is_bn=False, is_relu=False)

  e5_d4 = k.layers.UpSampling2D(size=(2, 2), interpolation='bilinear')(e5)
  e5_d4 = conv_block(e5_d4, cat_channels, n=1, is_bn=False, is_relu=False)

  d4 = k.layers.concatenate([e1_d4, e2_d4, e3_d4, e4_d4, e5_d4])
  d4 = conv_block(d4, upsample_channels, n=1)

  """ d3 """
  e1_d3 = k.layers.MaxPool2D(pool_size=(4, 4))(e1)
  e1_d3 = conv_block(e1_d3, cat_channels, n=1, is_bn=False, is_relu=False)

  e2_d3 = k.layers.MaxPool2D(pool_size=(2, 2))(e2)
  e2_d3 = conv_block(e2_d3, cat_channels, n=1, is_bn=False, is_relu=False)

  e3_d3 = conv_block(e3, cat_channels, n=1, is_bn=False, is_relu=False)

  e4_d3 = k.layers.UpSampling2D(size=(2, 2), interpolation='bilinear')(d4)
  e4_d3 = conv_block(e4_d3, cat_channels, n=1, is_bn=False, is_relu=False)

  e5_d3 = k.layers.UpSampling2D(size=(4, 4), interpolation='bilinear')(e5)
  e5_d3 = conv_block(e5_d3, cat_channels, n=1, is_bn=False, is_relu=False)

  d3 = k.layers.concatenate([e1_d3, e2_d3, e3_d3, e4_d3, e5_d3])
  d3 = conv_block(d3, upsample_channels, n=1)

  """ d2 """
  e1_d2 = k.layers.MaxPool2D(pool_size=(2, 2))(e1)
  e1_d2 = conv_block(e1_d2, cat_channels, n=1, is_bn=False, is_relu=False)

  e2_d2 = conv_block(e2, cat_channels, n=1, is_bn=False, is_relu=False)

  d3_d2 = k.layers.UpSampling2D(size=(2, 2), interpolation='bilinear')(d3)
  d3_d2 = conv_block(d3_d2, cat_channels, n=1, is_bn=False, is_relu=False)

  d4_d2 = k.layers.UpSampling2D(size=(4, 4), interpolation='bilinear')(d4)
  d4_d2 = conv_block(d4_d2, cat_channels, n=1, is_bn=False, is_relu=False)

  e5_d2 = k.layers.UpSampling2D(size=(8, 8), interpolation='bilinear')(e5)
  e5_d2 = conv_block(e5_d2, cat_channels, n=1, is_bn=False, is_relu=False)

  d2 = k.layers.concatenate([e1_d2, e2_d2, d3_d2, d4_d2, e5_d2])
  d2 = conv_block(d2, upsample_channels, n=1)

  """ d1 """
  e1_d1 = conv_block(e1, cat_channels, n=1, is_bn=False, is_relu=False)

  d2_d1 = k.layers.UpSampling2D(size=(2, 2), interpolation='bilinear')(d2)
  d2_d1 = conv_block(d2_d1, cat_channels, n=1, is_bn=False, is_relu=False)

  d3_d1 = k.layers.UpSampling2D(size=(4, 4), interpolation='bilinear')(d3)
  d3_d1 = conv_block(d3_d1, cat_channels, n=1, is_bn=False, is_relu=False)

  d4_d1 = k.layers.UpSampling2D(size=(8, 8), interpolation='bilinear')(d4)
  d4_d1 = conv_block(d4_d1, cat_channels, n=1, is_bn=False, is_relu=False)

  e5_d1 = k.layers.UpSampling2D(size=(16, 16), interpolation='bilinear')(e5)
  e5_d1 = conv_block(e5_d1, cat_channels, n=1, is_bn=False, is_relu=False)

  d1 = k.layers.concatenate([e1_d1, d2_d1, d3_d1, d4_d1, e5_d1, ])
  d1 = conv_block(d1, upsample_channels, n=1)

  if (encoder == 'seresnext') | (encoder == 'resnet'):
    d1 = k.layers.UpSampling2D(size=(2, 2), interpolation='bilinear')(d1)

  """ d """
  d = conv_block(d1, num_classes, kernel_size=1, n=1, is_bn=False, is_relu=False)
  d = k.activations.softmax(d)

  outputs = [d]

  return tf.keras.Model(inputs=input_layer, outputs=outputs, name='UNet_3Plus')

def create_mask(pred_mask):
  pred_mask = tf.argmax(pred_mask, axis=-1)
  pred_mask = pred_mask[..., tf.newaxis]
  pred_mask = pred_mask.numpy()
  return pred_mask

def prepare_image(image):
  image = cv2.resize(image, (512, 512))
  image = image / 255.0
  image = np.expand_dims(image, axis=(0, -1))
  image = np.repeat(image, repeats=3, axis=-1)  
  return image


def predict_mask(model, data):
  prepared_image = prepare_image(data)
  pred_mask = model.predict(prepared_image)
  pred_mask = create_mask(pred_mask[0])

  return pred_mask
