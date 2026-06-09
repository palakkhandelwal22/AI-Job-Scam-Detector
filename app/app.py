import streamlit as st
import pickle
import re
import os
import json
import nltk
from nltk.corpus import stopwords
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file (for local VS Code use)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# ── PAGE CONFIG ───────────────────────────────
st.set_page_config(
    page_title="AI Job Scam Detector",
    page_icon="🛡️",
    layout="wide"
)

# ── NLTK ──────────────────────────────────────
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

# ── PERSISTENT SCAN COUNTER ───────────────────
COUNTER_FILE = "scan_counter.json"

def get_total_scans():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            data = json.load(f)
            return data.get("total", 0)
    return 0

def increment_scan_counter():
    total = get_total_scans() + 1
    with open(COUNTER_FILE, "w") as f:
        json.dump({"total": total}, f)
    return total

# ── SESSION STATE ─────────────────────────────
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

# ── LOAD ML MODEL ─────────────────────────────
import os

@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    model_path = os.path.join(base_dir, "..", "models", "job_scam_detector.pkl")
    tfidf_path = os.path.join(base_dir, "..", "models", "tfidf_vectorizer.pkl")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    with open(tfidf_path, "rb") as f:
        tfidf = pickle.load(f)

    return model, tfidf

model, tfidf = load_model()

# ── GEMINI SETUP ──────────────────────────────
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_text(prompt):
    try:
        m = genai.GenerativeModel('gemini-2.5-flash')
        response = m.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI analysis unavailable: {str(e)}"

def get_gemini_vision(prompt, image):
    try:
        m =  genai.GenerativeModel('gemini-2.5-flash')
        response = m.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"⚠️ AI analysis unavailable: {str(e)}"

# ── TEXT CLEANING ─────────────────────────────
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = [w for w in text.split() if w not in stop_words]
    return " ".join(words)

# ── RISK LEVEL ────────────────────────────────
def get_risk_level(fake_conf):
    if fake_conf >= 60:
        return "🔴 HIGH RISK", "red", "This posting has strong indicators of fraud."
    elif fake_conf >= 30:
        return "🟡 MEDIUM RISK", "orange", "This posting has some suspicious elements. Verify carefully."
    else:
        return "🟢 LOW RISK", "green", "This posting appears legitimate. Still verify independently."

# ── SAMPLE POSTINGS ───────────────────────────
SAMPLE_FAKE = """Job Title: Work From Home Data Entry Executive
Company: GlobalEarnings Pvt Ltd

We are hiring 500 freshers URGENTLY. No experience required.
Earn Rs 25,000 to Rs 80,000 per month working just 2-3 hours daily from home.
GUARANTEED income. No targets. Simple copy paste work.

Requirements: Just a smartphone or laptop. No qualifications needed.
Contact us on WhatsApp only: +91-XXXXXXXXXX
Pay Rs 499 registration fee to get your work kit and login credentials.
Limited seats available. Apply in next 24 hours only!"""

SAMPLE_REAL = """Job Title: Junior Software Developer
Company: Infosys BPM Ltd, Bengaluru

Infosys BPM is looking for Junior Developers to join our Digital Services team.

Responsibilities: Develop and maintain web applications using Python and Java.
Work with senior developers on client projects. Write clean, documented code.

Requirements: B.E/B.Tech in Computer Science or related field.
0-2 years experience. Knowledge of Python, SQL, and Git required.
Good communication skills essential.

Salary: 3-5 LPA for freshers as per industry standards.
Benefits: Health insurance, PF, paid leaves, certification support.
Apply at: careers.infosys.com | Process: Online test followed by 2 interview rounds"""

# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/security-shield-green.png",
        width=65
    )
    st.title("AI Job Scam Detector")
    st.markdown("*Protecting graduates from job scams*")

    st.divider()
    st.markdown("### 🚨 Top Scam Warning Signs")
    st.markdown("""
- Registration or processing fees
- Unrealistic salary promises
- No company name or address
- WhatsApp or Gmail contact only
- Apply urgently in 24 hours
- No qualifications needed
- Guaranteed income claims
    """)

    st.divider()
    st.markdown("### 📋 Recent Scans")
    if st.session_state.scan_history:
        for item in st.session_state.scan_history[-5:][::-1]:
            icon = "🔴" if item['result'] == 'HIGH RISK' else ("🟡" if item['result'] == 'MEDIUM RISK' else "🟢")
            st.caption(f"{icon} {item['title'][:22]}...")
    else:
        st.caption("No scans yet.")

    st.divider()
    st.markdown("### 📞 Report Scams")
    st.markdown("**Cyber Crime:** cybercrime.gov.in\n\n**Helpline:** 1930")

# ══════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════
st.title("🛡️ AI Job Scam Detector")
st.markdown("**Protecting Indian students and fresh graduates from fraudulent job offers**")

total_scans = get_total_scans()
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Model Accuracy", "97.7%")
with c2: st.metric("Fraud Detection Rate", "88%")
with c3: st.metric("Jobs Analyzed", "14,107+")
with c4: st.metric("Total Scans Done", total_scans)

st.divider()

# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Analyze Job Posting",
    "📧 Email / Offer Letter Scanner",
    "🏢 Company Checker",
    "📖 Try Samples",
    "📊 How It Works",
    "📚 Scam Safety Guide"
])

# ══════════════════════════════════════════════
# TAB 1 — MAIN ANALYZER
# ══════════════════════════════════════════════
with tab1:
    st.subheader("Paste Any Job Posting to Analyze")

    col1, col2 = st.columns([1, 1])

    with col1:
        job_title = st.text_input(
            "📌 Job Title",
            placeholder="e.g. Data Entry Executive, Software Developer"
        )
        company_profile = st.text_area(
            "🏢 Company Description",
            placeholder="Paste company description here...",
            height=100
        )
        job_description = st.text_area(
            "📋 Job Description *",
            placeholder="Paste the full job description here (most important field)...",
            height=160
        )

    with col2:
        requirements = st.text_area(
            "✅ Requirements",
            placeholder="Paste job requirements...",
            height=100
        )
        benefits = st.text_area(
            "💰 Benefits / Salary",
            placeholder="Paste salary or benefits info...",
            height=80
        )
        recruiter_email = st.text_input(
            "📧 Recruiter Email (optional)",
            placeholder="e.g. hr@company.com or recruiter@gmail.com"
        )
        has_logo = st.selectbox(
            "Company has logo/website?",
            ["Yes", "No", "Not mentioned"]
        )
        employment_type = st.selectbox(
            "Employment Type",
            ["Full-time", "Part-time", "Contract", "Internship", "Not mentioned"]
        )

    st.divider()
    analyze_btn = st.button(
        "🔍 ANALYZE THIS JOB POSTING",
        type="primary",
        use_container_width=True
    )

    if analyze_btn:
        if not job_description.strip():
            st.error("⚠️ Please paste at least the Job Description to analyze.")
        else:
            with st.spinner("🤖 Running ML model analysis..."):
                combined = f"{job_title} {company_profile} {job_description} {requirements} {benefits}"
                cleaned = clean_text(combined)
                vectorized = tfidf.transform([cleaned])
                prediction = model.predict(vectorized)[0]
                probability = model.predict_proba(vectorized)[0]
                fake_conf = probability[1] * 100
                real_conf = probability[0] * 100

            risk_label, risk_color, risk_desc = get_risk_level(fake_conf)

            st.divider()

            # ── RISK METER ──────────────────────────
            st.markdown("## Risk Assessment")

            if fake_conf >= 60:
                st.error(f"## {risk_label}")
                st.error(risk_desc)
            elif fake_conf >= 30:
                st.warning(f"## {risk_label}")
                st.warning(risk_desc)
            else:
                st.success(f"## {risk_label}")
                st.success(risk_desc)

            # Confidence bars
            st.markdown("### Confidence Scores")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**✅ Legitimate Probability**")
                st.progress(real_conf / 100)
                st.metric("", f"{real_conf:.1f}%")
            with c2:
                st.markdown("**⚠️ Fraud Probability**")
                st.progress(fake_conf / 100)
                st.metric("", f"{fake_conf:.1f}%")

            # Update scan counter and history
            new_total = increment_scan_counter()
            title_save = job_title if job_title else job_description[:30]
            result_label = "HIGH RISK" if fake_conf >= 60 else ("MEDIUM RISK" if fake_conf >= 30 else "LOW RISK")
            st.session_state.scan_history.append({
                'title': title_save,
                'result': result_label
            })

            # ── RECRUITER EMAIL CHECK ────────────────
            if recruiter_email.strip():
                st.divider()
                st.markdown("### 📧 Recruiter Email Analysis")
                email_lower = recruiter_email.lower().strip()
                free_domains = ["gmail.com", "yahoo.com", "hotmail.com",
                                "outlook.com", "rediffmail.com", "ymail.com"]
                is_free = any(domain in email_lower for domain in free_domains)

                if is_free:
                    st.error(f"""
**⚠️ Suspicious Email Detected**
- Email uses a free email service: `{recruiter_email}`
- Legitimate companies always use their own domain (e.g., hr@infosys.com)
- A recruiter using Gmail or Yahoo is a major red flag
- Do NOT share personal documents with this contact
                    """)
                else:
                    domain = recruiter_email.split("@")[-1] if "@" in recruiter_email else "unknown"
                    st.success(f"""
**✅ Email Looks Professional**
- Uses company domain: `{domain}`
- This is a positive sign of a legitimate employer
- Still verify by visiting the official company website
                    """)

            st.divider()

            # ── AI RED FLAG EXTRACTOR ────────────────
            with st.spinner("🧠 Extracting red flags with AI..."):
                red_flag_prompt = f"""
You are a job scam expert helping Indian graduates stay safe.

Analyze this job posting and provide EXACTLY this format:

**Detected Red Flags:**
(list each red flag as: ⚠️ [flag name] — [one line explanation])
(if none found, write: ✅ No major red flags detected)

**Positive Signals:**
(list each as: ✅ [signal] — [one line explanation])
(if none found, write: ❌ No positive signals found)

**Specific Risk Factors for Indian Graduates:**
(2-3 bullet points about why this is or is not dangerous specifically for freshers in India)

**Verdict:**
(one clear sentence)

Job Posting:
{combined[:2000]}

ML Result: {'FRAUDULENT' if prediction == 1.0 else 'LEGITIMATE'} ({fake_conf:.1f}% fraud probability)
"""
                red_flag_result = get_gemini_text(red_flag_prompt)

            st.subheader("🧠 AI-Powered Analysis")
            st.markdown(red_flag_result)

            st.divider()

            # ── SAFETY CHECKLIST ─────────────────────
            st.subheader("📋 Safety Checklist")
            checks = {
                "Company description is provided": bool(company_profile.strip()),
                "Job description is detailed (200+ chars)": len(job_description) > 200,
                "Specific requirements are listed": bool(requirements.strip()),
                "No fees or deposits mentioned": (
                    "fee" not in job_description.lower()
                    and "deposit" not in job_description.lower()
                    and "registration" not in job_description.lower()
                    and "499" not in job_description
                    and "999" not in job_description
                ),
                "Employment type is specified": employment_type != "Not mentioned",
                "Company has a website or logo": has_logo == "Yes",
                "Professional email used": bool(recruiter_email) and not any(
                    d in recruiter_email.lower()
                    for d in ["gmail", "yahoo", "hotmail", "outlook"]
                ) if recruiter_email else True,
            }

            c1, c2 = st.columns(2)
            items = list(checks.items())
            for i, (check, passed) in enumerate(items):
                col = c1 if i < 4 else c2
                with col:
                    st.write(f"{'✅' if passed else '❌'} {check}")

            score = sum(checks.values())
            if score >= 6:
                st.success(f"**Safety Score: {score}/7** — Good signs of a legitimate posting")
            elif score >= 4:
                st.warning(f"**Safety Score: {score}/7** — Some concerns, verify carefully")
            else:
                st.error(f"**Safety Score: {score}/7** — Multiple red flags. Very high scam risk!")

            st.divider()

            # ── ACTION ADVICE ────────────────────────
            if fake_conf >= 60:
                st.error("""
### ❌ Immediate Action Required
- Do NOT pay any registration or processing fees
- Do NOT share your Aadhaar, PAN, or bank details
- Search the company name + "scam" + "fraud" on Google
- Report at **cybercrime.gov.in** or call **1930**
                """)
            elif fake_conf >= 30:
                st.warning("""
### ⚠️ Proceed With Caution
- Research the company on LinkedIn and their official website
- Ask for an official offer letter on company letterhead before sharing documents
- Verify the recruiter exists on the company's official LinkedIn page
- Never pay money at any stage — legitimate companies do not charge candidates
                """)
            else:
                st.info("""
### ✅ Looks Safe — But Still Verify
- Confirm the company exists on LinkedIn and their official website
- Make sure the recruiter email uses the company's domain
- Read reviews on Glassdoor or Ambitionbox before accepting
- Never pay money — even for background verification
                """)

# ══════════════════════════════════════════════
# TAB 2 — EMAIL / OFFER LETTER SCANNER
# ══════════════════════════════════════════════
with tab2:
    st.subheader("📧 Email Screenshot & Offer Letter Scanner")
    st.markdown(
        "Upload a screenshot of a job email, WhatsApp message, or offer letter. "
        "Our AI will analyze it for scam indicators."
    )

    upload_type = st.radio(
        "What are you uploading?",
        ["Job Email Screenshot", "Offer Letter (Image)", "WhatsApp Message Screenshot"],
        horizontal=True
    )

    uploaded_file = st.file_uploader(
        "Upload image (JPG, PNG, JPEG)",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("🔍 Analyze for Scam Indicators", type="primary", use_container_width=True):
            with st.spinner("🧠 AI is reading and analyzing your image..."):

                if upload_type == "Job Email Screenshot":
                    prompt = """
You are an expert at detecting job scam emails targeting Indian graduates.

Carefully read this email screenshot and analyze it.

Provide EXACTLY this format:

**Overall Risk Level:** 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW

**Red Flags Found:**
(list as: ⚠️ [flag] — [explanation])

**What Looks Legitimate:**
(list as: ✅ [signal] — [explanation])

**Analysis:**
(3-4 sentences explaining your overall assessment)

**What This Person Should Do:**
(3 specific action steps)

Focus especially on: fee requests, urgency language, unprofessional email addresses,
grammar errors, unrealistic promises, requests for personal information.
"""
                elif upload_type == "Offer Letter (Image)":
                    prompt = """
You are an expert at verifying job offer letters for Indian graduates.

Carefully read this offer letter image and analyze it.

Provide EXACTLY this format:

**Offer Letter Authenticity: SUSPICIOUS / LIKELY GENUINE / CANNOT DETERMINE**

**Red Flags Found:**
(list as: ⚠️ [flag] — [explanation])
Consider: missing company address, no registration number, grammar errors,
unrealistic salary, fee requests, missing HR signature, fake-looking letterhead

**Positive Indicators:**
(list as: ✅ [indicator] — [explanation])

**Salary Assessment:**
Is the salary realistic for this role and experience level in India?

**What This Person Should Do:**
(3-4 specific steps to verify this offer letter)

**Verdict:**
(one clear sentence)
"""
                else:
                    prompt = """
You are an expert at detecting job scam messages on WhatsApp targeting Indian graduates.

Read this WhatsApp message screenshot carefully.

Provide EXACTLY this format:

**Risk Level:** 🔴 HIGH RISK / 🟡 MEDIUM RISK / 🟢 LOW RISK

**Scam Indicators Found:**
(list as: ⚠️ [indicator] — [explanation])

**What Legitimate Recruiters Would NOT Do:**
(compare this message against professional recruitment practices)

**Verdict:**
(one clear sentence)

**Immediate Action:**
(what should this person do right now)
"""

                result = get_gemini_vision(prompt, image)
                new_total = increment_scan_counter()

            st.divider()
            st.subheader("🧠 AI Analysis Result")
            st.markdown(result)

            st.divider()
            st.info("""
**Remember:** Screenshots can be altered. Even if this looks real,
always verify by calling the company's official phone number found on their website.
            """)

# ══════════════════════════════════════════════
# TAB 3 — COMPANY CHECKER
# ══════════════════════════════════════════════
with tab3:
    st.subheader("🏢 Company Reputation & Verification Checker")
    st.markdown("Enter a company name or recruiter email to get AI-powered verification guidance.")

    check_type = st.radio(
        "What do you want to check?",
        ["Company Name", "Recruiter Email Address"],
        horizontal=True
    )

    if check_type == "Company Name":
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g. GlobalEarnings Pvt Ltd, Infosys BPM"
        )
        job_role = st.text_input(
            "Job Role (optional)",
            placeholder="e.g. Data Entry, Software Developer"
        )

        if st.button("🔍 Check This Company", type="primary", use_container_width=True):
            if not company_name.strip():
                st.error("Please enter a company name.")
            else:
                with st.spinner("🧠 AI is analyzing this company..."):
                    prompt = f"""
You are a career counselor helping Indian fresh graduates verify job offers.

A student received a job offer from: "{company_name}"
Job Role: "{job_role if job_role else 'Not specified'}"

Based on the company name and context, provide:

**Company Assessment:**
Does this name sound like a legitimate Indian company or a potential scam setup?
(Note: You may not have real-time data, so focus on patterns and red flags in the name itself)

**How to Verify This Company (Step by Step):**
1. (specific website or method)
2. (specific website or method)
3. (specific website or method)
4. (specific website or method)
5. (specific website or method)

**Questions to Ask the Recruiter:**
(5 specific questions a candidate should ask to verify legitimacy)

**Documents You Should Request Before Joining:**
(list of legitimate documents a real company would provide)

**What Documents You Should NEVER Share Before Joining:**
(list of documents/info that scammers typically ask for)

**Red Flag Names Pattern:**
Does "{company_name}" follow any common scam company naming patterns?
(Generic names like "Global", "Earn", "Work From Home" in company names are common scam indicators)

Be specific and practical for a fresh graduate in India.
"""
                    result = get_gemini_text(prompt)

                st.subheader("🧠 Company Verification Analysis")
                st.markdown(result)

    else:
        email_input = st.text_input(
            "Recruiter Email Address",
            placeholder="e.g. hr.recruitment@gmail.com or careers@infosys.com"
        )

        if st.button("🔍 Analyze This Email", type="primary", use_container_width=True):
            if not email_input.strip():
                st.error("Please enter an email address.")
            else:
                email_lower = email_input.lower().strip()
                free_domains = ["gmail.com", "yahoo.com", "hotmail.com",
                                "outlook.com", "rediffmail.com", "ymail.com",
                                "protonmail.com", "icloud.com"]

                domain = email_lower.split("@")[-1] if "@" in email_lower else ""
                is_free = any(fd in email_lower for fd in free_domains)

                st.divider()

                if is_free:
                    st.error(f"""
## 🔴 HIGH RISK EMAIL
**{email_input}**

This email uses **{domain}** — a free email service.

**Why This is a Red Flag:**
- Every legitimate company has its own email domain (e.g., @infosys.com, @tcs.com)
- Real HR teams never use Gmail or Yahoo for official recruitment
- This is one of the most common signs of a fake job offer
- Scammers use free emails because they cannot create company domains

**What You Should Do:**
- Go to the company's official website and find their actual HR email
- Do NOT reply to this email with any personal documents
- Do NOT pay any fees requested from this email address
                    """)
                else:
                    st.success(f"""
## 🟢 EMAIL LOOKS PROFESSIONAL
**{email_input}**

This email uses company domain: **{domain}**

**This is a Positive Sign:**
- Using a company domain shows the recruiter has official company access
- This is consistent with legitimate recruitment

**Still Verify:**
- Visit the company website and confirm {domain} is their official domain
- Search the recruiter's name on LinkedIn to confirm they work at this company
                    """)

                with st.spinner("🧠 Getting detailed AI analysis..."):
                    email_prompt = f"""
Analyze this recruiter email address for a job seeker in India: {email_input}

Provide:
**Email Domain Assessment:** (is {domain} a known company domain or suspicious?)
**Risk Level:** 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW
**Specific Advice:** (3 concrete steps to verify this email's legitimacy)
**Verdict:** (one sentence)
"""
                    email_result = get_gemini_text(email_prompt)

                st.markdown(email_result)

# ══════════════════════════════════════════════
# TAB 4 — SAMPLE POSTINGS
# ══════════════════════════════════════════════
with tab4:
    st.subheader("📖 Try With Sample Job Postings")
    st.markdown("See how the detector works on a clearly fake job vs a clearly real job.")

    col1, col2 = st.columns(2)

    with col1:
        st.error("### 🚨 Sample: Fake Job Posting")
        st.text_area("", SAMPLE_FAKE, height=200, disabled=True, key="fake_display")
        if st.button("🔍 Analyze This Fake Job", use_container_width=True, key="btn_fake"):
            with st.spinner("Analyzing..."):
                cleaned = clean_text(SAMPLE_FAKE)
                vec = tfidf.transform([cleaned])
                pred = model.predict(vec)[0]
                prob = model.predict_proba(vec)[0]
                fc = prob[1] * 100
                rc = prob[0] * 100
                risk_l, _, risk_d = get_risk_level(fc)
            st.error(f"**Result: {risk_l}**")
            st.write(f"Fraud Probability: **{fc:.1f}%** | Legitimate: **{rc:.1f}%**")
            with st.spinner("Getting AI explanation..."):
                r = get_gemini_text(f"Analyze this fake job posting briefly for an Indian graduate. List 3 main red flags:\n{SAMPLE_FAKE}")
            st.markdown(r)

    with col2:
        st.success("### ✅ Sample: Real Job Posting")
        st.text_area("", SAMPLE_REAL, height=200, disabled=True, key="real_display")
        if st.button("🔍 Analyze This Real Job", use_container_width=True, key="btn_real"):
            with st.spinner("Analyzing..."):
                cleaned = clean_text(SAMPLE_REAL)
                vec = tfidf.transform([cleaned])
                pred = model.predict(vec)[0]
                prob = model.predict_proba(vec)[0]
                fc = prob[1] * 100
                rc = prob[0] * 100
                risk_l, _, risk_d = get_risk_level(fc)
            st.success(f"**Result: {risk_l}**")
            st.write(f"Fraud Probability: **{fc:.1f}%** | Legitimate: **{rc:.1f}%**")
            with st.spinner("Getting AI explanation..."):
                r = get_gemini_text(f"Analyze this real job posting briefly for an Indian graduate. List 3 positive signals:\n{SAMPLE_REAL}")
            st.markdown(r)

# ══════════════════════════════════════════════
# TAB 5 — HOW IT WORKS
# ══════════════════════════════════════════════
with tab5:
    st.subheader("How This System Works")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
### 🤖 Machine Learning Model
- **Dataset:** EMSCAD — 14,107 real job postings (Kaggle)
- **Fake jobs in dataset:** 516 (3.66%)
- **Algorithm:** Logistic Regression
- **Class imbalance:** Handled with `class_weight='balanced'`
- **Text features:** TF-IDF Vectorization (5000 features)
- **Overall Accuracy:** 97.7%
- **Fraud Detection Recall:** 88%
- **False Negatives:** Only 13 per 104 fake jobs

### 🔄 NLP Text Processing Pipeline
1. Combine title + company + description + requirements + benefits
2. Convert everything to lowercase
3. Remove numbers and special characters
4. Remove common English stopwords
5. TF-IDF vectorization converts text to numbers
6. Model predicts probability of fraud
        """)
    with col2:
        st.markdown("""
### 🧠 Google Gemini AI Layer
- Reads the complete job posting text
- Understands context beyond just keywords
- Identifies specific suspicious phrases
- Explains exactly WHY a job looks fake or real
- Analyzes images (email screenshots, offer letters)
- Tailored explanations for Indian job market

### 📊 Why We Combined ML + AI
| Feature | ML Model | Gemini AI |
|---|---|---|
| Speed | Very Fast | Moderate |
| Explanation | None | Detailed |
| Works on text | Yes | Yes |
| Works on images | No | Yes |
| Handles context | Statistical | Contextual |

**Together:** Fast detection + Smart explanation + Image analysis
        """)

    st.divider()
    st.markdown("### 📈 Model Performance Summary")
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.metric("Accuracy", "97.7%")
    with m2: st.metric("Precision", "64%")
    with m3: st.metric("Recall (Fraud)", "88%")
    with m4: st.metric("F1 Score", "0.74")
    with m5: st.metric("False Negatives", "13")

# ══════════════════════════════════════════════
# TAB 6 — SCAM SAFETY GUIDE
# ══════════════════════════════════════════════
with tab6:
    st.subheader("📚 Complete Job Scam Safety Guide for Indian Graduates")

    col1, col2 = st.columns(2)
    with col1:
        st.error("""
### 🚨 NEVER Do These
- Pay any registration or processing fees
- Share Aadhaar, PAN card, or bank account details upfront
- Respond to recruiter emails from Gmail or Yahoo
- Attend interviews at residential addresses
- Believe any "guaranteed income" claims
- Wire money for training equipment or ID cards
- Give your OTP or passwords to anyone
- Click links in suspicious recruitment emails
        """)
    with col2:
        st.success("""
### ✅ ALWAYS Do These
- Search the company on Google + LinkedIn + official website
- Verify the recruiter exists on the company's official LinkedIn
- Check company reviews on Glassdoor or Ambitionbox
- Talk to a trusted person before accepting any offer
- Apply only through official portals like Naukri, LinkedIn, Internshala
- Call the company's official customer service number to verify
- Ask for the offer letter on official company letterhead
- Save all communication in case you need to report
        """)

    st.divider()
    st.markdown("### 🎯 Common Job Scam Types in India")

    scam1, scam2, scam3 = st.columns(3)
    with scam1:
        st.warning("""
**📦 Work From Home Scams**
- Data entry, copy-paste jobs
- Earn ₹500 per hour claims
- Pay to get work kit
- No office, no interview
- Target: housewives, students
        """)
    with scam2:
        st.warning("""
**🏢 Fake Company Scams**
- Made-up company names
- No physical address
- No website or fake website
- Only WhatsApp contact
- Disappear after taking fees
        """)
    with scam3:
        st.warning("""
**📝 Fake Offer Letter Scams**
- Looks official but fake
- Asks for security deposit
- Immediate joining pressure
- Fake company logo
- No verifiable HR contact
        """)

    st.divider()
    st.warning("""
### 🚩 These Exact Phrases Mean SCAM
- *"Earn ₹50,000/month, no experience required"*
- *"Work from home, just 2-3 hours daily"*
- *"Pay ₹499/₹999 registration fee to start"*
- *"Immediate joining, no interview needed"*
- *"Contact on WhatsApp only for details"*
- *"Limited seats available, apply in 24 hours"*
- *"No qualifications needed, anyone can apply"*
- *"Guaranteed income, no targets"*
    """)

    st.divider()
    st.info("""
### 📞 Report Job Scams in India
| Platform | Contact |
|---|---|
| National Cyber Crime Portal | cybercrime.gov.in |
| Cyber Crime Helpline | **1930** |
| Consumer Helpline | **1800-11-4000** (toll free) |
| Nearest Police Station | cybercrime.gov.in/reportAndTrack |
    """)