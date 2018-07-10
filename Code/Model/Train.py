import os

import tensorflow as tf
import time
import platform
from Graph.Graph import Model
import DataProcessing.American.Globals as Globals
from DataProcessing.American.FeatureExtractionSecond import FeatureExtractionSecond
from ModelDataGenerator import ModelDataGenerator
from DataProcessing.American.DataParser import DataParser
from DataGenerator import DataGenerator
import numpy as np
import sklearn as sk

class Train:
    def __init__(self, ModelDataGenerator_IN=False):
        self.FLAGS = tf.app.flags.FLAGS
        if ModelDataGenerator_IN != False:
            self.model_data_generator = ModelDataGenerator_IN
        else:
            self.model_data_generator = ModelDataGenerator()

        tf.app.flags.DEFINE_string('data_dir', os.getcwd() + '/dataset/',
                                   'Directory where the dataset will be stored and checkpoint. (default: %(default)s)')
        tf.app.flags.DEFINE_integer('max_steps', 16000,
                                    'Number of mini-batches to train on. (default: %(default)d)')
        tf.app.flags.DEFINE_integer('log_frequency', 20,
                                    'Number of steps between logging results to the console and saving summaries (default: %(default)d)')
        tf.app.flags.DEFINE_integer('flush_frequency', 50,
                                    'Number of steps between flushing summary results. (default: %(default)d)')
        tf.app.flags.DEFINE_integer('save_model_frequency', 100,
                                    'Number of steps between model saves. (default: %(default)d)')

        # Optimisation hyperparameters
        # tf.app.flags.DEFINE_integer('batch_size', 590,
        tf.app.flags.DEFINE_integer('batch_size', Globals.BATCH_SIZE,
                                    'Number of examples per mini-batch (default: %(default)d)')
        tf.app.flags.DEFINE_float('learning_rate', 0.0002,
                                  'Number of examples to run. (default: %(default)d)')
        tf.app.flags.DEFINE_float('weight_decay_rate', 0.0001,
                                  'Weight decay rate. (default: %(default)d)')
        tf.app.flags.DEFINE_integer('input_length', self.model_data_generator.input_length,
                                    'Length of input vector (default: %(default)d)')
        tf.app.flags.DEFINE_integer('class_count', self.model_data_generator.class_count,
                                    'Number of classes (default: %(default)d)')
        tf.app.flags.DEFINE_string('log_dir', (Globals.get_log_dir() + Globals.CURRENT_DESCRIPTION).format(cwd=os.getcwd()),
                                   'Directory where to write event logs and checkpoint. (default: %(default)s)')
        tf.app.flags.DEFINE_float('dropout_rate', 0.25,
                                  'Dropout, probability to drop a unit')
        tf.app.flags.DEFINE_float('validation_iterations', 400,
                                  'Dropout, probability to drop a unit')
        tf.app.flags.DEFINE_float('weight_ratio', 1.0,
                                  'Dropout, probability to drop a unit')

        self.run_log_dir = os.path.join(self.FLAGS.log_dir,
                                        'bs_{bs}'.format(bs=self.FLAGS.batch_size,
                                                         name=Globals.CURRENT_DESCRIPTION))

        self.checkpoint_path = os.path.join(self.run_log_dir, 'model.ckpt')

        self.model_data_generator.batch_size = self.FLAGS.batch_size

        # limit the process memory to a third of the total gpu memory
        self.gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.33)


    def main(self):
        NPV = 0;Precision = 0;roc_auc = 0;acc = 0; cm=[];
        tf.reset_default_graph()

        # Build the graph for the deep net
        with tf.name_scope('inputs'):
            x = tf.placeholder(tf.float32, [None, self.FLAGS.input_length])
            # x_image = tf.reshape(x, [-1, self.FLAGS.img_width, self.FLAGS.img_height, self.FLAGS.img_channels])
            y_ = tf.placeholder(tf.float32, [None, self.FLAGS.class_count])

        training = tf.placeholder(tf.bool, name='training')

        with tf.name_scope('model'):
            y_conv = Model().network(x, training, self.FLAGS.class_count)

        if Globals.MULTI_LABEL:
            cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y_conv)
        else:
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv)


        class_ratio = tf.placeholder(tf.float32, shape=[])

        # [label bad, label good]
        # class_ratio = number of bad loans / total loans

        # 0 < weight_ratio < 2
        # class_ratio = tf.maximum(class_ratio, 0.001)

        class_weights = [(1 - class_ratio) * self.FLAGS.weight_ratio, class_ratio * (2 - self.FLAGS.weight_ratio)]



        # deduce weights for batch samples based on their true label
        weights = tf.reduce_sum(class_weights * y_, axis=1)
        # apply the weights, relying on broadcasting of the multiplication
        weighted_losses = cross_entropy * weights
        # reduce the result to get your final loss
        cross_entropy = tf.reduce_mean(weighted_losses)


        # cross_entropy = tf.reduce_mean(cross_entropy)



        global_step = tf.Variable(0, trainable=False)  # this will be incremented automatically by tensorflow
        decay_steps = 100000  # decay the learning rate every 1000 steps
        decay_rate = 0.01 # the base of our exponential for the decay
        decayed_learning_rate = tf.train.exponential_decay(0.000001, global_step,
                                                           decay_steps, decay_rate, staircase=True)

        # TURN ON for BN
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update_ops):
            # Ensures that we execute the update_ops before performing the train_step
            train_step = tf.train.AdamOptimizer(decayed_learning_rate).minimize(cross_entropy, global_step=global_step)


        # Mortgage Risk Learning Rate
        t = tf.placeholder(tf.float32, shape=[])
        # lr0 = 0.0001
        # lr0 = 0.00002
        # decayed_learning_rate = pow(lr0,1/(t/800))
        decayed_learning_rate = self.FLAGS.learning_rate / (1 + t/100000)
        momentum = 0.9
        train_step = tf.train.MomentumOptimizer(decayed_learning_rate, momentum).minimize(cross_entropy)
        # train_step = tf.train.AdamOptimizer(decayed_learning_rate).minimize(cross_entropy, global_step=global_step)
        epoc_itr = 0


        train_step = tf.train.AdamOptimizer(0.00001).minimize(cross_entropy, global_step=global_step)


        if Globals.MULTI_LABEL:
            # prediction = tf.round(y_conv)
            # correct_prediction = tf.equal(prediction, y_)
            correct_prediction = tf.equal(tf.round(tf.nn.sigmoid(y_conv)), y_)

        else:
            # correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
            correct_prediction = tf.equal(tf.round(tf.nn.softmax(y_conv)), y_)


        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')
        loss_summary = tf.summary.scalar("Loss", cross_entropy)
        acc_summary = tf.summary.scalar("Accuracy", accuracy)
        learning_rate_summary = tf.summary.scalar("Learning Rate", decayed_learning_rate)

        # summaries for TensorBoard visualisation
        validation_summary = tf.summary.merge([acc_summary, loss_summary, learning_rate_summary])
        train_summary = tf.summary.merge([acc_summary, loss_summary, learning_rate_summary])

        saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)




        with tf.Session(config=tf.ConfigProto(gpu_options=self.gpu_options)) as sess:
            self.train_writer = tf.summary.FileWriter(self.run_log_dir + "_train", sess.graph)
            self.validation_writer = tf.summary.FileWriter(self.run_log_dir + "_validation", sess.graph)

            sess.run(tf.global_variables_initializer())
            sess.run(tf.local_variables_initializer())

            start_time = time.time()

            # Training and validation
            for step in range(self.FLAGS.max_steps):
                start_time_batch = time.time()

                x_shape = [-1, self.FLAGS.input_length]

                if step % 6 == 0:
                    (train_data, train_labels) = self.model_data_generator.getTrainBatch()
                    batch_ratio = float(len( np.where( train_labels[:,0] == 1 )[0] )) / len(train_labels[:,0])
                    # print batch_ratio

                # print("Time batch: " + str(((time.time() - start_time_batch)) * 100))

                if (step * self.FLAGS.batch_size % self.model_data_generator.training_size < self.FLAGS.batch_size):
                    epoc_itr = epoc_itr + 1
                    self.model_data_generator.shuffle_data()

                _, train_summary_str = sess.run([train_step, train_summary],
                                                feed_dict={x: train_data,
                                                           y_: train_labels, training: True,
                                                           t: epoc_itr,
                                                           class_ratio: batch_ratio})

                # Validation: Monitoring accuracy using validation set
                if (step + 1) % self.FLAGS.log_frequency == 0:
                    # print('step {}'.format(step))
                    (validation_data, validation_labels) = self.model_data_generator.getValidationBatch()
                    batch_ratio = float(len( np.where( validation_labels[:,0] == 1 )[0] )) / len(validation_labels[:,0])

                    # print "%f.02 , %f.02" % ((1-batch_ratio), batch_ratio)
                    # print len(validation_data[0])

                    # self.model_data_generator.print_class_ratios(validation_labels, "Validation batch ratio: ")

                    validation_accuracy, validation_summary_str = sess.run([accuracy, validation_summary],
                                                                           feed_dict={x: validation_data,
                                                                                      y_: validation_labels, training: False,
                                                                                      t: epoc_itr,
                                                                                      class_ratio: batch_ratio})

                    # print('step {}, epoc {}, accuracy on validation set : {}'.format(step, epoc_itr, validation_accuracy))

                    # print("Time: " + str(((time.time() - start_time) / self.FLAGS.batch_size) * 100))
                #     start_time = time.time()

                    self.train_writer.add_summary(train_summary_str, step)
                    self.validation_writer.add_summary(validation_summary_str, step)

                # Save the model checkpoint periodically.
                if (step + 1) % self.FLAGS.save_model_frequency == 0 or (step + 1) == self.FLAGS.max_steps:
                    saver.save(sess, self.checkpoint_path, global_step=step)

                if (step + 1) % self.FLAGS.flush_frequency == 0:
                    self.train_writer.flush()
                    self.validation_writer.flush()

            validation_accuracy_avg = 0
            validation_labels_real = []
            validation_labels_pred = []
            for i in range(0, self.FLAGS.validation_iterations):
                (validation_data, validation_labels) = self.model_data_generator.getValidationBatch()
                batch_ratio = float(len(np.where(validation_labels[:, 0] == 1)[0])) / len(validation_labels[:, 0])
                if Globals.MULTI_LABEL:
                    y_conv = tf.round(tf.nn.sigmoid(y_conv))
                else:
                    y_conv = tf.round(tf.nn.softmax(y_conv))


                validation_labels_out, validation_accuracy = sess.run([y_conv, accuracy], feed_dict={x: validation_data,
                                                                                          y_: validation_labels,
                                                                                          training: False,
                                                                                          t: epoc_itr,
                                                                                          class_ratio: batch_ratio})
                if i == 0:
                    validation_accuracy_avg = validation_accuracy
                    validation_labels_real = validation_labels
                    validation_labels_pred = validation_labels_out
                    # print validation_labels[0]
                    # print validation_labels_pred[0]
                else:
                    validation_accuracy_avg = (validation_accuracy_avg + validation_accuracy) / 2
                    validation_labels_real = np.concatenate([validation_labels_real, validation_labels])
                    validation_labels_pred = np.concatenate([validation_labels_pred, validation_labels_out])

            print('Accuracy on test set : {}'.format(validation_accuracy_avg))

            classes = DataGenerator().ActiveTargetClass
            np.set_printoptions(threshold=np.nan)

            from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, roc_curve, auc, roc_auc_score

            if len(validation_labels_real.shape) == 1:
                con = tf.confusion_matrix(labels=validation_labels_real, predictions=validation_labels_pred)
                print("Confusion Matrix " + str(classes[0]) + ": ")
                with tf.Session() as sess:
                    print sess.run(con)
                from sklearn.metrics import confusion_matrix, accuracy_score
                print accuracy_score(validation_labels_real, validation_labels_pred)
            else:
                num_of_labels = validation_labels_real.shape[1]
                # for i in range(0, num_of_labels):
                for i in range(0, 1):
                    validation_labels_real_i = validation_labels_real[:, i]
                    validation_labels_pred_i = validation_labels_pred[:, i]
                    np.set_printoptions(threshold=np.nan)
                    print("\nConfusion Matrix " + str(classes[i]) + ": " )
                    cm = confusion_matrix(validation_labels_real_i, validation_labels_pred_i)
                    print cm
                    print
                    # print "\nPrecision: " + str(precision_score(validation_labels_real_i, validation_labels_pred_i))
                    # print "Recall: " + str(recall_score(validation_labels_real_i, validation_labels_pred_i))
                    NPV = float(cm[1][1] / float(cm[1][0] + cm[1][1]))
                    Precision = float(cm[0][0] / float(cm[0][0] + cm[0][1]))
                    roc_auc = roc_auc_score(validation_labels_real_i, validation_labels_pred_i)
                    print "TPR (Recall): %.4f" % NPV
                    print "TNR (Specificity): %.4f" % Precision
                    print "ROC AUC: %.4f" % roc_auc
                    print
                    acc = accuracy_score(validation_labels_real, validation_labels_pred)
                    print "Accuracy: %.4f" % acc

                    print "train.FLAGS.weight_ratio = %.4f" % self.FLAGS.weight_ratio
                    print "train.FLAGS.learning_rate = %.8f" % self.FLAGS.learning_rate
                    print "train.FLAGS.max_steps = %.0f" % self.FLAGS.max_steps


                    print "%.4f, %.4f, %.4f, %.4f, %.4f, %.8f, %.0f" % (NPV, Precision, roc_auc, acc, self.FLAGS.weight_ratio, self.FLAGS.learning_rate, self.FLAGS.max_steps)




            # Print Gradients
            # var = tf.Variable(tf.int64)  # Must be a tf.float32 or tf.float64 variable.
            # x = tf.placeholder(tf.float32, [None, self.FLAGS.input_length])
            #
            # loss = cross_entropy # some_function_of() returns a `Tensor`.
            # var_grad = tf.gradients(loss, [x])[0]

            # optimiser = tf.train.MomentumOptimizer(decayed_learning_rate, momentum)
            # gradients = optimiser.compute_gradients(loss=cross_entropy)
            # l2_norm = lambda t: tf.sqrt(tf.reduce_sum(tf.pow(t, 2)))
            # for gradient, variable in gradients:
            #     tf.summary.histogram("gradients/" + variable.name, l2_norm(gradient))
            #     tf.summary.histogram("variables/" + variable.name, l2_norm(variable))
            # train_op = optimiser.apply_gradients(gradients)
            # summaries_op = tf.summary.merge_all()
            # _, summary = sess.run([train_op, summaries_op], feed_dict={x: train_data,
            #                                                            y_: train_labels, training: True,
            #                                                            t: epoc_itr})
            # self.train_writer.add_summary(summary, step)



            self.train_writer.close()
            self.validation_writer.close()

            return (NPV, Precision, roc_auc, acc, cm)


if __name__ == "__main__":
    run_info = "Base data only -1"

    print run_info

    if platform.system() == 'Darwin':
        dataset = DataParser().AmericanCombo_i_FE2(-3)
        df_OHE = FeatureExtractionSecond().filter_main(dataset)
        DataParser()._write_HDFStore_OHE(df_OHE, -3)
        df_OHE = DataParser()._read_HDFStore_OHE(-3)
        modelDataGenerator = ModelDataGenerator(False)
        modelDataGenerator.load_data(df_OHE, DataGenerator().ActiveTargetClass)
    else:
        dataset = DataParser().AmericanCombo_i_FE2(-3)
        df_OHE = FeatureExtractionSecond().filter_main(dataset)
        DataParser()._write_HDFStore_OHE(df_OHE, -3)
        df_OHE = DataParser()._read_HDFStore_OHE(-3)
        modelDataGenerator = ModelDataGenerator(False)
        modelDataGenerator.load_data(df_OHE, DataGenerator().ActiveTargetClass)




    train = Train(modelDataGenerator)
    log_str = 0

    # weight_ratios = [1.6975, 1.6975, 1.6975, 1.6975, 1.6975]
    # weight_ratios = [1.25, 1.25, 1.25, 1.25]
    weight_ratios = [1.0, 1.0, 1.05, 1.05]

    lrs = [0.0001]
    NPV = 0; Precision = 0; roc_auc = 0; acc = 0; cm = []

    first_time = True
    for lr in lrs:
        print "-------------------------" + str(lr) + "------------------------------"

        for w in weight_ratios:
            print "-------------------------" + str(w) + "------------------------------"
            start_time = time.time()

            log_str = log_str + 1
            train.FLAGS.log_dir = (Globals.get_log_dir() + Globals.CURRENT_DESCRIPTION + str(log_str)).format(
                cwd=os.getcwd())
            train.run_log_dir = os.path.join(train.FLAGS.log_dir, 'bs_{bs}'.format(bs=train.FLAGS.batch_size))
            train.checkpoint_path = os.path.join(train.run_log_dir, 'model.ckpt')

            train.FLAGS.weight_ratio = w
            train.FLAGS.learning_rate = lr
            train.FLAGS.max_steps = 1000000
            train.FLAGS.validation_iterations = 2000


            (NPV_i, Precision_i, roc_auc_i, acc_i, cm_i) = train.main()
            if first_time:
                first_time = False
                NPV = NPV_i
                Precision = Precision_i
                roc_auc = roc_auc_i
                acc = acc_i
                cm_i = np.array(cm_i).astype(np.float32, copy=False)
                cm = cm_i
            else:
                NPV = (NPV + NPV_i) / 2
                Precision = (Precision + Precision_i) / 2
                roc_auc = (roc_auc + roc_auc_i) / 2
                acc = (acc + acc_i) / 2
                cm_i = np.array(cm_i).astype(np.float32, copy=False)
                cm = (cm + cm_i) / 2
            print("--- %s seconds ---" % (time.time() - start_time))
            start_time = time.time()


    print
    print("Confusion Matrix : ")
    print cm
    print "TPR (Recall): %.4f" % NPV
    print "TNR (Specificity): %.4f" % Precision
    print "ROC AUC: %.4f" % roc_auc
    print
    print "Accuracy: %.4f" % acc
    print
    print "%.4f, %.4f, %.4f, %.4f" % (NPV, Precision, roc_auc, acc)

    print run_info






    # train = Train()
    # print "Model: Initialisation Done"
    # train.main()
