import PyPDF2
import docx
from nltk.tokenize import sent_tokenize
import os
import io

def extract_chunks_from_pdf(filename, chunk_size=500):
    with open(filename, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        
        chunks = []
        current_chunk = ""
        
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            
            text = page.extract_text()
            sentences = sent_tokenize(text)
            
            for sentence in sentences:
                current_chunk += sentence
                
                if len(current_chunk) >= chunk_size:
                    chunks.append(current_chunk[:chunk_size])
                    
                    # Reset the current chunk
                    current_chunk = current_chunk[chunk_size:]
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
def extract_chunks_from_pdf_stream(uploaded_file, chunk_size=500):
        reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(reader.pages)
        
        chunks = []
        current_chunk = ""
        
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            
            # Extract the text content from the current page
            text = page.extract_text()
            
            # Tokenize the text into sentences
            sentences = sent_tokenize(text)
            
            for sentence in sentences:
                current_chunk += sentence
                
                if len(current_chunk) >= chunk_size:
                    chunks.append(current_chunk[:chunk_size])
                    
                    # Reset the current chunk
                    current_chunk = current_chunk[chunk_size:]
        
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks

def extract_chunks_from_docx(filename, chunk_size=500):
    # Load the .doc or .docx file
    doc = docx.Document(filename)
    
    chunks = []
    current_chunk = ""
    
    for para in doc.paragraphs:
        text = para.text
        
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        for sentence in sentences:
            current_chunk += sentence
            
            # Check if the current chunk has reached the desired size
            if len(current_chunk) >= chunk_size:
                chunks.append(current_chunk[:chunk_size])
                
                # Reset the current chunk
                current_chunk = current_chunk[chunk_size:]
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def extract_chunks_from_txt(filename, chunk_size=500):
    chunks = []
    current_chunk = ""
    
    # Open the .txt file in read mode
    with open(filename, 'r') as file:
        # Read the entire file content
        text = file.read()
        
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        for sentence in sentences:
            current_chunk += sentence
            
            if len(current_chunk) >= chunk_size:
                chunks.append(current_chunk[:chunk_size])
                
                current_chunk = current_chunk[chunk_size:]
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def upload_file(uploaded_file):
    file_name = uploaded_file.name
    save_directory = "./files"
    file_path = os.path.join(save_directory, file_name)
        
    # Save the uploaded file to the specified directory
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
        
def get_file_content(file):
    if file is not None:
        filename = file.name
        if filename:
            extensions = os.path.splitext(filename)
            if extensions and extensions.__len__:
                extension = extensions[1]
                
                extension = os.path.splitext(filename)[1]
                if extension in ['.doc', '.docx']:
                    pass # need to be handled
                elif extension == '.pdf':
                    return extract_chunks_from_pdf_stream(file)
                elif extension == '.txt':
                    pass # need to be handled
                else:
                    return None
    
    return None
                        
    