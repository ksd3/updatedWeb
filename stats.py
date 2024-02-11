import pickle
import numpy as np
import sys

def predict_claim_probability(sample):
    with open('logit_model.pickle', 'rb') as f:
        logit_model = pickle.load(f)
    prob = logit_model.predict([sample])
    print(np.round(prob[0],2))
