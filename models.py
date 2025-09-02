# ==================================================================================================
#
# File: SARSLambda/models.py
#
# Description:
# This module defines the data structures (models) for representing tender information
# sourced from the South African Revenue Service (SARS) procurement page. This service
# relies entirely on web scraping, as SARS does not provide a public API for tenders.
#
# The classes defined here are:
#   - SupportingDoc: A simple class to represent a downloadable document.
#   - TenderBase: An abstract base class defining the common interface for all tenders.
#   - SarsTender: A concrete class for SARS tenders. Its `from_api_response` method
#     takes a URL and closing date string, scrapes the detail page for all necessary
#     information, and constructs a structured tender object.
#
# ==================================================================================================

# --- Import necessary libraries ---
from abc import ABC, abstractmethod
from datetime import datetime
from bs4 import BeautifulSoup # For parsing HTML from the details page.
import requests # For making the HTTP request to the details page.
import re # For using regular expressions to find tender numbers and other data.
import html # For unescaping HTML entities.
import logging

# ==================================================================================================
# Class: SupportingDoc
# Purpose: Represents a single supporting document associated with a tender.
# ==================================================================================================
class SupportingDoc:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def to_dict(self):
        return {"name": self.name, "url": self.url}

# ==================================================================================================
# Class: TenderBase (Abstract Base Class)
# ==================================================================================================
class TenderBase(ABC):
    def __init__(self, title: str, description: str, source: str, published_date: datetime, closing_date: datetime, supporting_docs: list = None, tags: list = None):
        self.title = title
        self.description = description
        self.source = source
        self.published_date = published_date
        self.closing_date = closing_date
        self.supporting_docs = supporting_docs if supporting_docs is not None else []
        self.tags = tags if tags is not None else []

    @classmethod
    @abstractmethod
    def from_api_response(cls, response_item: dict):
        pass

    def to_dict(self):
        # Override this in the child class to handle the specific tags implementation.
        return {
            "title": self.title,
            "description": self.description,
            "source": self.source,
            "publishedDate": self.published_date.isoformat() if self.published_date else None,
            "closingDate": self.closing_date.isoformat() if self.closing_date else None,
            "supporting_docs": [doc.to_dict() for doc in self.supporting_docs],
            "tags": self.tags
        }

# ==================================================================================================
# Class: SarsTender
# Purpose: A concrete implementation for SARS-specific tenders.
# ==================================================================================================
class SarsTender(TenderBase):
    def __init__(
        self,
        # --- Base fields ---
        title: str, description: str, source: str, published_date: datetime, closing_date: datetime, supporting_docs: list, tags: list,
        # --- SARS-specific fields ---
        tender_number: str,
        briefing_session: str,
    ):
        super().__init__(title, description, source, published_date, closing_date, supporting_docs, tags)
        self.tender_number = tender_number
        self.briefing_session = briefing_session

    @classmethod
    def from_api_response(cls, response_item: dict):
        """
        Factory method to create a SarsTender object by scraping a details page.

        Args:
            response_item (dict): A dictionary containing the URL of the tender details
                                  page and the closing date string.

        Returns:
            SarsTender or None: An instance of the class, or None if scraping or validation fails.
        """
        detail_url = response_item.get("url")
        closing_date_str = response_item.get("closing_date_str")
        if not detail_url:
            return None

        try:
            # --- Step 1: Scrape the detail page ---
            headers = {'User-Agent': 'Mozilla/5.0'}
            page_response = requests.get(detail_url, headers=headers, timeout=15)
            page_response.raise_for_status()
            soup = BeautifulSoup(page_response.text, 'html.parser')

            # --- Step 2: Extract data from the scraped HTML ---
            # Extract the title from the H1 tag.
            title_tag = soup.select_one('h1.elementor-heading-title')
            title = title_tag.get_text(strip=True).replace("Tender:", "").strip() if title_tag else ""

            # Use regex to find the tender number (e.g., RFP01/2023) within the title.
            tender_number_match = re.search(r'(RFP\d{2,}/\d{4})', title, re.IGNORECASE)
            tender_number = tender_number_match.group(1) if tender_number_match else ""

            # Find briefing session information, if available.
            briefing_session = ""
            briefing_title_span = soup.find('span', class_='elementor-alert-title', string=re.compile(r'Briefing Session'))
            if briefing_title_span:
                briefing_desc_span = briefing_title_span.find_next_sibling('span', class_='elementor-alert-description')
                if briefing_desc_span:
                    briefing_session = briefing_desc_span.get_text(strip=True)

            # Find all downloadable documents within the main content area.
            doc_list = []
            content_div = soup.select_one('div.elementor-widget-theme-post-content')
            if content_div:
                for a_tag in content_div.find_all('a'):
                    doc_url = a_tag.get('href')
                    doc_name = a_tag.get_text(strip=True)
                    if doc_url and doc_name:
                        doc_list.append(SupportingDoc(name=doc_name, url=doc_url))

            # --- Step 3: Parse dates and create the object ---
            close_date = None
            try:
                if closing_date_str:
                    # The date is expected in 'DD/MM/YYYY HH:MM' format.
                    close_date = datetime.strptime(closing_date_str, '%d/%m/%Y %H:%M')
            except (ValueError, TypeError):
                logging.warning(f"Could not parse closing date for {tender_number}: {closing_date_str}")

            # NOTE: The SARS website does not provide a "published date" for tenders.
            # As a fallback, we use the current timestamp of when the scraper is run.
            # This provides a reasonable approximation for when the tender was discovered.
            published_date = datetime.now()

            # Create and return an instance of the class with the scraped and processed data.
            return cls(
                title=title.title(),
                description=title.title(), # Use the title as the description as no separate description is available.
                source="SARS",
                published_date=published_date,
                closing_date=close_date,
                supporting_docs=doc_list,
                tags=[], # Initialize with an empty list for the downstream AI service.
                tender_number=tender_number,
                briefing_session=briefing_session
            )
        except (requests.exceptions.RequestException, Exception) as e:
            # If any part of the scraping process fails, log the error and skip this tender.
            logging.error(f"Failed to scrape SARS detail page {detail_url}: {e}")
            return None

    def to_dict(self):
        """
        Serializes the SarsTender object to a dictionary.
        """
        data = super().to_dict()
        data.update({
            "tenderNumber": self.tender_number,
            "briefingSession": self.briefing_session,
        })
        return data