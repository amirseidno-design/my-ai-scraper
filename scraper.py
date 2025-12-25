import os
import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field

# 1. Define WHAT you want to find (The Schema)
class ProductPrice(BaseModel):
    product_name: str = Field(..., description="The name of the item")
    price: float = Field(..., description="The current selling price")
    currency: str = Field(..., description="The currency (e.g. AED, SAR, USD)")

async def main():
    # 2. Configure the "Brain" (Using Groq for FREE)
    # Get your key at console.groq.com
    llm_strategy = LLMExtractionStrategy(
        provider="groq/llama-3.3-70b-versatile", 
        api_token="YOUR_GROQ_API_KEY",
        schema=ProductPrice.model_json_schema(),
        instruction="Extract the product name and current price. Ignore 'original price' if there is a discount; only take the final price."
    )

    # 3. Configure the "Eyes" (The Browser)
    browser_config = BrowserConfig(headless=True, verbose=True)
    crawler_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Put the URL of the product here
        url = "https://www.noon.com/uae-en/iphone-16-pro-256gb-desert-titanium-5g-with-facetime-international-version/N70034449V/p/"
        
        result = await crawler.arun(url=url, config=crawler_config)

        if result.success:
            data = json.loads(result.extracted_content)
            print("--- SCRAPED DATA ---")
            print(json.dumps(data, indent=2))
        else:
            print(f"Failed to scrape: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())
