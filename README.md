# 🧠 Aave Credit Scoring System

This project builds a machine learning system to assign credit scores (0–1000) to DeFi wallets based on their transaction behavior on the Aave V2 protocol.

---

## 🎯 Problem Statement

You are provided with 100K raw transaction records from the Aave V2 protocol. Each record corresponds to a wallet interacting with the protocol through actions such as:

- `deposit`
- `borrow`
- `repay`
- `redeemunderlying`
- `liquidationcall`

The objective is to assign each wallet a **credit score between 0 and 1000** based on its behavioral data — where:

- **Higher scores** → Reliable, responsible DeFi usage  
- **Lower scores** → Risky, bot-like, or exploitative usage

---

## 📁 Project Structure

aave-credit-scoring/
├── data/ # Raw data (JSON)
├── src/ # Core scripts
│ ├── preprocess.py
│ ├── feature_engineering.py
│ ├── model.py
│ └── score.py
├── notebooks/ # EDA and analysis notebooks
├── output/ # Results (e.g., wallet_scores.csv)
├── README.md # Project documentation
├── analysis.md # Score interpretation and insights
├── requirements.txt # Python dependencies
└── .gitignore # Files and folders to ignore in version control


---

## ⚙️ Setup Instructions

### Step 1: Clone the Repository

``bash
git clone https://github.com/cesardushime/aave-credit-scoring.git

cd aave-credit-scoring

### Step 2: Create and Activate Virtual Environment (Windows)

python -m venv venv
venv\Scripts\activate

### Step 3: Install Dependencies
bash
Copy code
pip install -r requirements.txt
🚀 Usage
To generate wallet credit scores:

python src/score.py --input data/user_transactions.json --output output/wallet_scores.csv

📊 Deliverables
✅ README.md: Project overview and instructions

✅ analysis.md: Score distribution and behavioral insights

✅ Python script: Loads JSON and generates credit scores

✅ CSV output: File with wallet_address, score for each wallet

📈 Potential Features (Coming Soon)
Feature importance visualization

Model tuning for better score calibration

