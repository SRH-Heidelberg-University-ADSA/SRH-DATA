import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from reportlab.lib import colors
from textwrap import wrap

def save_article_as_pdf(title, content, folder_path='/Users/nguyentienhuy/Documents/SRH/CaseStudy/Data/PDF_files'):
    filename = "".join([c if c.isalnum() else "_" for c in title]) + ".pdf"
    filepath = os.path.join(folder_path, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    text_object = c.beginText(40, height - 100)
    text_object.setFont("Helvetica-Bold", 14)
    text_object.setFillColor(colors.black)

    # Add title to the PDF
    text_object.textLine(title)

    text_object.setFont("Helvetica", 10)

    wrapped_text = wrap(content, width=80)

    # Add the wrapped text to the PDF, line by line
    for line in wrapped_text:
        text_object.textLine(line)
        if text_object.getY() < 50:
            c.drawText(text_object)
            c.showPage()
            text_object = c.beginText(40, height - 50)
            text_object.setFont("Helvetica", 10)
            text_object.setFillColor(colors.black)

    c.drawText(text_object)
    c.save()
    print(f"Saved article: {title} as PDF")

def scrape_article_content(article_url, headers):
    response = requests.get(article_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve article at {article_url}")
        return ""

    soup = BeautifulSoup(response.content, 'html.parser')

    article_content = soup.find('div', class_='nv-content-wrap entry-content')
    if article_content:
        return article_content.get_text(strip=True)
    else:
        return "Content not found."

def scrape_data_science_central(base_url, headers, max_pages=600, max_articles_per_page=10):
    for page in range(0, max_pages + 1):
        url = f"{base_url}/page/{page}/?s=data+science"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage for page {page}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')

        for article in articles[:max_articles_per_page]:
            title = article.find('h2').get_text(strip=True)
            article_url = article.find('a')['href']

            article_text = scrape_article_content(article_url, headers)
            # print(title)
            # print("\n")
            # print(article_text)
            # print("\n")
            # print("\n")
            # Save the article's content as a PDF
            save_article_as_pdf(title, article_text)
            print(f"Saved article: {title} as PDF")

headers = {'User-Agent': 'Mozilla/5.0'}
base_url = 'https://www.datasciencecentral.com'
scrape_data_science_central(base_url, headers)



