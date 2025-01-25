from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import fitz  # PyMuPDF for PDF text extraction

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

# Define the route for uploading and processing PDF files
@app.route('/upload', methods=['POST'])
def upload_pdf():
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

    # Process the file if it is a PDF
    if filename.endswith('.pdf'):
        pdf_text = extract_text_from_pdf(file_path)  # Extract text from the PDF
        sentiment_scores = analyze_sentiment(pdf_text)  # Perform sentiment analysis
        return jsonify({
            'sentiment': sentiment_scores  # Return the sentiment scores
        })

    else:
        return "Unsupported file type", 400  # Return an error for unsupported file types

# Analyze the sentiment of a given text using VADER
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()  # Create an instance of the sentiment analyzer
    sentiment_scores = analyzer.polarity_scores(text)  # Get sentiment scores for the text
    return sentiment_scores  # Return the sentiment scores

# Extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)  # Open the PDF document
    text = ""  # Initialize an empty string to hold the extracted text
    
    # Iterate over each page in the PDF
    for page_num in range(document.page_count):
        page = document.load_page(page_num)  # Load the page
        text += page.get_text()  # Extract text from the page
    
    return text  # Return the concatenated text

# Define the route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)  # Send the requested file

# Run the Flask application in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)
