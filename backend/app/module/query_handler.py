from urllib.parse import urlparse
from app.module.flipkart import handle_flipkart
from app.module.amazon import handle_amazon
import asyncio
import inspect




# Map sites to their handlers
site_handlers = {
    "flipkart": handle_flipkart,
    "amazon": handle_amazon,
}

async def queryhandler(query):
    parsed_url = urlparse(query)
    domain = parsed_url.netloc.lower()  # get domain from URL

    for site, handler in site_handlers.items():
        if site in domain:
            result = handler(query)
            # Check if handler is async
            if inspect.iscoroutine(result):
                return await result
            else:
                return result
    return "No match found in query"
