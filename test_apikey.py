
import google.generativeai as genai
import os

def test_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY environment variable is not set.")
        return

    print(f"Found API Key: {api_key[:5]}...{api_key[-5:]}")
    
    genai.configure(api_key=api_key)
    
    print("\n--- Listing Available Models ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"[ERROR] Failed to list models: {e}")

    print("\n--- Testing Specific Model: gemini-3-flash-preview ---")
    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")
        response = model.generate_content("Hello from AI Studio!")
        print(f"[SUCCESS] Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Failed to generate content with 'gemini-3-flash-preview': {e}")

if __name__ == "__main__":
    test_key()
