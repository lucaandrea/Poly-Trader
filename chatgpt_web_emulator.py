#!/usr/bin/env python3
import openai
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_polymarket_markets_ending_tomorrow():
    """
    Search for Polymarket markets ending tomorrow using GPT-4.1 with web search
    """
    try:
        # Get tomorrow's date in a readable format
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%B %d, %Y')
        today = datetime.now().strftime('%B %d, %Y')
        
        print(f"🔍 Searching for Polymarket markets ending tomorrow ({tomorrow})...")
        print("Using GPT-4.1 with web search capabilities")
        print("=" * 80)
        
        # Create a response with web search enabled
        response = client.responses.create(
            model="gpt-4.1",
            tools=[{
                "type": "web_search_preview",
                "search_context_size": "high",  # High context for detailed search
                "user_location": {
                    "type": "approximate",
                    "country": "US",
                    "timezone": "America/New_York"
                }
            }],
            input=f"""Today is {today}. Search for active prediction markets on Polymarket.com that are specifically ending tomorrow ({tomorrow}).

            Focus on finding:
            1. Bitcoin/cryptocurrency price predictions ending tomorrow
            2. Ethereum or other crypto markets ending tomorrow  
            3. Temperature records or weather-related markets ending tomorrow
            4. Company market capitalization bets ending tomorrow
            5. Political or election markets ending tomorrow
            6. Sports or entertainment markets ending tomorrow
            
            For each market found, provide:
            - Exact market question/title
            - Current odds/probabilities 
            - End date/time (confirm it's tomorrow)
            - Current market volume if available
            - Direct link to the market
            - Brief analysis of why this market is interesting
            
            Please search thoroughly on Polymarket.com and provide the most current information available."""
        )
        
        # Display the results
        print(f"\n🎯 POLYMARKET MARKETS ENDING TOMORROW ({tomorrow})")
        print("Generated using GPT-4.1 Web Search")
        print("=" * 80)
        
        # Process the response output
        for item in response.output:
            if item.type == "web_search_call":
                print(f"🔍 Web search executed (ID: {item.id})")
                print(f"📊 Search status: {item.status}")
                print()
            elif item.type == "message":
                # Extract the main content
                for content in item.content:
                    if content.type == "output_text":
                        print(content.text)
                        
                        # Display citations if available
                        if hasattr(content, 'annotations') and content.annotations:
                            print("\n" + "=" * 80)
                            print("📚 SOURCES AND REFERENCES:")
                            print("=" * 80)
                            for i, annotation in enumerate(content.annotations, 1):
                                if annotation.type == "url_citation":
                                    print(f"{i}. {annotation.title}")
                                    print(f"   🔗 {annotation.url}")
                                    print()
        
        print("\n" + "=" * 80)
        print("✅ Search completed successfully using GPT-4.1!")
        print("💡 Tip: Run this script daily to find tomorrow's expiring markets")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error during web search: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Verify your OPENAI_API_KEY is set correctly in .env")
        print("2. Ensure you have access to GPT-4.1 and web search")
        print("3. Check your OpenAI usage limits and billing")
        print("4. Verify internet connection for web search")

def search_specific_polymarket_category(category):
    """
    Search for a specific category of Polymarket markets ending tomorrow
    """
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%B %d, %Y')
        
        print(f"🎯 Searching for {category} markets ending tomorrow ({tomorrow})...")
        
        response = client.responses.create(
            model="gpt-4.1",
            tools=[{
                "type": "web_search_preview",
                "search_context_size": "high"
            }],
            input=f"""Search Polymarket.com specifically for {category} prediction markets that end tomorrow ({tomorrow}).
            
            Provide detailed information including:
            - Current odds and probabilities
            - Market volume and activity
            - Recent price movements
            - Key factors affecting the market
            - Analysis of potential outcomes"""
        )
        
        print(f"\n📊 {category.upper()} MARKETS ENDING TOMORROW")
        print("=" * 60)
        
        for item in response.output:
            if item.type == "message":
                for content in item.content:
                    if content.type == "output_text":
                        print(content.text)
        
    except Exception as e:
        print(f"❌ Error searching for {category} markets: {str(e)}")

if __name__ == "__main__":
    # Check for command line arguments for specific categories
    import sys
    
    if len(sys.argv) > 1:
        # Search for specific category
        category = " ".join(sys.argv[1:])
        search_specific_polymarket_category(category)
    else:
        # General search for all markets ending tomorrow
        search_polymarket_markets_ending_tomorrow()
