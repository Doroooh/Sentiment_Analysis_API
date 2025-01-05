import uvicorn
from fastapi import FastAPI
from inputText import InputText
import pickle

from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
from keras.models import load_model

def predict_class(input_text):
    '''This function will predict the sentiment class of passed text'''
    
    text = []
    text.append(input_text)

    sentiment_classes = ['Neutral', 'Negative', 'Positive']
    max_len=50
    
    # Transforming the text to a sequence of integers using a tokenizer object
    xt = tokenizer.texts_to_sequences(text)
    # Padding sequences to the same length
    xt = pad_sequences(xt, padding='post', maxlen=max_len)
    # Prediction using a loaded model
    yt = model.predict(xt).argmax(axis=1)
    # Printing predicted sentiment
    return ('The sentiment is', sentiment_classes[yt[0]])

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

app = FastAPI(title="A sentiment analysis API",
    description="A sentiment analysis API to take in text from a client, respond if neutral, negative or positive.")

model = load_model('model.h5')

@app.get('/')
def index():
    return {'message':'Consumer feedback!'}

@app.post('/predict')
def predict_sentiment(data:InputText):
    data = data.dict()
    text = data['text'] 
    prediction = predict_class(text)
    return prediction 

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

# python -m uvicorn app:app --reload
