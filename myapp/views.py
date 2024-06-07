from django.http import JsonResponse
#import nltk
#from nltk.corpus import wordnet
#import gensim.downloader as api
from google.cloud import translate_v2 as translate
#from transformers import T5ForConditionalGeneration, T5Tokenizer, BartForConditionalGeneration, BartTokenizer
#import torch
import os
import google.generativeai as genai

# Replace with your API key
api_key = "AIzaSyDFfv9bSCsmELltZ_Id9SK8mk2BRlcTmfY"

# Configure the API key
genai.configure(api_key=api_key)



# Function to translate text from Shona to English
def translate_shona_to_english(shona_text, credentials_file):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
    translate_client = translate.Client()
    translation = translate_client.translate(shona_text, source_language='sn', target_language='en')
    english_translation = translation['translatedText']

    prompt = "give me synonyms of " + shona_text

    response = genai.generate_text(
        prompt=prompt,
    )
    return [english_translation,response.result]
    

# # Function to translate text from English to Shona
def translate_english_to_shona(english_text, credentials_file):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
    translate_client = translate.Client()
    translation = translate_client.translate(english_text, source_language='en', target_language='sn')
    shona_translation = translation['translatedText']
    return shona_translation


def translate_view(request):
    shona_text = request.GET.get('text')
    credentials_file = "C:/Users/agorejena/Music/abc.json"
    english_text = translate_shona_to_english(shona_text, credentials_file)
    synonyms=english_text[1]
    english_text=english_text[0]
    
    return JsonResponse({'translated_text': english_text,
                         'synonyms':synonyms
                         })

def summarise_view(request):
    shona_text = request.GET.get('text')
    credentials_file = "C:/Users/agorejena/Music/abc.json"
    shona_text=translate_shona_to_english(shona_text, credentials_file)
    shona_text=shona_text[0]
    shona_word = "In the vast tapestry of human experience, the pursuit of knowledge stands as a testament to our inherent curiosity and desire for understanding. From the earliest days of our species, when primitive humans gazed up at the stars with wonder and trepidation, to the modern era where science and technology unlock the mysteries of the cosmos, this quest has driven remarkable achievements and profound insights. It has propelled us to explore the depths of the oceans, the expanses of space, and the intricacies of the human mind. The cumulative efforts of countless individuals across generations have led to groundbreaking discoveries in fields as diverse as medicine, physics, literature, and the arts, each contributing to the ever-growing reservoir of human knowledge. This relentless pursuit not only satiates our curiosity but also underpins the advancement of society, enabling improvements in quality of life, fostering innovation, and addressing the complex challenges that face humanity. As we continue to push the boundaries of what is known, the pursuit of knowledge remains a beacon guiding us towards a future where understanding and wisdom pave the way for greater harmony, prosperity, and fulfillment for all."

    prompt = "generate a summaries of this statement," + shona_text + ",to 50 words"
    response = genai.generate_text(
        prompt=prompt,
    )



    return JsonResponse({'summarised text':  translate_english_to_shona(response.result,credentials_file)})

def paraphrase_view(request):
    shona_text = request.GET.get('text')
    credentials_file = "C:/Users/agorejena/Music/abc.json"
    shona_text=translate_shona_to_english(shona_text, credentials_file)
    shona_text=shona_text[0]
    shona_word = "In the vast tapestry of human experience, the pursuit of knowledge stands as a testament to our inherent curiosity and desire for understanding. From the earliest days of our species, when primitive humans gazed up at the stars with wonder and trepidation, to the modern era where science and technology unlock the mysteries of the cosmos, this quest has driven remarkable achievements and profound insights. It has propelled us to explore the depths of the oceans, the expanses of space, and the intricacies of the human mind. The cumulative efforts of countless individuals across generations have led to groundbreaking discoveries in fields as diverse as medicine, physics, literature, and the arts, each contributing to the ever-growing reservoir of human knowledge. This relentless pursuit not only satiates our curiosity but also underpins the advancement of society, enabling improvements in quality of life, fostering innovation, and addressing the complex challenges that face humanity. As we continue to push the boundaries of what is known, the pursuit of knowledge remains a beacon guiding us towards a future where understanding and wisdom pave the way for greater harmony, prosperity, and fulfillment for all."

    prompt = "paraphrase" + shona_text

    response = genai.generate_text(
        prompt=prompt,
    )

    return JsonResponse({'paraphrased text': translate_english_to_shona(response.result,credentials_file)})