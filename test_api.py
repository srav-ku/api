
#!/usr/bin/env python3
"""
Test script for Movie API v2 - Database & API Key Edition
Tests all endpoints with proper API key authentication
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
# BASE_URL = "https://your-replit-url.repl.co"  # Use this for deployed version

def test_api():
    """Test all API endpoints"""
    print("🎬 Testing Movie API v2 - Database & API Key Edition")
    print("=" * 60)
    
    # Test 1: Root endpoint (no API key required)
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint works!")
            print(f"   Version: {data.get('version')}")
            print(f"   Features: {len(data.get('features', []))} features available")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        return False
    
    # Test 2: Create API key (admin endpoint)
    print("\n2. Creating test API key...")
    try:
        api_key_request = {
            "owner_name": "Test User",
            "plan": "free",
            "monthly_limit": 1000
        }
        response = requests.post(f"{BASE_URL}/admin/api-keys", json=api_key_request)
        if response.status_code == 200:
            api_key_data = response.json()
            api_key = api_key_data["key"]
            print(f"✅ API key created successfully!")
            print(f"   API Key: {api_key}")
            print(f"   Owner: {api_key_data['owner_name']}")
            print(f"   Plan: {api_key_data['plan']}")
        else:
            print(f"❌ Failed to create API key: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating API key: {e}")
        return False
    
    # Headers for authenticated requests
    headers = {"X-API-KEY": api_key}
    
    # Test 3: Get movies with pagination
    print("\n3. Testing movies endpoint with pagination...")
    try:
        response = requests.get(f"{BASE_URL}/movies?page=1&per_page=5", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Movies endpoint works!")
            print(f"   Total movies: {data['total_movies']}")
            print(f"   Movies on page 1: {len(data['movies'])}")
            print(f"   Total pages: {data['total_pages']}")
            if data['movies']:
                print(f"   First movie: {data['movies'][0]['title']} ({data['movies'][0]['year']})")
        else:
            print(f"❌ Movies endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing movies endpoint: {e}")
    
    # Test 4: Search movies
    print("\n4. Testing search endpoint...")
    try:
        # Search by title
        response = requests.get(f"{BASE_URL}/search?title=god", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search by title works!")
            print(f"   Results for 'god': {data['total_results']} movies")
            if data['movies']:
                for movie in data['movies'][:3]:  # Show first 3 results
                    print(f"   - {movie['title']} ({movie['year']})")
        
        # Search by year
        response = requests.get(f"{BASE_URL}/search?year=1994", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search by year works!")
            print(f"   Results for year 1994: {data['total_results']} movies")
        
        # Search by genre
        response = requests.get(f"{BASE_URL}/search?genre=drama", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search by genre works!")
            print(f"   Results for 'drama': {data['total_results']} movies")
        
    except Exception as e:
        print(f"❌ Error testing search endpoint: {e}")
    
    # Test 5: Get movie by ID
    print("\n5. Testing movie detail endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/movies/1", headers=headers)
        if response.status_code == 200:
            movie = response.json()
            print(f"✅ Movie detail endpoint works!")
            print(f"   Movie: {movie['title']} ({movie['year']})")
            print(f"   Director: {movie['director']}")
            print(f"   Genres: {', '.join(movie['genre'])}")
        else:
            print(f"❌ Movie detail endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing movie detail endpoint: {e}")
    
    # Test 6: Get API key usage stats
    print("\n6. Testing usage stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api-key/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Usage stats endpoint works!")
            print(f"   Usage: {stats['usage_count']}/{stats['monthly_limit']} requests")
            print(f"   Usage percentage: {stats['usage_percentage']}%")
            print(f"   Plan: {stats['plan']}")
        else:
            print(f"❌ Usage stats endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing usage stats endpoint: {e}")
    
    # Test 7: Admin stats
    print("\n7. Testing admin stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/admin/stats")
        if response.status_code == 200:
            admin_stats = response.json()
            print(f"✅ Admin stats endpoint works!")
            print(f"   Total API keys: {admin_stats['total_api_keys']}")
            print(f"   Active API keys: {admin_stats['active_api_keys']}")
            print(f"   Total movies: {admin_stats['total_movies']}")
        else:
            print(f"❌ Admin stats endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing admin stats endpoint: {e}")
    
    # Test 8: Test without API key (should fail)
    print("\n8. Testing authentication (should fail without API key)...")
    try:
        response = requests.get(f"{BASE_URL}/movies")
        if response.status_code == 401:
            print(f"✅ Authentication working correctly!")
            print(f"   Correctly rejected request without API key")
        else:
            print(f"⚠️ Authentication might have issues: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing authentication: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 API testing completed!")
    print(f"🔑 Your test API key: {api_key}")
    print("💡 Use this API key to test the endpoints manually")
    
    return True

if __name__ == "__main__":
    print("Starting API tests...")
    print("Make sure the API server is running on http://localhost:5000")
    print("Waiting 2 seconds for server to be ready...")
    time.sleep(2)
    
    success = test_api()
    if success:
        print("\n✅ All tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Check the server logs.")
