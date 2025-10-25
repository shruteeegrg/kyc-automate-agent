"""
KYC Verification Agent
======================

A comprehensive AI-driven solution for automated customer onboarding
with document OCR, facial recognition, and fraud detection.

Features:
---------
- Document text extraction using EasyOCR
- Face verification using DeepFace
- Fraud risk assessment
- Support for multiple document types

Example:
--------
    >>> from src.kyc_agent import KYCAgent
    >>> agent = KYCAgent()
    >>> result = agent.process_kyc(id_card, selfie)

Author: Shruti Gurung
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Shruti Gurung"
__email__ = "gurungshrutee44@gmail.com"

from .kyc_agent import KYCAgent

__all__ = ['KYCAgent']