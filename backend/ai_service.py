import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AIExpenseAnalyzer:
    def __init__(self):
        self.hf_token = os.getenv('HUGGING_FACE_TOKEN')
        self.base_url = "https://api-inference.huggingface.co/models"
        
    def categorize_expense(self, description):  # Remove 'async'
        """Categorize expense using Hugging Face API"""
        if not self.hf_token:
            return self._fallback_categorization(description)
            
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        model_url = f"{self.base_url}/facebook/bart-large-mnli"
        
        candidate_labels = [
            "Food and Dining", "Transportation", "Entertainment", 
            "Shopping", "Bills and Utilities", "Healthcare", 
            "Education", "Travel", "Other"
        ]
        
        payload = {
            "inputs": description,
            "parameters": {"candidate_labels": candidate_labels}
        }
        
        try:
            response = requests.post(model_url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result['labels'][0] if result['labels'] else 'Other'
            else:
                return self._fallback_categorization(description)
        except Exception as e:
            print(f"AI categorization error: {e}")
            return self._fallback_categorization(description)
    
    def get_spending_insights(self, expenses_data):
        # Generate spending insights using Hugging Face
        if not self.hf_token:
            return self._fallback_insights(expenses_data)
            
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        model_url = f"{self.base_url}/microsoft/DialoGPT-medium"
        
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
        # Simple keyword-based categorization as fallback
        description_lower = description.lower()
        
        food_keywords = ['restaurant', 'food', 'grocery', 'coffee', 'lunch', 'dinner', 'pizza', 'burger']
        transport_keywords = ['gas', 'uber', 'taxi', 'bus', 'train', 'parking', 'fuel']
        entertainment_keywords = ['movie', 'cinema', 'game', 'concert', 'music', 'netflix']
        shopping_keywords = ['amazon', 'store', 'mall', 'clothes', 'shoes', 'shopping']
        bills_keywords = ['electric', 'water', 'internet', 'phone', 'rent', 'mortgage', 'utility']
        
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