import tensorflow as tf

from Model.Graph.Graph import deepNN
from Model.ModelDataGenerator import ModelDataGenerator


class TestModel:
    def __init__(self):
        self.model_data_generator = ModelDataGenerator()

    def main(self):

        tf.reset_default_graph()

        # Build the graph for the deep net
        with tf.name_scope('inputs'):
            x = tf.placeholder(tf.float32, [None, self.model_data_generator.input_length])
            y_ = tf.placeholder(tf.float32, [None, self.model_data_generator.class_count])


        with tf.name_scope('model'):
            y_conv = deepNN(x, False, self.model_data_generator.class_count)

        x_shape = [-1, self.model_data_generator.input_length]

        saver = tf.train.Saver(tf.global_variables(), max_to_keep=1, save_relative_paths=True)

        sess = tf.Session()
        # First let's load meta graph and restore weights
        saver = tf.train.import_meta_graph('../logs/exp_bs_100/model.ckpt-1999.meta')
        saver.restore(sess, tf.train.latest_checkpoint('../logs/exp_bs_100/'))

        (testImages, testLabels) = self.model_data_generator.getValidationBatch()

        prediction = tf.argmax(y_conv, 1)
        labels = sess.run(prediction,
                          feed_dict={x: testImages.reshape(x_shape), y_: testLabels})

        print(labels)



if __name__ == "__main__":
    s = TestModel()
    s.main()

