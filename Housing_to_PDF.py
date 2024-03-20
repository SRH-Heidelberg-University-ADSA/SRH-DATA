import os
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to save content to a file, with index for duplicate titles
# def save_to_local_file(base_name, content, directory):
#     # Ensure the output directory exists
#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     # Clean base_name to remove disallowed characters in filenames
#     base_name = "".join([c if c.isalnum() or c in " _-()" else "_" for c in base_name])

#     # Check if file already exists and append an index if it does
#     index = 0
#     while True:
#         index_str = f"_{index:04d}" if index > 0 else ""
#         file_name = f"{base_name}{index_str}.txt"
#         file_path = os.path.join(directory, file_name)
#         if not os.path.exists(file_path):
#             break
#         index += 1

#     # Write the content to the file
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.write(content)
#     print(f"Saved locally: {file_name}")

def save_to_local_file(base_name, content, directory):
    # Ensure the output directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Clean base_name to remove disallowed characters in filenames
    base_name = "".join([c if c.isalnum() or c in " _-()" else "_" for c in base_name])

    # Check if file already exists and append an index if it does
    index = 0
    while True:
        index_str = f"_{index:04d}" if index > 0 else ""
        file_name = f"{base_name}{index_str}.pdf"  # Change file extension to .pdf
        file_path = os.path.join(directory, file_name)
        if not os.path.exists(file_path):
            break
        index += 1

    # Create a PDF file and write the content to it
    c = canvas.Canvas(file_path, pagesize=letter)
    text = c.beginText(40, 750)  # Starting position of the text
    text.setFont("Helvetica", 10)
    for line in content.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()
    print(f"Saved locally: {file_name}")

# Function to scrape a single page
def scrape_page(page_url, output_directory):
    response = requests.get(page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('li', class_='row article property')

    
        for article in articles:
            # Extracting the title
            title_tag = article.find('h2', class_='article__title')
            title = title_tag.text.strip() if title_tag else 'No title found'

            subtitle_tag = article.find('span', class_='article__info')
            subtitle = subtitle_tag.text.strip() if subtitle_tag else 'No subtitle found'

            # Extracting the summary
            summary_tag = article.find('div', class_='article__summary')
            summary = summary_tag.text.strip() if summary_tag else 'No summary found'

            detail_tag = article.find('div', class_='article__details')

            if detail_tag:
                # spans = detail_tag.find_all('span')
                # surface = spans[1].text.strip() if len(spans) > 1 and spans[1].text.strip() else 'No surface found'
                # bedrooms = spans[3].text.strip() if len(spans) > 3 and spans[3].text.strip() else 'No bedrooms found'
                # interior = spans[5].text.strip() if len(spans) > 5 and spans[5].text.strip() else 'No interior found'
                # date = spans[7].text.strip() if len(spans) > 7 and spans[7].text.strip() else 'No date found'
                surface = soup.find('span', class_='property__label label label--surface').find_next_sibling('span').text.strip()
                bedrooms = soup.find('span', class_='property__label label label--bedrooms').find_next_sibling('span').text.strip()
                interior = soup.find('span', class_='property__label label label--interior').find_next_sibling('span').text.strip()
                date = soup.find('span', class_='property__label label label--date').find_next_sibling('span').text.strip()


            else:
                surface = 'No surface found'
                bedrooms = 'No bedrooms found'
                interior = 'No interior found'
                date = 'No date'

            print(f"Title: {title}\nStreet: {subtitle}\nSummary: {summary}\nSurface: {surface}\nBedrooms: {bedrooms}\nInterior: {interior}\nDate: {date}\n")

            content = f"Title: {title}\nStreet: {subtitle}\nSummary: {summary}\nSurface: {surface}\nBedrooms: {bedrooms}\nInterior: {interior}\nDate: {date}\n"

            # Generate a valid filename from the title
            # Format the title to be filesystem safe
            safe_title = title.replace(' ', '_').replace('/', '_')

            # Save the article content to a local file
            save_to_local_file(safe_title, content, output_directory)


            print(f"Saved locally: {title}")

    else:
        print(f"Failed to retrieve {page_url}")


# Directory to save text files
output_directory = '/Users/nguyentienhuy/Documents/SRH/CaseStudy/Final_Data/Housing_pdf'  # Update this to your local directory

# Base URL without the page number
base_url = 'https://www.iamexpat.de/housing/rentals?page='

# Loop through pages 1 to 10
for page_number in range(1, 300):
    page_url = f"{base_url}{page_number}"
    print(f"Scraping page {page_number}\n")
    scrape_page(page_url, output_directory)