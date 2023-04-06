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