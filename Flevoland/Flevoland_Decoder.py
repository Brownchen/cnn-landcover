import tensorflow as tf
import CNNModel_3D as CNNModel_3D
import numpy as np
from spectral import get_rgb


def decode(input, config, model_ckp):

    patch_size = config['patch_size']
    kernel_size = config['kernel_size']
    conv1_channels = config['conv1_channels']
    conv2_channels = config['conv2_channels']
    fc1_units = config['fc1_units']

    tf.reset_default_graph()

    with tf.Graph().as_default():

        # Create placeholders
        images_pl, labels_pl, phase_train = CNNModel_2D.placeholder_inputs(patch_size, input.bands)

        # Build a Graph that computes the logits predictions from the
        # inference model.
        logits, keep_prob = CNNModel_2D.inference(images_pl, input.bands, patch_size,
                                                  kernel_size, conv1_channels, conv2_channels,
                                                  fc1_units, input.num_classes, phase_train)

        softmax = tf.nn.softmax(logits)

        saver = tf.train.Saver()

        sess = tf.Session()

        saver.restore(sess, model_ckp)

        predicted_image = np.zeros(shape=(input.height, input.width))
        correct_pixels_train, correct_pixels_test = [], []

        dist_border = int((patch_size - 1) / 2)  # Distance from center to border of the patch

        for i in range(input.height):
            col_patches = []
            # col_labels = []
            for j in range(input.width):

                label = 0
                # is_train = input.train_data[i, j] != 0
                #
                # if is_train:
                #     label = input.train_data[i, j]

                patch = input.Patch(patch_size, i+dist_border, j+dist_border, pad=True)
                col_patches.append(patch)
                # patch = np.expand_dims(patch, axis=0)  # Shape [-1,patch_size,patch_size,in_channels]
                # predictions = sess.run(softmax, feed_dict={images_pl: patch, keep_prob: 1, phase_train: False})
                # y_ = np.argmax(predictions) + 1
                # predicted_image[i][j] = y_

                # if label == y_:
                #     if is_train:
                #         correct_pixels_train.append(1)
                #
                # else:
                #     if is_train:
                #         correct_pixels_train.append(0)

            predictions = sess.run(softmax, feed_dict={images_pl: col_patches, keep_prob: 1, phase_train: False})
            y_ = [np.argmax(pred) + 1 for pred in predictions]
            predicted_image[i] = y_

        # train_acc = np.asarray(correct_pixels_train).mean()*100
        # test_acc = np.asarray(correct_pixels_test).mean()*100
        sess.close()
        return predicted_image


def output_image(input, output):
    return get_rgb(output, color_scale=input.color_scale)



def decode3D(input, config, model_ckp):

    patch_size = config['patch_size']
    in_depth = config['in_depth']
    in_channels = config['in_channels']
    spectral_kernel_size = config['spectral_kernel_size']
    spatial_kernel_size = config['spatial_kernel_size']
    conv1_channels = config['conv1_channels']
    conv2_channels = config['conv2_channels']
    fc1_units = config['fc1_units']

    tf.reset_default_graph()

    with tf.Graph().as_default():

        # Create placeholders
        images_pl, labels_pl, phase_train = CNNModel_3D.placeholder_inputs(patch_size, input.bands)

        # Build a Graph that computes the logits predictions from the
        # inference model.
        logits, keep_prob = CNNModel_3D.inference(images_pl, in_depth, in_channels, patch_size,
                                                  spectral_kernel_size, spatial_kernel_size, conv1_channels, conv2_channels,
                                                  fc1_units, input.num_classes, phase_train)

        softmax = tf.nn.softmax(logits)

        saver = tf.train.Saver()

        sess = tf.Session()

        saver.restore(sess, model_ckp)

        predicted_image = np.zeros(shape=(input.height, input.width))
        correct_pixels_train, correct_pixels_test = [], []

        dist_border = int((patch_size - 1) / 2)  # Distance from center to border of the patch

        for i in range(input.height):
            col_patches = []
            # col_labels = []
            for j in range(input.width):

                label = 0
                # is_train = input.train_data[i, j] != 0
                #
                # if is_train:
                #     label = input.train_data[i, j]

                patch = input.Patch(patch_size, i+dist_border, j+dist_border, pad=True)
                col_patches.append(patch)
                # patch = np.expand_dims(patch, axis=0)  # Shape [-1,patch_size,patch_size,in_channels]
                # predictions = sess.run(softmax, feed_dict={images_pl: patch, keep_prob: 1, phase_train: False})
                # y_ = np.argmax(predictions) + 1
                # predicted_image[i][j] = y_

                # if label == y_:
                #     if is_train:
                #         correct_pixels_train.append(1)
                #
                # else:
                #     if is_train:
                #         correct_pixels_train.append(0)

            col_patches = np.asarray(col_patches)
            col_patches = np.transpose(col_patches, axes=(0, 3, 1, 2))
            col_patches = np.expand_dims(col_patches, axis=4)

            predictions = sess.run(softmax, feed_dict={images_pl: col_patches, keep_prob: 1, phase_train: False})
            y_ = [np.argmax(pred) + 1 for pred in predictions]
            predicted_image[i] = y_

        # train_acc = np.asarray(correct_pixels_train).mean()*100
        # test_acc = np.asarray(correct_pixels_test).mean()*100
        sess.close()
        return predicted_image
