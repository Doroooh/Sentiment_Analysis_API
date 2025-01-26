from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from string import punctuation
import re
from nltk.corpus import stopwords

# Download NLTK stopwords package
nltk.download('stopwords')

# Initializing the stopwords set to prevent redundancy during function calls
set(stopwords.words('english'))

# Creating an instance for the Flask app
app = Flask(__name__)

# Defining root route for display the form page
@app.route('/')
def my_form():
    return render_template('form.html')

# Defining route for processing the form data on submission
@app.route('/', methods=['POST'])
def my_form_post():
    # Loading list of English stopwords
    stop_words = stopwords.words('english')

    # Retrieving and processing text input from the form
    text1 = request.form['text1'].upper()  # Converting text to uppercase
    
    # Remove numeric characters from the input text
    text_final = ''.join(k for k in text1 if not k.isdigit())

    # Remove stopwords from the processed text
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    # Initializing VADER SentimentIntensityAnalyzer
    sa = SentimentIntensityAnalyzer()

    # Perform sentiment analysis on the cleaned text
    dd = sa.polarity_scores(text=processed_doc1)

    # Calculating a normalized compound score (scale: 0 to 1)
    compound = round((1 + dd['compound'])/2, 2)

    # Render the form page with sentiment analysis results
    return render_template('form.html', final=compound, text1=text_final, text2=dd['positive'], text5=dd['negative'], text4=compound, text3=dd['neutral'])

# Run the Flask application with specified host and port settings
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5002, threaded=True)
