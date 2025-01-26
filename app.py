from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import re
from string import punctuation
from nltk.corpus import stopwords

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')

# Flask app initialization
app = Flask(__name__)

@app.route('/')
def index():
    # Render the HTML form
    return render_template('form.html')

@app.route('/', methods=['POST'])
def analyze_sentiment():
    stop_words = set(stopwords.words('english'))
    
    # Get input text from the form
    user_input = request.form['text1'].lower()
    
    # Remove digits and punctuations
    cleaned_text = ''.join([char for char in user_input if char not in punctuation and not char.isdigit()])
    
    # Remove stopwords
    processed_text = ' '.join([word for word in cleaned_text.split() if word not in stop_words])
    
    # Sentiment analysis
    sentiment_analyzer = SentimentIntensityAnalyzer()
    scores = sentiment_analyzer.polarity_scores(processed_text)
    compound_score = round((1 + scores['compound']) / 2, 2)  # Normalize compound score to 0-1 scale

    # Render results with updated template
    return render_template(
        'form.html',
        final=compound_score,
        text1=cleaned_text,
        text2=scores['positive'],
        text3=scores['neutral'],
        text4=compound_score,
        text5=scores['negative']
    )

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5002, threaded=True)
