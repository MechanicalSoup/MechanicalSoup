SDKs
Python
Firecrawl Python SDK is a wrapper around the Firecrawl API to help you easily turn websites into markdown.

​
Installation
To install the Firecrawl Python SDK, you can use pip:

Python

pip install firecrawl-py
​
Usage
Get an API key from firecrawl.dev
Set the API key as an environment variable named FIRECRAWL_API_KEY or pass it as a parameter to the FirecrawlApp class.
Here’s an example of how to use the SDK:

Python

from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape a website:
scrape_status = app.scrape_url(
  'https://firecrawl.dev', 
  params={'formats': ['markdown', 'html']}
)
print(scrape_status)

# Crawl a website:
crawl_status = app.crawl_url(
  'https://firecrawl.dev', 
  params={
    'limit': 100, 
    'scrapeOptions': {'formats': ['markdown', 'html']}
  }
)
print(crawl_status)
​
Scraping a URL
To scrape a single URL, use the scrape_url method. It takes the URL as a parameter and returns the scraped data as a dictionary.

Python

# Scrape a website:
scrape_result = app.scrape_url('firecrawl.dev', params={'formats': ['markdown', 'html']})
print(scrape_result)
​
Crawling a Website
To crawl a website, use the crawl_url method. It takes the starting URL and optional parameters as arguments. The params argument allows you to specify additional options for the crawl job, such as the maximum number of pages to crawl, allowed domains, and the output format.

Python

crawl_status = app.crawl_url(
  'https://firecrawl.dev', 
  params={
    'limit': 100, 
    'scrapeOptions': {'formats': ['markdown', 'html']}
  }, 
  poll_interval=30
)
print(crawl_status)
​
Asynchronous Crawling
To crawl a website asynchronously, use the crawl_url_async method. It returns the crawl ID which you can use to check the status of the crawl job. It takes the starting URL and optional parameters as arguments. The params argument allows you to specify additional options for the crawl job, such as the maximum number of pages to crawl, allowed domains, and the output format.

Python

crawl_status = app.async_crawl_url(
  'https://firecrawl.dev', 
  params={
    'limit': 100, 
    'scrapeOptions': {'formats': ['markdown', 'html']}
  }
)
print(crawl_status)
​
Checking Crawl Status
To check the status of a crawl job, use the check_crawl_status method. It takes the job ID as a parameter and returns the current status of the crawl job.

Python

crawl_status = app.check_crawl_status("<crawl_id>")
print(crawl_status)
​
Cancelling a Crawl
To cancel an asynchronous crawl job, use the cancel_crawl method. It takes the job ID of the asynchronous crawl as a parameter and returns the cancellation status.

Python

cancel_crawl = app.cancel_crawl(id)
print(cancel_crawl)
​
Map a Website
Use map_url to generate a list of URLs from a website. The params argument let you customize the mapping process, including options to exclude subdomains or to utilize the sitemap.

Python

# Map a website:
map_result = app.map_url('https://firecrawl.dev')
print(map_result)
​
Crawling a Website with WebSockets
To crawl a website with WebSockets, use the crawl_url_and_watch method. It takes the starting URL and optional parameters as arguments. The params argument allows you to specify additional options for the crawl job, such as the maximum number of pages to crawl, allowed domains, and the output format.

Python

# inside an async function...
nest_asyncio.apply()

# Define event handlers
def on_document(detail):
    print("DOC", detail)

def on_error(detail):
    print("ERR", detail['error'])

def on_done(detail):
    print("DONE", detail['status'])

    # Function to start the crawl and watch process
async def start_crawl_and_watch():
    # Initiate the crawl job and get the watcher
    watcher = app.crawl_url_and_watch('firecrawl.dev', { 'excludePaths': ['blog/*'], 'limit': 5 })

    # Add event listeners
    watcher.add_event_listener("document", on_document)
    watcher.add_event_listener("error", on_error)
    watcher.add_event_listener("done", on_done)

    # Start the watcher
    await watcher.connect()

# Run the event loop
await start_crawl_and_watch()
​
Error Handling
The SDK handles errors returned by the Firecrawl API and raises appropriate exceptions. If an error occurs during a request, an exception will be raised with a descriptive error message.