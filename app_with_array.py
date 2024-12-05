from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)  # Enable CORS

# Konfigurasi JWT
app.config['JWT_SECRET_KEY'] = 'bangkit101'
jwt = JWTManager(app)

# Data pengguna sementara (digunakan sebagai pengganti database)
users = []

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

# Registrasi User
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Cek apakah username sudah digunakan
    for user in users:
        if user['username'] == username:
            return jsonify({"error": "Username already exists"}), 400

    # Hash password sebelum disimpan
    hashed_password = generate_password_hash(password)

    # Simpan pengguna ke array
    users.append({'username': username, 'password': hashed_password})

    return jsonify({"message": "User registered successfully"}), 201

# Login dan Mendapatkan JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Cari pengguna berdasarkan username
    user = next((user for user in users if user['username'] == username), None)

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Generate JWT
    access_token = create_access_token(identity={"username": user["username"]})
    return jsonify({"access_token": access_token}), 200

# Endpoint untuk Prediksi Sentimen
@app.route('/predict', methods=['POST'])
@jwt_required()
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
    app.run(debug=True)