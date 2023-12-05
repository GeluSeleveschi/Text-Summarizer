from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import requests
from bs4 import BeautifulSoup

def main(url, model, tokenizer):
    print('started')
    summarizer = pipeline("summarization")
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
    summarized_text = []

    for chunk in chunks:
        inputs = tokenizer.encode(chunk, truncation=True, max_length=512, return_tensors="pt")
        outputs = model.generate(inputs, max_length=150, min_length=30, num_beams=4, early_stopping=True)
        summaries = tokenizer.decode(outputs[0], skip_special_tokens=True)
        summarized_text.append(summaries)

    return summarizer(summarized_text, max_length=130, min_length=30, do_sample=False)


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


if __name__ == "__main__":
    # Load the BART model
    model_path = "facebook/bart-large"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large")

    URL = input("Enter URL: ")
    summarized_content = main(URL, model)
    
    for summary in summarized_content:
        print(summary)