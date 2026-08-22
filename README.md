# 🛡️ TrustGuard: AI-Powered Flipkart Fake Review Detection System

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Web_Framework-Flask_3.0-lightgrey.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Deep Learning](https://img.shields.io/badge/Deep_Learning-PyTorch_2.1-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn_1.4-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Visualization](https://img.shields.io/badge/Charts-Chart.js_4.4-FF6384.svg?logo=chart.js&logoColor=white)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Project_Status-Completed-brightgreen.svg)]()

> **TrustGuard** is a full-stack, AI-powered review authenticity verification and product credibility auditing platform designed for **Flipkart** e-commerce product pages. It combines natural language processing (NLP), hybrid statistical feature engineering, classical machine learning classifiers, and deep neural networks (PyTorch BiLSTM) to detect computer-generated (CG) fake reviews, rating inflation attacks, and promotional spam in real time.

---

## 📌 Table of Contents
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Model Performance Benchmark](#-model-performance-benchmark)
- [Mathematical & Algorithmic Foundations](#-mathematical--algorithmic-foundations)
- [UI & Functional Modules Overview](#-ui--functional-modules-overview)
- [Repository Structure](#-repository-structure)
- [Installation & Quickstart Guide](#-installation--quickstart-guide)
- [REST API Specification](#-rest-api-specification)

---

## 🚀 Key Features

* **🔍 Live Flipkart Product URL Inspector**: Extracts up to 30 customer reviews directly from any live Flipkart product page via the **Parse.bot API**, complete with product name extraction, category auto-detection, and an in-memory **URL caching layer** to conserve API credits.
* **📝 Multi-Paragraph Bulk Review Analyzer**: Allows shoppers to copy and paste blocks of raw reviews directly from e-commerce listings for instantaneous batch evaluation.
* **🧪 Single Review Inspector**: Interactive manual testing suite featuring a 1-to-5 star rating slider and instant real-time prediction output.
* **🎯 Automated Product Trust Index (%)**: Computes an aggregate product authenticity score:
  $$\text{Trust Index (\%)} = \left( \frac{\text{Count of REAL Reviews}}{\text{Total Reviews Analyzed}} \right) \times 100\%$$
* **🚩 Explainable Suspicion Flagging**: Instead of acting as an opaque black box, TrustGuard flags specific spam indicators including:
  * 🔠 **Excessive Capitalization** (All-caps shouting spam)
  * ❗ **Repeated Exclamation Marks** (Over-enthusiastic bot text)
  * 🔁 **Repetitive Vocabulary** (Low lexical diversity)
  * 📢 **Generic Promotional Phrases** (*"100% RECOMMENDED"*, *"BUY BUY BUY"*, *"MUST BUY"*)
* **⚡ Multi-Model Switching**: Allows instant model toggling in the UI header between **PyTorch BiLSTM**, **Linear SVM**, **Logistic Regression**, and **Multinomial Naive Bayes**.
* **📱 Responsive Glassmorphic Dashboard**: Dark-mode aesthetic with fluid touch-friendly UI controls (44px–48px touch targets) optimized for desktop computers, tablets, and smartphones.
* **🔄 Production Resilience & 24/7 Keep-Alive**: Includes an integrated `/ping` health endpoint for automated UptimeRobot monitoring, alongside offline category-tailored fallback review generators.

---

## 🏗️ System Architecture

TrustGuard follows a modular **3-Tier Model-View-Controller (MVC)** architectural design:

```text
[ Shopper / Client Browser ]
           │
           ▼  (HTTP / JSON REST API Calls)
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PRESENTATION TIER (View)                                                 │
│    • Glassmorphic Single-Page Application (HTML5, CSS3, Vanilla JS)         │
│    • Animated SVG Trust Index Progress Ring & Metrics Stat Cards            │
│    • Dynamic Chart.js Doughnut (Authenticity) & Bar Charts (Star Ratings)   │
│    • Filterable Real-time Review Feed with Confidence Badges & Flags        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. APPLICATION TIER (Controller)                                            │
│    • Flask REST API Server (`app.py`)                                       │
│    • URL Domain & Path Validator (`flipkart.com`, `/p/`, `pid=`)            │
│    • In-Memory `URL_CACHE` Hash Table (Zero Credit Waste on Duplicates)     │
│    • Live Scraping Gateway (`scraper.py`) via Parse.bot API                 │
│    • Feature Engineering & Inference Engine (`model.py`)                    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. DATA & MODEL TIER (Model Storage)                                        │
│    • 40,432 Kaggle Labeled Dataset (`CG` Computer-Generated vs `OR` Real)   │
│    • Serialized Scikit-Learn Classifiers (`Linear_SVM.pkl`, `LogReg.pkl`)   │
│    • PyTorch Deep Learning BiLSTM Architecture (`BiLSTMClassifier`)         │
│    • Vectorizers: 15,000 Word N-Grams + 10,000 Char N-Grams + StandardScaler│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏆 Model Performance Benchmark

All models were trained and benchmarked on a stratified 80% training / 20% test split of the **40,432-row e-commerce review dataset**:

| Model Architecture | Model Family | Accuracy | F1-Score | Feature Matrix Used | Inference Time |
| :--- | :---: | :---: | :---: | :--- | :---: |
| **BiLSTM (Bidirectional LSTM)** | **Deep Learning** | **96.40%** | **96.38%** | Word Embeddings (128d) + Spatial Dropout + Dense | **< 0.02s** |
| **Linear SVM (LinearSVC)** | **Machine Learning** | **95.70%** | **95.68%** | TF-IDF Word (15k) + Char (10k) + 7 Scaled Meta | **< 0.01s** |
| **Logistic Regression** | **Machine Learning** | **94.95%** | **94.93%** | TF-IDF Word (15k) + Char (10k) + 7 Scaled Meta | **< 0.01s** |
| **Multinomial Naive Bayes** | **Machine Learning** | **90.96%** | **90.96%** | TF-IDF Word Matrix (1-2 N-Grams) | **< 0.01s** |

---

## 🧮 Mathematical & Algorithmic Foundations

### 1. Hybrid TF-IDF Feature Vectorization
$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \left[ \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1 \right]$$

### 2. StandardScaler Z-Score Metadata Normalization
Seven quantitative behavioral features (character length, word count, average word length, exclamation count, uppercase ratio, unique word ratio, and star rating) are standardized:
$$z = \frac{x - \mu}{\sigma} \quad \text{where } \mu = \frac{1}{N}\sum_{i=1}^{N} x_i, \quad \sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N} (x_i - \mu)^2}$$

### 3. Linear SVM Maximum-Margin Hyperplane
$$\min_{w,b} \frac{1}{2} \|w\|^2 + C \sum_{i=1}^N \max(0, 1 - y_i(w^T x_i + b)) \quad \Longrightarrow \quad P(\text{Fake} \mid X) = \frac{1}{1 + e^{-1.2 \cdot (w^T X + b)}}$$

### 4. PyTorch Bi-directional LSTM Gated Equations
$$\begin{aligned}
f_t &= \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) \quad \text{[Forget Gate]} \\
i_t &= \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) \quad \text{[Input Gate]} \\
\tilde{C}_t &= \tanh(W_c \cdot [h_{t-1}, x_t] + b_c) \quad \text{[Candidate State]} \\
C_t &= f_t \odot C_{t-1} + i_t \odot \tilde{C}_t \quad \text{[Cell State Update]} \\
o_t &= \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) \quad \text{[Output Gate]} \\
h_t &= o_t \odot \tanh(C_t) \quad \text{[Hidden Output State]} \\
h_{\text{BiLSTM}} &= [h_{\text{forward}} \, ; \, h_{\text{backward}}] \\
P(\text{Fake} \mid X) &= \sigma(W_2 \cdot \text{ReLU}(W_1 \cdot \text{MeanPool}(h_{\text{BiLSTM}})))
\end{aligned}$$

---

## 💻 UI & Functional Modules Overview

| Module Component | Interface Functionality | User Experience & Output |
| :--- | :--- | :--- |
| **Tab 1: Bulk Reviews** | Paste multi-line raw review blocks directly from any Flipkart product page. | Instant batch analysis with Trust Index score, total counts, and review breakdown cards. |
| **Tab 2: URL Inspector** | Enter a live Flipkart product link (`flipkart.com/.../p/...`). | Live scraping of 30 customer reviews via Parse.bot API with product name extraction. |
| **Tab 3: Single Tester** | Enter single review text + interactive star rating slider (1–5). | Real-time classification verdict (`REAL` / `FAKE`) with percentage confidence. |
| **Trust Score Ring** | Animated circular SVG progress ring. | Visual percentage gauge color-coded (Green for Authentic, Red for High Spam Risk). |
| **Chart.js Analytics** | Interactive Doughnut & Bar charts. | Visual split of authentic vs fake distribution and star rating breakdown. |
| **Review Feed** | Filterable cards with `All`, `Real Only`, and `Fake Only` tabs. | Displays review author, rating, text, confidence badge, and specific suspicion warning tags. |
| **Benchmark Modal** | Header action button opening live benchmark table. | Side-by-side comparison of accuracy and F1 scores across all trained models. |

---

## 📂 Repository Structure

```text
Fake-Product-Review-Detection-System/
├── app.py                      # Flask REST Server & Application Controller
├── model.py                    # PyTorch BiLSTM & Scikit-Learn Feature Extraction Pipeline
├── scraper.py                  # Parse.bot Flipkart Scraper & URL Caching Gateway
├── fake reviews dataset.csv    # 40,432 Labeled Training Dataset (CG vs OR)
├── requirements.txt            # Python Dependencies (Flask, PyTorch, Scikit-Learn, etc.)
├── README.md                   # Project Architecture & Documentation (This File)
├── templates/
│   └── index.html              # Responsive Glassmorphic Single-Page Application Layout
├── static/
│   ├── css/
│   │   └── style.css           # Glassmorphism Modern Dark-Theme Design System
│   └── js/
│       └── main.js             # Async REST Client, DOM Controller & Chart.js Visualizations
└── saved_models/               # Serialized Models & Feature Transformers
    ├── Linear_SVM.pkl          # Trained Linear Support Vector Classifier (95.70%)
    ├── Logistic_Regression.pkl # Trained Logistic Regression Classifier (94.95%)
    ├── Naive_Bayes.pkl         # Trained Multinomial Naive Bayes Classifier (90.96%)
    ├── tfidf_word.pkl          # 15,000 Word N-Gram TF-IDF Vectorizer
    ├── tfidf_char.pkl          # 10,000 Character N-Gram TF-IDF Vectorizer
    ├── scaler.pkl              # StandardScaler for Review Metadata Attributes
    └── metrics.pkl             # Serialized Accuracy and F1 Benchmark Data
```

---

## ⚡ Installation & Quickstart Guide

### Prerequisites
* **Python 3.9 or higher** (Python 3.11 recommended)
* **Git** installed on your operating system

### 1. Clone the Repository
```bash
git clone https://github.com/Jaykishan-0077/Fake-Product-Review-Detection-System.git
cd Fake-Product-Review-Detection-System
```

### 2. Create and Activate a Virtual Environment
```bash
# On macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. (Optional) Set Parse.bot Scraping API Key
The scraper includes a pre-configured key and fallback review generator. To set your own API key:
```bash
# On macOS / Linux:
export PARSE_BOT_API_KEY="your_api_key_here"

# On Windows (Command Prompt):
set PARSE_BOT_API_KEY="your_api_key_here"

# On Windows (PowerShell):
$env:PARSE_BOT_API_KEY="your_api_key_here"
```

### 5. Launch the Application
```bash
python3 app.py
```

### 6. Access the Dashboard
Open your web browser and navigate to:
👉 **`http://localhost:5050`** (or `http://127.0.0.1:5050`)

---

## 🔌 REST API Specification

| Endpoint | Method | Input Parameters | Output Response | Description |
| :--- | :---: | :--- | :--- | :--- |
| **`/api/analyze-url`** | `POST` | `{"url": "https://flipkart.com/...", "model": "Linear SVM"}` | `{"product_name": "...", "trust_score": 92.3, "reviews": [...]}` | Scrapes live reviews from Flipkart URL and performs batch evaluation. |
| **`/api/analyze-bulk`** | `POST` | `{"text": "Review paragraph 1\nReview paragraph 2", "model": "Linear SVM"}` | `{"trust_score": 100.0, "total_analyzed": 2, "reviews": [...]}` | Evaluates pasted blocks of multi-line review text. |
| **`/api/analyze-text`** | `POST` | `{"text": "Sample review text", "rating": 5, "model": "Linear SVM"}` | `{"prediction": "REAL", "confidence": 97.8, "flags": []}` | Classifies a single manually typed review text. |
| **`/api/models`** | `GET` | *None* | `{"Linear SVM": {"accuracy": 95.70, "f1": 95.68}, ...}` | Returns benchmark metrics for all trained models. |
| **`/ping`** | `GET` | *None* | `{"status": "active"}` | Health-check endpoint for automated keep-alive monitors. |
