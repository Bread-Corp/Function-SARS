import unittest
from unittest.mock import patch, Mock
import sys
import re
# Patch boto3.client BEFORE importing lambda_function
mock_boto3 = Mock()
mock_boto3.client.return_value = Mock()
sys.modules['boto3'] = mock_boto3

import lambda_function
import logging
logging.getLogger().setLevel(logging.CRITICAL)

class TestLambdaFunction(unittest.TestCase):
    
    @patch('lambda_function.requests.get')
    @patch('lambda_function.SarsTender.from_api_response')
    @patch('lambda_function.sqs_client.send_message_batch')
    def test_lambda_handler_success(self, mock_sqs, mock_model, mock_get):
        # Test the full successful flow of lambda_handler:
        # - Mocks the HTML response from the SARS main page
        # - Mocks the SarsTender model to return a valid tender object
        # - Mocks SQS to simulate successful message sending
        mock_get.return_value = Mock(status_code=200, text='''
            <div class="elementor-element-ffe39ed">
                <p><a href="https://sars.gov.za/detail">Tender Link</a> Closing Date: 12/10/2025 11:00</p>
            </div>
        ''')

        mock_model.return_value = Mock(to_dict=lambda: {"title": "Tender Title"})
        mock_sqs.return_value = {"Successful": [{"Id": "tender_message_0_0"}]}

        result = lambda_function.lambda_handler({}, {})
        self.assertEqual(result['statusCode'], 200)  # Ensure success status code
        self.assertIn("Tender data processed", result['body'])  # Confirm success message


    @patch('lambda_function.requests.get')
    def test_lambda_handler_fetch_fail(self, mock_get):
        # Test error handling when the main SARS page fetch fails.
        # Simulates a network error during requests.get()
        mock_get.side_effect = lambda_function.requests.exceptions.RequestException("Network error")
        result = lambda_function.lambda_handler({}, {})
        self.assertEqual(result['statusCode'], 502)  # Ensure error status code
        self.assertIn("Failed to fetch or parse source page", result['body'])

    def test_closing_date_regex(self):
        # Test the regex used to extract the closing date from tender text.
        # Ensures the pattern correctly captures the date and time string.
        text = "Closing Date: 12/10/2025 11:00"
        match = re.search(r'Closing Date:\s*([\d/]+\s*[\d:]+)', text)
        self.assertEqual(match.group(1), "12/10/2025 11:00")  # Validate extracted date string
