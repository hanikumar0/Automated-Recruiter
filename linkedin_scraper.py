import json
import time
import random
import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from openai import OpenAI

COMPANY_URL = "https://www.linkedin.com/company/gohypemedia/people/"
OUTPUT_FILE = "employees.json"
RANKED_FILE = "top_candidates.json"
CSV_FILE = "best_candidates.csv"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def setup_driver():
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def manual_login(driver):
    print("Opening LinkedIn for manual login...")
    driver.get("https://www.linkedin.com/login")
    print("Please log in manually in the opened browser window.")
    while True:
        try:
            if "linkedin.com/feed" in driver.current_url or "linkedin.com/company" in driver.current_url:
                print("Login detected!")
                break
        except Exception:
            print("[!] Browser connection lost.")
            return False
        time.sleep(2)
    return True

def scrape_employees(driver, limit=50):
    print(f"Navigating to {COMPANY_URL}...")
    driver.get(COMPANY_URL)
    employees = []
    try:
        print("Waiting for list container...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".org-people-profile-card, .artdeco-card, .org-people-profiles-module"))
        )
    except TimeoutException:
        print("❌ Wait timed out. Check if the page loaded correctly.")
        return []

    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(employees) < limit:
        card_selectors = [
            "li.org-people-profile-card__card-spacing",
            ".org-people-profile-card",
            ".artdeco-card",
            "li.grid-community-item"
        ]
        cards = []
        for selector in card_selectors:
            found = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(found) > 0:
                cards = found
                break
        if not cards:
            cards = driver.find_elements(By.CSS_SELECTOR, ".org-people-profiles-module li")

        for card in cards:
            try:
                name = ""
                for s in [".org-people-profile-card__profile-title", ".lt-line-clamp--single-line", "div[class*='title']"]:
                    try:
                        name = card.find_element(By.CSS_SELECTOR, s).text.strip()
                        if name: break
                    except: continue

                headline = ""
                for s in [".lt-line-clamp--multi-line", ".artdeco-entity-lockup__subtitle", "div[class*='subtitle']"]:
                    try:
                        headline = card.find_element(By.CSS_SELECTOR, s).text.strip()
                        if headline: break
                    except: continue

                profile_url = "None"
                try:
                    link_elem = card.find_element(By.CSS_SELECTOR, "a")
                    href = link_elem.get_attribute("href")
                    if href and "/in/" in href:
                        profile_url = href.split('?')[0]
                except: pass
                
                if name and headline:
                    employee_data = {"name": name, "headline": headline, "profile_url": profile_url}
                    if not any(e['profile_url'] == profile_url for e in employees if profile_url != "None"):
                        employees.append(employee_data)
                        print(f"✅ [{len(employees)}] {name}")
                if len(employees) >= limit: break
            except: continue

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(4, 7)) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollBy(0, -500);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            if driver.execute_script("return document.body.scrollHeight") == last_height:
                break
        last_height = new_height
    return employees

def rank_candidates(employees):
    weights = {
        "mern": 25, "react": 15, "node": 15, "express": 10, "mongodb": 10, "full stack": 20
    }
    ranked = []
    for emp in employees:
        score = 0
        txt = emp.get('headline', '').lower()
        for kw, val in weights.items():
            if kw in txt: score += val
        emp_copy = emp.copy()
        emp_copy['score'] = score
        emp_copy['tier'] = "Top Talent" if score >= 30 else "Qualified" if score >= 15 else "Other"
        ranked.append(emp_copy)
    return sorted(ranked, key=lambda x: x['score'], reverse=True)

def analyze_with_ai(employees, api_key):
    client = OpenAI(api_key=api_key)
    profiles = "\n".join([f"- {e['name']}: {e['headline']}" for e in employees])
    prompt = f"Analyze these candidates for a MERN Stack project:\n{profiles}\n\nReturn JSON: {{'ranked_candidates': [{{'name':'','relevance_score':0,'reasoning':'','headline':'','profile_url':''}}]}}"
    try:
        print("🤖 AI Recruiter is analyzing candidates...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content).get("ranked_candidates", [])
    except Exception as e:
        print(f"❌ AI Failed: {e}. Switching to internal ranking.")
        return []

def save_to_csv(candidates, filename):
    if not candidates: return
    keys = candidates[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(candidates)
    print(f"📊 CSV saved to: {filename}")

def main():
    print("\n" + "="*50 + "\nAI RECRUITER BOT\n" + "="*50)
    data = []
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            data = json.load(f)
        if data:
            ans = input(f"[?] Found {len(data)} profiles. Use them? (y/n): ").lower()
            if ans != 'y': data = []

    if not data:
        bot = setup_driver()
        if manual_login(bot):
            data = scrape_employees(bot)
            bot.quit()
            if data:
                with open(OUTPUT_FILE, 'w') as f: json.dump(data, f, indent=2)
        else:
            bot.quit(); return

    res = analyze_with_ai(data, OPENAI_API_KEY)
    if not res:
        print("Applying internal keyword ranking...")
        raw_ranked = rank_candidates(data)
        res = []
        for r in raw_ranked:
            if r['score'] > 0:
                res.append({"name": r['name'], "relevance_score": r['score'], "reasoning": f"Headline Match ({r['tier']})", "headline": r['headline'], "profile_url": r['profile_url']})

    if res:
        save_to_csv(res, CSV_FILE)
        print("\n--- TOP RANKED ---")
        for i, c in enumerate(res[:5], 1):
            print(f"{i}. {c['name']} (Score: {c['relevance_score']}) -> {c['headline'][:60]}...")
    else:
        print("[!] No matching candidates found.")

if __name__ == "__main__":
    main()
