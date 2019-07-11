import pickle
import re
import nltk
import pandas as pd
oo=pd.read_json('cyberdata.json',lines=True)

def annot2target(x):
    return x['label'][0]

oo['target']=oo.annotation.apply(lambda x:annot2target(x))
print('loaded data')
oo.drop(labels=['annotation','extras'],axis=1,inplace=True)


oo['target']=oo.target.astype('int')

troll=oo[oo.target==1]
not_troll=oo[oo.target==0]
troll_content=list(troll.content)[:10000]
troll_label=list(troll.target)[:10000]
not_troll_content=list(not_troll.content)[:10000]
not_troll_label=list(not_troll.target)[:10000]


content=troll_content+not_troll_content
labels=troll_label+not_troll_label

def clean(x):
    string=x.lower()
    line=''
    for word in nltk.word_tokenize(string):
        if word not in nltk.corpus.stopwords.words('english') and word.isdigit()==False and re.search(r'[^!@#$%^&*()_.+=]+',word):
            line+=word+' '
    line=line.rstrip()
    return line

cleancontent=[clean(x) for x in content]

print('cleaned data')

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
tokenizer=Tokenizer(num_words=3000,oov_token='<OOV>')
tokenizer.fit_on_texts(cleancontent)
sequences=tokenizer.texts_to_sequences(cleancontent)
maxlen=max([len(x) for x in sequences])
#print(maxlen)
padded=pad_sequences(sequences,maxlen=maxlen)
print(maxlen)
import pickle

# saving
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)



print('converted text to padded sequences')
from sklearn.model_selection import train_test_split

trainx,testx,trainy,testy=train_test_split(padded,labels)


#print(len(trainx)==len(trainy))

from tensorflow.keras.callbacks import TensorBoard,ModelCheckpoint

class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self,epoch,logs={}):
        if logs.get('val_acc')>0.85:
            self.model.stop_training=True

callbacks=myCallback()

import numpy as np
NAME="troll_detection_model-"+str(np.random.rand(1)[0])
tensorboard=TensorBoard(log_dir=f'trolllogs/{NAME}')

filepath='Troll-Killer-{epoch:02d}-{val_acc:.3f}-{acc:.3f}'#unique file name that will include the epoch and the validation acc for that epoch
checkpoint=ModelCheckpoint("trollmodels/{}.model".format(filepath,monitor='val_acc',verbose=1,save_best_only=True,mode='max'))#saves the best ones


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling1D,Dense,Embedding,LSTM,Bidirectional

model=Sequential()
model.add(Embedding(3000,64,input_length=maxlen))
model.add(Bidirectional(LSTM(150,return_sequences=True)))
#model.add(tf.keras.layers.Dropout(0.3))
model.add(Bidirectional(LSTM(150,return_sequences=True)))
#model.add(tf.keras.layers.Dropout(0.3))
model.add(Bidirectional(LSTM(150)))
model.add(Dense(100,activation='tanh'))
model.add(Dense(1,activation='sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
print(model.summary())


print('Starting training')
history=model.fit(trainx,trainy,epochs=30,validation_data=(testx,testy),callbacks=[tensorboard,callbacks,checkpoint])

predictions=model.predict_classes(testx)
preds=[x[0] for x in predictions]


from sklearn.metrics import confusion_matrix,roc_auc_score

print(confusion_matrix(testy,preds),roc_auc_score(testy,preds))
print('training complete!')
