from django.http import JsonResponse
import nltk
from nltk.corpus import wordnet
import gensim.downloader as api
from google.cloud import translate_v2 as translate
from transformers import T5ForConditionalGeneration, T5Tokenizer, BartForConditionalGeneration, BartTokenizer
import torch
import os
import html

# Ensure NLTK WordNet corpus is downloaded
nltk.download('wordnet')

# Load the pre-trained Word2Vec model
w2v_model = api.load("word2vec-google-news-300")

# Function to translate text from Shona to English
def translate_shona_to_english(shona_text, credentials_file):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
    translate_client = translate.Client()
    translation = translate_client.translate(shona_text, source_language='sn', target_language='en')
    english_translation = html.unescape(translation['translatedText'])
    return english_translation

# Function to translate text from English to Shona
def translate_english_to_shona(english_text, credentials_file):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
    translate_client = translate.Client()
    translation = translate_client.translate(english_text, source_language='en', target_language='sn')
    shona_translation = html.unescape(translation['translatedText'])
    return shona_translation

# Initialize the T5 paraphrasing model and tokenizer
paraphrase_tokenizer = T5Tokenizer.from_pretrained("hetpandya/t5-small-tapaco")
paraphrase_model = T5ForConditionalGeneration.from_pretrained("hetpandya/t5-small-tapaco")

# Initialize the BART summarization model and tokenizer
summarize_tokenizer = BartTokenizer.from_pretrained('eugenesiow/bart-paraphrase')
summarize_model = BartForConditionalGeneration.from_pretrained('eugenesiow/bart-paraphrase').to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

def translate_view(request):
    shona_text = request.GET.get('text')
    if not shona_text:
        return JsonResponse({'error': 'No text provided'}, status=400)
    credentials_file = "C:/Users/agorejena/Music/abc.json"
    try:
        english_text = translate_shona_to_english(shona_text, credentials_file)
        return JsonResponse({'translated_text': english_text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def paraphrase_view(request):
    shona_text = request.GET.get('text')
    if not shona_text:
        return JsonResponse({'error': 'No text provided'}, status=400)
    credentials_file = "C:/Users/agorejena/Music/abc.json"
    try:
        english_text = translate_shona_to_english(shona_text, credentials_file)
        paraphrases = get_paraphrases(english_text, paraphrase_model, paraphrase_tokenizer)
        paraphrased_english_text = paraphrases[0] if paraphrases else english_text
        paraphrased_shona_text = translate_english_to_shona(paraphrased_english_text, credentials_file)
        return JsonResponse({'paraphrased_text': paraphrased_shona_text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def summarize_view(request):
    shona_text = request.GET.get('text')
    if not shona_text:
        return JsonResponse({'error': 'No text provided'}, status=400)
    credentials_file = "C:/Users/agorejena/Music/abc.json"
    try:
        english_text = translate_shona_to_english(shona_text, credentials_file)
        summarized_english_text = summarize_text(english_text, summarize_model, summarize_tokenizer)
        summarized_shona_text = translate_english_to_shona(summarized_english_text, credentials_file)
        return JsonResponse({'summarized_text': summarized_shona_text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Function to get paraphrases of English text
def get_paraphrases(text, model, tokenizer):
    input_text = f"paraphrase: {text} </s>"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", add_special_tokens=True)
    outputs = model.generate(input_ids=input_ids, max_length=256, num_return_sequences=5, num_beams=5, temperature=1.5, early_stopping=True)
    paraphrases = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return paraphrases

# Function to summarize English text
def summarize_text(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors='pt').to(model.device)
    summary_ids = model.generate(inputs['input_ids'], max_length=150, num_beams=5, early_stopping=True)
    summarized_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summarized_text
