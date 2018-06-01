import keras.backend as K
from keras.layers import Input, Conv2D, UpSampling2D, BatchNormalization, ZeroPadding2D, MaxPooling2D, Concatenate, \
    Reshape
from keras.models import Model
from keras.utils import plot_model

from config import num_classes
from custom_layers.unpooling_layer import Unpooling


def build_encoder_decoder():
    kernel = 3

    # Encoder
    input_tensor = Input(shape=(320, 320, 3))
    x = Conv2D(64, (kernel, kernel), activation='relu', padding='same', name='conv1_1', kernel_initializer='he_normal',
               bias_initializer='zeros')(input_tensor)
    x = Conv2D(64, (kernel, kernel), activation='relu', padding='same', name='conv1_2', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    orig_1 = x
    x = MaxPooling2D((2, 2), strides=(2, 2))(x)

    x = Conv2D(128, (kernel, kernel), activation='relu', padding='same', name='conv2_1', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = Conv2D(128, (kernel, kernel), activation='relu', padding='same', name='conv2_2', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    orig_2 = x
    x = MaxPooling2D((2, 2), strides=(2, 2))(x)

    x = Conv2D(256, (kernel, kernel), activation='relu', padding='same', name='conv3_1', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = Conv2D(256, (kernel, kernel), activation='relu', padding='same', name='conv3_2', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = Conv2D(256, (kernel, kernel), activation='relu', padding='same', name='conv3_3', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    orig_3 = x
    x = MaxPooling2D((2, 2), strides=(2, 2))(x)

    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='conv4_1', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='conv4_2', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='conv4_3', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    orig_4 = x
    x = MaxPooling2D((2, 2), strides=(2, 2))(x)

    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='conv5_1', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='conv5_2', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='conv5_3', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    orig_5 = x
    x = MaxPooling2D((2, 2), strides=(2, 2))(x)

    # Decoder
    x = UpSampling2D(size=(2, 2))(x)
    the_shape = K.int_shape(orig_5)
    shape = (1, the_shape[1], the_shape[2], the_shape[3])
    origReshaped = Reshape(shape)(orig_5)
    xReshaped = Reshape(shape)(x)
    together = Concatenate(axis=1)([origReshaped, xReshaped])
    x = Unpooling()(together)
    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='deconv5_1',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)
    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='deconv5_2',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)
    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='deconv5_3',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)

    x = UpSampling2D(size=(2, 2))(x)
    the_shape = K.int_shape(orig_4)
    shape = (1, the_shape[1], the_shape[2], the_shape[3])
    origReshaped = Reshape(shape)(orig_4)
    xReshaped = Reshape(shape)(x)
    together = Concatenate(axis=1)([origReshaped, xReshaped])
    x = Unpooling()(together)
    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='deconv4_1',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)
    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='deconv4_2',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)
    x = Conv2D(512, (kernel, kernel), activation='relu', padding='same', name='deconv4_3',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)

    x = UpSampling2D(size=(2, 2))(x)
    the_shape = K.int_shape(orig_3)
    shape = (1, the_shape[1], the_shape[2], the_shape[3])
    origReshaped = Reshape(shape)(orig_3)
    xReshaped = Reshape(shape)(x)
    together = Concatenate(axis=1)([origReshaped, xReshaped])
    x = Unpooling()(together)
    x = Conv2D(256, (kernel, kernel), activation='relu', padding='same', name='deconv3_1',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)
    x = Conv2D(256, (kernel, kernel), activation='relu', padding='same', name='deconv3_2',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)
    x = Conv2D(256, (kernel, kernel), activation='relu', padding='same', name='deconv3_3',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)

    x = UpSampling2D(size=(2, 2))(x)
    the_shape = K.int_shape(orig_2)
    shape = (1, the_shape[1], the_shape[2], the_shape[3])
    origReshaped = Reshape(shape)(orig_2)
    xReshaped = Reshape(shape)(x)
    together = Concatenate(axis=1)([origReshaped, xReshaped])
    x = Unpooling()(together)
    x = Conv2D(128, (kernel, kernel), activation='relu', padding='same', name='deconv2_1',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)
    x = Conv2D(128, (kernel, kernel), activation='relu', padding='same', name='deconv2_2',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)

    x = UpSampling2D(size=(2, 2))(x)
    the_shape = K.int_shape(orig_1)
    shape = (1, the_shape[1], the_shape[2], the_shape[3])
    origReshaped = Reshape(shape)(orig_1)
    xReshaped = Reshape(shape)(x)
    together = Concatenate(axis=1)([origReshaped, xReshaped])
    x = Unpooling()(together)
    x = Conv2D(64, (kernel, kernel), activation='relu', padding='same', name='deconv1_1',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)
    x = Conv2D(64, (kernel, kernel), activation='relu', padding='same', name='deconv1_2',
               kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)

    x = Conv2D(num_classes, (1, 1), activation='softmax', padding='valid', name='pred', kernel_initializer='he_normal',
               bias_initializer='zeros')(x)
    x = BatchNormalization()(x)

    model = Model(inputs=input_tensor, outputs=x)
    return model


if __name__ == '__main__':
    encoder_decoder = build_encoder_decoder()
    # input_layer = model.get_layer('input')
    print(encoder_decoder.summary())
    plot_model(encoder_decoder, to_file='encoder_decoder.svg', show_layer_names=True, show_shapes=True)

    K.clear_session()
