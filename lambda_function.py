# ==================================================================================================
#
# File: SARSLambda/lambda_function.py
#
# Description:
# This script contains an AWS Lambda function designed to scrape tender data from the SARS
# (South African Revenue Service) "Published Tenders" webpage. Since there is no API, this
# function relies entirely on HTML parsing.
#
# The function performs the following steps:
# 1. Fetches the HTML content of the main SARS procurement page.
# 2. Uses BeautifulSoup to parse the HTML and find the container holding the list of tenders.
# 3. Iterates through each paragraph (`<p>`) tag within the container, as each one represents a tender.
# 4. For each tender, it extracts the URL to the details page and the closing date string.
# 5. It passes this initial data to the `SarsTender` model, which is responsible for the
#    secondary scraping of the details page.
# 6. Skips and logs any items that fail the initial parsing.
# 7. Batches the successfully processed tender objects and sends them to the SQS queue.
#
# ==================================================================================================

# --- Import necessary libraries ---
import json
import requests
import logging
import boto3
import re
from bs4 import BeautifulSoup
from models import SarsTender

# --- Global Constants and Configuration ---
# The URL of the SARS procurement page to be scraped.
SARS_API_URL = "https://www.sars.gov.za/procurement/published-tenders/"

# Standard HTTP headers to mimic a web browser.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

# --- Logger Setup ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- AWS Service Client Initialization ---
sqs_client = boto3.client('sqs')
SQS_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/211635102441/AIQueue.fifo'

# ==================================================================================================
# Lambda Function Handler
# ==================================================================================================
def lambda_handler(event, context):
    """
    The main handler function for the AWS Lambda.
    """
    logger.info("Starting SARS tenders processing job.")

    # --- Step 1: Fetch and Parse the Main Tender List Page ---
    try:
        logger.info(f"Fetching data from {SARS_API_URL}")
        response = requests.get(SARS_API_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        # Use BeautifulSoup to parse the raw HTML.
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # The main container holding all tender listings is identified by a specific CSS class.
        tender_container = soup.select_one('div.elementor-element-ffe39ed')
        if not tender_container:
            raise ValueError("Main tender container not found on page.")
            
        # Within the container, each tender is in a separate <p> tag.
        tender_paragraphs = tender_container.find_all('p')
        logger.info(f"Found {len(tender_paragraphs)} potential tender items on the main page.")

    except (requests.exceptions.RequestException, ValueError) as e:
        logger.error(f"Failed to fetch or parse main page: {e}")
        return {'statusCode': 502, 'body': json.dumps({'error': 'Failed to fetch or parse source page'})}

    # --- Step 2: Extract Initial Data and Delegate to the Model ---
    processed_tenders = []
    skipped_count = 0

    for p_tag in tender_paragraphs:
        try:
            # Find the link (<a> tag) to the detail page.
            link_tag = p_tag.find('a')
            if not link_tag or not link_tag.get('href'):
                continue # If there's no link, it's not a valid tender listing.

            detail_url = link_tag.get('href')
            
            # Use regex to find and extract the closing date from the paragraph's text.
            p_text = p_tag.get_text()
            closing_date_match = re.search(r'Closing Date:\s*([\d/]+\s*[\d:]+)', p_text)
            closing_date_str = closing_date_match.group(1).strip() if closing_date_match else ""

            # Prepare a dictionary with the initial data to pass to the model.
            tender_data = {
                "url": detail_url,
                "closing_date_str": closing_date_str
            }

            # The model's from_api_response method will handle the rest of the scraping.
            tender_object = SarsTender.from_api_response(tender_data)
            if tender_object:
                processed_tenders.append(tender_object)
            else:
                skipped_count += 1
        except Exception as e:
            # Catch any unexpected errors during this initial extraction.
            skipped_count += 1
            logger.warning(f"Skipping tender due to a processing error: {e}. Raw paragraph: {p_tag.get_text()}")
            continue

    logger.info(f"Successfully processed {len(processed_tenders)} tenders.")
    if skipped_count > 0:
        logger.warning(f"Skipped a total of {skipped_count} tenders due to errors.")

    # --- Step 3: Batch and Send to SQS ---
    processed_tender_dicts = [tender.to_dict() for tender in processed_tenders]

    batch_size = 10
    message_batches = [
        processed_tender_dicts[i:i + batch_size]
        for i in range(0, len(processed_tender_dicts), batch_size)
    ]

    sent_count = 0
    for batch_index, batch in enumerate(message_batches):
        entries = []
        for i, tender_dict in enumerate(batch):
            entries.append({
                'Id': f'tender_message_{batch_index}_{i}',
                'MessageBody': json.dumps(tender_dict),
                'MessageGroupId': 'SARSTenderScrape'
            })

        if not entries:
            continue

        try:
            response = sqs_client.send_message_batch(
                QueueUrl=SQS_QUEUE_URL,
                Entries=entries
            )
            sent_count += len(response.get('Successful', []))
            logger.info(f"Successfully sent a batch of {len(entries)} messages to SQS.")
            if 'Failed' in response and response['Failed']:
                logger.error(f"Failed to send some messages in a batch: {response['Failed']}")
        except Exception as e:
            logger.error(f"Failed to send a message batch to SQS: {e}")

    logger.info(f"Processing complete. Sent a total of {sent_count} messages to SQS.")
    
    # --- Step 4: Return a Success Response ---
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Tender data processed and sent to SQS queue.'})
    }