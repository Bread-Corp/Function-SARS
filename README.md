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

This section covers three deployment methods for the SARS Tender Processing Lambda Service. Choose the method that best fits your workflow and infrastructure preferences.

### 🛠️ Prerequisites

Before deploying, ensure you have:
- AWS CLI configured with appropriate credentials 🔑
- AWS SAM CLI installed (`pip install aws-sam-cli`)
- Python 3.13 runtime support in your target region
- Access to AWS Lambda, SQS, and CloudWatch Logs services ☁️
- Required Python dependencies: `beautifulsoup4` and `requests`

### 🎯 Method 1: AWS Toolkit Deployment

Deploy directly through your IDE using the AWS Toolkit extension.

#### Setup Steps:
1. **Install AWS Toolkit** in your IDE (VS Code, IntelliJ, etc.)
2. **Configure AWS Profile** with your credentials
3. **Open Project** containing `lambda_function.py` and `models.py`

#### Deploy Process:
1. **Right-click** on `lambda_function.py` in your IDE
2. **Select** "Deploy Lambda Function" from AWS Toolkit menu
3. **Configure Deployment**:
   - Function Name: `SarsLambda`
   - Runtime: `python3.13`
   - Handler: `lambda_function.lambda_handler`
   - Memory: `128 MB`
   - Timeout: `120 seconds`
4. **Add Layers** manually after deployment:
   - beautifulsoup4-library layer
   - requests-library layer
5. **Set Environment Variables** as needed
6. **Configure IAM Permissions** for SQS, Logs, and EC2 (for VPC if needed)

#### Post-Deployment:
- Test the function using the AWS Toolkit test feature
- Monitor logs through CloudWatch integration
- Update function code directly from IDE for quick iterations

### 🚀 Method 2: SAM Deployment

Use AWS SAM for infrastructure-as-code deployment with the provided template.

#### Initial Setup:
```bash
# Install AWS SAM CLI
pip install aws-sam-cli

# Verify installation
sam --version
```

#### Create Required Layer Directories:
Since the template references layers not included in the repository, create them:

```bash
# Create layer directories
mkdir -p beautifulsoup4-library/python
mkdir -p requests-library/python

# Install beautifulsoup4 layer
pip install beautifulsoup4 -t beautifulsoup4-library/python/

# Install requests layer  
pip install requests -t requests-library/python/
```

#### Build and Deploy:
```bash
# Build the SAM application
sam build

# Deploy with guided configuration (first time)
sam deploy --guided

# Follow the prompts:
# Stack Name: sars-lambda-stack
# AWS Region: us-east-1 (or your preferred region)
# Confirm changes before deploy: Y
# Allow SAM to create IAM roles: Y
# Save parameters to samconfig.toml: Y
```

#### Subsequent Deployments:
```bash
# Quick deployment after initial setup
sam build && sam deploy
```

#### Local Testing with SAM:
```bash
# Test function locally
sam local invoke SarsLambda

# Start local API Gateway (if needed)
sam local start-api
```

#### SAM Deployment Advantages:
- ✅ Complete infrastructure management
- ✅ Automatic layer creation and management
- ✅ IAM permissions defined in template
- ✅ Easy rollback capabilities
- ✅ CloudFormation integration

### 🔄 Method 3: Workflow Deployment (CI/CD)

Automated deployment using GitHub Actions workflow for production environments.

#### Setup Requirements:
1. **GitHub Repository Secrets**:
   ```
   AWS_ACCESS_KEY_ID: Your AWS access key
   AWS_SECRET_ACCESS_KEY: Your AWS secret key
   AWS_REGION: us-east-1 (or your target region)
   ```

2. **Pre-existing Lambda Function**: The workflow updates an existing function, so deploy initially using Method 1 or 2.

#### Deployment Process:
1. **Create Release Branch**:
   ```bash
   # Create and switch to release branch
   git checkout -b release
   
   # Make your changes to lambda_function.py or models.py
   # Commit changes
   git add .
   git commit -m "feat: update SARS tender processing logic"
   
   # Push to trigger deployment
   git push origin release
   ```

2. **Automatic Deployment**: The workflow will:
   - Checkout the code
   - Configure AWS credentials
   - Create deployment zip with `lambda_function.py` and `models.py`
   - Update the existing Lambda function code
   - Maintain existing configuration (layers, environment variables, etc.)

#### Manual Trigger:
You can also trigger deployment manually:
1. Go to **Actions** tab in your GitHub repository
2. Select **"Deploy Python Scraper to AWS"** workflow
3. Click **"Run workflow"**
4. Choose the `release` branch
5. Click **"Run workflow"** button

#### Workflow Deployment Advantages:
- ✅ Automated CI/CD pipeline
- ✅ Consistent deployment process
- ✅ Audit trail of deployments
- ✅ Easy rollback to previous commits
- ✅ No local environment dependencies

### 🔧 Post-Deployment Configuration

Regardless of deployment method, configure the following:

#### Environment Variables:
```bash
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/211635102441/AIQueue.fifo
SCRAPING_TIMEOUT=30
BATCH_SIZE=10
USER_AGENT=Mozilla/5.0 (compatible; SARS-Tender-Bot/1.0)
```

#### CloudWatch Events (Optional):
Set up scheduled execution:
```bash
# Create CloudWatch Events rule for daily execution
aws events put-rule \
    --name "SarsLambdaSchedule" \
    --schedule-expression "cron(0 9 * * ? *)" \
    --description "Daily SARS tender scraping"

# Add Lambda as target
aws events put-targets \
    --rule "SarsLambdaSchedule" \
    --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:211635102441:function:SarsLambda"
```

### 🧪 Testing Your Deployment

After deployment, test the function:

```bash
# Test via AWS CLI
aws lambda invoke \
    --function-name SarsLambda \
    --payload '{}' \
    response.json

# Check the response
cat response.json
```

#### Expected Success Indicators:
- ✅ Function executes without errors
- ✅ CloudWatch logs show successful scraping activity
- ✅ SQS queue receives tender messages
- ✅ No timeout or memory errors
- ✅ Valid JSON tender data in queue messages

### 🔍 Monitoring and Maintenance

#### CloudWatch Metrics to Monitor:
- **Duration**: Function execution time
- **Error Rate**: Failed invocations
- **Memory Utilization**: RAM usage patterns
- **Throttles**: Concurrent execution limits

#### Log Analysis:
```bash
# View recent logs
aws logs tail /aws/lambda/SarsLambda --follow

# Search for errors
aws logs filter-log-events \
    --log-group-name /aws/lambda/SarsLambda \
    --filter-pattern "ERROR"
```

### 🚨 Troubleshooting Deployments

<details>
<summary><strong>Layer Dependencies Missing</strong></summary>

**Issue**: `beautifulsoup4` or `requests` import errors

**Solution**: Ensure layers are properly created and attached:
```bash
# For SAM: Verify layer directories exist and contain packages
ls -la beautifulsoup4-library/python/
ls -la requests-library/python/

# For manual deployment: Create and upload layers separately
```
</details>

<details>
<summary><strong>IAM Permission Errors</strong></summary>

**Issue**: Access denied for SQS or CloudWatch operations

**Solution**: Verify the Lambda execution role has required permissions:
- `sqs:SendMessage`
- `sqs:GetQueueUrl` 
- `sqs:GetQueueAttributes`
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`
</details>

<details>
<summary><strong>Workflow Deployment Fails</strong></summary>

**Issue**: GitHub Actions workflow errors

**Solution**: Check repository secrets are correctly configured and the target Lambda function exists in AWS.
</details>

Choose the deployment method that best fits your development workflow and infrastructure requirements. SAM deployment is recommended for development environments, while workflow deployment excels for production CI/CD pipelines.

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
