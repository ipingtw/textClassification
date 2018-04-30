#import packages
import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import pickle
import gc

project_file_path = os.path.dirname(os.path.abspath(__file__))

#hyper-parameters
MAX_SEQUENCE_LENGTH = 100 
EMBEDDING_DIM = 200 
VALIDATION_SPLIT = 0.16 
TEST_SPLIT = 0.2 

#import file
data = pd.read_csv(os.path.join(project_file_path,'../data/news_final_sample.csv'))
data = data.dropna()

#select columns
data = data[['cat_int','words']]
#shuffle data
data =data.sample(frac=1).reset_index(drop=True)

#tokenize words
tokenizer = Tokenizer()
#feed all the words into tokenizer to create a word-index mapping dicitonary
tokenizer.fit_on_texts(data['words'])
#word-index dictionary
word_index = tokenizer.word_index
#convert each document into sequences of integers corresponding to each word(using word_index)
sequences = tokenizer.texts_to_sequences(data['words'])
#one hot encoding for all the labels
labels = to_categorical(data['cat_int'])
#pad all the documents with less than 100 words into 100 words (zero padding)
data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

#save tokenizer so can be reused for future inferring
with open(os.path.join(project_file_path,'../model/tokenizer.pickle'), 'wb') as f:
	pickle.dump(tokenizer, f)

#split data
p1 = int(len(data)*(1-VALIDATION_SPLIT-TEST_SPLIT))
p2 = int(len(data)*(1-TEST_SPLIT))
x_train = data[:p1]
y_train = labels[:p1]
x_val = data[p1:p2]
y_val = labels[p1:p2]
x_test = data[p2:]
y_test = labels[p2:]

#train
#import packages
from keras.layers import Dense, Input, Flatten, Dropout
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Sequential

#model design
model = Sequential()
model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
model.add(Dropout(0.2))
model.add(Conv1D(250, 3, padding='valid', activation='relu', strides=1))
model.add(MaxPooling1D(3))
model.add(Flatten())
model.add(Dense(EMBEDDING_DIM, activation='relu'))
model.add(Dense(labels.shape[1], activation='softmax'))
model.summary()
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['acc'])
#train model
model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=2, batch_size=128)

#save model
model.save(os.path.join(project_file_path,'../model/text_classifier.h5')) 

#predict testing set
y_predict_prob = model.predict(x_test)
y_predict = np.argmax(y_predict_prob, axis = 1)
y_labels = np.argmax(y_test, axis = 1 )

#create a dataframe, result, which contains a column of target and another column storing the
#truth value of label == prediction
result = pd.DataFrame(np.transpose(np.array([y_labels,y_predict == y_labels])), columns = ['label', 'truth'])
#map integer categories back into original categories
result['label'] = result['label'].map({
	1 : 'auto',
	2 : 'money',
	3 : 'it',
	4 : 'health',
	5 : 'sports',
	6 : 'travel',
	7 : 'learning',
	8 : 'entertaiment'})
#calculate accuracy rate for each category respectively
accuracy = result.groupby(['label']).mean()
print(accuracy)
print(result['truth'].mean())

