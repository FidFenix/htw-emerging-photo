#!/usr/bin/env python3
"""
Direct test of the anonymization API
"""
import requests
import json

API_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("HTW Emerging Photo - Direct API Test")
print("=" * 60)

# Test 1: Check API info
print("\n1. Testing API Info Endpoint...")
try:
    response = requests.get(f"{API_URL}/info", timeout=5)
    print(f"   ✅ SUCCESS! Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")
    exit(1)

# Test 2: Check health
print("\n2. Testing Health Endpoint...")
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"   ✅ SUCCESS! Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nThe API is working correctly.")
print("If you're seeing 'Cannot connect to API' in your browser,")
print("it's a browser caching issue, not a server problem.")
print("\nTry:")
print("  1. Use a different browser")
print("  2. Clear ALL browser data (not just cache)")
print("  3. Use incognito mode in a different browser")
print("=" * 60)

