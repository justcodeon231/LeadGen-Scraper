# **Business Data Scraper and Outreach Email Generator**  

## **Overview**  
This application is a powerful tool for scraping business or restaurant data from the Wanderlog website and generating personalized outreach emails using AI. The seamless workflow integrates data extraction, content generation, and email customization, enabling efficient and targeted communication for businesses.  

---

## **Features**

### **1. Wanderlog Data Scraper**  
- Extracts comprehensive business data, including:  
  - Name  
  - Phone number  
  - Website  
  - Ratings (Google, TripAdvisor, Wanderlog)  
  - Description (About)  
  - Wanderlog ranking and list position  
  - Direct links to their pages  
- Saves the extracted data to **CSV** and **Excel** formats for easy handling and future reference.  

### **2. AI-Powered Email Generator**  
- **Personalized Summaries**:  
  - AI generates concise, tailored summaries for each business.  
- **Custom Email Creation**:  
  - Emails are crafted based on the website type:  
    - `.co.za` domains: Queries about who manages the website.  
    - Facebook links: Proposes benefits tailored to their social media presence.  
    - Other domains: Focuses on optimization and general improvement suggestions.  
- **Flexible Prompts**:  
  - Prompts leverage business details from the scraped data to make emails engaging and personalized.  

### **3. File Outputs**  
- Generates three key files:  
  - Raw data: `wanderlog_restaurants.csv` and `wanderlog_restaurants.xlsx`.  
  - Final enriched file with summaries and emails: `enriched_data.xlsx`.  

---

## **Installation**  

### **Prerequisites**  
1. **Python Version**: Requires Python 3.7+  
2. **Libraries**: Install dependencies via pip:  
   ```bash
   pip install pandas openpyxl requests beautifulsoup4 google-generativeai
   ```  
3. **Google Gemini API Setup**:  
   - Obtain an API key from the [Google Cloud Console](https://console.cloud.google.com/).  
   - Add the key to a `config.ini` file in the root directory:  
     ```ini
     [GoogleGeminiAPI]
     api_key = YOUR_API_KEY
     ```  

---

## **How to Use**  

### **Step 1: Scrape Business Data**  
1. Update the `url` variable in `scraper.py` to your target Wanderlog page.  
2. Run the scraper:  
   ```bash
   python scraper.py
   ```  
3. Extracted data will be saved as:  
   - `wanderlog_restaurants.csv`  
   - `wanderlog_restaurants.xlsx`  

### **Step 2: Generate AI-Powered Emails**  
1. Ensure the Excel file from Step 1 is in the same directory as `ai_email_generator.py`.  
2. Run the email generator script:  
   ```bash
   python ai_email_generator.py
   ```  
3. The final enriched file (`enriched_data.xlsx`) will include AI-generated summaries and personalized emails.  

---

## **Key Project Files**  
1. **`scraper.py`**: Handles data scraping from Wanderlog.  
2. **`ai_email_generator.py`**: Processes scraped data and generates summaries/emails using AI.  
3. **`config.ini`**: Contains your Google Gemini API key.  
4. **Output Files**:  
   - `wanderlog_restaurants.csv`  
   - `wanderlog_restaurants.xlsx`  
   - `enriched_data.xlsx`  

---

## **Customization**  

- **Scraper Configuration**:  
  - Update the `url` variable in `scraper.py` to scrape different Wanderlog pages.  
  - Add new fields by modifying the `scrape_restaurant_page` function.  

- **AI Prompt Templates**:  
  - Modify the prompts in `ai_email_generator.py` to customize the tone and style of generated emails.  

- **File Outputs**:  
  - Adjust the structure of output Excel files to match specific needs.  

---

## **Example Workflow**  

### **Input Data (Scraped Excel File)**:  
| Name       | Phone         | Website               | About                      | Link                           |  
|------------|---------------|-----------------------|----------------------------|--------------------------------|  
| Example A  | +27 123 4567  | exampleA.co.za        | A family restaurant...     | https://wanderlog.com/...      |  
| Example B  | +27 987 6543  | facebook.com/exampleB | A modern café...           | https://wanderlog.com/...      |  

### **Output Data (Enriched Excel File)**:  
| Name       | Summary                          | Email                                                                                       |  
|------------|----------------------------------|---------------------------------------------------------------------------------------------|  
| Example A  | Example A is a family...         | Dear Example A, I’m Leo from LiiStudios... Who is responsible for maintaining your website? |  
| Example B  | Example B is a modern café...    | Dear Example B, I’m Leo from LiiStudios... Let me propose an idea for improving your...    |  

---

## **Error Handling**  
- **Duplicate Data**: Avoids duplicate entries in output files.  
- **API Failures**: Retries up to three times for AI errors.  
- **Request Timeouts**: Automatically retries failed web page requests.  

---

## **Contribution**  
We welcome contributions! Feel free to submit issues, feature requests, or pull requests to enhance the project.  

---

## **License**  
This project is licensed under the MIT License.  

---  

Let me know if you need further edits or enhancements!