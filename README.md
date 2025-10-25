# AI-Driven KYC Verification Agent 🔐

Automates customer onboarding with document OCR, facial recognition, and fraud detection.

## Features

- 📄 **Document OCR** - Extract data from identity documents using EasyOCR
- 👤 **Face Verification** - Compare ID photo with selfie using DeepFace
- 🔍 **Fraud Detection** - Automated risk assessment and scoring
- 🌍 **Multi-Format Support** - Passports, licenses, national IDs, citizenship certificates
- 🚀 **Easy Deployment** - Web interface with Gradio

## Installation Methods

### Method 1: Local Installation

```bash
# Clone the repository
git clone https://github.com/shruteeegrg/kyc-verification-agent.git


# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/app.py
```

### Method 2: Google Colab (Recommended for Testing)

1. Open the Colab notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shruteeegrg/kyc-verification-agent/blob/main/notebooks/kyc_agent.ipynb)

2. Run the installation cell:
```python
!apt-get update
!apt-get install -y tesseract-ocr
!pip install gradio opencv-python-headless easyocr deepface tf-keras regex
```

3. Run all cells to start the interface

## Supported Documents

- ✅ Passports
- ✅ Driver's Licenses
- ✅ National ID Cards
- ✅ Citizenship Certificates (optimized for Nepal)

## Output Example

```
KYC Verification Results
Status: ✅ VERIFIED
Timestamp: 2025-10-25T10:30:00

📄 Extracted Document Data
Name: SHRUTI GURUNG
Document Number: 123-45-67-89
Date Of Birth: 2004-JUN-23
...

👤 Face Verification
Message: ✅ Faces Match!

🔍 Fraud Detection
Fraud Score: 15/100
Risk Level: 🟢 Low
```

## Tech Stack

- **EasyOCR** - Text extraction
- **DeepFace** - Face verification  
- **OpenCV** - Image processing
- **Gradio** - Web interface
- **TensorFlow** - Deep learning backend


## Project Structure

```
kyc-verification-agent/
├── src/
│   ├── kyc_agent.py      # Main KYC logic
│   ├── app.py            # Gradio interface
│   └── utils.py          # Helper functions          
└── notebooks/            # Colab demos
```

## Acknowledgments

Built with:
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [DeepFace](https://github.com/serengil/deepface)
- [Gradio](https://gradio.app/)

## Contact

For questions or support, please open an issue.