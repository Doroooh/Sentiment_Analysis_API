from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import matplotlib.pyplot as plt
import pandas as pd

# Create a Flask application instance
app = Flask(__name__)

# Define the folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the folder if it does not exist

# Define the root route that serves the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Render the homepage template

# Define the route for uploading and processing CSV files
@app.route('/upload', methods=['POST'])
def upload_csv():
    # Check if a file is included in the request
    if 'file' not in request.files:
        return "No file part", 400  # Return an error if no file is found
    
    file = request.files['file']  # Get the uploaded file
    
    # Check if the filename is empty
    if file.filename == '':
        return "No selected file", 400  # Return an error if no file is selected
    
    filename = secure_filename(file.filename)  # Secure the filename to avoid security issues
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Construct the file path
    file.save(file_path)  # Save the uploaded file to the designated folder

    # Process the file if it is a CSV
    if filename.endswith('.csv'):
        csv_sentiments = process_csv(file_path)  # Perform sentiment analysis on the CSV
        return jsonify(csv_sentiments)  # Return the results as a JSON response

    else:
        return "Unsupported file type", 400  # Return an error for unsupported file types

# Analyze the sentiment of a given text using VADER
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()  # Create an instance of the sentiment analyzer
    sentiment_scores = analyzer.polarity_scores(text)  # Get sentiment scores for the text
    return sentiment_scores  # Return the sentiment scores

# Process a CSV file to analyze sentiments for each review
def process_csv(csv_path):
    df = pd.read_csv(csv_path)  # Read the CSV file into a DataFrame
    
    # Check if the 'Review' column exists in the CSV
    if 'Review' not in df.columns:
        return {"error": "CSV file must contain a 'Review' column"}  # Return an error if missing

    analyzer = SentimentIntensityAnalyzer()  # Create an instance of the sentiment analyzer
    results = []  # Initialize a list to store results

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        review = str(row['Review'])  # Get the review text as a string
        sentiment_scores = analyzer.polarity_scores(review)  # Analyze the sentiment of the review
        results.append({
            'review': review,  # Include the original review text
            'sentiment': sentiment_scores  # Include the sentiment scores
        })

    return results  # Return the list of results

# Define the route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)  # Send the requested file

# Run the Flask application in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)
