"""
Utility Functions for KYC Agent

Helper functions for image processing, validation, and data formatting.
"""

import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import regex as re


def convert_image_format(image):
    """
    Convert image between PIL and numpy formats.
    
    Args:
        image: PIL Image or numpy array
        
    Returns:
        numpy.ndarray: Image as numpy array
    """
    if isinstance(image, Image.Image):
        return np.array(image)
    return image


def validate_image(image, min_width=400, min_height=400):
    """
    Validate image dimensions and quality.
    
    Args:
        image: numpy array or PIL Image
        min_width: Minimum required width
        min_height: Minimum required height
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        if isinstance(image, Image.Image):
            width, height = image.size
        else:
            height, width = image.shape[:2]
        
        if width < min_width or height < min_height:
            return False, f"Image too small. Minimum size: {min_width}x{min_height}"
        
        return True, None
        
    except Exception as e:
        return False, f"Image validation error: {str(e)}"


def preprocess_image(image):
    """
    Preprocess image for better OCR results.
    
    Args:
        image: numpy array (BGR format)
        
    Returns:
        numpy.ndarray: Preprocessed image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply denoising
    denoised = cv2.fastNlMeansDenoising(gray)
    
    # Apply adaptive thresholding
    processed = cv2.adaptiveThreshold(
        denoised, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 
        2
    )
    
    return processed


def calculate_image_quality(image):
    """
    Calculate image quality score based on blur detection.
    
    Args:
        image: numpy array
        
    Returns:
        float: Quality score (higher is better)
    """
    if isinstance(image, Image.Image):
        image = np.array(image)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    return blur_score


def validate_date_format(date_string):
    """
    Validate and normalize date formats.
    
    Args:
        date_string: Date string in various formats
        
    Returns:
        tuple: (is_valid, normalized_date or error_message)
    """
    date_patterns = [
        (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
        (r'(\d{2})/(\d{2})/(\d{4})', '%d/%m/%Y'),
        (r'(\d{4})/(\d{2})/(\d{2})', '%Y/%m/%d'),
    ]
    
    for pattern, format_str in date_patterns:
        match = re.match(pattern, date_string)
        if match:
            try:
                date_obj = datetime.strptime(date_string, format_str)
                return True, date_obj.strftime('%Y-%m-%d')
            except:
                continue
    
    return False, "Invalid date format"


def extract_numbers(text):
    """
    Extract all numeric patterns from text.
    
    Args:
        text: String containing numbers
        
    Returns:
        list: List of extracted numbers
    """
    return re.findall(r'\d+', text)


def clean_text(text):
    """
    Clean and normalize extracted text.
    
    Args:
        text: Raw text string
        
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters except common punctuation
    text = re.sub(r'[^\w\s\-\.,:/]', '', text)
    
    return text.strip()


def format_report_json(parsed_details, face_verification, fraud_detection):
    """
    Format verification results as JSON.
    
    Args:
        parsed_details: Dictionary of parsed document fields
        face_verification: Dictionary of face verification results
        fraud_detection: Dictionary of fraud detection results
        
    Returns:
        dict: Formatted JSON report
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "document_data": parsed_details,
        "face_verification": face_verification,
        "fraud_detection": fraud_detection,
        "status": determine_overall_status(
            parsed_details, 
            face_verification, 
            fraud_detection
        )
    }


def determine_overall_status(parsed_details, face_verification, fraud_detection):
    """
    Determine overall KYC verification status.
    
    Args:
        parsed_details: Dictionary of parsed fields
        face_verification: Face verification results
        fraud_detection: Fraud detection results
        
    Returns:
        str: Overall status message
    """
    if fraud_detection.get('fraud_score', 0) >= 60:
        return "REJECTED - High fraud risk"
    
    if not face_verification.get('match', False):
        return "REJECTED - Face mismatch"
    
    missing_critical = sum(
        1 for v in parsed_details.values() 
        if v == "Not found"
    )
    
    if missing_critical > 3:
        return "MANUAL REVIEW REQUIRED"
    
    return "VERIFIED"


def save_verification_log(report, log_file="kyc_logs.txt"):
    """
    Save verification report to log file.
    
    Args:
        report: Verification report string
        log_file: Path to log file
        
    Returns:
        bool: Success status
    """
    try:
        with open(log_file, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(report)
            f.write(f"\n{'='*50}\n")
        return True
    except Exception as e:
        print(f"Error saving log: {e}")
        return False