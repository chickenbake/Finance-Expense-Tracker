from paddleocr import PaddleOCR
import cv2
import numpy as np
import os

os.environ['GLOG_minloglevel'] = '2'  # Suppress paddle warnings

def extract_receipt_data(image_path):
    # Read in Image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image from {image_path}")
        return ""

    # Preprocess
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.medianBlur(gray, 5)
    _, thresh = cv2.threshold(denoised, 150, 255, cv2.THRESH_BINARY)
    kernel = np.ones((1,1), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
    print("Preprocessing Completed!")

    # OCR Inference
    ocr = PaddleOCR(
        use_angle_cls=True,
        lang='en',
    )
    result = ocr.predict(input=img)
    print(f"OCR Result: {result}")

    # Extract Text in Structured Format
    lines = []
    if result and len(result) > 0:
        # The result structure is: [{'rec_texts': [...], 'rec_scores': [...], ...}]
        first_result = result[0]
        if 'rec_texts' in first_result:
            rec_texts = first_result['rec_texts']
            rec_scores = first_result.get('rec_scores', [])
            
            for i, text in enumerate(rec_texts):
                if i < len(rec_scores):
                    confidence = rec_scores[i]
                    if confidence > 0.69:
                        lines.append(text)
                        print(f"Text {i}: '{text}', Confidence: {confidence}")
                else:
                    lines.append(text)
                    print(f"Text: '{text}'")

    extracted_text = "\n".join(lines)
    return extracted_text

def parse_receipt(ocr_text):
    """
    Placeholder function for fine-tuned GPT-2 which will output JSON:
    {
        merchant: "..."
        description: "..."
        amount: "..."
        category: "..."
        payment_method: "..."
        date: "..."
    }
    """
    return {"raw_text": ocr_text}