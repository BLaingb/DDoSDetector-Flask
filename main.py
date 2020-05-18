from flask import Flask, request, abort
import pickle
from tensorflow.keras.models import load_model
import os

app = Flask(__name__)
svm_loaded = False
svm_model = None
mlp_model = None

def load_svm():
    global svm_loaded, svm_model
    if not svm_loaded:
        # load the model from disk
        svm_filename = './classifiers/svm_classifier.sav'
        svm_model = pickle.load(open(svm_filename, 'rb'))
        svm_loaded = True
    return svm_model

def load_mlp():
    global mlp_model
    if mlp_model == None:
        mlp_model = load_model('./classifiers/MLP-IDS')
    return mlp_model

load_svm()
load_mlp()

def mlp_predict(data):
    global mlp_model
    return mlp_model.predict(data)

def svm_predict(data):
    global svm_model
    return svm_model.predict(data)

@app.route('/predict', methods=['POST'])
def predict():
    method = os.environ.get('CLASSIFIIER')
    if method == 'MLP':
        mlp_predict(request.form["data"])
        return {
            "class": "normal"
        }
    elif method == 'SVM':
        svm_predict(request.form["data"])
        return {
            "class": "ddos"
        }
    return abort(400)

@app.route("/test")
def test():
    print("In test function")
    return { "test": True }

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9001)

