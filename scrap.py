from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from docx import Document
import re
driver = webdriver.Firefox()
driver.get("https://www.materiamedica.info/en/materia-medica/james-tyler-kent/-preface:-lectures-on-homoeopathic-materia-medica")
driver.implicitly_wait(10)  
elements=driver.find_element(By.CLASS_NAME, "content").text
driver.quit()
index_123 = elements.find("123")

# Extract content starting from "123"
extracted_content = elements[index_123 + len("123"):]
#pattern = r"LECTURES ON Homoeopathic Materia Medica is available at Remedia Homeopathy more information and order at Remedia Homeopathy 5,500 homeopathic remedies Family run pharmacy since 1760"
pattern = r"LECTURES ON Homoeopathic Materia Medica is available at Remedia Homeopathy.*?Family run pharmacy since 1760"

# Remove the pattern using regex
cleaned_text = re.sub(pattern, "", extracted_content, flags=re.DOTALL)
from docx import Document

# Create a new Document
doc = Document()


# Add cleaned text to the Document
doc.add_paragraph(cleaned_text)

doc_file = "cleaned_text.docx"
doc.save(doc_file)

print(f"DOC file saved as: {doc_file}")

