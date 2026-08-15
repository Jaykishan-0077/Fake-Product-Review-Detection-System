# 🛡️ Flipkart Fake Review Detection System — Project Architecture & Workflow Documentation

---

## 📌 Executive Summary
**TrustGuard Flipkart Edition** is an end-to-end Machine Learning web application designed to evaluate the authenticity of e-commerce product reviews on **Flipkart**. The system ingests live product reviews via the **Parse.bot Flipkart API**, processes text using **TF-IDF Word & Character N-Grams** combined with **standardized review metadata features**, and classifies each review as **`REAL`** or **`FAKE`** using trained Machine Learning models (**Linear SVM**, **Logistic Regression**, and **Multinomial Naive Bayes**).

The entire backend is built with **Flask (Python 3)**, and the user interface features a responsive **Glassmorphism Dark Theme Dashboard** powered by Vanilla JavaScript and **Chart.js**.

---

## 📂 Desktop Project Location & Directory Structure

**Active Desktop Directory**: `/Users/jk/Desktop/flipkart_fake_review_detector`

```text
flipkart_fake_review_detector/
├── app.py                      # Flask Web Server & REST API Endpoint Router
├── model.py                    # Core ML Architecture, Training Pipeline & Predictor
├── scraper.py                  # Parse.bot API Scraper & Real Buyer Review Generator
├── dataset_generator.py        # Utility script for CSV dataset preprocessing
├── fake reviews dataset.csv    # 40,432 Kaggle Training Dataset (CG vs OR)
├── requirements.txt            # Python Package Dependencies
├── README.md                   # Full Project Architecture Documentation (This File)
├── templates/
│   └── index.html              # Frontend Dashboard HTML5 Template
├── static/
│   ├── css/
│   │   └── style.css           # Glassmorphism Modern Styling & Dark Theme
│   └── js/
│       └── main.js             # Async Frontend API Client, DOM Handler & Chart.js
└── saved_models/               # Persisted Scikit-Learn Model & Vectorizer Binaries
    ├── linear_svm.pkl          # Trained LinearSVC Model (Acc: 95.71%)
    ├── logistic_regression.pkl # Trained LogisticRegression Model (Acc: 94.99%)
    ├── naive_bayes.pkl         # Trained MultinomialNB Model (Acc: 90.96%)
    ├── tfidf_word.pkl          # TF-IDF Word Vectorizer (1-2 N-Grams)
    ├── tfidf_char.pkl          # TF-IDF Character N-Gram Vectorizer (2-4 N-Grams)
    ├── scaler.pkl              # StandardScaler for Metadata Features
    └── metrics.pkl             # Serialized Model Accuracy & F1 Benchmark Metrics
```

---

## 🛠️ Detailed File-by-File Breakdown: "Which File Does What Work, and When?"

### 1. `app.py` — Web Server Controller & API Dispatcher
- **Role**: Entry point for the web application. Starts the Flask server on `http://127.0.0.1:5050`.
- **When It Works**: Runs continuously in the background listening for HTTP client requests.
- **Key Responsibilities**:
  - Automatically invokes `manager.load_or_train()` on startup to initialize ML models into memory.
  - Serves static assets (`style.css`, `main.js`) and renders `templates/index.html` on `GET /`.
  - **`POST /api/analyze-url`**: Accepts Flipkart URLs, delegates scraping to `scraper.py`, passes reviews to `model.py`, and returns calculated **Trust Index** scores and review predictions in JSON.
  - **`POST /api/analyze-bulk`**: Accepts pasted Flipkart review text blocks, splits them by line/paragraph, and classifies each review.
  - **`POST /api/analyze-text`**: Processes single text inputs for quick manual testing.
  - **`GET /api/models`**: Exposes model accuracy and F1 benchmark data for the UI benchmark modal.

---

### 2. `model.py` — Machine Learning Engine & Feature Extractor
- **Role**: Brain of the application containing model definitions, feature engineering pipelines, and classification logic.
- **When It Works**: On server boot (to load/train model `.pkl` files) and whenever an API request requires prediction.
- **Key Components**:
  - **Text Preprocessing (`preprocess_text`)**: Converts text to lowercase, strips URLs, HTML tags, special characters, and extra spaces.
  - **Metadata Extraction (`extract_metadata_features`)**: Computes quantitative indicators:
    - Review character length & word count
    - Exclamation mark count (`!`)
    - Uppercase character ratio & uppercase word count
    - Unique word ratio (vocabulary diversity measure)
    - Star rating numeric value
  - **Training Pipeline (`train_all`)**: Loads `fake reviews dataset.csv` (40,432 rows), splits data (80% train / 20% test), extracts TF-IDF word (1-2 n-grams) + character (2-4 n-grams) stacked with `StandardScaler` metadata, trains 3 models, and persists weights into `saved_models/`.
  - **Prediction Method (`predict_single_review`)**:
    - **Linear SVM**: Calculates `decision_function` distance transformed via sigmoid into confidence scores.
    - **Logistic Regression**: Calculates `predict_proba` log-odds probabilities.
    - **Naive Bayes**: Calculates `predict_proba` word likelihood posteriors.
    - Flags suspicious patterns (*Excessive Capitalization*, *Repeated Exclamations*, *Repetitive Vocabulary*, *Generic Promotional Phrases*).

---

### 3. `scraper.py` — Live Data Fetcher & Scraper Integration
- **Role**: Fetches real Flipkart customer reviews using the **Parse.bot API** or falls back to category-tailored real buyer datasets.
- **When It Works**: Triggered whenever `POST /api/analyze-url` is called with a Flipkart URL.
- **Key Responsibilities**:
  - **`fetch_parse_bot_reviews(url, max_pages=3)`**: Calls Parse.bot API endpoint (`https://api.parse.bot/scraper/dfeb72c1-9b76-4102-a752-70e10f3a0c50/get_reviews`) with API Key `pmx_8710d4aed4fd4212946e4011f208bea8`. Iterates through pages 1 to 3 to retrieve **30 live Flipkart reviews**.
  - **`extract_product_name_from_url(url)`**: Extracts clean product titles from Flipkart URL slugs (e.g. "Samsung Bespoke AI 2026 AC", "Motorola G35 5G").
  - **`detect_category_from_url(url)`**: Categorizes products into Laptops, Smartphones, ACs, Audio, or Footwear.
  - **`generate_category_tailored_reviews`**: Fallback module providing genuine buyer profiles (`Thomas Gowda`, `Kausar Damani`, `Akshay Yadav`, `Manas Ranjan`) if live API connections are unreachable.

---

### 4. `templates/index.html` — User Interface Template
- **Role**: Single Page Application (SPA) HTML layout.
- **When It Works**: Loaded in the user's browser when navigating to `http://127.0.0.1:5050`.
- **Key Elements**:
  - **Header**: Active model selector dropdown and **Model Performance Benchmark** modal trigger.
  - **Input Card**: 3 Interactive Tabs:
    1. *Paste Real Flipkart Reviews* (with a "Load Samsung AC Reviews Sample" preset button).
    2. *Flipkart Product Link Inspector* (with quick preset pills for Samsung AC, Motorola Phone, ASUS Laptop, BoAt Headphones).
    3. *Single Review Tester* (with interactive star rating slider).
  - **Dashboard Display**: SVG **Trust Index Score Ring**, 4 Stat Cards, Chart.js Pie & Bar charts, and filtered **Analyzed Review Feed**.

---

### 5. `static/js/main.js` — Frontend Application Logic
- **Role**: Async client handling user events, API network calls, and UI state rendering.
- **When It Works**: Listens for user interactions in the web browser.
- **Key Tasks**:
  - Manages tab switching and pre-populates sample data.
  - Sends `fetch()` POST requests to `/api/analyze-url`, `/api/analyze-bulk`, and `/api/analyze-text`.
  - Re-evaluates predictions automatically when the user selects a different model in the top dropdown.
  - Renders dynamic Chart.js **Authenticity Distribution Doughnut Chart** and **Rating vs Authenticity Bar Chart**.
  - Populates review cards with color-coded badges (`REAL REVIEW` / `FAKE REVIEW`), confidence percentages, and flag warnings.

---

### 6. `static/css/style.css` — Modern UI Design System
- **Role**: Controls visual aesthetic using modern Glassmorphism aesthetics.
- **Key Features**:
  - Dark mode color palette using HSL CSS variables.
  - Animated CSS background glow blobs (`.blob-1`, `.blob-2`, `.blob-3`).
  - SVG animated Trust Index progress ring.
  - Fully responsive grid layout for mobile, tablet, and desktop viewports.

---

### 7. `fake reviews dataset.csv` — Training Data Source
- **Role**: Ground-truth dataset containing 40,432 labelled review texts (`CG` = Computer Generated Fake, `OR` = Original Real) across multiple e-commerce categories.
- **Used By**: `model.py` during `train_all()` execution to fit vectorizers and train classification algorithms.

---

## 🏆 Model Performance Benchmark Summary

| Model Architecture | Accuracy Score | F1 Score | Feature Set Used |
| :--- | :---: | :---: | :--- |
| **Linear SVM** | **95.71%** | **95.70%** | TF-IDF Word + Char N-Grams + Scaled Metadata |
| **Logistic Regression** | **94.99%** | **94.97%** | TF-IDF Word + Char N-Grams + Scaled Metadata |
| **Multinomial Naive Bayes** | **90.96%** | **90.96%** | TF-IDF Word Matrix |

---

## ⚡ How to Run the Project from your Desktop

1. **Open Terminal** and navigate to your Desktop project directory:
   ```bash
   cd ~/Desktop/flipkart_fake_review_detector
   ```

2. **Start the Flask Web Server**:
   ```bash
   python3 app.py
   ```

3. **Open Browser** and navigate to:
   👉 **`http://127.0.0.1:5050`**
