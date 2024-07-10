from flask import Flask, request, jsonify
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
import PyPDF2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Hugging Face pipeline
model_id = 'meta-llama/Llama-2-7b-chat-hf'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = AutoModelForCausalLM.from_pretrained(model_id, device_map='auto')
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Initialize FAISS vector store
vectorstore = FAISS()

# Initialize ConversationalRetrievalChain
chain = ConversationalRetrievalChain.from_llm(model, vectorstore.as_retriever(), return_source_documents=True)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    pdf_file = request.files.get('pdf_file')
    if pdf_file is None:
        return jsonify({'error': 'No PDF file provided'}), 400

    # Convert PDF to text
    text = convert_pdf_to_text(pdf_file)
    
    # Split text into chunks
    chunks = split_text_into_chunks(text)
    
    # Create embeddings for each chunk
    embeddings = create_embeddings(chunks)
    
    # Store embeddings in FAISS vector store
    vectorstore.add_vectors(embeddings)
    
    return jsonify({'message': 'PDF uploaded successfully'}), 200

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json['question']
    result = chain({'question': question, 'chat_history': []})
    answer = result['answer']
    return jsonify({'answer': answer})

def convert_pdf_to_text(pdf_file):
    reader = PyPDF2.PdfFileReader(pdf_file)
    text = ""
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        text += page.extract_text()
    return text

def split_text_into_chunks(text):
    # Assuming chunk size of 1000 characters for simplicity
    chunk_size = 1000
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def create_embeddings(chunks):
    embeddings = HuggingFaceEmbeddings(model_name=model_id)
    return [embeddings.embed(chunk) for chunk in chunks]

if __name__== '_main_':
    app.run(debug=True, host='127.0.0.1', port=5002)