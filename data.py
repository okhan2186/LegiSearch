import os
import sqlite3
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Download NLTK resources (run only once)
# nltk.download('punkt')
# nltk.download('stopwords')

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

# Function to extract title from text
def extract_title(text):
    sentences = sent_tokenize(text)
    return sentences[0] if sentences else ""

# Function to extract keywords from text
def extract_keywords(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
    
    # Count word frequencies
    word_freq = Counter(filtered_tokens)
    
    # Get top N keywords
    top_keywords = word_freq.most_common(10)  # Change 10 to adjust the number of keywords
    return top_keywords

# Directory containing PDF files
pdf_directory = r'C:\Users\Hp\Desktop\Legi\path'

# Connect to SQLite database
conn = sqlite3.connect('pdf_data.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS pdf_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, title TEXT, keywords TEXT)''')

# Iterate over PDF files in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, filename)
        
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            # Extract title
            title = extract_title(text)
            
            # Extract keywords
            keywords = extract_keywords(text)
            
            # Insert data into the database
            c.execute("INSERT INTO pdf_data (filename, title, keywords) VALUES (?, ?, ?)", (filename, title, str(keywords)))
            conn.commit()

            print("File:", filename)
            print("Title:", title)
            print("Keywords:", keywords)
            print("Stored in database successfully.")
            print("-----------------------------")