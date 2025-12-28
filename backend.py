import speech_recognition as sr
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk
import re

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def record_and_convert():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st = "🎙️ Listening..."
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        text = ""
    except sr.RequestError:
        text = "Speech recognition unavailable."
    return text

def analyze_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    return "Neutral"

def extract_keywords(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    words = [w for w in tokens if w.isalpha() and w not in stopwords.words('english')]
    freq = Counter(words)
    return [w for w, _ in freq.most_common(3)]

def generate_insight_card(mood, keywords):
    if mood == "Positive":
        suggestion = "🌞 You're radiating positivity today! Keep embracing gratitude and joy."
    elif mood == "Negative":
        suggestion = "🌧️ It seems you're feeling low. Take a deep breath — this too shall pass 💙."
    else:
        suggestion = "🌤️ You seem calm and reflective. Maintain your balance and peace."
    return {
        "Mood": mood,
        "Keywords": ", ".join(keywords),
        "Suggestion": suggestion
    }
