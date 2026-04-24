"""
Test script for Sentiment Analysis API
Tests all endpoints and functionality
"""

import requests
import json
import sys
from typing import Dict, Any

# Configuration
API_URL = "http://localhost:5000"
TIMEOUT = 10

# Test cases
TEST_CASES = [
    {
        "name": "Positive Sentiment",
        "text": "I absolutely love this product! It's amazing and works perfectly.",
        "expected": "Positive"
    },
    {
        "name": "Negative Sentiment",
        "text": "This is the worst experience ever. Terrible quality and poor service.",
        "expected": "Negative"
    },
    {
        "name": "Neutral-Positive",
        "text": "The product works as described.",
        "expected": "Positive"
    },
    {
        "name": "Neutral-Negative",
        "text": "It doesn't work as expected.",
        "expected": "Negative"
    },
    {
        "name": "Strong Positive",
        "text": "Excellent! Best purchase ever. Highly recommended to everyone!",
        "expected": "Positive"
    },
    {
        "name": "Strong Negative",
        "text": "Awful! Complete waste of money. Never buying again!",
        "expected": "Negative"
    },
]

ERROR_CASES = [
    {
        "name": "Empty Text",
        "data": {"text": ""},
        "expect_error": True
    },
    {
        "name": "Missing Text Field",
        "data": {},
        "expect_error": True
    },
    {
        "name": "Null Text",
        "data": {"text": None},
        "expect_error": True
    },
]


class bcolors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print section header"""
    print(f"\n{bcolors.HEADER}{bcolors.BOLD}{'=' * 70}{bcolors.ENDC}")
    print(f"{bcolors.HEADER}{bcolors.BOLD}{text}{bcolors.ENDC}")
    print(f"{bcolors.HEADER}{bcolors.BOLD}{'=' * 70}{bcolors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{bcolors.OKGREEN}✓ {text}{bcolors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{bcolors.FAIL}✗ {text}{bcolors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{bcolors.OKCYAN}ℹ {text}{bcolors.ENDC}")


def test_health_endpoint():
    """Test health check endpoint"""
    print_header("Testing Health Endpoint")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Health endpoint responding")
            print(f"  Status: {data.get('status')}")
            print(f"  Service: {data.get('service')}")
            print(f"  Version: {data.get('version')}")
            return True
        else:
            print_error(f"Health endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Failed to reach health endpoint: {e}")
        return False


def test_index_endpoint():
    """Test index endpoint"""
    print_header("Testing Index Endpoint")
    
    try:
        response = requests.get(f"{API_URL}/", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Index endpoint responding")
            print(f"  Message: {data.get('message')}")
            return True
        else:
            print_error(f"Index endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Failed to reach index endpoint: {e}")
        return False


def test_predictions():
    """Test sentiment predictions"""
    print_header("Testing Sentiment Predictions")
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(TEST_CASES, 1):
        name = test_case['name']
        text = test_case['text']
        expected = test_case['expected']
        
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json={"text": text},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                prediction = data.get('prediction')
                confidence = data.get('confidence')
                
                # Check if prediction matches expected
                if prediction == expected:
                    print_success(f"Test {i}: {name}")
                    print(f"  Text: {text[:50]}...")
                    print(f"  Prediction: {prediction} ({confidence:.4f})")
                    passed += 1
                else:
                    print_error(f"Test {i}: {name}")
                    print(f"  Expected: {expected}, Got: {prediction}")
                    print(f"  Confidence: {confidence:.4f}")
                    failed += 1
            else:
                print_error(f"Test {i}: {name} - Status {response.status_code}")
                failed += 1
        
        except Exception as e:
            print_error(f"Test {i}: {name} - {e}")
            failed += 1
    
    print(f"\n{bcolors.OKBLUE}Predictions: {passed} passed, {failed} failed{bcolors.ENDC}")
    return failed == 0


def test_error_handling():
    """Test error handling"""
    print_header("Testing Error Handling")
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(ERROR_CASES, 1):
        name = test_case['name']
        data = test_case['data']
        
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=data,
                timeout=TIMEOUT
            )
            
            if response.status_code >= 400:
                error_data = response.json()
                if not error_data.get('success', True):
                    print_success(f"Test {i}: {name} - Correctly rejected")
                    print(f"  Error: {error_data.get('error')}")
                    passed += 1
                else:
                    print_error(f"Test {i}: {name} - Should have failed")
                    failed += 1
            else:
                print_error(f"Test {i}: {name} - Should return 400+")
                failed += 1
        
        except Exception as e:
            print_error(f"Test {i}: {name} - {e}")
            failed += 1
    
    print(f"\n{bcolors.OKBLUE}Error Handling: {passed} passed, {failed} failed{bcolors.ENDC}")
    return failed == 0


def test_performance():
    """Test API performance"""
    print_header("Testing Performance")
    
    import time
    
    text = "This is a test sentence for performance measurement."
    times = []
    
    print_info("Running 5 predictions to measure speed...")
    
    for i in range(5):
        try:
            start = time.time()
            response = requests.post(
                f"{API_URL}/predict",
                json={"text": text},
                timeout=TIMEOUT
            )
            elapsed = (time.time() - start) * 1000  # Convert to ms
            
            if response.status_code == 200:
                times.append(elapsed)
                print(f"  Prediction {i+1}: {elapsed:.2f}ms")
            else:
                print_error(f"Prediction {i+1} failed")
        
        except Exception as e:
            print_error(f"Prediction {i+1} failed: {e}")
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n{bcolors.OKGREEN}Performance Results:{bcolors.ENDC}")
        print(f"  Average: {avg_time:.2f}ms")
        print(f"  Min: {min_time:.2f}ms")
        print(f"  Max: {max_time:.2f}ms")
        print(f"  Throughput: {1000/avg_time:.1f} requests/sec")
        return True
    else:
        return False


def main():
    """Run all tests"""
    print(f"{bcolors.BOLD}{bcolors.OKCYAN}")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "SENTIMENT ANALYSIS API TEST SUITE" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")
    print(f"{bcolors.ENDC}")
    
    print_info(f"Testing API at: {API_URL}")
    
    # Run tests
    results = {
        "Health Endpoint": test_health_endpoint(),
        "Index Endpoint": test_index_endpoint(),
        "Predictions": test_predictions(),
        "Error Handling": test_error_handling(),
        "Performance": test_performance(),
    }
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{bcolors.OKGREEN}✓ PASSED{bcolors.ENDC}" if result else f"{bcolors.FAIL}✗ FAILED{bcolors.ENDC}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{bcolors.BOLD}Overall: {passed}/{total} test suites passed{bcolors.ENDC}\n")
    
    if passed == total:
        print(f"{bcolors.OKGREEN}{bcolors.BOLD}✓ All tests passed!{bcolors.ENDC}\n")
        return 0
    else:
        print(f"{bcolors.FAIL}{bcolors.BOLD}✗ Some tests failed{bcolors.ENDC}\n")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{bcolors.WARNING}Tests interrupted by user{bcolors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"{bcolors.FAIL}Test error: {e}{bcolors.ENDC}")
        sys.exit(1)
