import tensorflow as tf

class Model:
    def __init__(self):
        self.node_count = 0

    def network(self, input, training, class_count):

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

        hidden_layers = [100,100]
        dropout_rate = 1

        layer_input = input
        for layer in hidden_layers:
            layer_input = Dense(layer_input, layer)
            layer_input = tf.nn.dropout(layer_input, dropout_rate)

        # Output: fully connected 64 -> class_count
        logits = tf.layers.dense(
            inputs=layer_input,
            units=class_count,
            name='fc_final'
        )

        return logits