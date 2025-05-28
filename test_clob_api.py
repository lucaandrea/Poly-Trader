#!/usr/bin/env python3
import requests
import json
from typing import Dict, Any, Optional

def test_clob_endpoints():
    """
    Test various CLOB API endpoints to diagnose connection issues
    """
    print("=" * 80)
    print("POLYMARKET CLOB API DIAGNOSTIC TEST")
    print("=" * 80)
    
    base_url = "https://clob.polymarket.com"
    
    # Test endpoints to try
    endpoints_to_test = [
        "/ping",
        "/health", 
        "/status",
        "/markets",
        "/books",
        "/book",
        "/prices"
    ]
    
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print("\n1. Testing CLOB API Base Endpoints:")
    print("-" * 40)
    
    for endpoint in endpoints_to_test:
        try:
            url = f"{base_url}{endpoint}"
            print(f"Testing: {url}")
            
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  Response: {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"  Response: {response.text[:200]}...")
            else:
                print(f"  Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"  Exception: {str(e)}")
        
        print()
    
    print("\n2. Testing Market Data from Gamma API:")
    print("-" * 40)
    
    # Test getting a sample token ID from Gamma API
    try:
        gamma_url = "https://gamma-api.polymarket.com/markets"
        params = {"limit": 5, "active": True}
        
        response = requests.get(gamma_url, params=params, headers=headers)
        
        if response.status_code == 200:
            markets = response.json()
            print(f"Retrieved {len(markets)} markets from Gamma API")
            
            for i, market in enumerate(markets[:3]):
                question = market.get("question", "Unknown")
                token_ids = market.get("clobTokenIds", [])
                
                print(f"\nMarket {i+1}: {question}")
                print(f"Token IDs: {token_ids}")
                
                # Test order book for first token ID
                if token_ids and len(token_ids) > 0:
                    if isinstance(token_ids, list):
                        first_token = str(token_ids[0])
                    else:
                        # Try to parse the token IDs string
                        try:
                            import ast
                            parsed_tokens = ast.literal_eval(str(token_ids))
                            if isinstance(parsed_tokens, list) and len(parsed_tokens) > 0:
                                first_token = str(parsed_tokens[0])
                            else:
                                first_token = str(token_ids)
                        except:
                            first_token = str(token_ids)
                    
                    print(f"Testing order book for token: {first_token}")
                    test_order_book_for_token(first_token)
                
        else:
            print(f"Failed to get markets from Gamma API: {response.status_code}")
            
    except Exception as e:
        print(f"Error testing Gamma API: {str(e)}")

def test_order_book_for_token(token_id: str):
    """
    Test various order book endpoint formats for a specific token
    """
    endpoints_to_test = [
        f"https://clob.polymarket.com/book?token_id={token_id}",
        f"https://clob.polymarket.com/books?token_id={token_id}",
        f"https://clob.polymarket.com/book/{token_id}",
        f"https://clob.polymarket.com/books/{token_id}",
        f"https://clob.polymarket.com/price?token_id={token_id}",
        f"https://clob.polymarket.com/prices?token_id={token_id}",
    ]
    
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    for url in endpoints_to_test:
        try:
            print(f"  Trying: {url}")
            response = requests.get(url, headers=headers, timeout=5)
            print(f"    Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"    Success! Data: {json.dumps(data, indent=2)[:150]}...")
                    return data  # Return first successful response
                except:
                    print(f"    Text response: {response.text[:100]}...")
            else:
                print(f"    Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"    Exception: {str(e)}")
    
    print(f"  ❌ No working endpoint found for token {token_id}")
    return None

def test_polymarket_web_api():
    """
    Test alternative web APIs that might be available
    """
    print("\n3. Testing Alternative Polymarket APIs:")
    print("-" * 40)
    
    web_endpoints = [
        "https://polymarket.com/api/markets",
        "https://api.polymarket.com/markets",
        "https://strapi-matic.polymarket.com/markets",
    ]
    
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    for url in web_endpoints:
        try:
            print(f"Testing: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  Success! Found {len(data) if isinstance(data, list) else 'data'}")
                except:
                    print(f"  Response: {response.text[:200]}...")
            else:
                print(f"  Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"  Exception: {str(e)}")
        
        print()

if __name__ == "__main__":
    test_clob_endpoints()
    test_polymarket_web_api()
    
    print("\n" + "=" * 80)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 80)
    print("\n💡 Tips:")
    print("1. If CLOB API is unavailable, the simplified betting approach should still work")
    print("2. Check if Polymarket requires API authentication for CLOB access") 
    print("3. Some endpoints might be region-restricted")
    print("4. Consider using the Gamma API for market data instead of CLOB") 