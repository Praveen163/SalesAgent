from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from agents import  function_tool
from dotenv import load_dotenv
load_dotenv()
# Ensure the Gemini API key is set
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

# Create the same embedding function
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Load the existing Chroma DB
db = Chroma(persist_directory="/chroma_db/", embedding_function=embeddings)

# Now query it
@function_tool
def ragTool(query:str):
    results = db.similarity_search(query, k=8)
    return results

# print("before function call")
# docs = ragTool("tell me about LPU")
# print(docs)
# for doc in docs:
#     print(doc.page_content)
