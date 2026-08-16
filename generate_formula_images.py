import os
import matplotlib.pyplot as plt

formula_dir = "/Users/jk/Desktop/flipkart_fake_review_detector/report_images/formulas"
os.makedirs(formula_dir, exist_ok=True)

plt.rcParams['mathtext.fontset'] = 'cm' # Computer Modern (Standard LaTeX font)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

def render_equation_card(eq_title, eq_latex_lines, filename, figsize=(9.5, 1.8), fontsize=13):
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    ax.axis('off')
    
    # Background card with subtle border
    fig.patch.set_facecolor('#f8fafc')
    fig.patch.set_edgecolor('#cbd5e1')
    fig.patch.set_linewidth(1.5)
    
    # Title
    ax.text(0.5, 0.88, f"[{eq_title}]", fontsize=11, fontweight='bold', 
            ha='center', va='center', color='#1e3a8a')
    
    # Formula lines
    y_pos = 0.45 if len(eq_latex_lines) == 1 else 0.5
    if len(eq_latex_lines) == 1:
        ax.text(0.5, 0.38, eq_latex_lines[0], fontsize=fontsize, ha='center', va='center', color='#0f172a')
    else:
        line_gap = 0.7 / (len(eq_latex_lines))
        for idx, line in enumerate(eq_latex_lines):
            y = 0.72 - idx * line_gap
            ax.text(0.5, y, line, fontsize=fontsize, ha='center', va='center', color='#0f172a')

    out_path = os.path.join(formula_dir, filename)
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.12, dpi=300, facecolor=fig.get_facecolor(), edgecolor=fig.get_edgecolor())
    plt.close()
    print(f"Rendered: {out_path}")

# ==========================================
# 1. Formula 1: TF-IDF
# ==========================================
render_equation_card(
    "Formula 1: Term Frequency - Inverse Document Frequency (TF-IDF)",
    [r"$\mathrm{TF\text{-}IDF}(t, d, D) = \mathrm{TF}(t, d) \times \left[ \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1 \right]$"],
    "formula_1_tfidf.png",
    figsize=(9.2, 1.5),
    fontsize=13.5
)

# ==========================================
# 2. Formula 2: Z-Score Normalization
# ==========================================
render_equation_card(
    "Formula 2: StandardScaler Z-Score Normalization",
    [r"$z = \frac{x - \mu}{\sigma}, \quad \text{where } \mu = \frac{1}{N}\sum_{i=1}^N x_i, \quad \sigma = \sqrt{\frac{1}{N}\sum_{i=1}^N (x_i - \mu)^2}$"],
    "formula_2_zscore.png",
    figsize=(9.2, 1.5),
    fontsize=13
)

# ==========================================
# 3. Formula 3: Linear SVM Objective & Sigmoid Mapping
# ==========================================
render_equation_card(
    "Formula 3: Linear SVM Objective & Calibrated Sigmoidal Distance Mapping",
    [
        r"$\min_{w,b} \; \frac{1}{2} \|w\|^2 + C \sum_{i=1}^N \max\left(0, \, 1 - y_i(w^T x_i + b)\right)$",
        r"$P(\mathrm{Fake} \mid X) = \frac{1}{1 + \exp\left(-1.2 \cdot (w^T X + b)\right)}$"
    ],
    "formula_3_svm.png",
    figsize=(9.5, 2.2),
    fontsize=12.5
)

# ==========================================
# 4. Formula 4: PyTorch Bi-directional LSTM Cell Equations
# ==========================================
render_equation_card(
    "Formula 4: PyTorch Bi-directional LSTM (BiLSTM) Gated Neural Equations",
    [
        r"$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) \quad \text{[Forget Gate]}, \quad i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) \quad \text{[Input Gate]}$",
        r"$\tilde{C}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c), \quad C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t \quad \text{[Cell State Update]}$",
        r"$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) \quad \text{[Output Gate]}, \quad h_t = o_t \odot \tanh(C_t) \quad \text{[Hidden Output]}$",
        r"$h_{\mathrm{BiLSTM}} = [h_{\mathrm{forward}} \, ; \, h_{\mathrm{backward}}], \quad P(\mathrm{Fake} \mid X) = \sigma(W_2 \cdot \mathrm{ReLU}(W_1 \cdot \mathrm{MeanPool}(h_{\mathrm{BiLSTM}})))$"
    ],
    "formula_4_bilstm.png",
    figsize=(10.0, 3.4),
    fontsize=11.5
)

# ==========================================
# 5. Formula 5: Product Trust Index Percentage
# ==========================================
render_equation_card(
    "Formula 5: Product Trust Index Percentage Score",
    [r"$\mathrm{Trust\ Index\ (\%)} = \left[ \frac{\mathrm{Count(REAL\ Reviews)}}{\mathrm{Total\ Reviews\ Analyzed}} \right] \times 100\%$"],
    "formula_5_trust_index.png",
    figsize=(8.8, 1.5),
    fontsize=13.5
)

# ==========================================
# 6. Formula 6: Classification Performance Metrics
# ==========================================
render_equation_card(
    "Formula 6: Binary Classification Performance Evaluation Metrics",
    [
        r"$\mathrm{Accuracy} = \frac{\mathrm{TP} + \mathrm{TN}}{\mathrm{TP} + \mathrm{TN} + \mathrm{FP} + \mathrm{FN}}, \qquad \mathrm{Precision} = \frac{\mathrm{TP}}{\mathrm{TP} + \mathrm{FP}}$",
        r"$\mathrm{Recall} = \frac{\mathrm{TP}}{\mathrm{TP} + \mathrm{FN}}, \qquad F_1 = 2 \times \frac{\mathrm{Precision} \times \mathrm{Recall}}{\mathrm{Precision} + \mathrm{Recall}}$"
    ],
    "formula_6_metrics.png",
    figsize=(9.2, 2.2),
    fontsize=12.5
)

print("All 6 formula images generated successfully!")
