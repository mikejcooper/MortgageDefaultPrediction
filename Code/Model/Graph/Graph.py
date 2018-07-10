import tensorflow as tf

class Config:
    def __init__(self):
        print "maybe to do"



class Model:
    def __init__(self):
        print "Graph"
        self.node_count = 0

    def network(self, input, training, class_count):

        def Dense_BN(input, units):
            self.node_count += 1
            regularizer = tf.contrib.layers.l2_regularizer(scale=0.1)
            initializer = tf.contrib.layers.xavier_initializer()
            fc = tf.layers.dense(
                inputs=input,
                activation=None,
                # kernel_regularizer=regularizer,
                kernel_initializer=initializer,
                units=units,
                name='fc' + str(self.node_count)
            )
            bn = tf.layers.batch_normalization(fc, training=training, name='bn' + str(self.node_count))
            relu = tf.nn.relu(bn)
            return relu

        def Dense(input, units):
            self.node_count += 1
            regularizer = tf.contrib.layers.l2_regularizer(scale=0.1)
            initializer = tf.contrib.layers.xavier_initializer()
            return tf.layers.dense(
                inputs=input,
                activation=tf.nn.relu,
                kernel_regularizer=regularizer,
                kernel_initializer=initializer,
                units=units,
                name='fc' + str(self.node_count)
            )

        def Conv(input):
            self.node_count += 1
            return tf.layers.conv1d(
                inputs=input,
                filters=32,
                kernel_size=5,
                padding='same',
                use_bias=False,
                strides=1,
                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                kernel_regularizer=tf.contrib.layers.l2_regularizer(0.1),
                name='conv2d_' + str(self.node_count)
            )

        # hidden_layers = [200,140,140,140,140]
        hidden_layers = [30,30]
        hidden_layers = [100,100]
        dropout_rate = 0.5
        # hidden_layers = [200, 150, 180, 80, 100, 90, 38]

        layer_input = input
        # layer_input = tf.layers.batch_normalization(layer_input, training=training, name='bn' + str(self.node_count))
        # layer_input = tf.nn.dropout(layer_input, dropout_rate)
        for layer in hidden_layers:
            # layer_input = tf.layers.batch_normalization(layer_input, training=training, name='bn' + str(self.node_count))
            layer_input = Dense(layer_input, layer)
            layer_input = tf.nn.dropout(layer_input, dropout_rate)




        # Output: fully connected 64 -> class_count
        logits = tf.layers.dense(
            inputs=layer_input,
            units=class_count,
            name='fc_final'
        )

        return logits



    def simple_fully_connected(self, input, training, class_count):
        # Output: fully connected class_count -> 35
        fc1 = tf.layers.dense(
            inputs=input,
            activation=tf.nn.relu,
            units=200,
            name='fc1'
        )

        fc1 = tf.nn.relu(tf.layers.batch_normalization(fc1, training=training))

        # Output: fully connected 64 -> class_count
        logits = tf.layers.dense(
            inputs=fc1,
            units=class_count,
            name='fc2'
        )

        return logits