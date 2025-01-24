# **Business Data Scraper and Outreach Email Generator**

This application is designed to scrape restaurant or business data from the Wanderlog website and create personalized emails using AI. The workflow is seamless, combining data extraction, AI content generation, and email personalization to simplify outreach for businesses.

## **Features**
### **1. Wanderlog Data Scraper**
- Extracts business information such as:
  - Name
  - Phone number
  - Website
  - Ratings (Google, TripAdvisor, Wanderlog)
  - Description (About)
  - Wanderlog ranking and list position
  - Direct links to their pages
- Saves the extracted data to **CSV** and **Excel** formats for easy handling.

### **2. AI-Powered Email Generator**
- **Personalized Summaries**: 
  - Generates a concise business summary for each store using AI.
- **Custom Email Creation**:
  - Emails are tailored based on the type of website:
    - `.co.za` domains: Inquire about who is responsible for the website.
    - Facebook links: Propose benefits tailored to their business.
    - Other domains: Focus on general optimization suggestions.
- **Flexible Prompts**:
  - The AI leverages business details from the scraped data to make the content engaging and informative.

---

## **Installation**

### **Prerequisites**
1. **Python Version**: Ensure you have Python 3.7+ installed.
2. **Libraries**: Install the following dependencies:
   ```bash
   pip install pandas openpyxl requests beautifulsoup4 google-generativeai
   ```
3. **Google Gemini API Setup**:
   - Obtain an API key for Google Gemini from the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a `config.ini` file in the root directory and include your API key:
     ```ini
     [GoogleGeminiAPI]
     api_key = YOUR_API_KEY
     ```

---

## **How to Use**

### **Step 1: Scrape Business Data**
1. Update the `url` variable in the scraper script to the Wanderlog page of your choice.
2. Run the scraper:
   ```bash
   python scraper.py
   ```
3. Output files:
   - `wanderlog_restaurants.csv`
   - `wanderlog_restaurants.xlsx`

### **Step 2: Generate AI-Powered Emails**
1. Place the generated Excel file from the scraper in the same directory as the AI email generator script.
2. Run the script:
   ```bash
   python ai_email_generator.py
   ```
3. Output:
   - A new Excel file with company summaries and tailored emails.

---

## **Project Files**
1. **`scraper.py`**: Handles scraping data from Wanderlog and saving it in Excel/CSV formats.
2. **`ai_email_generator.py`**: Processes the Excel file, generates AI-powered summaries and emails, and saves the results.
3. **`config.ini`**: Contains the Google Gemini API key.
4. **Output Files**:
   - `wanderlog_restaurants.csv`
   - `wanderlog_restaurants.xlsx`
   - `enriched_data.xlsx`: Final output with AI-generated content.

---

## **Customization**
- **Scraper**:
  - Modify the `url` variable to scrape different Wanderlog pages.
  - Adjust the scraper to include additional fields if needed.
- **AI Prompts**:
  - Edit the prompt templates in `ai_email_generator.py` to match your tone and style.
- **Output**:
  - Modify the script to adjust the structure of the output Excel file if necessary.

---

## **Example Workflow**
### **Input (Excel File)**:
| Name       | Phone         | Website               | About                      | Link                           |
|------------|---------------|-----------------------|----------------------------|--------------------------------|
| Example A  | +27 123 4567  | exampleA.co.za        | A family restaurant...     | https://wanderlog.com/...      |
| Example B  | +27 987 6543  | facebook.com/exampleB | A modern café...           | https://wanderlog.com/...      |

### **Output (Enriched Excel File)**:
| Name       | Summary                          | Email                                                                                       |
|------------|----------------------------------|---------------------------------------------------------------------------------------------|
| Example A  | Example A is a family...         | Dear Example A, I’m Leo from LiiStudios... Who is responsible for maintaining your website? |
| Example B  | Example B is a modern café...    | Dear Example B, I’m Leo from LiiStudios... Let me propose an idea for improving your...    |

---

## **Contribution**
Feel free to submit issues or pull requests if you want to improve this project or add new features.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

Let me know if you'd like me to customize this further!