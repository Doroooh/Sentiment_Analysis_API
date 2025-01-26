from flask import Flask, request, jsonify, render_template, abort
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize Flask application
app = Flask(__name__)


results_cache = {}

def analyze_sentiment(text):
    """
    Analyze sentiment of given text using NLTK's VADER sentiment analyzer.

    Args:
        text (str): The input text to analyze.

    Returns:
        str: 'Positive' or 'Negative' or 'Neutral' based on the sentiment score.
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text).get('compound', 0)
    return "Positive" if sentiment_score > 0 else "Negative" else "Neutral"

@app.route("/", methods=["GET", "POST"])
def handle_sentiment():
    """
    Handles sentiment analysis requests via GET and POST methods.

    For POST requests:
        Expects 'sentiment_input' in form data and returns JSON response.

    For GET requests:
        Expects 'sentiment_input' as query parameter and returns JSON response.

    Returns:
        JSON response containing the sentiment result.
    """
    if request.method == "POST":
        user_input = request.form.get("sentiment_input", "")
        if not user_input:
            return jsonify({"error": "No input provided."}), 400

        result = analyze_sentiment(user_input)
        results_cache['sentiment'] = result
        return jsonify({"sentiment": result})

    elif request.method == "GET":
        user_input = request.args.get("sentiment_input", "")
        if not user_input:
            return jsonify({"error": "No input provided."}), 400

        result = analyze_sentiment(user_input)
        results_cache['sentiment'] = result
        return jsonify({"sentiment": result})

    else:
        abort(405)  # Method Not Allowed

# Start the Flask server in debug mode
if __name__ == "__main__":
    app.run(debug=True)
