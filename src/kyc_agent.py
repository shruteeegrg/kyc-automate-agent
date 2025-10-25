"""
KYC Agent Core Module

Main KYC Agent class that handles document processing, face verification,
and fraud detection for customer onboarding.
"""

import cv2
import numpy as np
from PIL import Image
import regex as re
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Initialize EasyOCR
try:
    import easyocr
    reader = easyocr.Reader(['en'], gpu=False)
    EASYOCR_AVAILABLE = True
except Exception as e:
    EASYOCR_AVAILABLE = False
    print(f"EasyOCR initialization failed: {e}")

# Initialize DeepFace
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except Exception as e:
    DEEPFACE_AVAILABLE = False
    print(f"DeepFace initialization failed: {e}")


class KYCAgent:
    """
    Main KYC Agent class for automated customer verification.
    
    Attributes:
        supported_docs (list): List of supported document types
        
    Methods:
        extract_text_from_document: Extract text using OCR
        parse_kyc_details: Parse structured data from text
        verify_faces: Compare faces between ID and selfie
        calculate_fraud_score: Assess fraud risk
        process_kyc: Main processing pipeline
    """
    
    def __init__(self):
        """Initialize the KYC Agent with supported document types."""
        self.supported_docs = [
            'passport', 
            'drivers_license', 
            'national_id', 
            'citizenship_certificate'
        ]
    
    def extract_text_from_document(self, image):
        """
        Extract text from document using EasyOCR.
        
        Args:
            image: numpy array or PIL Image of the document
            
        Returns:
            tuple: (extracted_text as string, raw OCR results)
        """
        try:
            if not EASYOCR_AVAILABLE:
                return "EasyOCR not available", []
            
            if isinstance(image, Image.Image):
                image = np.array(image)
            
            results = reader.readtext(image)
            extracted_text = "\n".join([result[1] for result in results])
            
            return extracted_text, results
            
        except Exception as e:
            print(f"OCR Error: {e}")
            return "", []
    
    def parse_kyc_details(self, text):
        """
        Parse unstructured text from ID card to extract key details.
        Optimized for Nepalese citizenship certificates and various ID formats.
        
        Args:
            text: Raw text extracted from the document
            
        Returns:
            dict: Parsed details including name, document number, DOB, etc.
        """
        details = {
            "Name": "Not found",
            "Document Number": "Not found",
            "Date Of Birth": "Not found",
            "Issue Date": "Not found",
            "Address": "Not found",
            "Nationality": "NEPALESE"
        }
        
        if not text or len(text.strip()) < 10:
            return details
        
        text_upper = text.upper()
        
        # Extract Full Name
        name_patterns = [
            r'FULL\s+NAME\s*\n\s*([A-Z\s]+?)\s*(\n|$)',
            r'NAME\s*[:\.]?\s*\n?\s*([A-Z\s]{3,50})',
            r'NAAM\s*[:\.]?\s*\n?\s*([A-Z\s]{3,50})',
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text_upper, re.IGNORECASE)
            if match:
                potential_name = match.group(1).strip()
                name_words = [
                    w for w in potential_name.split() 
                    if len(w) > 1 and w not in ['DATE', 'YEAR', 'MONTH', 'DAY', 'OF', 'BIRTH']
                ]
                if len(name_words) >= 2:
                    details["Name"] = ' '.join(name_words)
                    break
        
        # Extract Document Number
        doc_patterns = [
            r'CERTIFICATE\s+NO\.?\s*[:\.\s]*\n?([\d-]+)',
            r'CITIZENSHIP\s+NO\.?\s*[:\.]?\s*([\d-]+)',
            r'ID\s+NO\.?\s*[:\.]?\s*([\d-]+)',
            r'\b(\d{2,3}[-/]\d{2,3}[-/]\d{2,3}[-/]\d{2,5})\b',
        ]
        
        for pattern in doc_patterns:
            match = re.search(pattern, text_upper, re.IGNORECASE)
            if match:
                details["Document Number"] = match.group(1).strip()
                break
        
        # Extract Date of Birth
        dob_pattern = r'YEAR\s*:\s*(\d{4})\s*MONTH\s*:\s*([A-Z]{3})\s*DAY\s*\.?\s*(\d{1,2})'
        dob_match = re.search(dob_pattern, text_upper, re.IGNORECASE)
        
        if dob_match:
            year, month, day = dob_match.groups()
            details["Date Of Birth"] = f"{year}-{month}-{day}"
        else:
            date_patterns = [
                r'\b(\d{4})[/-](\d{2})[/-](\d{2})\b',
                r'\b(\d{2})[/-](\d{2})[/-](\d{4})\b',
            ]
            for pattern in date_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    details["Date Of Birth"] = '-'.join(matches[0])
                    break
        
        # Extract Issue Date
        issue_patterns = [
            r'ISSUE\s+DATE\s*[:\.]?\s*(\d{4}[/-]\d{2}[/-]\d{2})',
            r'ISSUED\s+ON\s*[:\.]?\s*(\d{4}[/-]\d{2}[/-]\d{2})',
            r'(\d{4}[-.]\d{2}[-.]\d{2})',
        ]
        
        for pattern in issue_patterns:
            match = re.search(pattern, text_upper)
            if match:
                details["Issue Date"] = match.group(1).strip()
                break
        
        # Extract Address
        address_patterns = [
            r'PERMANENT\s+ADDRESS[\s\S]*?DISTRICT\s*:\s*([A-Za-z]+)',
            r'DISTRICT\s*:\s*([A-Za-z]+)',
            r'ADDRESS\s*[:\.]?\s*([A-Z\s,]+)',
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, text_upper, re.IGNORECASE)
            if match:
                address_text = match.group(1).strip()
                details["Address"] = "District: " + address_text
                break
        
        # Extract Nationality
        if 'NEPAL' in text_upper or 'CITIZENSHIP' in text_upper:
            details["Nationality"] = "NEPALESE"
        
        return details
    
    def detect_face_opencv(self, image):
        """
        Detect faces in an image using OpenCV's Haar Cascade classifier.
        
        Args:
            image: numpy array or PIL Image
            
        Returns:
            tuple: (face_detected as bool, face_locations)
        """
        try:
            if isinstance(image, Image.Image):
                image = np.array(image)
            
            if len(image.shape) == 3 and image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            return len(faces) > 0, faces
            
        except Exception as e:
            print(f"Face detection error: {e}")
            return False, []
    
    def verify_faces(self, id_card_image, selfie_image):
        """
        Compare faces using DeepFace library for robust verification.
        
        Args:
            id_card_image: numpy array of ID card
            selfie_image: numpy array of selfie
            
        Returns:
            tuple: (message as string, is_match as bool)
        """
        try:
            if isinstance(id_card_image, Image.Image):
                id_card_image = np.array(id_card_image)
            if isinstance(selfie_image, Image.Image):
                selfie_image = np.array(selfie_image)
            
            # Try DeepFace verification
            if DEEPFACE_AVAILABLE:
                try:
                    cv2.imwrite('/tmp/id_card.jpg', cv2.cvtColor(id_card_image, cv2.COLOR_RGB2BGR))
                    cv2.imwrite('/tmp/selfie.jpg', cv2.cvtColor(selfie_image, cv2.COLOR_RGB2BGR))
                    
                    result = DeepFace.verify(
                        img1_path='/tmp/id_card.jpg',
                        img2_path='/tmp/selfie.jpg',
                        model_name='VGG-Face',
                        enforce_detection=False
                    )
                    
                    if result['verified']:
                        return "Faces Match!", True
                    else:
                        if result.get('face_confidence', 1.0) < 0.5:
                            return "Face not clearly detected in one or both images.", False
                        return "Faces Do Not Match!", False
                    
                except Exception as e:
                    print(f"DeepFace error: {e}")
            
            # Fallback to OpenCV
            id_has_face, _ = self.detect_face_opencv(id_card_image)
            selfie_has_face, _ = self.detect_face_opencv(selfie_image)
            
            if not id_has_face:
                return "Face not detected in the ID Card.", False
            if not selfie_has_face:
                return "Face not detected in the Selfie.", False
            
            return " Faces detected in both images (basic verification)", True
        
        except Exception as e:
            error_message = str(e)
            if "cuda" in error_message.lower() or "dlib" in error_message.lower():
                return "Face comparison error: Could not initialize processing library. Please check environment.", False
            return f"CRITICAL ERROR during face verification: {str(e)}", False
    
    def calculate_fraud_score(self, parsed_details, face_match_status):
        """
        Calculate fraud risk score based on missing data and verification results.
        
        Args:
            parsed_details: Dictionary of parsed document fields
            face_match_status: Boolean indicating if faces matched
            
        Returns:
            tuple: (fraud_score, risk_level, list of indicators)
        """
        score = 0
        indicators = []
        
        # Check for missing fields
        missing_fields = [
            key for key, value in parsed_details.items() 
            if value == "Not found"
        ]
        
        if missing_fields:
            score += len(missing_fields) * 15
            indicators.append(f"Could not extract: {', '.join(missing_fields)}")
        
        # Face verification failure
        if not face_match_status:
            score += 40
            indicators.append("Face verification failed or faces did not match.")
        
        # Validate date of birth
        if parsed_details.get("Date Of Birth") != "Not found":
            try:
                dob_str = parsed_details["Date Of Birth"]
                year_match = re.search(r'(\d{4})', dob_str)
                if year_match:
                    year = int(year_match.group(1))
                    current_year = datetime.now().year
                    age = current_year - year
                    
                    if age < 18:
                        score += 30
                        indicators.append(f"Person appears to be under 18 (age: {age})")
                    elif age > 120:
                        score += 40
                        indicators.append(f"Invalid age calculated: {age}")
            except:
                pass
        
        score = min(score, 100)
        
        # Determine risk level
        if score >= 60:
            risk_level = "🔴 High"
        elif score >= 30:
            risk_level = "🟡 Medium"
        else:
            risk_level = "🟢 Low"
        
        return score, risk_level, indicators
    
    def process_kyc(self, id_card, selfie):
        """
        Main orchestrator function that processes the entire KYC workflow.
        
        Args:
            id_card: Image of the identity document
            selfie: Image of the user's selfie
            
        Returns:
            str: Formatted verification report
        """
        if id_card is None or selfie is None:
            return "Please upload both an ID card and a selfie."
        
        try:
            # Step 1: Extract text from ID card
            raw_text, _ = self.extract_text_from_document(id_card)
            
            # Step 2: Parse extracted text
            parsed_details = self.parse_kyc_details(raw_text)
            
            # Step 3: Verify faces
            face_message, faces_match = self.verify_faces(id_card, selfie)
            
            # Step 4: Calculate fraud score
            fraud_score, risk_level, fraud_indicators = self.calculate_fraud_score(
                parsed_details, 
                faces_match
            )
            
            # Step 5: Determine overall status
            status = "VERIFIED"
            
            if "Not found" in parsed_details.values() or not faces_match:
                status = "MANUAL REVIEW REQUIRED"
            
            if "CRITICAL ERROR" in face_message:
                status = "PROCESSING ERROR"
            
            # Step 6: Generate report
            report = f"""
KYC Verification Results
Status: {status}
Timestamp: {datetime.now().isoformat()}

📄 Extracted Document Data
Name: {parsed_details['Name']}
Document Number: {parsed_details['Document Number']}
Date Of Birth: {parsed_details['Date Of Birth']}
Issue Date: {parsed_details['Issue Date']}
Address: {parsed_details['Address']}
Nationality: {parsed_details['Nationality']}

👤 Face Verification
Message: {face_message}

🔍 Fraud Detection
Fraud Score: {fraud_score}/100
Risk Level: {risk_level}
Indicators:
- {chr(10) + "- ".join(fraud_indicators) if fraud_indicators else "No significant risk indicators found."}
"""
            return report
            
        except Exception as e:
            return f"PROCESSING ERROR: {str(e)}"