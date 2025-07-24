import ast
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

# helper function to get the names from lists object
def extract_genres_keywords(obj):
    list_of_names = []
    for i in ast.literal_eval(obj):
        list_of_names.append(i['name'])
    return list_of_names

def extract_cast(obj):
    list_of_names = []
    for i in ast.literal_eval(obj):
        list_of_names.append(i['name'])
        if len(list_of_names) >= 5:
            break
    return list_of_names

def get_director_name(obj):
    director = []
    obj = ast.literal_eval(obj)
    for i in obj:
        if i['job'] == 'Director':
            director.append(i['name'])
            return director
        
def stem_text(text):
    stemmed_words = []
    for word in text.split():
        stemmed_words.append(ps.stem(word))
    
    return " ".join(stemmed_words)