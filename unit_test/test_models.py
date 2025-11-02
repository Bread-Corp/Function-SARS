import unittest
from unittest.mock import patch, Mock
from models import SarsTender, SupportingDoc
from datetime import datetime

class TestSupportingDoc(unittest.TestCase):
    def test_to_dict(self):
        # Test that SupportingDoc correctly serializes to a dictionary.
        doc = SupportingDoc(name="Spec Sheet", url="https://example.com/spec.pdf")
        self.assertEqual(doc.to_dict(), {"name": "Spec Sheet", "url": "https://example.com/spec.pdf"})

class TestSarsTender(unittest.TestCase):
    @patch('models.requests.get')
    def test_from_api_response_success(self, mock_get):
        # Test that SarsTender.from_api_response correctly parses a valid detail page.
        # Mocks the HTML response to simulate a real tender detail page.
        html_content = '''
            <html>
                <h1 class="elementor-heading-title">Tender: RFP01/2023</h1>
                <span class="elementor-alert-title">Briefing Session</span>
                <span class="elementor-alert-description">Online via Teams</span>
                <div class="elementor-widget-theme-post-content">
                    <a href="https://example.com/doc1.pdf">Document 1</a>
                </div>
            </html>
        '''
        mock_get.return_value = Mock(status_code=200, text=html_content)

        response_item = {
            "url": "https://sars.gov.za/tender-detail",
            "closing_date_str": "12/10/2025 11:00"
        }

        tender = SarsTender.from_api_response(response_item)
        self.assertIsNotNone(tender)  # Ensure the tender object was created
        self.assertEqual(tender.tender_number, "RFP01/2023")  # Check tender number extraction
        self.assertEqual(tender.briefing_session, "Online via Teams")  # Check briefing session parsing
        self.assertEqual(len(tender.supporting_docs), 1)  # Ensure one supporting document was found
        self.assertEqual(tender.closing_date, datetime(2025, 10, 12, 11, 0))  # Validate closing date parsing

    def test_from_api_response_missing_url(self):
        # Test that from_api_response returns None when the URL is missing.
        tender = SarsTender.from_api_response({"closing_date_str": "12/10/2025 11:00"})
        self.assertIsNone(tender)

    def test_to_dict_structure(self):
        # Test that SarsTender.to_dict serializes all fields correctly, including inherited and custom ones.
        tender = SarsTender(
            title="Tender Title",
            description="Tender Description",
            source="SARS",
            published_date=datetime(2025, 10, 10),
            closing_date=datetime(2025, 10, 12, 11, 0),
            supporting_docs=[SupportingDoc("Doc", "url")],
            tags=["finance"],
            tender_number="RFP01/2023",
            briefing_session="Online"
        )
        data = tender.to_dict()
        self.assertEqual(data["tenderNumber"], "RFP01/2023")  # Check custom field
        self.assertEqual(data["briefingSession"], "Online")  # Check custom field
        self.assertEqual(data["supporting_docs"][0]["name"], "Doc")  # Check nested doc serialization
