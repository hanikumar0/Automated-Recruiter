# Automated Recruiter 🤖

A professional Python-based automation tool designed to scrape employee data from LinkedIn company pages and identify the best candidates for **MERN Stack** projects using AI analysis and smart keyword matching.

## 🚀 Key Features

- **LinkedIn Scraper**: Uses Selenium to navigate company "People" tabs and extract employee names, headlines, and profile URLs.
- **Manual Login Integration**: Avoids bot detection and CAPTCHAs by allowing the user to log in manually before the scraping starts.
- **AI Recruiter (Step 2)**: Integrates with **OpenAI GPT-4o** to analyze candidate headlines and provide a relevance score based on specific technical criteria (MongoDB, Express, React, Node.js).
- **Smart Fallback Ranking**: If no API key is provided or the quota is exceeded, the bot uses an internal weighted keyword matching engine to rank candidates.
- **Multi-Format Export**: Automatically generates detailed reports in both **CSV** (for Excel/Google Sheets) and **JSON** formats.

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Automation**: Selenium WebDriver
- **AI**: OpenAI API (GPT-4o)
- **Data Handling**: JSON, CSV

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/hanikumar0/Automated-Recruiter.git
    cd Automated-Recruiter
    ```

2.  Install required dependencies:
    ```bash
    pip install selenium openai
    ```

3.  Ensure you have **Google Chrome** installed.

## 🚀 Usage

1.  Run the main script:
    ```bash
    python linkedin_scraper.py
    ```

2.  **Scrape Data**:
    - Choose `s` to start a new scrape.
    - A Chrome window will open. **Log in manually** to your LinkedIn account.
    - Once logged in, the script will automatically navigate to the company's people page and begin extraction.

3.  **Process & Rank**:
    - The script will ask for an OpenAI API Key.
    - If provided, it uses GPT-4o for deep analysis.
    - If skipped, it uses a built-in keyword ranking algorithm.

4.  **View Results**:
    - Check `best_candidates.csv` for the final ranked list.

## 📂 Project Structure

- `linkedin_scraper.py`: The core script for scraping and ranking.
- `employees.json`: Raw data extracted from LinkedIn.
- `top_candidates.json`: AI/Keyword-ranked result in JSON.
- `best_candidates.csv`: Final exported report.
- `.gitignore`: Prevents sensitive files and cache from being uploaded.

## ⚖️ Disclaimer

This tool is intended for educational and professional recruitment purposes only. Users must comply with LinkedIn's Terms of Service while using automation.

---
Built with ❤️ by [Hanikumar](https://github.com/hanikumar0)
