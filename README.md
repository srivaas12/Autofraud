#  Credit Card Fraud Detection

**Author:** Srivaas

A machine learning-based system to detect fraudulent credit card transactions using Logistic Regression and Random Forest.

---

##  Overview

Fraudulent transactions are rare and hard to detect. This project builds an ML model to accurately identify fraud while minimizing false positives.

---

##  Dataset

| Feature | Description |
|---------|-------------|
| `distance_from_home` | Distance from cardholder's home |
| `distance_from_last_transaction` | Distance from previous transaction |
| `ratio_to_median_purchase_price` | Ratio of transaction to median price |
| `repeat_retailer` | Repeat retailer (1: Yes, 0: No) |
| `used_chip` | Chip used (1: Yes, 0: No) |
| `used_pin_number` | PIN used (1: Yes, 0: No) |
| `online_order` | Online order (1: Yes, 0: No) |
| `fraud` | Target variable (1: Fraud, 0: Legit) |

---

##  Workflow

1. **Data Preprocessing** — Missing value handling, outlier capping (IQR method)
2. **EDA** — Correlation heatmap, class distribution analysis
3. **Feature Engineering** — Distance ratio, transaction risk score, purchase categories
4. **Modeling** — Logistic Regression & Random Forest
5. **Deployment** — Streamlit web app

---

##  Model Results

| Metric | Logistic Regression | Random Forest |
|--------|-------------------|---------------|
| **Accuracy** | 91.65% | **94.27%** |
| **Precision (Fraud)** | 0.51 | **0.60** |
| **Recall (Fraud)** | 0.94 | **0.99** |
| **F1-Score (Fraud)** | 0.66 | **0.75** |

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/srivaas12/Autofraud.git
cd Autofraud

# 
