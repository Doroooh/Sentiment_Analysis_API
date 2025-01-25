# Import necessary libraries
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF for PDF handling
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import matplotlib.pyplot as plt

# Initialize the Flask application
app = Flask(__name__)

# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route for the home page
@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return "No file part", 400  # Return error if no file is found
    
    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        return "No selected file", 400  # Return error if no file is selected
    
    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)  # Save the uploaded file to the specified path
    
    # Extract text from the uploaded PDF file
    text = extract_text_from_pdf(file_path)
    
    # Analyze the sentiment of the extracted text
    sentiment = analyze_sentiment(text)
    
    # Generate a sentiment plot and get the filename
    plot_filename = plot_sentiment(sentiment, filename)
    
    # Return the sentiment scores and plot filename as JSON
    return jsonify({'sentiment': sentiment, 'plot_filename': plot_filename})

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)  # Open the PDF document
    text = ""
    
    # Loop through each page and extract text
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()  # Append the text from each page
    
    return text  # Return the complete text

# Function to analyze sentiment using VADER
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()  # Initialize the sentiment analyzer
    sentiment_scores = analyzer.polarity_scores(text)  # Get sentiment scores
    return sentiment_scores  # Return the sentiment scores

# Function to create a bar plot of sentiment scores
def plot_sentiment(sentiment, filename):
    # Define categories and their corresponding scores
    categories = ['Negative', 'Neutral', 'Positive']
    scores = [sentiment['neg'], sentiment['neu'], sentiment['pos']]
    colors = ['#ff4c4c', '#ffc107', '#4caf50']  # Colors for the bars

    # Create a bar plot
    plt.figure(figsize=(8, 6))
    plt.bar(categories, scores, color=colors)
    plt.xlabel('Sentiment')  # Label for the x-axis
    plt.ylabel('Score')  # Label for the y-axis
    plt.title('Sentiment Analysis')  # Title of the plot
    plt.ylim(0, 1)  # Set the y-axis limits

    # Save the plot as a PNG file
    plot_filename = f"{filename}_sentiment.png"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], plot_filename)
    plt.savefig(output_path)  # Save the figure to the output path
    plt.close()  # Close the plot to free up memory

    return plot_filename  # Return the filename of the saved plot

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Send the requested file from the upload directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run the application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
