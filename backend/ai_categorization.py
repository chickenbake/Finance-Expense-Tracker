import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AIExpenseAnalyzer:
    def __init__(self):
        self.hf_token = os.getenv('HUGGING_FACE_TOKEN')
        if self.hf_token:
            self.hf_token = self.hf_token.strip()  # Remove any whitespace/newlines
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
            # Food & Groceries
            'Groceries',
            'Eating Out',
            'Coffee & Snacks',
            # Transportation
            'Public Transit',
            'Rideshare & Taxi',
            'Fuel & Gas',
            'Car Payment',
            'Car Maintenance',
            'Parking & Tolls',
            # Housing & Utilities
            'Rent/Mortgage',
            'Electricity',
            'Water & Sewer',
            'Internet',
            'Mobile Phone',
            'Home Maintenance',
            # Insurance
            'Health Insurance',
            'Car Insurance',
            'Home/Renters Insurance',
            'Life Insurance',
            # Healthcare
            'Medical Bills',
            'Pharmacy',
            'Dental & Vision',
            # Personal & Family
            'Childcare',
            'Pet Care',
            'Personal Care',
            'Fitness & Sports',
            # Shopping
            'Clothing & Accessories',
            'Electronics',
            'Home & Garden',
            # Entertainment
            'Streaming Services',
            'Movies & Events',
            'Hobbies',
            # Education
            'Tuition',
            'Books & Supplies',
            'Courses & Subscriptions',
            # Travel
            'Flights',
            'Hotels & Lodging',
            'Vacation',
            # Savings & Investments
            'Retirement',
            'Emergency Fund',
            'Investments',
            # Gifts & Donations
            'Gifts',
            'Charity/Donations',
            # Miscellaneous
            'Taxes',
            'Fees',
            'Other'
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
        
        groceries_keywords = ['grocery', 'supermarket', 'groceries', 'market']
        eating_out_keywords = ['restaurant', 'dining', 'eat out', 'takeout', 'fast food', 'pizza', 'burger', 'cafe', 'bistro']
        coffee_snacks_keywords = ['coffee', 'snack', 'tea', 'bakery', 'donut', 'pastry']
        public_transit_keywords = ['bus', 'train', 'metro', 'subway', 'transit', 'commute']
        rideshare_taxi_keywords = ['uber', 'lyft', 'taxi', 'cab', 'rideshare']
        fuel_gas_keywords = ['gas', 'fuel', 'petrol', 'diesel']
        car_payment_keywords = ['car payment', 'auto loan', 'vehicle finance']
        car_maintenance_keywords = ['car repair', 'maintenance', 'oil change', 'tire', 'mechanic']
        parking_tolls_keywords = ['parking', 'toll', 'meter']
        rent_mortgage_keywords = ['rent', 'mortgage', 'lease']
        electricity_keywords = ['electric', 'electricity', 'power bill']
        water_sewer_keywords = ['water', 'sewer']
        internet_keywords = ['internet', 'wifi', 'broadband']
        mobile_phone_keywords = ['mobile', 'cell phone', 'phone bill']
        home_maintenance_keywords = ['home repair', 'plumber', 'electrician', 'appliance']
        health_insurance_keywords = ['health insurance', 'medical insurance']
        car_insurance_keywords = ['car insurance', 'auto insurance']
        home_renters_insurance_keywords = ['home insurance', 'renters insurance']
        life_insurance_keywords = ['life insurance']
        medical_bills_keywords = ['doctor', 'hospital', 'medical bill', 'clinic']
        pharmacy_keywords = ['pharmacy', 'medicine', 'prescription', 'drugstore']
        dental_vision_keywords = ['dental', 'dentist', 'vision', 'optometrist']
        childcare_keywords = ['childcare', 'daycare', 'babysitter', 'nanny']
        pet_care_keywords = ['pet', 'vet', 'grooming', 'pet food']
        personal_care_keywords = ['haircut', 'salon', 'spa', 'personal care']
        fitness_sports_keywords = ['gym', 'fitness', 'yoga', 'sports', 'workout']
        clothing_accessories_keywords = ['clothing', 'shoes', 'apparel', 'accessories']
        electronics_keywords = ['electronics', 'gadget', 'device', 'laptop', 'phone']
        home_garden_keywords = ['furniture', 'garden', 'decor', 'home improvement']
        streaming_services_keywords = ['netflix', 'hulu', 'disney+', 'streaming']
        movies_events_keywords = ['movie', 'cinema', 'event', 'concert', 'show']
        hobbies_keywords = ['hobby', 'craft', 'art', 'music lesson']
        tuition_keywords = ['tuition', 'school fee', 'enrollment']
        books_supplies_keywords = ['book', 'textbook', 'school supplies']
        courses_subscriptions_keywords = ['course', 'subscription', 'online class']
        flights_keywords = ['flight', 'airline', 'plane ticket']
        hotels_lodging_keywords = ['hotel', 'motel', 'lodging', 'bnb']
        vacation_keywords = ['vacation', 'holiday', 'trip', 'travel']
        retirement_keywords = ['retirement', 'ira', '401k']
        emergency_fund_keywords = ['emergency fund', 'rainy day']
        investments_keywords = ['investment', 'stock', 'bond', 'crypto']
        gifts_keywords = ['gift', 'present']
        charity_donations_keywords = ['charity', 'donation', 'nonprofit']
        taxes_keywords = ['tax', 'irs']
        fees_keywords = ['fee', 'charge', 'service fee']
        
        
        # Check each category
        if any(keyword in description_lower for keyword in groceries_keywords):
            return 'Groceries'
        elif any(keyword in description_lower for keyword in eating_out_keywords):
            return 'Eating Out'
        elif any(keyword in description_lower for keyword in coffee_snacks_keywords):
            return 'Coffee & Snacks'
        elif any(keyword in description_lower for keyword in public_transit_keywords):
            return 'Public Transit'
        elif any(keyword in description_lower for keyword in rideshare_taxi_keywords):
            return 'Rideshare & Taxi'
        elif any(keyword in description_lower for keyword in fuel_gas_keywords):
            return 'Fuel & Gas'
        elif any(keyword in description_lower for keyword in car_payment_keywords):
            return 'Car Payment'
        elif any(keyword in description_lower for keyword in car_maintenance_keywords):
            return 'Car Maintenance'
        elif any(keyword in description_lower for keyword in parking_tolls_keywords):
            return 'Parking & Tolls'
        elif any(keyword in description_lower for keyword in rent_mortgage_keywords):
            return 'Rent/Mortgage'
        elif any(keyword in description_lower for keyword in electricity_keywords):
            return 'Electricity'
        elif any(keyword in description_lower for keyword in water_sewer_keywords):
            return 'Water & Sewer'
        elif any(keyword in description_lower for keyword in internet_keywords):
            return 'Internet'
        elif any(keyword in description_lower for keyword in mobile_phone_keywords):
            return 'Mobile Phone'
        elif any(keyword in description_lower for keyword in home_maintenance_keywords):
            return 'Home Maintenance'
        elif any(keyword in description_lower for keyword in health_insurance_keywords):
            return 'Health Insurance'
        elif any(keyword in description_lower for keyword in car_insurance_keywords):
            return 'Car Insurance'
        elif any(keyword in description_lower for keyword in home_renters_insurance_keywords):
            return 'Home/Renters Insurance'
        elif any(keyword in description_lower for keyword in life_insurance_keywords):
            return 'Life Insurance'
        elif any(keyword in description_lower for keyword in medical_bills_keywords):
            return 'Medical Bills'
        elif any(keyword in description_lower for keyword in pharmacy_keywords):
            return 'Pharmacy'
        elif any(keyword in description_lower for keyword in dental_vision_keywords):
            return 'Dental & Vision'
        elif any(keyword in description_lower for keyword in childcare_keywords):
            return 'Childcare'
        elif any(keyword in description_lower for keyword in pet_care_keywords):
            return 'Pet Care'
        elif any(keyword in description_lower for keyword in personal_care_keywords):
            return 'Personal Care'
        elif any(keyword in description_lower for keyword in fitness_sports_keywords):
            return 'Fitness & Sports'
        elif any(keyword in description_lower for keyword in clothing_accessories_keywords):
            return 'Clothing & Accessories'
        elif any(keyword in description_lower for keyword in electronics_keywords):
            return 'Electronics'
        elif any(keyword in description_lower for keyword in home_garden_keywords):
            return 'Home & Garden'
        elif any(keyword in description_lower for keyword in streaming_services_keywords):
            return 'Streaming Services'
        elif any(keyword in description_lower for keyword in movies_events_keywords):
            return 'Movies & Events'
        elif any(keyword in description_lower for keyword in hobbies_keywords):
            return 'Hobbies'
        elif any(keyword in description_lower for keyword in tuition_keywords):
            return 'Tuition'
        elif any(keyword in description_lower for keyword in books_supplies_keywords):
            return 'Books & Supplies'
        elif any(keyword in description_lower for keyword in courses_subscriptions_keywords):
            return 'Courses & Subscriptions'
        elif any(keyword in description_lower for keyword in flights_keywords):
            return 'Flights'
        elif any(keyword in description_lower for keyword in hotels_lodging_keywords):
            return 'Hotels & Lodging'
        elif any(keyword in description_lower for keyword in vacation_keywords):
            return 'Vacation'
        elif any(keyword in description_lower for keyword in retirement_keywords):
            return 'Retirement'
        elif any(keyword in description_lower for keyword in emergency_fund_keywords):
            return 'Emergency Fund'
        elif any(keyword in description_lower for keyword in investments_keywords):
            return 'Investments'
        elif any(keyword in description_lower for keyword in gifts_keywords):
            return 'Gifts'
        elif any(keyword in description_lower for keyword in charity_donations_keywords):
            return 'Charity/Donations'
        elif any(keyword in description_lower for keyword in taxes_keywords):
            return 'Taxes'
        elif any(keyword in description_lower for keyword in fees_keywords):
            return 'Fees'
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