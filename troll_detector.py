import re
import nltk
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

model_filepath='trollmodels/Troll-Killer-06-0.736-0.909.model'
model=load_model(model_filepath)
print(model.summary())

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

print("enter sentence")
string=input('>')

def process_input(x):
    x=x.lower()
    line=''
    for word in nltk.word_tokenize(x):
        if word not in nltk.corpus.stopwords.words('english') and word.isdigit()==False and re.search(r'[^!@#$%^&*()_.+=]+',word):
            line+=word+' '
    line=line.rstrip()
    sequence=tokenizer.texts_to_sequences(line)[0]
    padded=pad_sequences([sequence],maxlen=56)
    return padded

        
processed=process_input(string)
prediction=model.predict_classes(processed)[0][0]
if prediction==1:
	print('troll')
