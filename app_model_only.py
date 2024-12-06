from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)  # Enable CORS

# Memuat model dan vectorizer
try:
    model = joblib.load('knn_model.pkl')
    tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
except FileNotFoundError:
    model = None
    tfidf_vectorizer = None
    print("Model atau vectorizer tidak ditemukan. Pastikan file 'knn_model.pkl' dan 'tfidf_vectorizer.pkl' tersedia.")

# Endpoint Home
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Microservice Sentiment Prediction!"})

# Endpoint untuk Prediksi Sentimen
@app.route('/predict', methods=['POST'])
def predict_sentiment():
    if not model or not tfidf_vectorizer:
        return jsonify({"error": "Model or vectorizer not loaded"}), 500

    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({"error": "Text is required for prediction"}), 400

    # Transform text menggunakan TF-IDF dan prediksi
    text_tfidf = tfidf_vectorizer.transform([text])
    prediction = model.predict(text_tfidf)

    return jsonify({"text": text, "sentiment": prediction[0]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)