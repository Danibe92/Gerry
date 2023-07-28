from nltk import word_tokenize
#nltk.download('punkt')
import os
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import pickle
import json
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
stemmer = LancasterStemmer()

def load():
    words = []
    labels = []
    training = []
    output = []

    with open('intents.json') as intents:
        data = json.load(intents)

    try:
        with open('data.pickle','rb') as f:
            words, labels, training, output = pickle.load(f)
    except:
        x_docs = []
        y_docs = []

        for intent in data['intents']:
            for pattern in intent['patterns']:
                wrds = word_tokenize(pattern)
                words.extend(wrds)
                x_docs.append(wrds)
                y_docs.append(intent['tag'])

                if intent['tag'] not in labels:
                    labels.append(intent['tag'])

        words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
        words = sorted(list(set(words)))
        labels = sorted(labels)

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(x_docs):
            bag = []
            wrds = [stemmer.stem(w) for w in doc]
            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(y_docs[x])] = 1

            training.append(bag)
            output.append(output_row)

        training = np.array(training)
        output = np.array(output)

        with open('data.pickle','wb') as f:
            pickle.dump((words, labels, training, output), f)
    model = Sequential()
    model.add(Dense(8, input_shape=(len(training[0]),), activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(len(output[0]), activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    if os.path.exists('model/model.h5'):
        model.load_weights('model/model.h5')
    else:
        model.fit(training, output, epochs=500, batch_size=8, verbose=1)
        model.save_weights('model/model.h5')

    return words, labels, model, data


def generate_response(inp, words, labels,model,data):


    results = model.predict(np.expand_dims(bag_of_words(inp, words), axis=0))
    results_index = np.argmax(results)
    if results[0][results_index] < 0.9:
        return None
    else:
        tag = labels[results_index]
        if tag =="musica":
            return "musica"
        else:
         for tg in data['intents']:
            if tg['tag'] == tag:
                responses = tg['responses']
                return random.choice(responses)




def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)
