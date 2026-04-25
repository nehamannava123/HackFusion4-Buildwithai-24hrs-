# test_ai.py - Simple AI Diagnostic
import os
from dotenv import load_dotenv

print("=" * 50)
print("CODE NAV AI DIAGNOSTIC")
print("=" * 50)

# Load .env file
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Check API key
print("\n1. Checking API Key:")
if api_key:
    print(f"   ✅ API Key found: {api_key[:15]}...")
    print(f"   Length: {len(api_key)} characters")
else:
    print("   ❌ API Key NOT found - Create .env file")

# Check import
print("\n2. Checking Google Gemini import:")
try:
    import google.generativeai as genai
    print("   ✅ Import successful")
except Exception as e:
    print(f"   ❌ Import failed: {e}")

# Test API call
if api_key:
    print("\n3. Testing API call:")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'API works'")
        print(f"   ✅ API Success: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ API Failed: {e}")
else:
    print("\n3. Skipping API test - no key")

print("\n" + "=" * 50)