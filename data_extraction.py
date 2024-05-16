import requests
from bs4 import BeautifulSoup
import string
import nltk
# Download sentence tokenizer
nltk.download('punkt') 
from nltk.tokenize import sent_tokenize,word_tokenize
url = "https://en.wikipedia.org/wiki/India" 
response = requests.get(url)
if response.status_code == 200:# Check if the request was successful
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')# Find all paragraphs
    # Open a text file to save the extracted sentences
    with open("extracted_sentences_BS.txt", "w") as file: 
        # Loop through all paragraphs  # Get the text content of each paragraph
        for paragraph in paragraphs: 
            text = paragraph.get_text() # Split the text into individual sentences
            sentences = sent_tokenize(text)  # Use NLTK to split into sentences
            for sentence in sentences:
                file.write(sentence.strip() + "\n")
    print("Sentences extracted and saved to 'extracted_sentences_BS.txt'")
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
def remove_punctuation(text):
    # Tokenize the text into words
    tokens = word_tokenize(text)
    # Keep only alphanumeric tokens (remove punctuation)
    tokens = [word for word in tokens if word.isalnum()]
    # Join tokens back into a cleaned string
    cleaned_text = ' '.join(tokens)
    return cleaned_text
# Paths to your text files
input_files = ["extracted_sentences_BS.txt", "Realtime_chat.txt"]  # List of input file paths
output_file_path = "combined_cleaned.txt"  # Output file path
# Initialize a list to store cleaned texts
cleaned_texts = []
# Read and clean each text file
for input_file_path in input_files:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        cleaned_text = remove_punctuation(text)
        cleaned_texts.append(cleaned_text)
# Concatenate all cleaned texts
combined_cleaned_text = ' '.join(cleaned_texts)
# Write the combined cleaned text to the output file
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(combined_cleaned_text)
# Print the final combined cleaned text or a success message
print("Combined cleaned text written to:", output_file_path)
