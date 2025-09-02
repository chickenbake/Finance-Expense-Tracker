from paddleocr import PaddleOCR
import cv2

def extract_receipt_data(image_path):
    # Preprocesses
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # OCR
    ocr = PaddleOCR(lang='en')
    result = ocr.ocr(thresh, cls=True)

    # Combine text lines
    lines = []
    for line in result:
        for word_info in line:
            lines.append(word_info[1][0])
    return "\n".join(lines)

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