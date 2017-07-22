import tensorflow as tf
import numpy as np
import pandas as pd

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


trainData = np.genfromtxt('trainData.csv', delimiter=',')
testData = np.genfromtxt('testData.csv', delimiter=',')


train_x = trainData[0:,0:23]
train_y = trainData[0:,[24,25]]
test_x = testData[0:,0:23]
test_y = testData[0:,[24,25]]

nodes_hl1 = 4
nodes_hl2 = 4
n_classes = 2
batch_size = 100



# height x width
x = tf.placeholder('float', [None, 23])
y = tf.placeholder('float')


def neural_net(data):
    hidden_layer_1 = {'weights': tf.Variable(tf.random_normal([23,nodes_hl1],seed=1)),
                        'bias': tf.Variable(tf.random_normal([nodes_hl1],seed=1))}
    hidden_layer_2 = {'weights': tf.Variable(tf.random_normal([nodes_hl1,nodes_hl2],seed=1)),
                        'bias': tf.Variable(tf.random_normal([nodes_hl2],seed=1))}
    output_layer = {'weights': tf.Variable(tf.random_normal([nodes_hl2,n_classes],seed=1)),
                        'bias': tf.Variable(tf.random_normal([n_classes],seed=1))}

    # (data * weights) + bias

    l1 = tf.add(tf.matmul(data, hidden_layer_1['weights']), hidden_layer_1['bias'])
    l1 = tf.nn.relu(l1)
    l2 = tf.add(tf.matmul(l1, hidden_layer_2['weights']), hidden_layer_2['bias'])
    l2 = tf.nn.relu(l2)
    # Activation Function
    output = tf.add(tf.matmul(l2, output_layer['weights']), output_layer['bias'])
    return output


def train_NN(x):

    # Setup Model
    prediction = neural_net(x)

    #Produce Cost Function
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction,labels=y))

    # Optimizer
    optimize = tf.train.AdamOptimizer().minimize(cost)

    # Number of Back Prop Cycles
    cycles = 10

    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())
        for cycle in range(cycles):
            cycle_loss = 0
            i = 0
            while i < len(train_x):
                start = i
                end = batch_size+i
                batch_x = np.array(train_x[start:end])
                batch_y = np.array(train_y[start:end])
                _, c = sess.run([optimize,cost], feed_dict={x: batch_x, y: batch_y})
                cycle_loss += c
                i += batch_size

            print ("Epoch", cycle+1, "completed out of" , cycles)

        correct = tf.equal(tf.argmax(prediction,1),tf.argmax(y,1))
        accuracy = tf.reduce_mean(tf.cast(correct,'float'))
        print ('Accuracy', accuracy.eval({x:test_x, y:test_y}))

train_NN(x)
