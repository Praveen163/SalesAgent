from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
load_dotenv()
# Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


#PDF FILE URLs
pdf_files = [
    "/docs/part-a.pdf",
    "/docs/part-b.pdf",
    "/docs/brochure.pdf"
]


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# Step 2: Extract and combine text from all files
all_texts = []
for file_path in pdf_files:
    print(f"Processing {file_path}")
    text = extract_text_from_pdf(file_path)
    if text.strip():
        all_texts.append(text)

# Step 3: Extract and split text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.create_documents(all_texts)

# Step 4: Generate embeddings using Gemini
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
db.persist()


