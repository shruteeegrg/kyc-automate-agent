# AI-Powered KYC Verification Agent

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Gemini-4285F4?logo=google)](https://deepmind.google/technologies/gemini/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shruteeegrg/kyc-automate-agent/blob/main/notebooks/kyc_verification_agent.ipynb)

An intelligent, autonomous KYC (Know Your Customer) verification system that uses **Google's Gemini AI** as the orchestration brain. Unlike traditional rule-based systems, this agent dynamically decides the next best action at each step, making it adaptable, transparent, and production-ready.

## 🌟 Key Features

### **AI-Orchestrated Workflow**
- **LLM Decision Making**: The agent uses Gemini to intelligently choose which verification step to perform next
- **Dynamic Reasoning**: Adapts to different document types and quality issues
- **Transparent Logic**: Every decision is logged with justification

### **Comprehensive Verification**
- **Image Quality Assessment**: Detects blurry or low-quality ID cards
- **OCR Text Extraction**: Uses EasyOCR for accurate text recognition
- **Data Parsing**: Extracts Name, DOB, Document Number, Address, and more
- **Face Verification**: Compares ID photo with selfie using DeepFace
- **Fraud Detection**: Calculates risk scores with detailed indicators

### 📊 **Sample Output**
```
--- KYC Verification Agent Report ---
Final Status: VERIFIED
Fraud Score: 15/100
Risk Level:  Low

Extracted Data:
  - Name: SHRUTI GURUNG
  - Document Number: 46-01-78-09155
  - Date Of Birth: 2004-JUN-23
  - Address: District: Kaski
  
Face Verification:  Faces Match!

Fraud Detection:
  - Indicators: Could not extract: Issue Date
```

## 🚀 Quick Start

### Step 1: Open in Google Colab

Click the badge below to open the notebook directly in Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shruteeegrg/kyc-automate-agent/blob/main/notebooks/kyc_verification_agent.ipynb)

### Step 2: Set Up Your Gemini API Key

1. Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. In Colab, click the 🔑 **Secrets** icon in the left sidebar
3. Click **"Add new secret"**
4. Name: `GEMINI_API_KEY`
5. Value: Paste your API key
6. Toggle **"Notebook access"** ON

### Step 3: Run All Cells

Click **Runtime → Run all** or press `Ctrl+F9` (Windows) / `Cmd+F9` (Mac)

### Step 4: Use the Gradio Interface

After running all cells, a Gradio interface will appear at the bottom:
1. Upload an ID card image
2. Upload a selfie image
3. Click **Submit**
4. View the detailed verification report!


## 🛠️ How It Works

### Architecture Overview

```
User Uploads → Agent Initializes → Gemini Decides Tool → Tool Executes → 
Update State → Check Complete? → [Loop or Generate Report]
```

### The Agent's Toolbox

| Tool | Purpose | When Used |
|------|---------|-----------|
| `assess_image_quality` | Detects blurry images | First step, always |
| `extract_text_from_id` | OCR extraction | After quality check |
| `parse_kyc_details` | Structured data extraction | After OCR success |
| `verify_faces` | Biometric verification | After data extraction |
| `calculate_fraud_score_and_conclude` | Final decision | Last step |

### Agent Decision Loop

For each step:
1.  **Gemini analyzes** the current state
2.  **Gemini selects** the best tool with justification
3.  **Tool executes** and updates the state
4.  **Repeat** until verification is complete
5.  **Generate** comprehensive report

## 🎯 Use Cases

- **Banking & Fintech**: Customer onboarding, account verification
- **E-commerce**: Age verification, seller verification  
- **Healthcare**: Patient identity verification
- **Government Services**: Digital ID verification
- **Cryptocurrency**: Exchange KYC compliance
- **Sharing Economy**: Driver/host verification (Uber, Airbnb)

## 📊 Agent Reasoning Example

```
▶️ KYC process initiated.

--- Step 1: Agent is thinking... ---
🧠 Agent chose tool: `assess_image_quality`
   Justification: The process has just started, first step is quality check
EXECUTING: tool_assess_image_quality
🔧 Result: Image quality acceptable. Blur score: 4684.52

--- Step 2: Agent is thinking... ---
🧠 Agent chose tool: `extract_text_from_id`
   Justification: Quality check passed, now extract text with OCR
EXECUTING: tool_extract_text_from_id
🔧 Result: OCR successful. Extracted text is now in the state.

--- Step 3: Agent is thinking... ---
🧠 Agent chose tool: `parse_kyc_details`
   Justification: Raw text extracted, now parse into structured fields
EXECUTING: tool_parse_kyc_details
🔧 Result: Parsing complete. Found details: ['Name', 'Document Number', ...]

--- Step 4: Agent is thinking... ---
🧠 Agent chose tool: `verify_faces`
   Justification: All data extracted, now verify identity with face match
EXECUTING: tool_verify_faces
🔧 Result: Face verification complete. Match status: True

--- Step 5: Agent is thinking... ---
🧠 Agent chose tool: `calculate_fraud_score_and_conclude`
   Justification: All checks complete, calculate final score and decide
EXECUTING: tool_calculate_fraud_score_and_conclude
🔧 Result: Final fraud score calculated and decision concluded.

⏹️ Process concluded with status: VERIFIED
```

## 🔧 Customization

All customization can be done directly in the notebook cells:

### Modify Fraud Scoring Weights
Edit Cell 8 - `tool_calculate_fraud_score_and_conclude()`:
```python
# Change these values to adjust scoring
score += len(missing_fields) * 15  # Weight for missing fields
score += 50  # Weight for face verification failure
```

### Add New Document Types
Edit Cell 8 - `tool_parse_kyc_details()`:
```python
# Add new regex patterns for different ID types
passport_match = re.search(r'Passport No[:\s]*([A-Z0-9]+)', text)
if passport_match: 
    details["Passport Number"] = passport_match.group(1)
```

### Adjust Quality Threshold
Edit Cell 8 - `tool_assess_image_quality()`:
```python
if blur_score < 100:  # Change this threshold
    state['id_card_quality']['is_blurry'] = True
```

## 🎓 Learning Resources

### Understanding the Agent Pattern
- Each **tool** is an independent function that performs one specific task
- **Gemini** acts as the "brain" that decides which tool to use next
- The **state** dictionary holds all information and passes between tools
- The agent **loops** until the KYC verification is complete

### Key Concepts
1. **Agentic AI**: AI that makes decisions and takes actions autonomously
2. **Tool-based Architecture**: Modular functions that the agent can call
3. **State Management**: Shared memory across all verification steps
4. **Dynamic Orchestration**: LLM decides the workflow, not hard-coded rules
