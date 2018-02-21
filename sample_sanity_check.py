'''
This loads the trained model and runs it on the test set.
Should provide a sanity check on the TensorFlow model.
'''

import tensorflow as tf
from preprocess import load_data, update_channels
from tqdm import tqdm
import numpy as np
import settings_dist
import os
from tempfile import TemporaryFile

sample = "Brats17_TCIA_247_1"

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Get rid of the AVX, SSE warnings

batch_size = 1
export_dir=settings_dist.CHECKPOINT_DIRECTORY + "saved_model/"
print("Loading trained TensorFlow model from directory {}".format(export_dir))

def load_test_data():

    # Load test data
    print('-'*38)
    print('Loading and preprocessing test data...')
    print('-'*38)
    imgs_test, msks_test = load_data("/home/bduser/data_test/{0}/data/".format(sample),"_test")
    imgs_test, msks_test = update_channels(imgs_test, msks_test, settings_dist.IN_CHANNEL_NO, settings_dist.OUT_CHANNEL_NO, settings_dist.MODE)

    return imgs_test, msks_test

def calc_dice(a,b):

    a1 = np.ndarray.flatten(a)
    b1 = np.ndarray.flatten(b)

    return 2.0*(np.sum(a1*b1)+1.0)/(np.sum(a1+b1)+1.0)

with tf.Session(graph=tf.Graph()) as sess:
    tf.saved_model.loader.load(sess, ["serve"], export_dir)
    graph = tf.get_default_graph()
    imgs = graph.get_tensor_by_name("Placeholder:0")
    preds = graph.get_tensor_by_name("Mask/Sigmoid:0")

    imgs_test, msks_test = load_test_data()

    dice = 0.0
    i = 0

    msks_test_predictions = []

    for idx in tqdm(range(0, imgs_test.shape[0] - batch_size, batch_size), desc="Calculating metrics on test dataset", leave=False):
        x_test = imgs_test[idx:(idx+batch_size)]
        y_test = msks_test[idx:(idx+batch_size)]

        feed_dict = {imgs: x_test}

        p = np.array(sess.run([preds], feed_dict=feed_dict))
        dice += calc_dice(y_test, p)

        # Add prediction to numpy array
        msks_test_predictions.append(p)

        i += 1

# Save predictions
save_dir = "/home/bduser/data_test/{0}/data/".format(sample)
np.save("{0}msks_test_predictions.npy".format(save_dir), msks_test_predictions)

print("Average Dice for Test Set = {0}".format(dice/i))
