import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    text = re.sub(r'\S+@\S+', '', text)
    
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    try:
        tokens = word_tokenize(text)
    except:
        tokens = text.split()
    
    try:
        stop_words = set(stopwords.words('portuguese'))
        tokens = [token for token in tokens if token not in stop_words]
    except:
        try:
            stop_words = set(stopwords.words('english'))
            tokens = [token for token in tokens if token not in stop_words]
        except:
            pass
    
    try:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]
    except:
        pass
    
    processed_text = ' '.join(tokens)
    
    return processed_text