#!/usr/bin/env python3
import requests
import json
import os
from dotenv import load_dotenv
from eth_account import Account

# Load environment variables
load_dotenv()

def check_usdc_balance():
    # Get private key from environment
    private_key = os.getenv("POLYGON_WALLET_PRIVATE_KEY", "")
    
    if not private_key:
        print("No private key found in environment variables")
        return
    
    # Add 0x prefix if missing
    if not private_key.startswith("0x"):
        private_key = "0x" + private_key
    
    # Get wallet address from private key
    try:
        account = Account.from_key(private_key)
        wallet_address = account.address
        print(f"Wallet address: {wallet_address}")
    except Exception as e:
        print(f"Error getting wallet address: {e}")
        return
    
    # Multiple USDC contract addresses on Polygon
    usdc_contracts = {
        "USDC (PoS)": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",  # Most common
        "USDC.e (Bridged)": "0xA0b86a33E6441c8C4D86Fc4DebFd8B4cE3d80b7B",  # Bridged from Ethereum
        "Native USDC": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"   # Native Circle USDC
    }
    
    # Polygon RPC URL
    rpc_url = "https://polygon-rpc.com"
    
    total_usdc = 0.0
    found_balances = []
    
    for name, contract_address in usdc_contracts.items():
        try:
            print(f"\nChecking {name} at {contract_address}...")
            
            # Create ERC20 balanceOf function call data
            function_signature = "0x70a08231"  # keccak256("balanceOf(address)") first 4 bytes
            address_param = wallet_address[2:].lower().zfill(64)  # Remove 0x and pad to 32 bytes
            data = function_signature + address_param
            
            # Create JSON-RPC request
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_call",
                "params": [
                    {
                        "to": contract_address,
                        "data": data
                    },
                    "latest"
                ],
                "id": 1
            }
            
            # Make request
            response = requests.post(rpc_url, json=payload)
            result = response.json()
            
            if "result" in result:
                # Convert hex result to decimal and divide by 10^6 (USDC has 6 decimals)
                balance_hex = result["result"]
                balance_int = int(balance_hex, 16)
                balance_usdc = balance_int / 10**6
                
                print(f"  Balance: {balance_usdc} USDC")
                
                if balance_usdc > 0:
                    total_usdc += balance_usdc
                    found_balances.append((name, balance_usdc, contract_address))
            else:
                print(f"  Error: {result.get('error')}")
                
        except Exception as e:
            print(f"  Error checking {name}: {e}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if found_balances:
        print(f"Total USDC found: {total_usdc} USDC")
        print("\nBreakdown by contract:")
        for name, balance, contract in found_balances:
            print(f"  {name}: {balance} USDC ({contract})")
        
        print(f"\nGreat! You have USDC in your wallet.")
        print("Now you need to approve the Polymarket Exchange to spend it.")
        print("Run 'python approve_usdc.py' to approve spending.")
        
        # Check current allowances
        print("\nChecking current allowances for Polymarket...")
        polymarket_exchange = "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"
        
        for name, balance, contract in found_balances:
            try:
                # Check allowance
                function_signature = "0xdd62ed3e"  # allowance(owner,spender)
                owner_param = wallet_address[2:].lower().zfill(64)
                spender_param = polymarket_exchange[2:].lower().zfill(64)
                data = function_signature + owner_param + spender_param
                
                payload = {
                    "jsonrpc": "2.0",
                    "method": "eth_call",
                    "params": [
                        {
                            "to": contract,
                            "data": data
                        },
                        "latest"
                    ],
                    "id": 1
                }
                
                response = requests.post(rpc_url, json=payload)
                result = response.json()
                
                if "result" in result:
                    allowance_hex = result["result"]
                    allowance_int = int(allowance_hex, 16)
                    allowance_usdc = allowance_int / 10**6
                    
                    print(f"  {name} allowance: {allowance_usdc} USDC")
                    
                    if allowance_usdc >= balance:
                        print(f"    ✅ Sufficient allowance for {name}")
                    else:
                        print(f"    ❌ Need to approve {name} for spending")
            except Exception as e:
                print(f"  Error checking allowance for {name}: {e}")
                
    else:
        print("No USDC found in any of the checked contracts.")
        print("This could mean:")
        print("1. Your withdrawal is still processing")
        print("2. Your USDC is in a different network (Ethereum, Base, etc.)")
        print("3. You have a different token that looks like USDC")
        print(f"\nCheck your wallet on PolygonScan: https://polygonscan.com/address/{wallet_address}")

if __name__ == "__main__":
    print("=" * 60)
    print("COMPREHENSIVE POLYMARKET USDC BALANCE CHECKER")
    print("=" * 60)
    check_usdc_balance() 