from flask import Flask, render_template, abort, request, jsonify  
from sklearn.feature_extraction.text import TfidVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
import nltk 
from string import punctuation
import re
from nltk.corpus import stopwords

nltk.download('stopwords')

set(stopwords.words('english'))

# Initializing the app
app = Flask(__name__)

@app.route('/')
def my_form():
    retun render_template('form.html')

# the dictionary to store output for the response
output = {}

# this function will determine the sentiment of a customer's comment
def sentiment(customer_comment):
    """
    The function is using VADER sentiment analysis tool to analyze the polarity of a customer's comment on the bank's facebook posts.
    The sentiments are either Positive, Neutral or Negative based the compound score.
    """
    nltk.download('vader_lexicon')  
    sids = SentimentIntensityAnalyzer()  # Instantiating the sentiment analyzer
    sent_score = sids.polarity_scores(customer_comment)['compound']  # the is the computation of the sentiment polarity score of a comment. 
    # sentiment classification
    if score > 0:
        return "Positive"
    elif score < 0:  
        return "Negative"
    else:
        return "Neutral"

@app.route("/", methods=["GET", "POST"])  # Allow the GET and POST methods for this route
def sentimentRequest():
    """
    Handle the HTTP requests for sentiment analysis. 
    - For POST requests, retrieve the input from data.
    - For GET requests, retrieve input from query parameters.
    Return a JSON response with sentiment classification.
    """
    if request.method == "POST":  # Checking if request is a POST
        customer_comment = request.form['q']  
        cust_sent = sentiment(customer_comment) 
        output['sentiment'] = cust_sent   
        return jsonify(output)  # Return the output as JSON
    else:  # Handle GET requests
        customer_comment = request.args.get('q')  
        cust_sent = sentiment(customer_comment)  
        print(customer_comment)  
        output['sentiment'] = cust_sent  
        return jsonify(output)  

if __name__ == "__main__":
    """
    Run the Flask application in debug mode for development.
    The app listens for incoming connections on localhost:5000.
    """
    app.run(debug=True)
