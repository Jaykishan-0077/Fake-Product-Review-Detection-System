import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure output directory exists
output_dir = "/Users/jk/Desktop/flipkart_fake_review_detector/report_images"
os.makedirs(output_dir, exist_ok=True)

# Set global matplotlib parameters for clean academic typography
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# ==========================================
# 1. FIG 1.1: AGILE DEVELOPMENT LIFECYCLE
# ==========================================
def create_agile_flowchart():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title
    ax.text(5, 8.5, "Agile Software Development Lifecycle Flowchart", 
            fontsize=15, fontweight='bold', ha='center', color='#0f172a')

    steps = [
        ("1. Requirement Analysis & Dataset Acquisition\n(40,432 Reviews Curation, Kaggle Dataset Setup)", "#e0f2fe", "#0284c7"),
        ("2. NLP Feature Engineering & Text Preprocessing\n(TF-IDF Word/Char Matrices + 7 Scaled Metadata)", "#e0e7ff", "#4f46e5"),
        ("3. Multi-Model Training & Benchmarking\n(PyTorch BiLSTM, Linear SVM, LogReg, Naive Bayes)", "#fef3c7", "#d97706"),
        ("4. Flask REST API & Parse.bot Live Scraper Gateway\n(In-Memory URL_CACHE Hash Table, /api Endpoints)", "#dcfce7", "#16a34a"),
        ("5. Responsive Glassmorphism Dashboard UI & Analytics\n(Chart.js Visualizations, Trust Score Ring, Filters)", "#f3e8ff", "#9333ea"),
        ("6. Integration Testing (18 Test Cases) & Mobile Audit\n(Security Validation, Cross-Device Touch Testing)", "#ffe4e6", "#e11d48"),
        ("7. Cloud Deployment (Render.com) & Keep-Alive Monitoring\n(UptimeRobot 5-Min Pings, Production Readiness)", "#ccfbf1", "#0d9488")
    ]

    y_start = 7.4
    box_height = 0.75
    gap = 0.3

    for i, (text, bg_color, border_color) in enumerate(steps):
        y = y_start - i * (box_height + gap)
        
        # Rounded box
        rect = patches.FancyBboxPatch((1.2, y), 7.6, box_height,
                                      boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor=bg_color, edgecolor=border_color, linewidth=2.0)
        ax.add_patch(rect)
        ax.text(5, y + box_height/2, text, fontsize=10.5, fontweight='bold', ha='center', va='center', color='#1e293b')

        # Arrow down
        if i < len(steps) - 1:
            ax.annotate('', xy=(5, y - 0.05), xytext=(5, y + 0.05),
                        arrowprops=dict(arrowstyle="->", color="#475569", lw=2, mutation_scale=15))

    plt.tight_layout()
    save_path = os.path.join(output_dir, "fig_1_1_agile_lifecycle.png")
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Created {save_path}")

# ==========================================
# 2. FIG 2.1: DATA PIPELINE FLOWCHART
# ==========================================
def create_data_pipeline_flowchart():
    fig, ax = plt.subplots(figsize=(10, 11), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    ax.text(5, 11.5, "Activity Diagram of the Data Pipeline Process", 
            fontsize=15, fontweight='bold', ha='center', color='#0f172a')

    # Start pill
    start_pill = patches.FancyBboxPatch((4.0, 10.6), 2.0, 0.5, boxstyle="round,pad=0.1,rounding_size=0.25",
                                        facecolor="#0f172a", edgecolor="#0f172a")
    ax.add_patch(start_pill)
    ax.text(5, 10.85, "START", fontsize=11, fontweight='bold', ha='center', va='center', color="#ffffff")

    pipeline_steps = [
        ("1. Input Acquisition (Parse.bot Live Scraping / Bulk Paste Text)", "#f8fafc", "#3b82f6"),
        ("2. Input Validation (Domain: flipkart.com | Path: /p/ or pid=)", "#f8fafc", "#3b82f6"),
        ("3. Text Preprocessing (Lowercasing, Regex Cleaning, URL/HTML Stripping)", "#f8fafc", "#3b82f6"),
        ("4. Feature Engineering (TF-IDF Word 1-2 N-Grams + Char 2-4 N-Grams)", "#f8fafc", "#3b82f6"),
        ("5. Metadata Extraction (Caps Ratio, Exclamation Density, Unique Ratio)", "#f8fafc", "#3b82f6"),
        ("6. StandardScaler Scaling (Standardized Metadata Alignment)", "#f8fafc", "#3b82f6"),
        ("7. Model Matrix Inference (PyTorch BiLSTM / Linear SVM / LogReg / NB)", "#fef3c7", "#f59e0b"),
        ("8. Suspicion Flag Evaluation (Excessive Caps, Exclamations, Promo Phrases)", "#fee2e2", "#ef4444"),
        ("9. Trust Index Calculation: (Real Reviews / Total Reviews) * 100%", "#dcfce7", "#10b981"),
        ("10. Visual Output Generation (Dashboard Render, SVG Ring, Chart.js)", "#e0e7ff", "#6366f1")
    ]

    y_pos = 9.8
    box_h = 0.55
    gap = 0.35

    # Connect start to step 1
    ax.annotate('', xy=(5, y_pos + box_h), xytext=(5, 10.55),
                arrowprops=dict(arrowstyle="->", color="#475569", lw=2, mutation_scale=15))

    for i, (text, bg_color, border_color) in enumerate(pipeline_steps):
        y = y_pos - i * (box_h + gap)
        rect = patches.FancyBboxPatch((1.0, y), 8.0, box_h,
                                      boxstyle="round,pad=0.1,rounding_size=0.12",
                                      facecolor=bg_color, edgecolor=border_color, linewidth=2.0)
        ax.add_patch(rect)
        ax.text(5, y + box_h/2, text, fontsize=10, fontweight='bold', ha='center', va='center', color="#1e293b")

        if i < len(pipeline_steps) - 1:
            ax.annotate('', xy=(5, y - gap + 0.05), xytext=(5, y),
                        arrowprops=dict(arrowstyle="->", color="#475569", lw=2, mutation_scale=15))

    # End pill
    end_y = y_pos - len(pipeline_steps) * (box_h + gap) + 0.2
    ax.annotate('', xy=(5, end_y + 0.55), xytext=(5, end_y + 0.85),
                arrowprops=dict(arrowstyle="->", color="#475569", lw=2, mutation_scale=15))
    end_pill = patches.FancyBboxPatch((4.0, end_y), 2.0, 0.5, boxstyle="round,pad=0.1,rounding_size=0.25",
                                      facecolor="#0f172a", edgecolor="#0f172a")
    ax.add_patch(end_pill)
    ax.text(5, end_y + 0.25, "END", fontsize=11, fontweight='bold', ha='center', va='center', color="#ffffff")

    plt.tight_layout()
    save_path = os.path.join(output_dir, "fig_2_1_data_pipeline.png")
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Created {save_path}")

# ==========================================
# 3. FIG 3.1: SYSTEM ARCHITECTURE DIAGRAM
# ==========================================
def create_system_architecture_diagram():
    fig, ax = plt.subplots(figsize=(11, 9), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(5.5, 8.5, "TrustGuard System Architecture Diagram (3-Tier MVC Pattern)", 
            fontsize=15, fontweight='bold', ha='center', color='#0f172a')

    # Tier 1: Presentation Tier
    tier1 = patches.FancyBboxPatch((0.5, 6.4), 10.0, 1.4, boxstyle="round,pad=0.1,rounding_size=0.15",
                                   facecolor="#f0fdf4", edgecolor="#22c55e", linewidth=2.0)
    ax.add_patch(tier1)
    ax.text(0.8, 7.5, "PRESENTATION TIER (View Layer - HTML5, CSS3, Vanilla JS, Chart.js)", 
            fontsize=11, fontweight='bold', color="#15803d")
    ax.text(5.5, 6.9, "• Single-Page Glassmorphic Dashboard  • Multi-Tab Input (URL, Bulk, Single)  • Trust Score Ring (SVG)\n• Chart.js Authenticity Doughnut & Rating Bar Charts  • Filterable Review Feed  • Benchmark Modal", 
            fontsize=9.5, ha='center', va='center', color="#1e293b")

    # Arrow 1 to 2
    ax.annotate('HTTP JSON REST Requests (POST /api/analyze-*)', xy=(5.5, 5.7), xytext=(5.5, 6.3),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2, mutation_scale=15),
                ha='center', fontsize=9, fontweight='bold', color="#0369a1")

    # Tier 2: Application Tier
    tier2 = patches.FancyBboxPatch((0.5, 3.8), 10.0, 1.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                   facecolor="#eff6ff", edgecolor="#3b82f6", linewidth=2.0)
    ax.add_patch(tier2)
    ax.text(0.8, 5.3, "APPLICATION TIER (Controller Layer - Flask REST Server app.py)", 
            fontsize=11, fontweight='bold', color="#1d4ed8")

    # Sub-boxes in Application Tier
    box_app1 = patches.FancyBboxPatch((0.8, 4.0), 4.4, 1.1, boxstyle="round,pad=0.1,rounding_size=0.1",
                                      facecolor="#ffffff", edgecolor="#93c5fd", linewidth=1.5)
    ax.add_patch(box_app1)
    ax.text(3.0, 4.7, "Live Scraper Gateway (scraper.py)", fontsize=10, fontweight='bold', ha='center', color="#1e40af")
    ax.text(3.0, 4.3, "• Parse.bot API Client (30 Reviews)\n• URL_CACHE In-Memory Lookup", fontsize=8.5, ha='center', color="#334155")

    box_app2 = patches.FancyBboxPatch((5.8, 4.0), 4.4, 1.1, boxstyle="round,pad=0.1,rounding_size=0.1",
                                      facecolor="#ffffff", edgecolor="#93c5fd", linewidth=1.5)
    ax.add_patch(box_app2)
    ax.text(8.0, 4.7, "NLP & Classifier Engine (model.py)", fontsize=10, fontweight='bold', ha='center', color="#1e40af")
    ax.text(8.0, 4.3, "• TF-IDF Vectorizer (25,000 N-Grams)\n• Suspicion Flag Evaluator (<0.02s)", fontsize=8.5, ha='center', color="#334155")

    # Arrow 2 to 3
    ax.annotate('Loads Pre-Trained Weights & Vectorizer Vocabularies into RAM', xy=(5.5, 3.0), xytext=(5.5, 3.7),
                arrowprops=dict(arrowstyle="->", color="#6366f1", lw=2, mutation_scale=15),
                ha='center', fontsize=9, fontweight='bold', color="#4338ca")

    # Tier 3: Data Tier
    tier3 = patches.FancyBboxPatch((0.5, 0.8), 10.0, 2.0, boxstyle="round,pad=0.1,rounding_size=0.15",
                                   facecolor="#faf5ff", edgecolor="#a855f7", linewidth=2.0)
    ax.add_patch(tier3)
    ax.text(0.8, 2.5, "DATA TIER (Model & Storage Layer - Serialized Artifacts & Datasets)", 
            fontsize=11, fontweight='bold', color="#7e22ce")

    # Sub-boxes in Data Tier
    d_box1 = patches.FancyBboxPatch((0.8, 1.0), 3.0, 1.2, boxstyle="round,pad=0.1,rounding_size=0.1",
                                    facecolor="#ffffff", edgecolor="#d8b4fe", linewidth=1.5)
    ax.add_patch(d_box1)
    ax.text(2.3, 1.8, "Trained ML/DL Models", fontsize=9.5, fontweight='bold', ha='center', color="#6b21a8")
    ax.text(2.3, 1.3, "• PyTorch BiLSTM (96.40%)\n• Linear SVM (95.70%)\n• LogReg & Naive Bayes", fontsize=8.5, ha='center', color="#475569")

    d_box2 = patches.FancyBboxPatch((4.0, 1.0), 3.0, 1.2, boxstyle="round,pad=0.1,rounding_size=0.1",
                                    facecolor="#ffffff", edgecolor="#d8b4fe", linewidth=1.5)
    ax.add_patch(d_box2)
    ax.text(5.5, 1.8, "NLP Vectorizers & Scaler", fontsize=9.5, fontweight='bold', ha='center', color="#6b21a8")
    ax.text(5.5, 1.3, "• tfidf_word.pkl (15k Vocab)\n• tfidf_char.pkl (10k Vocab)\n• scaler.pkl (StandardScaler)", fontsize=8.5, ha='center', color="#475569")

    d_box3 = patches.FancyBboxPatch((7.2, 1.0), 3.0, 1.2, boxstyle="round,pad=0.1,rounding_size=0.1",
                                    facecolor="#ffffff", edgecolor="#d8b4fe", linewidth=1.5)
    ax.add_patch(d_box3)
    ax.text(8.7, 1.8, "Training Datasets", fontsize=9.5, fontweight='bold', ha='center', color="#6b21a8")
    ax.text(8.7, 1.3, "• 40,432 Labelled Reviews\n• 50% CG (Fake) / 50% OR (Real)\n• Stratified 80:20 Train/Test", fontsize=8.5, ha='center', color="#475569")

    plt.tight_layout()
    save_path = os.path.join(output_dir, "fig_3_1_system_architecture.png")
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Created {save_path}")

# ==========================================
# 4. FIG 3.4: PyTorch BiLSTM NEURAL NETWORK ARCHITECTURE
# ==========================================
def create_bilstm_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(5, 8.5, "PyTorch BiLSTM Deep Learning Neural Network Architecture", 
            fontsize=14, fontweight='bold', ha='center', color='#0f172a')

    layers = [
        ("Input Layer: Raw Review Word Token Integer Sequence (Max Length = 120 Tokens)", "#f8fafc", "#64748b"),
        ("Embedding Layer: nn.Embedding(num_embeddings=20,000, embedding_dim=128, padding_idx=0)", "#e0f2fe", "#0284c7"),
        ("Bidirectional LSTM: nn.LSTM(input_size=128, hidden_size=64, bidirectional=True)\n[Forward LSTM (64) + Backward LSTM (64) -> 128-dim Concatenated Output]", "#e0e7ff", "#4f46e5"),
        ("Temporal Mean Pooling: torch.mean(lstm_out, dim=1) -> Sequence Reduction to (Batch, 128)", "#fef3c7", "#d97706"),
        ("Dense Fully-Connected Layer 1: nn.Linear(128, 32) + nn.ReLU() + nn.Dropout(p=0.3)", "#fce7f3", "#db2777"),
        ("Dense Output Layer: nn.Linear(32, 1) + torch.sigmoid() -> Fake Probability P(Fake in [0, 1])", "#dcfce7", "#16a34a")
    ]

    y_pos = 7.4
    box_h = 0.8
    gap = 0.35

    for i, (text, bg_color, border_color) in enumerate(layers):
        y = y_pos - i * (box_h + gap)
        rect = patches.FancyBboxPatch((0.8, y), 8.4, box_h,
                                      boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor=bg_color, edgecolor=border_color, linewidth=2.0)
        ax.add_patch(rect)
        ax.text(5, y + box_h/2, text, fontsize=10, fontweight='bold', ha='center', va='center', color="#1e293b")

        if i < len(layers) - 1:
            ax.annotate('', xy=(5, y - gap + 0.05), xytext=(5, y),
                        arrowprops=dict(arrowstyle="->", color="#334155", lw=2, mutation_scale=15))

    plt.tight_layout()
    save_path = os.path.join(output_dir, "fig_3_4_bilstm_architecture.png")
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Created {save_path}")

# Run all generator functions
create_agile_flowchart()
create_data_pipeline_flowchart()
create_system_architecture_diagram()
create_bilstm_architecture_diagram()
print("All flowchart images generated successfully!")
