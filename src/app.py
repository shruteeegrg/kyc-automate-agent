"""
Gradio Web Interface for KYC Verification Agent

This module provides a web-based interface for the KYC verification system.
Users can upload ID cards and selfies to verify their identity.
"""

import gradio as gr
from kyc_agent import KYCAgent

# Initialize KYC Agent
print("Initializing KYC Agent...")
agent = KYCAgent()
print("KYC Agent Ready.")


def kyc_interface(id_card, selfie):
    """
    Wrapper function for Gradio interface.
    
    Args:
        id_card: Uploaded ID card image (numpy array)
        selfie: Uploaded selfie image (numpy array)
        
    Returns:
        str: Formatted verification report
    """
    return agent.process_kyc(id_card, selfie)


# Create Gradio interface
iface = gr.Interface(
    fn=kyc_interface,
    inputs=[
        gr.Image(type="numpy", label="Upload ID Card"),
        gr.Image(type="numpy", label="Upload Selfie")
    ],
    outputs=[
        gr.Textbox(label="Verification Report", lines=20)
    ],
    title="🔐 AI-Powered KYC Verification Agent",
    description="""
    Upload an ID card and a selfie. The system will extract data, verify the face, and generate a risk report.
    
    **Supported Documents:** Passports, Driver's Licenses, National IDs, Citizenship Certificates
    
    **Tips for Best Results:**
    - Use high-resolution images (minimum 800x600)
    - Ensure good lighting without glare
    - Keep document flat and fully visible
    - Face should be clearly visible in selfie
    """,
    examples=[
        # Add example file paths here if you have sample images
        # ["examples/sample_id_card.jpg", "examples/sample_selfie.jpg"]
    ],
    theme=gr.themes.Soft()
)


if __name__ == "__main__":
    print("Launching KYC Verification Interface...")
    iface.launch(
        debug=True,
        share=True,
        server_name="0.0.0.0",  # Allow external access
        server_port=7860  # Default Gradio port
    )