"""Test Gemini API"""
import google.generativeai as genai

API_KEY = "AIzaSyCEb70gZDmeCbuh7i1QGbnkfE0Fw6VzX4M"

print("Testing Gemini API...")
print(f"API Key: {API_KEY[:20]}...")

try:
    genai.configure(api_key=API_KEY)
    
    # Try without generation_config
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("\n✓ Model initialized successfully")
    
    test_message = "Trả lời ngắn gọn bằng tiếng Việt: Bầu trời có mấy ngôi sao?"
    
    print(f"\nSending: {test_message}")
    
    response = model.generate_content(test_message)
    print(f"\n✓ API Call SUCCESS!")
    
    # Check response details
    print(f"\nResponse object: {response}")
    print(f"Candidates: {response.candidates}")
    
    if response.candidates:
        candidate = response.candidates[0]
        print(f"\nFinish reason: {candidate.finish_reason}")
        print(f"Safety ratings: {candidate.safety_ratings}")
    
    # Try to get text
    try:
        print(f"\nResponse text: {response.text}")
    except ValueError as ve:
        print(f"\n⚠ Cannot get text: {ve}")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"Message: {str(e)}")
    
    # Print full traceback
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

