import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AIExpenseAnalyzer:
    def __init__(self):
        self.hf_token = os.getenv('HUGGING_FACE_TOKEN')
        if self.hf_token:
            self.hf_token = self.hf_token.strip()  # Remove any whitespace/newlines
        # Updated API URL to match the working sample
        self.api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
        print(f"HF Token exists: {bool(self.hf_token)}")  # Debug line
        
    def categorize_expense(self, description):
        """Categorize expense using Hugging Face API"""
        print(f"Categorizing: '{description}'")  # Debug line

        if not self.hf_token:
            print("No HF token, using fallback")  # Debug line
            return self._fallback_categorization(description)
            
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
        }
        
        candidate_labels = [
            "Food and Dining", "Transportation", "Entertainment", 
            "Shopping", "Bills and Utilities", "Healthcare", 
            "Education", "Travel", "Savings", "Other"
        ]
        
        # Enhanced input with more context for better categorization
        enhanced_input = f"This is an expense for: {description}. Categorize this expense."
        
        payload = {
            "inputs": enhanced_input,
            "parameters": {"candidate_labels": candidate_labels}
        }
        
        try:
            print("Calling Hugging Face API...")  # Debug line
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            print(f"API Response status: {response.status_code}")  # Debug line
            
            if response.status_code == 200:
                result = response.json()
                print(f"API Result: {result}")  # Debug line
                
                # Check if we have labels in the response
                if 'labels' in result and result['labels']:
                    best_category = result['labels'][0]
                    confidence = result['scores'][0] if 'scores' in result else 0
                    print(f"AI suggests: {best_category} (confidence: {confidence:.2f})")  # Debug line
                    
                    # Only use AI result if confidence is reasonable
                    if confidence > 0.17:
                        return best_category
                    else:
                        print(f"Low confidence, using fallback")
                        return self._fallback_categorization(description)
                else:
                    print("No labels in response, using fallback")  # Debug line
                    return self._fallback_categorization(description)
            else:
                print(f"API Error: {response.text}")  # Debug line
                return self._fallback_categorization(description)
        except Exception as e:
            print(f"AI categorization error: {e}")
            return self._fallback_categorization(description)
    
    def get_spending_insights(self, expenses_data):
        # Generate spending insights using Hugging Face
        if not self.hf_token:
            return self._fallback_insights(expenses_data)
            
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        model_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        # Create a summary of spending patterns
        total_amount = sum(exp['amount'] for exp in expenses_data)
        categories = {}
        for exp in expenses_data:
            cat = exp['category']
            categories[cat] = categories.get(cat, 0) + exp['amount']
        
        top_category = max(categories, key=categories.get) if categories else 'Unknown'
        
        prompt = f"""Based on spending data: Total: ${total_amount:.2f}, Top category: {top_category} (${categories.get(top_category, 0):.2f}). Give 2 brief budget tips."""
        
        payload = {"inputs": prompt}
        
        try:
            response = requests.post(model_url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result[0]['generated_text'] if result else self._fallback_insights(expenses_data)
            else:
                return self._fallback_insights(expenses_data)
        except Exception as e:
            print(f"AI insights error: {e}")
            return self._fallback_insights(expenses_data)
    
    def _fallback_categorization(self, description):
        """Simple keyword-based categorization as fallback"""
        description_lower = description.lower()
        
        food_keywords = ['restaurant', 'food', 'grocery', 'coffee', 'lunch', 'dinner', 'pizza', 'burger']
        transport_keywords = ['gas', 'uber', 'taxi', 'bus', 'train', 'parking', 'fuel']
        entertainment_keywords = ['movie', 'cinema', 'game', 'concert', 'music', 'netflix']
        shopping_keywords = ['amazon', 'store', 'mall', 'clothes', 'shoes', 'shopping']
        bills_keywords = ['electric', 'water', 'internet', 'phone', 'rent', 'mortgage', 'utility']
        healthcare_keywords = ['doctor', 'hospital', 'pharmacy', 'medicine', 'dental', 'medical', 'clinic', 'health']
        education_keywords = ['school', 'university', 'college', 'tuition', 'books', 'education', 'course', 'class']
        travel_keywords = ['hotel', 'flight', 'airline', 'vacation', 'trip', 'travel', 'airbnb', 'booking']
        
        
        if any(keyword in description_lower for keyword in food_keywords):
            return 'Food and Dining'
        elif any(keyword in description_lower for keyword in transport_keywords):
            return 'Transportation'
        elif any(keyword in description_lower for keyword in entertainment_keywords):
            return 'Entertainment'
        elif any(keyword in description_lower for keyword in shopping_keywords):
            return 'Shopping'
        elif any(keyword in description_lower for keyword in bills_keywords):
            return 'Bills and Utilities'
        elif any(keyword in description_lower for keyword in healthcare_keywords):
            return 'Healthcare'
        elif any(keyword in description_lower for keyword in education_keywords):
            return 'Education'
        elif any(keyword in description_lower for keyword in travel_keywords):
            return 'Travel'
        else:
            return 'Other'
    
    def _fallback_insights(self, expenses_data):
        # Generate basic insights without AI
        if not expenses_data:
            return "No expenses to analyze yet. Start tracking your spending!"
        
        total = sum(exp['amount'] for exp in expenses_data)
        avg_expense = total / len(expenses_data)
        
        return f"You've spent ${total:.2f} across {len(expenses_data)} transactions (avg: ${avg_expense:.2f}). Consider reviewing your largest expenses for potential savings."

# Create a global instance
ai_analyzer = AIExpenseAnalyzer()