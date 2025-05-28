#!/usr/bin/env python3
import openai
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_polymarket_markets():
    """
    Search for current active markets on Polymarket using OpenAI's web search
    """
    try:
        print("Searching for current Polymarket markets...")
        
        # Create a response with web search enabled
        response = client.responses.create(
            model="gpt-4.1",
            tools=[{
                "type": "web_search_preview",
                "search_context_size": "medium",  # Balanced context and cost
                "user_location": {
                    "type": "approximate",
                    "country": "US",
                    "timezone": "America/New_York"
                }
            }],
            input="""Search for the current trending prediction markets on Polymarket.com. 
            Focus on:
            1. Political markets (elections, political events)
            2. Sports markets (upcoming games, championships)
            3. Crypto/Finance markets (Bitcoin price, economic events)
            4. Current events markets
            
            For each market, provide:
            - Market question/title
            - Current odds or prices
            - End date if available
            - Brief description
            
            Format as a numbered list with clear categories."""
        )
        
        # Extract and display the results
        print(f"\nPOLYMARKET ACTIVE MARKETS ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
        print("=" * 70)
        
        # Process the response output
        for item in response.output:
            if item.type == "web_search_call":
                print(f"🔍 Web search completed (ID: {item.id})")
                print("📊 Status:", item.status)
                print()
            elif item.type == "message":
                # Extract the main content
                for content in item.content:
                    if content.type == "output_text":
                        print(content.text)
                        
                        # Display citations if available
                        if hasattr(content, 'annotations') and content.annotations:
                            print("\n" + "=" * 70)
                            print("📚 SOURCES:")
                            print("=" * 70)
                            for i, annotation in enumerate(content.annotations, 1):
                                if annotation.type == "url_citation":
                                    print(f"{i}. {annotation.title}")
                                    print(f"   URL: {annotation.url}")
                                    print()
        
        print("\n" + "=" * 70)
        print("✅ Search completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error searching Polymarket markets: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check that your OPENAI_API_KEY is set correctly in .env")
        print("2. Ensure you have access to GPT-4.1 and web search")
        print("3. Check your OpenAI usage limits")

def search_specific_market(query):
    """
    Search for a specific type of market or question
    """
    try:
        print(f"Searching for specific market: {query}")
        
        response = client.responses.create(
            model="gpt-4.1",
            tools=[{
                "type": "web_search_preview",
                "search_context_size": "high"  # More context for specific searches
            }],
            input=f"""Search Polymarket.com for prediction markets related to: {query}
            
            Provide detailed information including:
            - Current odds/prices
            - Market volume if available
            - End dates
            - Recent price movements
            - Any relevant news affecting the market"""
        )
        
        print(f"\nSPECIFIC MARKET SEARCH: {query}")
        print("=" * 70)
        
        for item in response.output:
            if item.type == "message":
                for content in item.content:
                    if content.type == "output_text":
                        print(content.text)
        
    except Exception as e:
        print(f"❌ Error searching for specific market: {str(e)}")

if __name__ == "__main__":
    # Check for command line arguments for specific searches
    import sys
    
    if len(sys.argv) > 1:
        # Search for specific market
        search_query = " ".join(sys.argv[1:])
        search_specific_market(search_query)
    else:
        # General market search
        search_polymarket_markets() 