# 🛡️ AI Job Scam Detector
### Fake Job Offer Detection System

> **Protecting Indian students and fresh graduates from fraudulent job postings using Machine Learning + Google Gemini AI**

🔗 **Live App:** https://ai-job-scam-detector-kmnbfck73fegfappzrvdxeq.streamlit.app/

🎥 **Demo Video:** https://drive.google.com/file/d/1I_4bfr2ANk_UAi2Uulo5FHrRsrlQQ50w/view?usp=drivesdk

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-red?logo=streamlit)](https://ai-job-scam-detector.streamlit.app)
[![Gemini AI](https://img.shields.io/badge/Google-Gemini%20AI-orange?logo=google)](https://ai.google.dev)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-green?logo=scikit-learn)](https://scikit-learn.org)
[![IBM SkillsBuild](https://img.shields.io/badge/IBM-SkillsBuild%20×%20AICTE-054ada)](https://skillsbuild.org)
[![Deployed on Streamlit](https://img.shields.io/badge/Deployed%20on-Streamlit%20Cloud-FF4B4B?logo=streamlit)](https://ai-job-scam-detector.streamlit.app)

---

## 📋 Table of Contents
- [Problem Statement](#-problem-statement)
- [Proposed Solution](#-proposed-solution)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Model Performance](#-model-performance)
- [Project Structure](#-project-structure)
- [How to Run Locally](#-how-to-run-locally)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [About](#-about)

---

## 🚨 Problem Statement

Every year, thousands of Indian fresh graduates fall victim to fraudulent job postings on platforms like Naukri, LinkedIn, and WhatsApp. Scammers create realistic-looking job listings that:

- **Steal money** through fake registration fees (₹499, ₹999, etc.)
- **Collect sensitive data** — Aadhaar, PAN card, bank account numbers
- **Disappear** after extracting money and personal documents

Fresh graduates with no prior work experience are the most targeted group. According to the EMSCAD dataset, **3.66% of all online job postings are fraudulent** — and with no easy tool to verify job authenticity, students have no protection.

---

## 💡 Proposed Solution

An AI-powered web application that analyzes any job posting text and detects whether it is fraudulent — with a clear explanation of why.

**How it works:**
```
User pastes job posting → ML model detects fraud probability 
→ 🟢🟡🔴 Risk Level displayed → Gemini AI explains red flags 
→ Safety checklist + action advice provided
```

---

## ✨ Features

| Tab | Feature | Description |
|-----|---------|-------------|
| 🔍 | **Job Text Analyzer** | Paste any job posting → ML model gives Real/Fake prediction with confidence % and 🟢🟡🔴 risk level |
| 📧 | **Email & Offer Letter Scanner** | Upload screenshot of job email, offer letter, or WhatsApp message → Gemini Vision analyzes for scam indicators |
| 🏢 | **Company Reputation Checker** | Enter company name or recruiter email → AI provides step-by-step verification guidance |
| 📖 | **Sample Postings** | Pre-loaded fake and real job examples to test the system |
| 📊 | **How It Works** | Technical explanation of the ML pipeline and AI layer |
| 📚 | **Scam Safety Guide** | Complete guide on common scam types, red flag phrases, and how to report in India |

**Additional features:**
- 🔴🟡🟢 **Risk Meter** — HIGH / MEDIUM / LOW based on fraud probability
- 🧠 **AI Red Flag Extractor** — Gemini identifies specific suspicious phrases
- 📧 **Recruiter Email Analyzer** — Flags Gmail/Yahoo as suspicious, validates company domains
- 📋 **Automated Safety Checklist** — Generated per posting based on inputs
- 🔢 **Persistent Scan Counter** — Tracks total scans across sessions

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit (Python) |
| ML Model | Logistic Regression with `class_weight='balanced'` |
| NLP / Text Features | TF-IDF Vectorization (5,000 features) + NLTK |
| AI Explanation | Google Gemini 2.5 Flash API |
| Image Analysis | Gemini Vision API + Pillow (PIL) |
| Dataset | EMSCAD — Employment Scam Aegean Dataset (Kaggle) |
| Deployment | VS Code (local) + Streamlit Cloud (permanent public URL) |

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Overall Accuracy | **97.7%** |
| Fraud Detection Recall | **88%** |
| Precision (Fake jobs) | 64% |
| F1 Score (Fake jobs) | 0.74 |
| False Negatives | Only **13** per 104 fake jobs |

**Confusion Matrix:**
```
                Predicted Real   Predicted Fake
Actual Real         2,667              51
Actual Fake            13              91
```

**Why Logistic Regression?**  
Fast, highly interpretable, and performs exceptionally well on high-dimensional sparse TF-IDF vectors — ideal for this text classification task.

---

## 📁 Project Structure

```
AI-Job-Scam-Detector/
│
├── app/
│   ├── app.py                    # Main Streamlit application (6 tabs)
│   └── scan_counter.json         # Persistent scan count (auto-created)
│
├── models/                       # Trained ML model files (add locally)
│   ├── job_scam_detector.pkl     # Logistic Regression model
│   └── tfidf_vectorizer.pkl      # TF-IDF vectorizer
│
├── notebooks/
│   └── 01_Data_Exploration.ipynb # EDA + preprocessing + model training
│
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

> **Note:** The `.pkl` model files are not included in the repository for size reasons. Run the training notebook `01_Data_Exploration.ipynb` to generate them, or download from the releases section.

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.8 or above
- A free Google Gemini API key from [aistudio.google.com](https://aistudio.google.com)

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/palakkhandelwal22/AI-Job-Scam-Detector.git
cd AI-Job-Scam-Detector
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your API key**

Create a `.env` file in the `app/` folder:
```
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

**4. Add model files**

Place `job_scam_detector.pkl` and `tfidf_vectorizer.pkl` in the `app/` folder  
(Generate them by running `notebooks/01_Data_Exploration.ipynb`)

**5. Run the app**
```bash
cd app
streamlit run app.py
```

App opens at **http://localhost:8501**

---

## ☁️ Deployment

### 🌐 Streamlit Cloud (Live — Permanent URL)

The app is deployed on **Streamlit Cloud** and is accessible 24/7 at:

**🔗 https://ai-job-scam-detector-kmnbfck73fegfappzrvdxeq.streamlit.app/

**How it was deployed:**
1. Pushed code to this GitHub repository
2. Went to [share.streamlit.io](https://share.streamlit.io) → New app → Selected this repo
3. Set main file path to `app/app.py`
4. Added Gemini API key under **Settings → Secrets**:
   ```
   GOOGLE_API_KEY = "your_key_here"
   ```
5. Clicked **Deploy** — live in under 2 minutes

### 💻 Google Colab + Localtunnel (Alternative)

A Colab deployment notebook is also included for reference.
See `notebooks/Deployment.ipynb`

```python
# Run in Google Colab
!pip install streamlit google-generativeai nltk scikit-learn Pillow -q
!npm install localtunnel
!streamlit run app.py &>/content/logs.txt & npx localtunnel --port 8501
```

This generates a temporary public URL like `https://abc-xyz.loca.lt` (active while Colab session is running).

---

## 🔑 API Key Management

- The Gemini API key is **never stored** in this repository
- **Local use:** store in a `.env` file in the `app/` folder (`.env` is in `.gitignore`)
  ```
  GOOGLE_API_KEY=your_actual_gemini_api_key_here
  ```
- **Streamlit Cloud:** added via **Settings → Secrets** on share.streamlit.io
  ```
  GOOGLE_API_KEY = "your_actual_gemini_api_key_here"
  ```
- **Colab deployment:** paste key directly in the notebook cell (notebook not pushed to GitHub)
- **Free tier:** Gemini API is free — if quota runs out, get a new free key from [aistudio.google.com](https://aistudio.google.com) and update it in Streamlit Cloud secrets

---

## 📸 Screenshots

### 🏠 Homepage
![Homepage](screenshots/homepage.png.jpeg)
---

### 🚨 Fake Job Detection

#### Job Input
![Fake Job Input](screenshots/fake_job_input.png.jpeg)
#### Detection Result 
![Fake Job Result 1](screenshots/fake_job_result1.png.jpeg)

![Fake Job Result 2](screenshots/fake_job_result2.png.jpeg)

#### Warning Analysis
![Fake Job Warning](screenshots/fake_job_warning.png.jpeg)
---

### ✅ Legitimate Job Detection

#### Real Job Input
![Real Job Input](screenshots/real_job_input.png.jpeg)
#### Result – Part 1
![Real Job Result 1](screenshots/real_job_result1.png.jpeg)

![Real Job Result 2](screenshots/real_job_result2.png.jpeg)

#### Safety Recommendations
![Real Job Safety](screenshots/real_job_safety.png.jpeg)
---

### 📧 Email & Screenshot Scanner

#### Upload Email Screenshot
![Email Upload 1](screenshots/email_upload1.png.jpeg)

![Email Upload 2](screenshots/email_upload2.png.jpeg)

#### AI Analysis Results
![Email Result 1](screenshots/email_result1.png.jpeg)

![Email Result 2](screenshots/email_result2.png.jpeg)
---

### 📄 Offer Letter Verification

#### Upload Offer Letter

![Offer Letter Upload 1](screenshots/offerletter1_upload.png.jpeg)

![Offer Letter Upload 2](screenshots/offerletter2_upload.png.jpeg)

#### Verification Results

![Offer Letter Result 1](screenshots/offerletter_result1.png.jpeg)

![Offer Letter Result 2](screenshots/offerletter_result2.png.jpeg)
---

### 🏢 Company Reputation Checker

#### Company Search
![Company Input](screenshots/company_input.png.jpeg)
#### Analysis Results
![Company Result 1](screenshots/company_result1.png.jpeg)

![Company Result 2](screenshots/company_result2.png.jpeg)

![Company Result 3](screenshots/company_result3.png.jpeg)

![Company Result 4](screenshots/company_result4.png.jpeg)

---

### 🧪 Sample Testing

#### Fake Sample Job
![Sample Fake Job 1](screenshots/samplefakejob1.png.jpeg)
![Sample Fake Job 2](screenshots/samplefakejob2.png.jpeg)

#### Real Sample Job
![Sample Real Job 1](screenshots/samplerealjob1.png.jpeg)
![Sample Real Job 2](screenshots/samplerealjob2.png.jpeg)

## 🎓 About

**Project:** IBM SkillsBuild × AICTE Artificial Intelligence Internship 2026 — Capstone Project

**Student:** Palak Khandelwal  
**GitHub:** [@palakkhandelwal22](https://github.com/palakkhandelwal22)

**Social Impact:** This project directly addresses the growing problem of job scams in India, helping thousands of fresh graduates make safer decisions when applying for jobs online.

---

## 📚 References

- EMSCAD Dataset: [kaggle.com/datasets/amruthjithrajvr/recruitment-scam](https://www.kaggle.com/datasets/amruthjithrajvr/recruitment-scam)
- Scikit-learn: [scikit-learn.org](https://scikit-learn.org)
- Google Gemini API: [ai.google.dev](https://ai.google.dev)
- NLTK: [nltk.org](https://nltk.org)
- Streamlit: [docs.streamlit.io](https://docs.streamlit.io)
- Report Cyber Crime: [cybercrime.gov.in](https://cybercrime.gov.in) | Helpline: **1930**
