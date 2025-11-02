# 💰 SARS Tender Processing Lambda Service

[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![Amazon SQS](https://img.shields.io/badge/AWS-SQS-yellow.svg)](https://aws.amazon.com/sqs/)
[![SARS Portal](https://img.shields.io/badge/Portal-SARS-darkgreen.svg)](https://www.sars.gov.za/)
[![BeautifulSoup](https://img.shields.io/badge/Scraping-BeautifulSoup-orange.svg)](https://www.crummy.com/software/BeautifulSoup/)

**Collecting revenue opportunities with tax-efficient precision!** 💼 This AWS Lambda service is the financial intelligence powerhouse of our tender scraping fleet - the fifth and final specialized crawler that captures opportunities from South Africa's premier tax collection agency. From data analytics platforms to digital transformation projects, we audit every opportunity! 📊

## 📚 Table of Contents

- [🎯 Overview](#-overview)
- [💰 Lambda Function (lambda_function.py)](#-lambda-function-lambda_functionpy)
- [📊 Data Model (models.py)](#-data-model-modelspy)
- [🏷️ AI Tagging Initialization](#️-ai-tagging-initialization)
- [📋 Example Tender Data](#-example-tender-data)
- [🚀 Getting Started](#-getting-started)
- [📦 Deployment](#-deployment)
- [🧰 Troubleshooting](#-troubleshooting)

## 🎯 Overview

Welcome to the treasury of digital opportunities! 🏛️ This service is your direct access to SARS's sophisticated procurement ecosystem, capturing cutting-edge technology projects, data analytics solutions, digital transformation initiatives, and specialized consulting services that power South Africa's tax collection and revenue administration! 💻

**What makes it tax-efficiently excellent?** 📈
- 💼 **Financial Sector Expertise**: Specialized in tax technology, data analytics, and revenue administration systems
- 🕵️ **Advanced Web Intelligence**: Pure HTML scraping mastery - no APIs, just surgical precision web extraction
- 🔍 **Dual-Phase Investigation**: Two-stage scraping process for comprehensive tender intelligence
- 🎯 **Digital Focus**: Captures high-tech opportunities in fintech, data science, and digital government services

## 💰 Lambda Function (`lambda_function.py`)

The financial forensics brain of our operation! 🧠 The `lambda_handler` orchestrates our sophisticated dual-audit extraction process:

### 🔄 The Revenue Collection Journey:

1. **🌐 Initial Tax Assessment**: Connects to the SARS procurement webpage - the official treasury for all technology and consulting opportunities across South Africa's revenue administration.

2. **🛡️ Audit-Grade Error Handling**: Built like a tax compliance system! Handles network audits, website maintenance periods, and response discrepancies with financial-grade precision. Every transaction is tracked! 📋

3. **🔍 Comprehensive Audit Process**: Here's where our tax investigation expertise shines! Unlike other agencies, SARS requires pure forensic web scraping:
   - **Phase 1**: Audit the main "Published Tenders" page to identify all active procurement opportunities
   - **Phase 2**: Conduct detailed investigation of each tender's individual page for comprehensive data extraction
   - **Phase 3**: Cross-reference and validate all financial and technical specifications

4. **⚙️ Tax Code Validation**: Each tender undergoes rigorous `SarsTender` model processing with specialized logic for HTML parsing, document extraction, and briefing session identification - because tax matters require precision! 📊

5. **✅ Compliance Inspector**: Our validation process ensures only regulation-compliant tenders make it through. Failed assessments get logged for review - no tax loopholes in our pipeline! 🔨

6. **📦 Revenue Batching**: Valid tenders are efficiently organized into fiscal batches of 10 messages - optimized for maximum SQS throughput like a well-structured tax return.

7. **🚀 Treasury Express**: Each batch flows to the central `AIQueue.fifo` SQS queue with the unique `MessageGroupId` of `SARSTenderScrape`. This keeps our revenue administration tenders organized and maintains perfect audit trail.

## 📊 Data Model (`models.py`)

Our data architecture is engineered for tax-grade accuracy! 🏗️

### `TenderBase` **(The Financial Foundation)** 💼
The solid fiscal foundation that supports all our tender accounting! This abstract class defines the core ledger that records all revenue opportunities:

**🔧 Core Attributes:**
- `title`: The procurement specification - what technology is being acquired?
- `description`: Detailed technical requirements and compliance specifications
- `source`: Always "SARS" for this revenue administration specialist
- `published_date`: When this opportunity entered our fiscal records *(special handling - see below)*
- `closing_date`: Submission deadline - when the tax window closes! ⏰
- `supporting_docs`: Critical procurement documents and briefing materials
- `tags`: Keywords for AI intelligence (starts empty, gets assessed by our AI service)

### `SarsTender` **(The Revenue Specialist)** 💰
This financial powerhouse inherits all the foundational strength from `TenderBase` and adds SARS's unique revenue administration features:

**🏛️ SARS-Specific Attributes:**
- `tender_number`: Official SARS procurement code (e.g., "RFP18/2025")
- `briefing_session`: Details about compulsory briefing sessions and presentations

**🔍 Advanced Revenue Processing:**
The `from_api_response` method is our master tax auditor! It performs:
- **HTML Audit**: BeautifulSoup-powered deep analysis of tender pages
- **Document Forensics**: Extraction of supporting documents, Q&A sessions, and briefing materials
- **Compliance Verification**: Validation of procurement timelines and requirements

### 📅 Special Published Date Handling

**Important Tax Note:** 🚨 SARS operates differently from other agencies - their website doesn't publish tender dates! Our solution:

```python
# From models.py - Tax-efficient timestamp management! 💼
# As a fallback, we use the current timestamp of when the scraper is run.
published_date = datetime.now()
```

We use the **exact moment of discovery** as the published date - providing consistent, auditable timestamps for when our system first identified each opportunity. It's like a tax assessment date! 📋

## 🏷️ AI Tagging Initialization

We're all about intelligent revenue optimization! 🤖 Every tender that processes through our system is perfectly prepared for downstream AI enhancement:

```python
# From models.py - Preparing for AI revenue classification! 💰
return cls(
    # ... other fields
    tags=[],  # Initialize tags as an empty list, ready for the AI service.
    # ... other fields
)
```

This ensures **seamless treasury integration** with our AI pipeline - every tender object arrives with a clean, empty `tags` field just waiting to be assessed with intelligent categorizations! 🧠💼

## 📋 Example Tender Data

Here's what a real SARS technology project looks like after our scraper works its financial magic! 🎩✨

```json
{
  "title": "Rfp18/2025: The Procurement Of Third-Party Data And Related Services",
  "description": "Rfp18/2025: The Procurement Of Third-Party Data And Related Services",
  "source": "SARS",
  "publishedDate": "2025-10-16T19:34:05.725453",
  "closingDate": "2025-10-22T11:00:00",
  "supporting_docs": [
    {
      "name": "The procurement of third-party data and related services",
      "url": "https://www.sars.gov.za/sars-rfp-18-2025-tender-pack/"
    },
    {
      "name": "Briefing session presentation",
      "url": "https://www.sars.gov.za/non-compulsary-briefing-for-rfp-18-2025/"
    },
    {
      "name": "Questions and answers",
      "url": "https://www.sars.gov.za/sars-rfp-18-2025-communication-1/"
    }
  ],
  "tags": [],
  "tenderNumber": "RFP18/2025",
  "briefingSession": "(Non-Compulsory) 2025/09/30 at 10:00"
}
```

**💰 What this revenue opportunity delivers:**
- 📊 **Data Analytics Focus**: Third-party data procurement for advanced tax analytics
- 💻 **Technology Integration**: Modern data services for revenue administration
- 📋 **Comprehensive Documentation**: Full tender pack, briefing presentations, and Q&A sessions
- ⏰ **Tight Timeline**: Quick turnaround from October 16 to October 22, 2025
- 🎯 **Professional Briefing**: Non-compulsory but valuable briefing session opportunity
- 🔍 **Transparent Process**: Multiple communication channels and Q&A support

## 🚀 Getting Started

Ready to calculate your way to success? Let's prepare your tax return of opportunities! 📊

### 📋 Prerequisites
- AWS CLI configured with appropriate credentials 🔑
- Python 3.9+ with pip 🐍
- BeautifulSoup4 for advanced web scraping 🔍
- Access to AWS Lambda and SQS services ☁️
- Understanding of revenue administration and financial technology 💼

### 🔧 Local Development
1. **📁 Clone the repository**
2. **📦 Install dependencies**: `pip install -r requirements.txt`
3. **🧪 Run tests**: `python -m pytest`
4. **🔍 Test locally**: Use AWS SAM for local Lambda simulation

## 📦 Deployment

### 🚀 Revenue Express Deploy
1. **📁 Package**: Bundle your code and dependencies like tax documents
2. **⬆️ Upload**: Deploy to AWS Lambda with treasury-grade settings
3. **⚙️ Configure**: Set up CloudWatch Events for scheduled revenue runs
4. **🎯 Test**: Trigger manually to verify treasury connection

### 🔧 Environment Variables
- `SQS_QUEUE_URL`: Target queue for processed revenue tenders
- `SCRAPING_TIMEOUT`: Timeout for comprehensive web scraping operations
- `BATCH_SIZE`: Number of tenders per SQS fiscal batch (default: 10)
- `USER_AGENT`: Browser identification for SARS website compatibility

## 🧰 Troubleshooting

### 🚨 Revenue Administration Challenges

<details>
<summary><strong>Pure HTML Scraping Complexity</strong></summary>

**Issue**: No API available - everything requires surgical HTML extraction.

**Solution**: SARS is a pure web scraping challenge! Maintain robust HTML parsing with fallback selectors and regular expression patterns. Tax websites require forensic precision! 🔍

</details>

<details>
<summary><strong>Website Structure Updates</strong></summary>

**Issue**: SARS website redesigns breaking the scraping logic.

**Solution**: Government websites evolve like tax regulations! Monitor for structural changes and maintain flexible selectors. Keep your scraping code as current as tax law! 📋

</details>

<details>
<summary><strong>Dual-Phase Scraping Timeouts</strong></summary>

**Issue**: Main page loads but individual tender pages timeout.

**Solution**: SARS tender pages can be document-heavy! Implement intelligent timeout handling and retry logic for individual page scraping. Sometimes tax documents take time to load! ⏰

</details>

<details>
<summary><strong>Missing Published Dates</strong></summary>

**Issue**: SARS doesn't provide published dates for tenders.

**Solution**: We use discovery timestamps! This provides consistent, auditable dates for when our system first identified each opportunity. Document your methodology like a tax audit! 📊

</details>

<details>
<summary><strong>Complex Document Structures</strong></summary>

**Issue**: SARS tenders often have multiple supporting documents and briefing materials.

**Solution**: Implement comprehensive document extraction logic that captures tender packs, briefing presentations, Q&A sessions, and communication updates. Treat each document like a tax form - every detail matters! 💼

</details>

---

> Built with love, bread, and code by **Bread Corporation** 🦆❤️💻
