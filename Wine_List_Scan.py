import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(img)
    return text

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def get_wine_rating(wine_name):
    search_url = f"https://www.vivino.com/search/wines?q={wine_name}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the rating element (assuming it's within a span with class 'average__number')
    rating_element = soup.find('span', class_='average__number')
    
    if rating_element:
        return rating_element.text.strip()
    else:
        return "Rating not found"

def process_wine_list(file_path):
    if file_path.endswith('.png') or file_path.endswith('.jpg'):
        text = extract_text_from_image(file_path)
    elif file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a .png, .jpg, or .pdf file.")
    
    # Split the text into lines and process each line
    wine_list = text.split('\n')
    
    # Create a DataFrame to store wine names and ratings
    df = pd.DataFrame(columns=['Wine Name', 'Rating'])
    
    for wine in wine_list:
        wine_name = wine.strip()
        if wine_name:
            rating = get_wine_rating(wine_name)
            df = df.append({'Wine Name': wine_name, 'Rating': rating}, ignore_index=True)
    
    return df

# Example usage:
file_path = "wine_list.png"  # Change this to "wine_list.pdf" if needed
wine_ratings_df = process_wine_list(file_path)
print(wine_ratings_df)
