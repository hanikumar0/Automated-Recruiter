# Automated Recruiter System

A Python-based automation framework designed for extracting employee information from LinkedIn company pages and identifying candidates for MERN Stack roles using artificial intelligence and weighted keyword evaluation.

## Functional Overview

The Automated Recruiter System streamlines the technical recruitment process by collecting data directly from LinkedIn and applying a scoring logic to identify high-potential candidates. The system handles anti-scraping measures through manual session integration and provides robust fallback mechanisms for data analysis.

## Core Features

- **Automated Data Extraction**: Utilizes Selenium WebDriver to navigate company people pages and capture essential data points including full names, professional headlines, and profile URLs.
- **Manual Authentication Integration**: Implements a dedicated manual login phase to ensure account safety and bypass automated detection systems.
- **AI-Driven Candidate Ranking**: Integrated with OpenAI GPT-4o API for advanced natural language processing of professional headlines to determine technical suitability.
- **Weighted Fallback Engine**: Includes a native ranking algorithm that calculates relevance scores based on technical keyword density (MongoDB, Express, React, Node.js) when API access is unavailable.
- **Data Export Utilities**: Generates standardized output files in both CSV and JSON formats for integration with external CRM or ATS platforms.

## Technical Specifications

- **Language**: Python 3.9 or higher
- **Browser Automation**: Selenium WebDriver
- **AI Integration**: OpenAI API (GPT-4o)
- **Data Formats**: Structured JSON for raw data, CSV for analytical reports

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/hanikumar0/Automated-Recruiter.git
   cd Automated-Recruiter
   ```

2. Install the necessary Python packages:
   ```bash
   pip install selenium openai
   ```

3. Ensure that a compatible version of Google Chrome is installed on the host system.

## Operational Guide

1. Initiate the main execution script:
   ```bash
   python linkedin_scraper.py
   ```

2. Data Collection Process:
   - Select the option to perform a fresh scrape.
   - Complete the authentication process manually in the automated browser window.
   - Allow the system to navigate and scroll through the company profile until the target limit is reached.

3. Analysis and Export:
   - The system will prompt for an OpenAI API key to perform advanced analysis.
   - If a key is not provided, the internal ranking logic will automatically execute.
   - Final results are saved to the project directory as 'best_candidates.csv'.

## Project Structure

- `linkedin_scraper.py`: Primary application containing scraping and analytical logic.
- `employees.json`: Permanent storage for raw profile data.
- `best_candidates.csv`: Final processed report containing ranked talent.
- `.gitignore`: Configuration to exclude environment-specific files and temporary data assets.

## Compliance and Usage

This software is developed for professional recruitment and educational research. Users are responsible for ensuring compliance with platform-specific terms of service and data privacy regulations.
