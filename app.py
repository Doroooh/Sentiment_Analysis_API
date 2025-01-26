from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from string import punctuation
import re
from nltk.corpus import stopwords

# Download NLTK stopwords package if not already present
nltk.download('stopwords')

# Initialize the stopwords set to avoid redundancy during function calls
set(stopwords.words('english'))

# Create an instance of the Flask application
app = Flask(__name__)

# Define the root route to display the form page
@app.route('/')
def my_form():
    return render_template('form.html')

# Define the route for processing the form data upon submission
@app.route('/', methods=['POST'])
def my_form_post():
    # Load the list of English stopwords
    stop_words = stopwords.words('english')

    # Retrieve and process the text input from the form
    text1 = request.form['text1'].lower()  # Convert text to lowercase for uniformity
    
    # Remove numeric characters from the input text
    text_final = ''.join(c for c in text1 if not c.isdigit())

    # Remove stopwords from the processed text
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    # Initialize the VADER SentimentIntensityAnalyzer
    sa = SentimentIntensityAnalyzer()

    # Perform sentiment analysis on the cleaned text
    dd = sa.polarity_scores(text=processed_doc1)

    # Calculate a normalized compound score (scale: 0 to 1)
    compound = round((1 + dd['compound'])/2, 2)

    # Render the form page with sentiment analysis results
    return render_template('form.html', final=compound, text1=text_final, text2=dd['pos'], text5=dd['neg'], text4=compound, text3=dd['neu'])

# Run the Flask application with specified host and port settings
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5002, threaded=True)
