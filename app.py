from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Download the required NLTK resource once
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Returns the sentiment of the given text as Positive, Negative, or Neutral."""
    score = analyzer.polarity_scores(text)['compound']
    return "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"

@app.route("/", methods=["GET", "POST"])
def sentiment_request():
    """Handles sentiment analysis requests via GET and POST."""
    text = request.form.get('q') if request.method == "POST" else request.args.get('q')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    return jsonify({"sentiment": analyze_sentiment(text)})

if __name__ == "__main__":
    app.run(debug=True)
