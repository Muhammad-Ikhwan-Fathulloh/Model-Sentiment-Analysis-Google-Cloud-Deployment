# 🚀 Model Sentiment Analysis – Deployment Google Cloud & Best Practices

Repository ini menyediakan **Model Sentiment Analysis** berbasis **Machine Learning** dan siap dideploy menggunakan **Google Cloud Run**, dilengkapi integrasi database **MySQL**, **MinIO** untuk manajemen model, dan **Docker + GitLab CI/CD** untuk automasi deployment.

* **Model Repository:** [GitHub: KNN Sentiment Analysis](https://github.com/Muhammad-Ikhwan-Fathulloh/Advanced-Machine-Learning-Course/tree/main/KNN)
* **Google Cloud Run:** [Cloud Run Docs](https://cloud.google.com/run?hl=id)
* **Database MySQL:** [FreeDB Tech](https://freedb.tech/)

---

## 🎯 Tujuan

1. Menyediakan API untuk **sentiment analysis** menggunakan model ML.
2. Menyimpan dan mengelola model ML secara efisien dengan **MinIO**.
3. Memudahkan deployment di **Google Cloud Run**.
4. Menerapkan **best practices Docker dan GitLab CI/CD** untuk deployment yang terotomatisasi dan aman.

---

## 📂 Format File Model Machine Learning

| Format     | Deskripsi                                        | Kegunaan                                |
| ---------- | ------------------------------------------------ | --------------------------------------- |
| `.joblib`  | Format untuk menyimpan model ML dengan `joblib`. | Cepat untuk model besar dan data array. |
| `.pkl`     | Format `pickle` bawaan Python.                   | Lebih generik dan fleksibel.            |
| `.h5`      | Format untuk model TensorFlow/Keras.             | Digunakan untuk model deep learning.    |
| `.pt/.pth` | Format untuk model PyTorch.                      | Digunakan dalam framework PyTorch.      |

> **Tip:** Gunakan `.joblib` untuk **scikit-learn** karena lebih cepat saat serialisasi/deserialisasi model besar.

---

## 🛠️ Setup Project

Clone repository:

```bash
git clone https://github.com/Muhammad-Ikhwan-Fathulloh/Model-Sentiment-Analysis-Google-Cloud-Deployment.git
cd Model-Sentiment-Analysis-Google-Cloud-Deployment
```

Install dependencies:

```bash
pip install -r requirements.txt
```

**Dependencies utama:**

* Flask & Flask-JWT-Extended → Membuat API dan authentication
* Flask-CORS → Menangani cross-origin requests
* MySQL Connector → Integrasi database
* Joblib → Load/save model scikit-learn
* Gunicorn → Production server untuk Flask
* Numpy & scikit-learn → Core machine learning libraries

---

## ⚡ Menjalankan API Lokal

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Atau menggunakan **Docker**:

```bash
docker build -t sentiment-analysis-app .
docker run -d -p 8080:8080 sentiment-analysis-app
```

Cek container:

```bash
docker ps
```

Push ke Docker Hub:

```bash
docker tag sentiment-analysis-app your_username_docker/sentiment-analysis-app:latest
docker login
docker push your_username_docker/sentiment-analysis-app:latest
```

---

## ☁️ Deployment di Google Cloud Run

1. **Build Docker Image**:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/sentiment-analysis-app
```

2. **Deploy Cloud Run**:

```bash
gcloud run deploy sentiment-analysis-app \
  --image gcr.io/PROJECT_ID/sentiment-analysis-app \
  --platform managed \
  --region REGION \
  --allow-unauthenticated
```

3. **Set environment variables** untuk MySQL & MinIO:

```bash
FLASK_ENV=production
DB_HOST=your-mysql-host
DB_USER=username
DB_PASS=password
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=access_key
MINIO_SECRET_KEY=secret_key
```

---

## 🗄️ MinIO – Model Management

Gunakan **MinIO** untuk menyimpan dan mengelola model ML, sehingga memudahkan:

* Load model versi terbaru secara dinamis
* Backup model otomatis
* Integrasi dengan CI/CD untuk update model

Contoh upload model ke MinIO:

```python
from minio import Minio

client = Minio(
    "minio-server:9000",
    access_key="minio-access-key",
    secret_key="minio-secret-key",
    secure=False
)

# Upload model
client.fput_object("models", "sentiment_model.joblib", "./models/sentiment_model.joblib")
```

---

## 🛡️ Best Practices Lanjutan

### 1️⃣ Docker Optimization

* Gunakan **multi-stage build** agar image lebih ringan:

```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt
COPY . .

# Stage 2: Runtime
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
```

* Gunakan **.dockerignore** untuk mengurangi size:

```
__pycache__/
*.pyc
*.pkl
*.joblib
.env
```

---

### 2️⃣ GitLab CI/CD (Automated Deployment)

Contoh `.gitlab-ci.yml`:

```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: registry.gitlab.com/username/sentiment-analysis-app

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

deploy:
  stage: deploy
  image: google/cloud-sdk:latest
  script:
    - gcloud auth activate-service-account --key-file $GOOGLE_SERVICE_ACCOUNT_JSON
    - gcloud run deploy sentiment-analysis-app --image $DOCKER_IMAGE --platform managed --region us-central1 --allow-unauthenticated
```

---

### 3️⃣ Versioning Model

* Simpan model dengan versi unik di MinIO:

```
sentiment_model_v1.0.joblib
sentiment_model_v1.1.joblib
```

* API selalu mengambil versi terbaru untuk production:

```python
latest_model = minio_client.list_objects('models', prefix='sentiment_model')
```

---

## 📈 Monitoring & Logging

* Gunakan **Cloud Logging** & **Cloud Monitoring** untuk memantau API.
* Gunakan **Gunicorn access logs** dan **Flask logging** untuk debugging.

---

## 🔑 Tips Tambahan

1. Gunakan **environment variables** untuk rahasia (DB password, MinIO keys, API keys).
2. Selalu buat **backup model** sebelum update di MinIO.
3. Terapkan **unit tests** untuk API sebelum deployment.
4. Gunakan **health check endpoint** agar Cloud Run bisa memantau container.

Apakah mau saya buatkan diagramnya juga?
