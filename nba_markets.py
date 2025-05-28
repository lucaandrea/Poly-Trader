#!/usr/bin/env python3
import requests
import datetime
import time
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta, timezone

def get_active_sports_markets() -> List[Dict[str, Any]]:
    """
    Fetch active sports markets from Polymarket with working order books
    """
    print("Fetching active sports markets...")
    
    # Step 1: Get all active markets
    markets_url = "https://gamma-api.polymarket.com/markets"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    
    params = {
        "limit": 100,  # Get up to 100 markets
        "active": True,  # Only get active markets
        "order": "volume24hr",  # Order by recent volume
        "ascending": False  # Most active first
    }
    
    # Try adding date filters to get more recent markets
    recent_date = (datetime.now(timezone.utc) - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # Try multiple API calls with different parameters to find current markets
    api_attempts = [
        # Attempt 1: Basic active markets
        {"limit": 100, "active": True, "order": "volume24hr", "ascending": False},
        
        # Attempt 2: Try with date filtering
        {"limit": 100, "active": True, "order": "endDate", "ascending": False},
        
        # Attempt 3: All markets, we'll filter client-side
        {"limit": 200, "order": "volume24hr", "ascending": False}
    ]
    
    try:
        response = requests.get(markets_url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch markets: {response.status_code}")
            return []
        
        all_markets = response.json()
        
        if not isinstance(all_markets, list):
            print("Unexpected API response format")
            return []
        
        print(f"Retrieved {len(all_markets)} active markets from Polymarket")
        
        # Step 2: Filter for tradable markets (with CLOB token IDs)
        tradable_markets = [
            market for market in all_markets 
            if market.get("clobTokenIds") and len(market.get("clobTokenIds", [])) > 0
        ]
        
        # Step 3: Filter for sports-related markets
        sports_keywords = [
            # NBA terms
            "nba", "basketball", "lakers", "celtics", "warriors", "knicks", "heat", "bucks",
            
            # MLB terms
            "mlb", "baseball", "yankees", "dodgers", "astros", "braves",
            
            # NFL terms
            "nfl", "football", "chiefs", "49ers", "cowboys", "eagles",
            
            # Soccer terms
            "soccer", "football", "premier league", "uefa", "champions league", "fifa", "world cup",
            "manchester united", "liverpool", "barcelona", "real madrid", "bayern",
            
            # Tennis terms
            "tennis", "atp", "wta", "grand slam", "wimbledon", "us open", "australian open",
            
            # General sports terms
            "sports", "game", "match", "playoff", "finals", "champion", "tournament"
        ]
        
        sports_markets = []
        for market in tradable_markets:
            question = market.get("question", "").lower()
            description = market.get("description", "").lower()
            
            # Check if any sports keyword is in the market text
            if any(keyword in question or keyword in description for keyword in sports_keywords):
                # Validate with game-related terms
                if any(term in question or term in description for term in ["win", "game", "vs", "score", "defeat", "champion", "match"]):
                    sports_markets.append(market)
        
        print(f"Found {len(sports_markets)} sports-related markets")
        
        # Step 4: Check for active order books
        active_markets = []
        for market in sports_markets:
            # Get token IDs
            token_ids = parse_token_ids(market)
            
            # Check if any token ID has an active order book
            has_active_book = False
            for token_id in token_ids:
                book = get_order_book(token_id)
                if book and (book.get("asks") or book.get("bids")):
                    has_active_book = True
                    break
            
            if has_active_book:
                active_markets.append(market)
        
        print(f"Found {len(active_markets)} sports markets with active order books")
        return active_markets
        
    except Exception as e:
        print(f"Error fetching markets: {e}")
        return []

def parse_token_ids(market: Dict[str, Any]) -> List[str]:
    """
    Parse token IDs from market data
    """
    token_ids = market.get("clobTokenIds", [])
    
    # If token_ids is a string, try to parse it
    if isinstance(token_ids, str):
        try:
            # Try to parse as JSON
            import ast
            parsed = ast.literal_eval(token_ids)
            if isinstance(parsed, list):
                return parsed
        except:
            # Try simple bracket parsing
            if token_ids.startswith("[") and token_ids.endswith("]"):
                # Remove brackets and split by comma
                tokens = token_ids[1:-1].split(",")
                # Clean up each token
                return [t.strip(' "\'') for t in tokens if t.strip()]
            
            # If no parsing works, return as single item
            return [token_ids]
    
    # If it's already a list, return it
    elif isinstance(token_ids, list):
        # Make sure all items are strings
        return [str(token_id) for token_id in token_ids]
    
    # Return empty list if we couldn't parse token IDs
    return []

def parse_outcomes(market: Dict[str, Any]) -> List[str]:
    """
    Parse outcomes from market data
    """
    outcomes = market.get("outcomes", [])
    
    # If outcomes is already parsed, return it
    if isinstance(outcomes, list):
        return outcomes
    
    # If outcomes is a string, try to parse it
    if isinstance(outcomes, str):
        try:
            # Try to parse as JSON
            import ast
            parsed = ast.literal_eval(outcomes)
            if isinstance(parsed, list):
                return parsed
        except:
            # Try simple parsing
            if outcomes.startswith("[") and outcomes.endswith("]"):
                # Remove brackets and split by comma
                outcomes_list = outcomes[1:-1].split(",")
                # Clean up each outcome
                return [o.strip(' "\'') for o in outcomes_list if o.strip()]
            
            # If no parsing works, return as single item
            return [outcomes]
    
    # Return empty list if we couldn't parse outcomes
    return []

def get_order_book(token_id: str) -> Optional[Dict[str, Any]]:
    """
    Get the order book for a specific token from the CLOB API
    """
    try:
        # Updated CLOB API endpoint based on Polymarket docs
        url = "https://clob.polymarket.com/books"
        params = {"token_id": token_id}
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Handle both single book and array responses
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            elif isinstance(data, dict):
                return data
            else:
                return None
        else:
            # Try alternative endpoint structure
            alt_url = f"https://clob.polymarket.com/book/{token_id}"
            alt_response = requests.get(alt_url, headers=headers, timeout=10)
            
            if alt_response.status_code == 200:
                return alt_response.json()
            else:
                # Only log specific errors for debugging
                if response.status_code == 404:
                    token_short = f"{token_id[:10]}...{token_id[-10:]}" if len(token_id) > 20 else token_id
                    print(f"Order book not found for token {token_short}")
                return None
                
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching order book: {str(e)}")
        return None
    except Exception as e:
        print(f"Error fetching order book: {str(e)}")
        return None

def classify_market(question: str) -> str:
    """
    Classify a market into a sports category
    """
    question = question.lower()
    
    # NBA related
    if any(term in question for term in ["nba", "basketball", "lakers", "celtics", 
                                        "warriors", "nets", "knicks", "heat", "bucks"]):
        return "Basketball"
    
    # MLB related
    elif any(term in question for term in ["mlb", "baseball", "yankees", "dodgers", 
                                          "red sox", "cubs", "cardinals", "braves"]):
        return "Baseball"
    
    # NFL related
    elif any(term in question for term in ["nfl", "football", "super bowl", "chiefs", 
                                          "49ers", "cowboys", "packers", "eagles"]):
        return "Football"
    
    # Soccer related
    elif any(term in question for term in ["soccer", "premier league", "uefa", "fifa", 
                                        "manchester", "liverpool", "barcelona", "real madrid"]):
        return "Soccer"
    
    # Tennis related
    elif any(term in question for term in ["tennis", "atp", "wta", "grand slam", "wimbledon"]):
        return "Tennis"
    
    # General sports
    return "Other Sports"

def display_market(market: Dict[str, Any]) -> None:
    """
    Display detailed information about a market and its order books
    """
    # Get market details
    question = market.get("question", "Unknown Market")
    end_date = market.get("endDate", "Unknown")
    
    # Get sport category
    category = classify_market(question)
    
    # Parse end date if available
    if end_date != "Unknown":
        try:
            date_obj = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            end_date = date_obj.strftime("%Y-%m-%d %H:%M")
        except:
            pass
    
    # Get token IDs and outcomes
    token_ids = parse_token_ids(market)
    outcomes = parse_outcomes(market)
    
    # Display market header
    print("\n" + "=" * 70)
    print(f"SPORTS MARKET: {question}")
    print(f"Category: {category}")
    print(f"End Date: {end_date}")
    print("=" * 70)
    
    # Get order books for each token ID
    for i, (outcome, token_id) in enumerate(zip(outcomes, token_ids)):
        # Get order book for this token
        order_book = get_order_book(token_id)
        
        # Display outcome header
        token_short = f"{token_id[:10]}...{token_id[-10:]}" if len(token_id) > 20 else token_id
        print(f"\nOUTCOME: {outcome}")
        print(f"Token ID: {token_short}")
        
        if order_book and (order_book.get("bids") or order_book.get("asks")):
            # Display bid and ask data
            bids = order_book.get("bids", [])
            asks = order_book.get("asks", [])
            
            # Best bid and ask
            best_bid = f"{float(bids[0]['price']):.3f}" if bids else "None"
            best_ask = f"{float(asks[0]['price']):.3f}" if asks else "None"
            
            print(f"Best Bid: {best_bid}")
            print(f"Best Ask: {best_ask}")
            
            # Show order depth (up to 3 levels)
            if bids:
                print("\nBid Depth:")
                for j, bid in enumerate(bids[:3]):
                    print(f"  {float(bid['price']):.3f} - Size: {float(bid['size']):.1f}")
            
            if asks:
                print("\nAsk Depth:")
                for j, ask in enumerate(asks[:3]):
                    print(f"  {float(ask['price']):.3f} - Size: {float(ask['size']):.1f}")
        else:
            print("No active order book available")
        
        print("-" * 50)

def main() -> None:
    """
    Main function to fetch and display active sports markets
    """
    print("SPORTS BETTING MARKETS - ACTIVE MARKETS")
    print("=" * 70)
    
    # Get active sports markets
    sports_markets = get_active_sports_markets()
    
    if not sports_markets:
        print("\nNo active sports markets found with working order books.")
        print("Please try again later.")
        return
    
    # Group markets by category
    market_categories = {}
    for market in sports_markets:
        category = classify_market(market.get("question", ""))
        if category not in market_categories:
            market_categories[category] = []
        market_categories[category].append(market)
    
    # Print summary of markets by category
    print("\nActive markets by category:")
    for category, markets in market_categories.items():
        print(f"- {category}: {len(markets)} markets")
    
    # Display each market
    for market in sports_markets:
        display_market(market)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"Total sports markets with active order books: {len(sports_markets)}")
    print("=" * 70)

def get_sports_markets_simplified() -> List[Dict[str, Any]]:
    """
    Simplified version that gets sports markets without requiring active order books
    """
    print("Fetching sports markets (simplified version)...")
    
    # Step 1: Try multiple API approaches to get current markets
    markets_url = "https://gamma-api.polymarket.com/markets"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    
    # Try multiple API parameter combinations
    api_attempts = [
        # Attempt 1: Order by end date descending (most recent first)
        {"limit": 200, "active": True, "order": "endDate", "ascending": False},
        
        # Attempt 2: Order by volume (most active first)  
        {"limit": 200, "active": True, "order": "volume24hr", "ascending": False},
        
        # Attempt 3: All markets ordered by creation date
        {"limit": 200, "order": "createdAt", "ascending": False},
        
        # Attempt 4: Basic active call
        {"limit": 100, "active": True}
    ]
    
    all_markets = []
    
    for i, params in enumerate(api_attempts):
        try:
            print(f"API Attempt {i+1}: {params}")
            response = requests.get(markets_url, params=params, headers=headers)
            
            if response.status_code == 200:
                markets = response.json()
                
                if isinstance(markets, list) and len(markets) > 0:
                    print(f"  Retrieved {len(markets)} markets")
                    
                    # Check the date range of markets we got
                    current_time = datetime.now(timezone.utc)
                    recent_count = 0
                    
                    for market in markets[:10]:  # Check first 10 markets
                        end_date_str = market.get("endDate")
                        if end_date_str:
                            try:
                                end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
                                if end_date > current_time:
                                    recent_count += 1
                                else:
                                    question = market.get("question", "Unknown")[:50]
                                    print(f"    Sample expired: {question}... (ended {end_date.strftime('%Y-%m-%d')})")
                            except:
                                pass
                    
                    print(f"  Found {recent_count} current markets in first 10 checked")
                    
                    # If this attempt found recent markets, use it
                    if recent_count > 0:
                        all_markets = markets
                        print(f"  ✅ Using this API call result")
                        break
                    else:
                        print(f"  ❌ No current markets found, trying next approach")
                else:
                    print(f"  No markets returned")
            else:
                print(f"  Failed: {response.status_code}")
                
        except Exception as e:
            print(f"  Error: {e}")
    
    if not all_markets:
        print("❌ All API attempts failed or returned no current markets")
        return []

    try:
        print(f"Processing {len(all_markets)} total markets...")
        
        # Step 2: Filter out expired markets (API seems to return old markets as "active")
        current_time = datetime.now(timezone.utc)
        current_markets = []
        expired_count = 0
        
        for market in all_markets:
            end_date_str = market.get("endDate")
            if end_date_str:
                try:
                    # Parse the end date
                    end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
                    
                    # Only include markets that haven't ended yet (with some buffer)
                    if end_date > current_time:
                        current_markets.append(market)
                    else:
                        expired_count += 1
                except Exception as e:
                    # If we can't parse the date, include the market anyway
                    current_markets.append(market)
            else:
                # If no end date, include the market
                current_markets.append(market)
        
        print(f"After filtering: {len(current_markets)} current markets, {expired_count} expired markets filtered out")
        
        # Step 3: Filter for tradable markets (with CLOB token IDs)
        tradable_markets = [
            market for market in current_markets 
            if market.get("clobTokenIds") and len(market.get("clobTokenIds", [])) > 0
        ]
        
        print(f"Tradable markets with token IDs: {len(tradable_markets)}")
        
        # Step 4: Filter for sports-related markets
        sports_keywords = [
            # Basketball terms
            "nba", "basketball", "lakers", "celtics", "warriors", "knicks", "heat", "bucks", "mvp",
            
            # Baseball terms
            "mlb", "baseball", "yankees", "dodgers", "astros", "braves", "world series",
            
            # Football terms
            "nfl", "football", "chiefs", "49ers", "cowboys", "eagles", "super bowl", "quarterback",
            
            # Soccer terms
            "soccer", "football", "premier league", "uefa", "champions league", "fifa", "world cup",
            "manchester united", "liverpool", "barcelona", "real madrid", "bayern", "messi", "ronaldo",
            
            # Tennis terms
            "tennis", "atp", "wta", "grand slam", "wimbledon", "us open", "australian open", "french open",
            
            # Basketball players
            "lebron", "curry", "durant", "giannis", "luka", "embiid", "jokic", "tatum",
            
            # General sports terms
            "sports", "game", "match", "playoff", "finals", "champion", "tournament", "season", "draft"
        ]
        
        sports_markets = []
        for market in tradable_markets:
            question = market.get("question", "").lower()
            description = market.get("description", "").lower()
            
            # Check if any sports keyword is in the market text
            if any(keyword in question or keyword in description for keyword in sports_keywords):
                # Validate with game-related terms for better filtering
                game_terms = ["win", "game", "vs", "score", "defeat", "champion", "match", "beat", "against", "over", "under"]
                if any(term in question or term in description for term in game_terms):
                    sports_markets.append(market)
        
        print(f"Found {len(sports_markets)} current sports-related markets")
        
        # If no sports markets found, show some sample current markets for debugging
        if len(sports_markets) == 0 and len(current_markets) > 0:
            print("\n🔍 No sports markets found. Sample current markets:")
            for i, market in enumerate(current_markets[:5]):
                question = market.get("question", "Unknown")
                end_date = market.get("endDate", "Unknown")
                print(f"  {i+1}. {question} (ends: {end_date})")
        
        return sports_markets
        
    except Exception as e:
        print(f"Error processing markets: {e}")
        return []

if __name__ == "__main__":
    main() 