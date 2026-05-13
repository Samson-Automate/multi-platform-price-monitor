# Multi-Platform Competitor Price Monitor and Alert System

A production-ready, automated Python scripting tool built to track competitor pricing changes in real-time. The system automatically extracts live pricing, logs history in a local SQLite database, and fires instant notifications via Discord Webhooks when a price drop is detected.

## Key Features

* Automated Web Scraping: Extracts dynamic pricing data securely from target product pages.
* Smart Alert Engine: Evaluates live data against history logs to identify price reductions immediately.
* Instant Discord Integration: Pushes real-time, clean markdown embedded alerts to your Discord channel.
* Lightweight Local Storage: Utilizes an SQLite3 database to maintain comprehensive pricing history records.
* Continuous Automation: Operational 24/7 via an internal Python scheduling background worker.
* Secure Environment: Zero hardcoded credentials. Managed cleanly via an external configuration file.

## Tech Stack

* Language: Python 3.8+
* Libraries: BeautifulSoup4, Requests, Schedule
* Database: SQLite3 (Built-in)
* Integration: Discord Webhooks API

## Repository File Structure

```text
├── config.json          # Credentials and target URLs configuration
├── requirements.txt     # Python environment external dependencies
└── scraper_alert.py     # Main background automation controller engine
```

## Terminal Execution Preview

Below is the live execution log showcasing successful database initialization and the automation engine transition into background monitoring state:

<img width="968" height="158" alt="terminal_output png" src="https://github.com/user-attachments/assets/3924064b-fcee-498d-ad74-dceb139f0136" />

## Quick Start Guide

### 1. Installation
Clone or download the project files to your local directory.

### 2. Dependencies Setup
Run the environment configuration installation command in your terminal:
```bash
pip install -r requirements.txt
```

### 3. Update Configuration
Configure your credentials in the config.json file:
```json
{
    "discord_webhook_url": "YOUR_DISCORD_WEBHOOK_URL",
    "check_interval_minutes": 60,
    "products_to_track": [
        {
            "name": "Sony Headphones",
            "url": "https://ebay.com"
        }
    ]
}
```

### 4. Initialize Tracker
Launch the script execution sequence inside the terminal:
```bash
python scraper_alert.py
```

## Business and Freelance Value

* Automated Overhead Reduction: Saves hours of daily manual auditing operations.
* Competitive Edge: Enables e-commerce store operators to react dynamically to pricing shifts.
* Lightweight Deployment: Runs entirely in the background without needing heavy browser engines.

## Contact and Collaboration

If you are looking to integrate custom web scrapers, data pipelines, or workflow automation tools for your business, feel free to reach out:

* Email: samsonpatras34@gmail.com
* X (Twitter): [Twitter/X Profile](https://x.com/Samson_Automate/)
* Discord: `samson005473`

Need help deploying this script or want a custom automation solution built for your specific business requirements? Let's connect and discuss your project.

Thanks and Best Regards,
Samson


