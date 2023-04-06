import json
import stix

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

#loading the enterprise-attack json file from the mitre dataset
with open ("mitre_data/enterprise-attack.json") as f:
    data = json.load(f)

#loading the dataset from data to stix
attack = stix2.TAXIICollectionSource(data)

#defining the stix objects
class AttackTechnique(stix2.v21.AttackPattern):
    _type = 'attack-pattern'

# Define function to get all attack techniques
def get_attack_techniques():
    filter = stix2.Filter('type', '=', 'attack-pattern')
    return attack.query(filter)

# Define function to preprocess and vectorize text data using the n-gram algorithm
def preprocess(text):
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 5))
    return vectorizer.fit_transform(text).toarray()


# Define function to train an AI model on labeled data
def train_model(X, y):
    clf = MultinomialNB()
    clf.fit(X, y)
    return clf


# Define function to predict the attack technique of a given text using the trained AI model
def predict_attack_technique(text, clf, vectorizer):
    X = preprocess([text])
    X = vectorizer.transform([text]).toarray()
    y_pred = clf.predict(X)
    return y_pred[0]


attack_techniques = get_attack_techniques()
technique_names = [t.name.lower() for t in attack_techniques]
X_train = preprocess(technique_names)
y_train = [t.id for t in attack_techniques]
clf = train_model(X_train, y_train)
vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 5))
text = "The attacker used a phishing email to steal login credentials."
technique_id = predict_attack_technique(text.lower(), clf, vectorizer)
technique = attack.get(technique_id)
print(f"Predicted attack technique: {technique.name}")