# SARS Tender Processing Lambda Service
## 1. Overview
This service contains an AWS Lambda function responsible for scraping tender information from the South African Revenue Service (SARS) procurement webpage. Unlike the other data sources, SARS does not provide a JSON API, so this service relies entirely on HTML web scraping to gather data.

The process involves two stages of scraping:
1. **Main Page Scraping**: The Lambda first scrapes the main "Published Tenders" page to get a list of all active tenders, including the URL to each tender's detail page and its closing date.

2. **Detail Page Scraping**: For each tender found, the service then scrapes the individual detail page to extract more comprehensive information, such as supporting documents and briefing session details.

## 2. Lambda Function (`lambda_function.py`)
The `lambda_handler` orchestrates the initial stage of the scraping process:
1. **Fetch Main Page**: It sends an HTTP GET request to the SARS procurement URL to retrieve the page's HTML content.
2. **Error Handling**: It includes robust error handling for network issues and parsing failures (e.g., if the webpage structure changes).
3. **Initial Parsing**: It uses BeautifulSoup to parse the HTML and identify the main `<div>` that contains the list of tenders. It then iterates through each `<p>` tag within this container.
4. **Data Extraction**: For each tender, it extracts the URL to the detail page and the closing date string.
5. **Delegation to Model**: This extracted information is passed to the `SarsTender` model, which is responsible for the more complex task of scraping the detail page.
6. **Batching and Queueing**: After the models have processed all the tenders, the Lambda batches the structured data and sends it to the central `AIQueue.fifo` SQS queue with a `MessageGroupId` of `SARSTenderScrape`.

## 3. Data Model (`models.py`)
The service uses a set of Python classes to define the structure of the tender data.

### `TenderBase` (Abstract Class)
This is the standard foundational class that defines the common attributes for any tender, ensuring consistency.
- **Core Attributes**: `title`, `description`, `source`, `published_date`, `closing_date`, `supporting_docs`, `tags`.

### `SarsTender` (Concrete Class)
This class inherits from `TenderBase` and adds fields specific to the data available from the SARS website. Its `from_api_response` method contains all the logic for the secondary scraping of the detail pages.
- **Inherited Attributes**: All attributes from `TenderBase`.
- **SARS-Specific Attributes**:
    - `tender_number`: The unique tender number (e.g., "RFP01/2023"), extracted from the page title.
    - `briefing_session`: Details about any compulsory briefing sessions, if mentioned.

## Published Date Handling
A critical point to note is that the SARS website **does not provide a "published date"** for its tenders. To address this, the `SarsTender` model uses the following fallback strategy:

```
# From models.py
# As a fallback, we use the current timestamp of when the scraper is run.
published_date = datetime.now()

```

The `published_date` is set to the timestamp of the exact moment the Lambda function scrapes the tender. This provides a reliable and consistent, albeit approximate, value for when the tender was first discovered by the system.

## AI Tagging Initialization
As with the other services, the `tags` attribute is intentionally initialized as an empty list (`[]`) within the `from_api_response` method.

```
# From models.py
return cls(
    # ... other fields
    tags=[], # Initialize with an empty list for the AI service.
    # ... other fields
)

```

The SARS portal does not provide predefined tags. By setting this field to an empty list, we create a consistent data structure that the downstream AI service can use to generate and populate relevant tags.