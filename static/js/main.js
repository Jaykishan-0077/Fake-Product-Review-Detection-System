document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const modelSelect = document.getElementById('modelSelect');
    const btnModelMetrics = document.getElementById('btnModelMetrics');
    const metricsModal = document.getElementById('metricsModal');
    const btnCloseModal = document.getElementById('btnCloseModal');
    const metricsTbody = document.getElementById('metricsTbody');

    // Tab buttons and containers
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Forms
    const bulkForm = document.getElementById('bulkForm');
    const bulkText = document.getElementById('bulkText');
    const btnLoadACSample = document.getElementById('btnLoadACSample');
    const urlForm = document.getElementById('urlForm');
    const flipkartUrl = document.getElementById('flipkartUrl');
    const textForm = document.getElementById('textForm');
    const reviewText = document.getElementById('reviewText');
    const ratingInput = document.getElementById('ratingInput');
    const ratingVal = document.getElementById('ratingVal');
    const starsPreview = document.getElementById('starsPreview');

    // Preset pills
    const pillButtons = document.querySelectorAll('.pill-btn');

    // Display Sections
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    const resultsSection = document.getElementById('resultsSection');

    // Results Header
    const resProductName = document.getElementById('resProductName');
    const resProductUrl = document.getElementById('resProductUrl');
    const trustScoreValue = document.getElementById('trustScoreValue');
    const circlePath = document.getElementById('circlePath');
    const trustStatus = document.getElementById('trustStatus');

    // Stats Elements
    const statTotalReviews = document.getElementById('statTotalReviews');
    const statRealCount = document.getElementById('statRealCount');
    const statFakeCount = document.getElementById('statFakeCount');
    const statFakeRatio = document.getElementById('statFakeRatio');

    // Filter Buttons & Reviews Feed
    const filterBtns = document.querySelectorAll('.filter-btn');
    const filterAllCount = document.getElementById('filterAllCount');
    const filterRealCount = document.getElementById('filterRealCount');
    const filterFakeCount = document.getElementById('filterFakeCount');
    const reviewsList = document.getElementById('reviewsList');

    // Global state for charts & current analysis
    let pieChartInstance = null;
    let barChartInstance = null;
    let currentAnalysisData = null;
    let lastActionType = 'bulk'; // 'bulk', 'url', or 'text'

    // Sample Samsung AC reviews directly from Flipkart screenshot
    const SAMSUNG_AC_SAMPLE = `Good and super cooling, ok for indoor noise and outdoor noise. Over all supper and budgeted AC
Very bad quality no cooling at all compressor stopped when you change temperature
Smart AC with good cooling. The WindFree technology provides comfortable cooling.
A/ C is not working cooling stop in 5 minutes
Excellent AC! Cooling is very fast and effective even during hot afternoons. The installation was smooth, and the Wi-Fi feature works great.
Very fast cooling.silent operation. With in 5 minutes room gets chilled.
Good Product and good cooling, value for money thankyou flipkart
Great cooling, energy efficient, installation delay, I am happy with samsung service....
Very nice cooling AC and flipkart experience very nice, value for money, thank you
Cooling is fast, operation is quiet, and the AI features with Wi-Fi connectivity are very useful. The build quality is premium.
Value for money and best cooling systems
Super work samsung design looking good and cooling system best....
Light cooling performance for small room.`;

    // 1. Tab Switching Logic
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // Load Samsung AC sample reviews button
    btnLoadACSample.addEventListener('click', () => {
        bulkText.value = SAMSUNG_AC_SAMPLE;
        analyzeBulkReviews();
    });

    // Rating Slider Preview
    ratingInput.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        ratingVal.textContent = val;
        starsPreview.textContent = '★'.repeat(val) + '☆'.repeat(5 - val);
    });

    // Preset Pill Click
    pillButtons.forEach(pill => {
        pill.addEventListener('click', () => {
            const url = pill.getAttribute('data-url');
            flipkartUrl.value = url;
            analyzeUrl(url);
        });
    });

    // Model Change Event -> Re-run current analysis
    modelSelect.addEventListener('change', () => {
        if (currentAnalysisData) {
            if (lastActionType === 'bulk' && bulkText.value.trim()) {
                analyzeBulkReviews();
            } else if (lastActionType === 'url' && flipkartUrl.value.trim()) {
                analyzeUrl(flipkartUrl.value.trim());
            } else if (lastActionType === 'text' && reviewText.value.trim()) {
                analyzeSingleText();
            }
        }
    });

    // 2. Form Submit Handlers
    bulkForm.addEventListener('submit', (e) => {
        e.preventDefault();
        analyzeBulkReviews();
    });

    urlForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const url = flipkartUrl.value.trim();
        if (url) analyzeUrl(url);
    });

    textForm.addEventListener('submit', (e) => {
        e.preventDefault();
        analyzeSingleText();
    });

    // 3. API Actions
    function analyzeBulkReviews() {
        const text = bulkText.value.trim();
        if (!text) return;

        lastActionType = 'bulk';
        showLoading('Analyzing pasted Flipkart reviews with AI model...');

        fetch('/api/analyze-bulk', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                model: modelSelect.value
            })
        })
        .then(res => res.json())
        .then(data => {
            hideLoading();
            if (data.status === 'success') {
                currentAnalysisData = data;
                renderDashboardResults(data);
            } else {
                alert(data.message || 'Analysis failed.');
            }
        })
        .catch(err => {
            hideLoading();
            console.error(err);
            alert('Error connecting to backend server.');
        });
    }

    function analyzeUrl(url) {
        lastActionType = 'url';
        showLoading('Inspecting product link & analyzing Flipkart reviews...');

        fetch('/api/analyze-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: url,
                model: modelSelect.value
            })
        })
        .then(res => res.json())
        .then(data => {
            hideLoading();
            if (data.status === 'success') {
                currentAnalysisData = data;
                renderDashboardResults(data);
            } else {
                alert(data.message || 'Scraping failed.');
            }
        })
        .catch(err => {
            hideLoading();
            console.error(err);
            alert('Error connecting to backend server.');
        });
    }

    function analyzeSingleText() {
        const text = reviewText.value.trim();
        if (!text) return;

        lastActionType = 'text';
        showLoading('Evaluating review text authenticity...');

        fetch('/api/analyze-text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                rating: parseInt(ratingInput.value),
                model: modelSelect.value
            })
        })
        .then(res => res.json())
        .then(data => {
            hideLoading();
            if (data.status === 'success') {
                const singleRes = data.result;
                const mockPayload = {
                    product_name: "Single Review Input Test",
                    url: "#single-test",
                    model_used: data.model_used,
                    summary: {
                        total_reviews: 1,
                        real_count: singleRes.is_fake ? 0 : 1,
                        fake_count: singleRes.is_fake ? 1 : 0,
                        fake_percentage: singleRes.is_fake ? 100.0 : 0.0,
                        trust_score: singleRes.is_fake ? 0.0 : 100.0,
                        avg_rating: singleRes.rating
                    },
                    reviews: [singleRes]
                };
                currentAnalysisData = mockPayload;
                renderDashboardResults(mockPayload);
            } else {
                alert(data.message || 'Analysis failed.');
            }
        })
        .catch(err => {
            hideLoading();
            console.error(err);
            alert('Error connecting to backend server.');
        });
    }

    // 4. Render Results Dashboard
    function renderDashboardResults(data) {
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        const summary = data.summary;

        // Header
        resProductName.textContent = data.product_name || "Flipkart Product";
        if (data.url && data.url.startsWith('http')) {
            resProductUrl.href = data.url;
            resProductUrl.style.display = 'inline-flex';
        } else {
            resProductUrl.style.display = 'none';
        }

        // Trust Score Ring
        const trust = summary.trust_score;
        trustScoreValue.textContent = `${trust.toFixed(1)}%`;
        circlePath.setAttribute('stroke-dasharray', `${trust}, 100`);

        if (trust >= 80) {
            circlePath.setAttribute('stroke', '#10b981');
            trustStatus.textContent = "High Authenticity";
            trustStatus.className = "trust-status text-green";
        } else if (trust >= 50) {
            circlePath.setAttribute('stroke', '#f59e0b');
            trustStatus.textContent = "Moderate Suspicion";
            trustStatus.className = "trust-status text-yellow";
        } else {
            circlePath.setAttribute('stroke', '#ef4444');
            trustStatus.textContent = "High Spam Risk";
            trustStatus.className = "trust-status text-red";
        }

        // Stats Overview
        statTotalReviews.textContent = summary.total_reviews;
        statRealCount.textContent = summary.real_count;
        statFakeCount.textContent = summary.fake_count;
        statFakeRatio.textContent = `${summary.fake_percentage}%`;

        // Render Feed & Charts
        renderFilterCounts(data.reviews);
        renderReviewsFeed(data.reviews, 'all');
        renderCharts(summary, data.reviews);
    }

    // 5. Reviews Feed & Filtering
    function renderFilterCounts(reviews) {
        filterAllCount.textContent = reviews.length;
        filterRealCount.textContent = reviews.filter(r => !r.is_fake).length;
        filterFakeCount.textContent = reviews.filter(r => r.is_fake).length;
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filterType = btn.getAttribute('data-filter');
            if (currentAnalysisData) {
                renderReviewsFeed(currentAnalysisData.reviews, filterType);
            }
        });
    });

    function renderReviewsFeed(reviews, filter = 'all') {
        reviewsList.innerHTML = '';

        let filtered = reviews;
        if (filter === 'real') filtered = reviews.filter(r => !r.is_fake);
        if (filter === 'fake') filtered = reviews.filter(r => r.is_fake);

        if (filtered.length === 0) {
            reviewsList.innerHTML = `<div class="empty-feed">No reviews match the selected filter.</div>`;
            return;
        }

        filtered.forEach(r => {
            const card = document.createElement('div');
            card.className = `review-item card ${r.is_fake ? 'fake-border' : 'real-border'}`;

            const badgeClass = r.is_fake ? 'badge-fake' : 'badge-real';
            const badgeText = r.is_fake ? `FAKE REVIEW (${r.confidence}%)` : `REAL REVIEW (${r.confidence}%)`;
            const icon = r.is_fake ? 'fa-triangle-exclamation' : 'fa-circle-check';

            let flagsHtml = '';
            if (r.flags && r.flags.length > 0) {
                flagsHtml = `<div class="flags-container">` +
                    r.flags.map(f => `<span class="flag-pill"><i class="fa-solid fa-flag"></i> ${f}</span>`).join('') +
                    `</div>`;
            }

            card.innerHTML = `
                <div class="review-header">
                    <div class="author-info">
                        <i class="fa-solid fa-user-circle"></i>
                        <span class="author-name">${r.author || 'Flipkart Buyer'}</span>
                        <span class="rating-stars">${'★'.repeat(r.rating || 5)}</span>
                    </div>
                    <div class="prediction-badge ${badgeClass}">
                        <i class="fa-solid ${icon}"></i> ${badgeText}
                    </div>
                </div>
                <div class="review-body">
                    <p>"${r.text}"</p>
                </div>
                ${flagsHtml}
            `;
            reviewsList.appendChild(card);
        });
    }

    // 6. Chart.js Graphs
    function renderCharts(summary, reviews) {
        // Pie Chart
        const ctxPie = document.getElementById('pieChart').getContext('2d');
        if (pieChartInstance) pieChartInstance.destroy();

        pieChartInstance = new Chart(ctxPie, {
            type: 'doughnut',
            data: {
                labels: ['Real Reviews', 'Fake Reviews'],
                datasets: [{
                    data: [summary.real_count, summary.fake_count],
                    backgroundColor: ['#10b981', '#ef4444'],
                    borderColor: '#1e293b',
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: '#f8fafc', font: { family: 'Outfit' } } }
                }
            }
        });

        // Bar Chart (Rating Breakdown)
        const ratingCountsReal = [0, 0, 0, 0, 0];
        const ratingCountsFake = [0, 0, 0, 0, 0];

        reviews.forEach(r => {
            const idx = Math.min(Math.max((r.rating || 5) - 1, 0), 4);
            if (r.is_fake) ratingCountsFake[idx]++;
            else ratingCountsReal[idx]++;
        });

        const ctxBar = document.getElementById('barChart').getContext('2d');
        if (barChartInstance) barChartInstance.destroy();

        barChartInstance = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
                datasets: [
                    {
                        label: 'Real',
                        data: ratingCountsReal,
                        backgroundColor: '#10b981'
                    },
                    {
                        label: 'Fake',
                        data: ratingCountsFake,
                        backgroundColor: '#ef4444'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                },
                plugins: {
                    legend: { labels: { color: '#f8fafc', font: { family: 'Outfit' } } }
                }
            }
        });
    }

    // 7. Benchmark Modal Logic
    btnModelMetrics.addEventListener('click', () => {
        fetch('/api/models')
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    renderMetricsTable(data.metrics);
                    metricsModal.classList.remove('hidden');
                }
            });
    });

    btnCloseModal.addEventListener('click', () => {
        metricsModal.classList.add('hidden');
    });

    function renderMetricsTable(metrics) {
        metricsTbody.innerHTML = '';
        Object.keys(metrics).forEach(mName => {
            const m = metrics[mName];
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td><strong>${mName}</strong></td>
                <td><span class="badge-acc">${(m.accuracy * 100).toFixed(2)}%</span></td>
                <td><span class="badge-f1">${(m.f1_score * 100).toFixed(2)}%</span></td>
                <td>${m.word_only ? 'TF-IDF Word Matrix' : 'TF-IDF Word + Char + Scaled Metadata'}</td>
            `;
            metricsTbody.appendChild(tr);
        });
    }

    // Helpers
    function showLoading(msg) {
        loadingText.textContent = msg;
        loadingOverlay.classList.remove('hidden');
        resultsSection.classList.add('hidden');
    }

    function hideLoading() {
        loadingOverlay.classList.add('hidden');
    }
});
