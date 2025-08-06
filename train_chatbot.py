import json
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

with open('intents.json') as f:
    intents = json.load(f)

corpus = []
labels = []
for intent in intents['intents']:
    for pattern in intent['patterns']:
        corpus.append(pattern)
        labels.append(intent['tag'])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)

model = MultinomialNB()
model.fit(X, labels)

pickle.dump(model, open('chatbot_model.pkl', 'wb'))
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
pickle.dump(intents, open('intents.pkl', 'wb'))

print("✅ Model trained and saved.")
