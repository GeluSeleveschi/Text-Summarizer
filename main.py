from transformers import pipeline
from bs4 import BeautifulSoup
import requests
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import helper

def handle_articles(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    results = soup.find_all(['h1', 'p'])
    
    text = [result.text for result in results]
    ARTICLE = ' '.join(text)
    ARTICLE = ARTICLE.replace(',', '<eos>')
    ARTICLE = ARTICLE.replace('!', '<eos>')
    ARTICLE = ARTICLE.replace('?', '<eos>')
    sentences = ARTICLE.split('<eos>')
    
    chunks = split_text_into_chunks(sentences)
    return chunks

def split_text_into_chunks(sentences):
    max_chunk = 500
    current_chunk = 0
    chunks = []
    
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])
        
    return chunks

def get_content_into_chunks(uploaded_file):
    chunks = helper.get_file_content(uploaded_file)
    
    return chunks;

def get_summary(chunks, model):
    print('started summarization', len(chunks))
    summarizer = pipeline('summarization')
    summarized_text = summarizer(chunks, max_length=120, min_length=30, do_sample=False)
    
    return summarized_text

if __name__ == "__main__":
    handle_articles()
