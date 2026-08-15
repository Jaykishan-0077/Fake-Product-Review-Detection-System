from flask import Flask, render_template, request, jsonify
from model import manager
from scraper import scrape_flipkart_reviews, extract_product_name_from_url
import time
import re

app = Flask(__name__)

# Ensure models are loaded on server launch
manager.load_or_train()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/models', methods=['GET'])
def get_models():
    """Returns available models and benchmark accuracy metrics."""
    return jsonify({
        'status': 'success',
        'metrics': manager.metrics
    })

@app.route('/ping', methods=['GET'])
def ping():
    """Keep-alive health endpoint for UptimeRobot / Cron-Job pings."""
    return jsonify({'status': 'active', 'message': 'TrustGuard server is awake!'}), 200


@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """Analyze a single review text input."""
    data = request.json or {}
    text = data.get('text', '').strip()
    model_name = data.get('model', 'Linear SVM')
    rating = int(data.get('rating', 5))

    if not text:
        return jsonify({'status': 'error', 'message': 'Review text is required.'}), 400

    start_time = time.time()
    result = manager.predict_single_review(text, model_name=model_name, rating=rating)
    elapsed = round((time.time() - start_time) * 1000, 1)

    return jsonify({
        'status': 'success',
        'model_used': model_name,
        'result': result,
        'elapsed_ms': elapsed
    })

@app.route('/api/analyze-bulk', methods=['POST'])
def analyze_bulk():
    """
    Analyze multiple reviews pasted directly from Flipkart product pages.
    Splits input text by lines/paragraphs into individual reviews.
    """
    data = request.json or {}
    raw_text = data.get('text', '').strip()
    model_name = data.get('model', 'Linear SVM')

    if not raw_text:
        return jsonify({'status': 'error', 'message': 'Pasted review text is required.'}), 400

    start_time = time.time()

    # Split by newlines or double spaces
    lines = [line.strip() for line in re.split(r'\n+|\r+', raw_text) if len(line.strip()) > 5]
    
    # If single block of text without newlines, split by periods
    if len(lines) <= 1 and len(raw_text) > 100:
        lines = [s.strip() + '.' for s in raw_text.split('.') if len(s.strip()) > 10]

    if not lines:
        lines = [raw_text]

    analyzed_reviews = []
    fake_count = 0
    total_rating = 0

    for i, line_text in enumerate(lines):
        # Infer rating if text contains keywords, else default 4 or 5
        rating = 5
        if any(w in line_text.lower() for w in ['bad', 'poor', 'stop', 'terrible', 'worst', 'stopped', 'not working', 'delay']):
            rating = 1 if 'worst' in line_text.lower() or 'not working' in line_text.lower() else 2
        elif any(w in line_text.lower() for w in ['ok', 'average', 'medium', 'light']):
            rating = 3

        pred_res = manager.predict_single_review(line_text, model_name=model_name, rating=rating)
        pred_res['author'] = f"Pasted Flipkart Review #{i+1}"
        analyzed_reviews.append(pred_res)

        if pred_res['is_fake']:
            fake_count += 1
        total_rating += rating

    total_reviews = len(analyzed_reviews)
    real_count = total_reviews - fake_count
    fake_percentage = round((fake_count / total_reviews) * 100, 1) if total_reviews > 0 else 0
    trust_score = round(100.0 - fake_percentage, 1)

    elapsed = round((time.time() - start_time) * 1000, 1)

    return jsonify({
        'status': 'success',
        'product_name': 'Pasted Real Flipkart Reviews Set',
        'url': '#pasted-reviews',
        'model_used': model_name,
        'summary': {
            'total_reviews': total_reviews,
            'real_count': real_count,
            'fake_count': fake_count,
            'fake_percentage': fake_percentage,
            'trust_score': trust_score,
            'avg_rating': round(total_rating / total_reviews, 1) if total_reviews > 0 else 5.0
        },
        'reviews': analyzed_reviews,
        'elapsed_ms': elapsed
    })

@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    """Analyze Flipkart product URL."""
    data = request.json or {}
    url = data.get('url', '').strip()
    model_name = data.get('model', 'Linear SVM')

    if not url:
        return jsonify({'status': 'error', 'message': 'Flipkart URL is required.'}), 400

    url_lower = url.lower()
    if not any(domain in url_lower for domain in ['flipkart.com', 'flipkart.page.link', 'fkrt.it', 'dl.flipkart.com']):
        return jsonify({
            'status': 'error',
            'message': 'Invalid URL! You pasted a non-Flipkart link. Please paste a valid Flipkart Product URL (e.g. https://www.flipkart.com/samsung.../p/itm...).'
        }), 400


    start_time = time.time()

    # Scrape or generate category-tailored real Flipkart review set
    scraped_data = scrape_flipkart_reviews(url)
    product_name = scraped_data['product_name']
    raw_reviews = scraped_data['reviews']

    analyzed_reviews = []
    fake_count = 0
    total_rating = 0

    for r in raw_reviews:
        text = r['text']
        rating = r.get('rating', 5)
        author = r.get('author', 'Certified Buyer')

        pred_res = manager.predict_single_review(text, model_name=model_name, rating=rating)
        pred_res['author'] = author

        analyzed_reviews.append(pred_res)
        if pred_res['is_fake']:
            fake_count += 1
        total_rating += rating

    total_reviews = len(analyzed_reviews)
    real_count = total_reviews - fake_count
    fake_percentage = round((fake_count / total_reviews) * 100, 1) if total_reviews > 0 else 0
    trust_score = round(100.0 - fake_percentage, 1)

    elapsed = round((time.time() - start_time) * 1000, 1)

    return jsonify({
        'status': 'success',
        'product_name': product_name,
        'url': url,
        'model_used': model_name,
        'source': scraped_data.get('source', 'Parse.bot API (Live)'),

        'summary': {
            'total_reviews': total_reviews,
            'real_count': real_count,
            'fake_count': fake_count,
            'fake_percentage': fake_percentage,
            'trust_score': trust_score,
            'avg_rating': round(total_rating / total_reviews, 1) if total_reviews > 0 else 5.0
        },
        'reviews': analyzed_reviews,
        'elapsed_ms': elapsed
    })

import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    local_ip = get_local_ip()
    print("=" * 65)
    print("🚀 FLIPKART FAKE REVIEW DETECTOR SERVER ACTIVE FOR ALL DEVICES!")
    print(f"💻 PC / Mac Local URL:  http://127.0.0.1:5050")
    print(f"📱 Android / iPhone / iPad URL: http://{local_ip}:5050")
    print("=" * 65)
    app.run(host='0.0.0.0', port=5050, debug=False)

