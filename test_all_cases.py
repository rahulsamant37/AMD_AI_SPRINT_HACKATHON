#!/usr/bin/env python3
"""
Test all cases from TestCases.ipynb against the /receive endpoint
"""
import json
import requests
import time
from pprint import pprint

def test_case_1():
    """Test Case 1: Both USERONE & USERTWO are available"""
    print("="*60)
    print("TEST CASE 1: Both users available")
    print("="*60)
    
    test_data = {
        "Request_id": "6118b54f-907b-4451-8d48-dd13d76033a5",
        "Datetime": "02-07-2025T12:34:55",
        "Location": "IIT Mumbai",
        "From": "teamadmin.amd@gmail.com",
        "Attendees": [
            {"email": "userone.amd@gmail.com"},
            {"email": "usertwo.amd@gmail.com"}
        ],
        "EmailContent": "Hi Team. Let's meet next Thursday and discuss about our Goals."
    }
    
    return run_test(test_data, "Test Case 1")

def test_case_2():
    """Test Case 2: USERONE available, USERTWO busy"""
    print("="*60)
    print("TEST CASE 2: USERONE available, USERTWO busy")
    print("="*60)
    
    test_data = {
        "Request_id": "6118b54f-907b-4451-8d48-dd13d76033b5",
        "Datetime": "02-07-2025T12:34:55",
        "Location": "IIT Mumbai",
        "From": "teamadmin.amd@gmail.com",
        "Attendees": [
            {"email": "userone.amd@gmail.com"},
            {"email": "usertwo.amd@gmail.com"}
        ],
        "EmailContent": "Hi Team. We've just received quick feedback from the client indicating that the instructions we provided aren't working on their end. Let's prioritize resolving this promptly. Let's meet Monday at 9:00 AM to discuss and resolve this issue."
    }
    
    return run_test(test_data, "Test Case 2")

def test_case_3():
    """Test Case 3: Both USERONE & USERTWO are busy"""
    print("="*60)
    print("TEST CASE 3: Both users busy")
    print("="*60)
    
    test_data = {
        "Request_id": "6118b54f-907b-4451-8d48-dd13d76033c5",
        "Datetime": "02-07-2025T12:34:55",
        "Location": "IIT Mumbai",
        "From": "teamadmin.amd@gmail.com",
        "Attendees": [
            {"email": "userone.amd@gmail.com"},
            {"email": "usertwo.amd@gmail.com"}
        ],
        "EmailContent": "Hi Team. Let's meet on Tuesday at 11:00 A.M and discuss about our on-going Projects."
    }
    
    return run_test(test_data, "Test Case 3")

def test_case_4():
    """Test Case 4: USERONE free, USERTWO busy"""
    print("="*60)
    print("TEST CASE 4: USERONE free, USERTWO busy")
    print("="*60)
    
    test_data = {
        "Request_id": "6118b54f-907b-4451-8d48-dd13d76033d5",
        "Datetime": "02-07-2025T12:34:55",
        "Location": "IIT Mumbai",
        "From": "teamadmin.amd@gmail.com",
        "Attendees": [
            {"email": "userone.amd@gmail.com"},
            {"email": "usertwo.amd@gmail.com"}
        ],
        "EmailContent": "Hi Team. We've received the final feedback from the client. Let's review it together and plan next steps. Let's meet on Wednesday at 10:00 A.M."
    }
    
    return run_test(test_data, "Test Case 4")

def test_processed_input():
    """Test with processed input format (your previous test case)"""
    print("="*60)
    print("TEST CASE: Processed Input Format")
    print("="*60)
    
    test_data = {
        "Request_id": "6118b54f-907b-4451-8d48-dd13d76033b5",
        "Datetime": "02-07-2025T12:34:55",
        "Location": "IIT Mumbai",
        "From": "teamadmin.amd@gmail.com",
        "Attendees": [
            {"email": "userone.amd@gmail.com"},
            {"email": "usertwo.amd@gmail.com"}
        ],
        "EmailContent": "Hi Team. We've just received quick feedback...",
        "Start": "2025-07-14T09:00:00+05:30",
        "End": "2025-07-14T09:30:00+05:30",
        "Duration_mins": "30"
    }
    
    return run_test(test_data, "Processed Input Format")

def run_test(test_data, test_name):
    """Run a single test case"""
    url = "http://localhost:5000/receive"
    
    try:
        print(f"\n🧪 Running {test_name}...")
        print("📤 Request data:")
        pprint(test_data, width=80)
        print("\n" + "-"*40)
        
        # Make POST request
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_json = response.json()
            print("✅ SUCCESS!")
            print("📥 Response:")
            pprint(response_json, width=80)
            
            # Validate key fields
            if 'EventStart' in response_json and 'EventEnd' in response_json:
                print(f"⏰ Scheduled Time: {response_json['EventStart']} to {response_json['EventEnd']}")
            if 'Subject' in response_json:
                print(f"📝 Subject: {response_json['Subject']}")
            
            return True
        else:
            print("❌ FAILED!")
            try:
                error_json = response.json()
                print("📥 Error Response:")
                pprint(error_json, width=80)
            except:
                print(f"📥 Raw Response: {response.text}")
            return False
                
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to server. Make sure it's running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all test cases"""
    print("🚀 Starting comprehensive test suite for /receive endpoint")
    print("📍 Server: http://localhost:5000/receive")
    print("📅 Test Date: July 13, 2025 (Today)")
    
    # Check server connectivity first
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and healthy")
        else:
            print("⚠️  Server responded but health check failed")
    except:
        print("❌ Cannot connect to server. Please start the server first!")
        print("💡 Run: start_server.bat or python -m uvicorn app.main:app --port 5000")
        return
    
    print("\n" + "="*80)
    
    # Run all test cases
    results = []
    results.append(("Test Case 1", test_case_1()))
    time.sleep(1)  # Small delay between tests
    
    results.append(("Test Case 2", test_case_2()))
    time.sleep(1)
    
    results.append(("Test Case 3", test_case_3()))
    time.sleep(1)
    
    results.append(("Test Case 4", test_case_4()))
    time.sleep(1)
    
    results.append(("Processed Input", test_processed_input()))
    
    # Summary
    print("\n" + "="*80)
    print("📋 TEST SUMMARY")
    print("="*80)
    
    passed = 0
    failed = 0
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed out of {len(results)} tests")
    
    if failed == 0:
        print("🎉 All tests passed! The /receive endpoint is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
