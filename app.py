from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    if filename.endswith('.csv'):
        csv_sentiments = process_csv(file_path)
        return jsonify(csv_sentiments)

    else:
        return "Unsupported file type", 400

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    return sentiment_scores

def process_csv(csv_path):
    df = pd.read_csv(csv_path)
    if 'Review' not in df.columns:
        return {"error": "CSV file must contain a 'Review' column"}

    analyzer = SentimentIntensityAnalyzer()
    results = []

    for index, row in df.iterrows():
        review = str(row['Review'])
        sentiment_scores = analyzer.polarity_scores(review)
        results.append({
            'review': review,
            'sentiment': sentiment_scores
        })

    return results

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
