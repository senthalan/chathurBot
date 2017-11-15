from __future__ import print_function

import os
import sys

import numpy as np
from keras.layers import Activation, TimeDistributed, Dense, RepeatVector, Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import text_to_word_sequence


def load_data(source, dist, max_len):
    # Reading raw text from source and destination files
    f = open(source, 'r')
    x_data = f.read()
    f.close()
    f = open(dist, 'r')
    y_data = f.read()
    f.close()

    # Splitting raw text into array of sequences
    X = [text_to_word_sequence(x) for x, y in zip(x_data.split('\n'), y_data.split('\n')) if
         len(x) > 0 and max_len >= 0 < len(y) <= max_len]
    y = [text_to_word_sequence(y) for x, y in zip(x_data.split('\n'), y_data.split('\n')) if
         len(x) > 0 and max_len >= 0 < len(y) <= max_len]

    # Converting each word to its index value
    for i, sentence in enumerate(X):
        for j, word in enumerate(sentence):
            X[i][j] = word

    for i, sentence in enumerate(y):
        for j, word in enumerate(sentence):
            y[i][j] = word
    return (X, y)


def load_test_data(source, max_len):
    f = open(source, 'r')
    X_data = f.read()
    f.close()

    X = [text_to_word_sequence(x) for x in X_data.split('\n') if len(x) > 0 and len(x) <= max_len]
    for i, sentence in enumerate(X):
        for j, word in enumerate(sentence):
            X[i][j] = word
    return X


def create_model(X_vocab_len, X_max_len, y_vocab_len, y_max_len, hidden_size, num_layers):
    model = Sequential()

    # Creating encoder network
    model.add(Embedding(X_vocab_len, 1000, input_length=X_max_len, mask_zero=True))
    model.add(LSTM(hidden_size))
    model.add(RepeatVector(y_max_len))

    # Creating decoder network
    for _ in range(num_layers):
        model.add(LSTM(hidden_size, return_sequences=True))
    model.add(TimeDistributed(Dense(y_vocab_len)))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    return model


def process_data(word_sentences, max_len):
    # Vectorizing each element in each sequence
    sequences = np.zeros((len(word_sentences), max_len, 40))
    for i, sentence in enumerate(word_sentences):
        for j, word in enumerate(sentence):
            sequences[i, j, word] = 1.
    return sequences


def find_checkpoint_file(folder):
    checkpoint_file = [folder + f for f in os.listdir(folder) if 'checkpoint' in f]
    if len(checkpoint_file) == 0:
        return []
    for f in checkpoint_file:
        print(f)
    modified_time = [os.path.getmtime(f) for f in checkpoint_file]
    return checkpoint_file[np.argmax(modified_time)]


MAX_LEN = 200
VOCAB_SIZE = 20000
BATCH_SIZE = 100
LAYER_NUM = 3
HIDDEN_DIM = 1000
NB_EPOCH = 20

# Loading input sequences, output sequences and the necessary mapping dictionaries
print('[INFO] Loading data...')
X, y = load_data('data/entity', 'data/sql', MAX_LEN)

# Finding the length of the longest sequence
X_max_len = max([len(sentence) for sentence in X])
y_max_len = max([len(sentence) for sentence in y])

# Padding zeros to make all sequences have a same length with the longest one
print('[INFO] Zero padding...')
X = pad_sequences(X, maxlen=X_max_len, dtype='int32')
y = pad_sequences(y, maxlen=y_max_len, dtype='int32')

# give X_vocab_len
X_vocab_len = y_vocab_len = 40

# Creating the network model
print('[INFO] Compiling model...')
model = create_model(X_vocab_len, X_max_len, y_vocab_len, y_max_len, HIDDEN_DIM, LAYER_NUM)

# Finding trained weights of previous epoch if any
saved_weights = find_checkpoint_file('saved/')

k_start = 1

# If any trained weight was found, then load them into the model
if len(saved_weights) != 0:
    print('[INFO] Saved weights found, loading...')
    epoch = saved_weights[saved_weights.rfind('_') + 1:saved_weights.rfind('.')]
    model.load_weights(saved_weights)
    k_start = int(epoch) + 1

i_end = 0
for k in range(k_start, NB_EPOCH + 1):
    # Shuffling the training data every epoch to avoid local minima
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    X = X[indices]
    y = y[indices]

    # Training 10 sequences at a time
    for i in range(0, len(X), 10):
        if i + 10 >= len(X):
            i_end = len(X)
        else:
            i_end = i + 10
        y_sequences = process_data(y[i:i_end], y_max_len)

        print('[INFO] Training model: epoch {}th {}/{} samples'.format(k, i, len(X)))
        model.fit(X[i:i_end], y_sequences, batch_size=BATCH_SIZE, nb_epoch=1, verbose=2)
    model.save_weights('saved/checkpoint_epoch_{}.hdf5'.format(k))


# Performing test if we chose test mode
def evaluaute():
    # Only performing test if there is any saved weights
    if len(saved_weights) == 0:
        print("The network hasn't been trained! Program will exit...")
        sys.exit()
    else:
        print("testing")
        X_test = load_test_data('data/test_one', MAX_LEN)
        X_test = pad_sequences(X_test, maxlen=X_max_len, dtype='int32')
        model.load_weights(saved_weights)
        predictions = np.argmax(model.predict(X_test), axis=2)
        sequences = []
        for prediction in predictions:
            sequence = ' '.join([str(index) for index in prediction if index > 0])
            sequences.append(sequence)
        print("perdition : ", sequences)
        f = open('data/test_ans', 'r')
        ans = f.read()
        f.close()
        print("answer    : ", ans.split('\n'))

        np.savetxt('data/test_result', sequences, fmt='%s')

def seq2seq_predict(X):
    # Only performing test if there is any saved weights
    if len(saved_weights) == 0:
        print("The network hasn't been trained! Program will exit...")
    else:
        model.load_weights(saved_weights)
        predictions = np.argmax(model.predict(np.array(X)), axis=2)
        print(predictions)