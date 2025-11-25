# NetCart-Autonomous-QA-Agent
An intelligent, autonomous QA agent that constructs a "testing brain" from project documentation and generates comprehensive test cases and executable Selenium scripts for web applications. 


## 🎯 Project Overview

This system ingests support documents (product specifications, UI/UX guidelines, API documentation) alongside HTML structure to:
- **Generate Documentation-Grounded Test Cases** - Produces comprehensive test plans with zero hallucinations
- **Generate Selenium Test Scripts** - Converts test cases into executable Python Selenium scripts with actual HTML selectors
- **RAG-Powered Intelligence** - Uses Retrieval Augmented Generation for context-aware test generation

## 🏗️ Architecture

- **Backend:** FastAPI with RAG pipeline (ChromaDB + Sentence Transformers)
- **Frontend:** Streamlit with Netflix-themed UI
- **Vector Database:** ChromaDB for document embeddings
- **HTML Parser:** BeautifulSoup4 for selector extraction
- **Test Generation:** Context-aware rule engine with LLM integration support

## 📁 Project Structure

```
autonomous-qa-agent/
├── backend/
│   └── app/
│       ├── __init__.py
│       ├── main.py              # FastAPI server
│       ├── rag.py               # RAG pipeline & test generation
│       ├── generator.py         # Selenium script generator
│       ├── html_parser.py       # HTML selector extraction
│       ├── llm_integration.py   # LLM integration layer
│       └── ingest_new.py        # Document parsing & ingestion
├── frontend/
│   ├── app.py                   # Streamlit UI
│   └── netflix_theme.css        # Custom Netflix-style theme
├── target_site/
│   ├── checkout.html            # Target web application
│   ├── css/
│   │   └── netflix.css
│   └── js/
│       └── validation.js
├── support_docs/
│   ├── product_specs.md         # Product specifications
│   ├── ui_ux_guide.txt          # UI/UX guidelines
│   └── api_endpoints.json       # API documentation
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser (for running Selenium scripts)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/autonomous-qa-agent.git
cd autonomous-qa-agent
```

2. **Create a virtual environment:**
```bash
python -m venv .venv
```

3. **Activate virtual environment:**

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Verify installation:**
```bash
python -c "import fastapi, streamlit, chromadb; print('✓ All dependencies installed')"
```

## 🎮 Running the Application

### Start Backend Server (Terminal 1)

```bash
# Make sure you're in the project root
cd autonomous-qa-agent

# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Start FastAPI server
uvicorn backend.app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
✓ HTML structure loaded from target_site/checkout.html
```

### Start Frontend Interface (Terminal 2)

```bash
# Open NEW terminal
cd autonomous-qa-agent

# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Start Streamlit frontend
streamlit run frontend/app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

The browser should automatically open to `http://localhost:8501`

## 📖 Usage Examples

### Example 1: Generate Discount Coupon Tests

1. **Upload Documentation**
   - Click "Browse files"
   - Select `support_docs/product_specs.md`
   - Click "Send to Backend & Upload"

2. **Build Knowledge Base**
   - Click "Build KB"
   - Wait for confirmation: `{"status": "kb_built", "added": 1}`

3. **Generate Test Cases**
   - Enter prompt: `Generate all positive and negative test cases for the discount code feature`
   - Click "Generate Test Cases"

**Output:**
```
Test_ID: TC-001
Feature: Discount Code
Test_Scenario: Apply a valid discount code 'SAVE15'

Steps:
1. Navigate to NetCart checkout page
2. Click 'Add to Cart' button for any product (class='.btn-add')
3. Locate coupon input field (id='coupon')
4. Enter discount code 'SAVE15' in the coupon field
5. Click 'Apply' button (id='apply-coupon')
6. Verify discount is reflected in cart total (id='cart-total')

Expected_Result: Total price is reduced by 15%. Discount applied successfully.
Grounded_In: product_specs.md
```

4. **Generate Selenium Script**
   - Click "Generate Selenium Script"
   - Click "Download Python Script"
   - Script saved as `TC-001.py`

### Example 2: Complete Checkout Flow Tests

**Prompt:**
```
Generate complete end-to-end checkout test with all steps including cart, shipping, and payment
```

**Generates:** Comprehensive test covering full user journey

### Example 3: Form Validation Tests

**Prompt:**
```
Create test cases for form validation with required fields and email format validation
```

**Generates:** Multiple test cases for positive and negative validation scenarios

## 📄 Support Documents Explanation

### 1. product_specs.md
Contains business rules and feature specifications:
- Discount coupons: SAVE15 (15% off), WELCOME10 (10% off)
- Shipping: Standard (Free), Express ($10)
- Payment methods: Credit Card, PayPal, UPI
- Cart functionality rules
- Form validation requirements

### 2. ui_ux_guide.txt
Defines UI/UX standards:
- Netflix-inspired dark theme colors
- Button styles and interactions
- Form error display rules
- Responsive design breakpoints
- Accessibility requirements

### 3. api_endpoints.json
API contract documentation:
- POST /cart/add - Add items to cart
- POST /coupon/apply - Apply discount codes
- POST /payment/process - Process checkout
- Validation rules and response formats

## 🎯 Key Features

### 1. Documentation-Grounded Testing
- Zero hallucinations - all tests based strictly on uploaded documents
- Clear source attribution with "Grounded_In" field
- Context-aware test generation using RAG

### 2. HTML-Aware Selenium Scripts
- Parses actual HTML to extract real selectors
- Uses IDs, classes, and attributes from YOUR checkout page
- No hardcoded or fake selectors

### 3. Professional Script Quality
- Comprehensive error handling
- Explicit waits for element availability
- Screenshot capture on failures
- Detailed logging and assertions
- Production-ready code structure

### 4. Netflix-Themed UI
- Modern, professional dark theme
- Intuitive workflow: Upload → Build → Generate → Export
- Real-time backend status monitoring
- Clean, responsive design

## 🧪 Running Generated Tests

After downloading a Selenium script:

1. **Update the file path** in the script:
```python
self.base_url = "file:///YOUR_PATH/autonomous-qa-agent/target_site/checkout.html"
```

2. **Install Selenium (if not already installed):**
```bash
pip install selenium webdriver-manager
```

3. **Run the test:**
```bash
python TC-001.py
```

**Expected output:**
```
[TC-001] ============================================================
[TC-001] Starting Test: TC-001
[TC-001] Feature: Discount Code
[TC-001] ============================================================
[TC-001] Step 1: Navigate to NetCart checkout page
[TC-001] ✓ Add to Cart button found
[TC-001] Step 2: Click 'Add to Cart' button
...
[TC-001] ✓✓✓ TEST PASSED ✓✓✓
```

## 🛠️ Technology Stack

- **Backend Framework:** FastAPI 0.104+
- **Frontend Framework:** Streamlit 1.28+
- **Vector Database:** ChromaDB 0.4+
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **HTML Parsing:** BeautifulSoup4
- **Document Parsing:** PyMuPDF, python-docx, python-pptx
- **Test Automation:** Selenium WebDriver
- **Python Version:** 3.8+

## 📊 System Requirements

- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** ~500MB for dependencies + models
- **CPU:** Any modern processor (model loading takes ~10 seconds first time)
- **OS:** Windows 10/11, macOS 10.15+, Ubuntu 20.04+

## 🐛 Troubleshooting

### Issue: Backend fails to start
**Solution:** Check if port 8000 is already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID  /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Issue: "HTML structure not loaded"
**Solution:** Verify `target_site/checkout.html` exists
```bash
# From project root
ls target_site/checkout.html
```

### Issue: Frontend shows "Backend Offline"
**Solution:** 
1. Ensure backend is running on port 8000
2. Check firewall isn't blocking localhost connections
3. Verify `BACKEND_URL` in `frontend/app.py` is `http://127.0.0.1:8000`

### Issue: No test cases generated
**Solution:**
1. Upload support documents first
2. Click "Build KB" and wait for confirmation
3. Make sure prompt keywords match document content

## 🙏 Acknowledgments

- Assignment designed to demonstrate RAG-based test automation
- Netflix UI inspiration for modern, professional interface
- ChromaDB and Sentence Transformers for vector search capabilities
