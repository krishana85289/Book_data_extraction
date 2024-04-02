from selenium import webdriver
from selenium.webdriver.common.by import By
from docx import Document
import re
import getpass

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def extract_remedy_links(base_url):
    """
    Extract the links of the remedies from the materia medica page

    Parameters:
    base_url (str): the base URL of the website

    Returns:
    list: a list of remedy links
    """

    # Make a request to the page
    response = requests.get(f"{base_url}/index")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the `a` elements within the `remedy_list` class
    remedy_links = soup.find("div", class_="remedy_list").find_all("a")

    # Extract the `href` attribute of each `a` element and append it to the base URL
    remedy_links_list = []
    for link in remedy_links:
        if "href" in link.attrs:
            parsed_url = urlparse(link["href"])
            if parsed_url.scheme or parsed_url.netloc:
                # Skip external links
                continue
            full_url = urljoin(base_url, link["href"])
            remedy_links_list.append(full_url)

    return remedy_links_list

driver = webdriver.Firefox()
base_url = "https://www.materiamedica.info/en/materia-medica/adolf-zur-lippe/index"

# Extract the remedy links
links = extract_remedy_links(base_url)
# Create a new Document
doc = Document()

for link in links:
    driver.get(link)
    #driver.implicitly_wait(10)
    elements = driver.find_element(By.CLASS_NAME, "content").text

    # Extract content starting from "123"
    index_123 = elements.find("123")
    extracted_content = elements[index_123 + len("123"):]

    # Remove specific pattern using regex
    pattern = r"LECTURES ON Homoeopathic Materia Medica is available at Remedia Homeopathy.*?Family run pharmacy since 1760"
    cleaned_text = re.sub(pattern, "", extracted_content, flags=re.DOTALL)

    # Add cleaned text to the Document
    doc.add_paragraph(cleaned_text)

# Save the DOC file
doc_file = "cleaned_text.docx"
doc.save(doc_file)
print(f"DOC file saved as: {doc_file}")

# Close the WebDriver
driver.quit()
