import pandas as pd
import configparser
import os
import google.generativeai as genai
import time

# Load API configuration
def configure_api(config_path='config.ini'):
    print("Configuring API...")
    config = configparser.ConfigParser()
    config.read(config_path)
    try:
        api_key = config['GoogleGeminiAPI']['api_key']
        print("API key loaded from config file.")
    except KeyError:
        api_key = input("Enter your Google Gemini API key: ")
        print("API key entered manually.")
    genai.configure(api_key=api_key)
    print("API configured successfully.")

# Generate AI response for a specific prompt with rate limiting
def generate_ai_response(prompt):
    print(f"Generating AI response for prompt: {prompt}")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    print("AI response generated.")
    time.sleep(1)  # Rate limiting to avoid overloading the API
    return response.text.strip()

# Process the Excel file and generate emails
def process_excel(file_path, output_path='output.xlsx'):
    print(f"Loading Excel file from {file_path}...")
    data = pd.read_excel(file_path)
    print("Excel file loaded successfully.")

    # Columns for output
    data['Summary'] = ''
    data['Email'] = ''

    for idx, row in data.iterrows():
        print(f"Processing row {idx + 1}...")
        # Extract data
        name = row['Name']
        phone = row['Phone']
        website = row['Website']
        about = row['About']

        # Step 1: Generate a company summary
        summary_prompt = f"Write a brief, professional company summary for a business named {name}. Description: {about}"
        summary = generate_with_retries(summary_prompt)
        data.at[idx, 'Summary'] = summary
        print(f"Summary for {name}: {summary}")

        # Step 2: Generate an introductory email
        if website.endswith('.co.za'):
            email_prompt = (f"Write an introductory email. Introduce me as Leo from Liistudios, a software agency based in East London. "
                            f"Include a personalized approach to {name} and ask who is in charge of their webpage ({website}). "
                            f"Make the email engaging and encourage them to inquire about how we can help improve their business.")
        elif 'facebook' in website:
            email_prompt = (f"Write an introductory email. Introduce me as Leo from Liistudios, a software agency based in East London. "
                            f"Propose a solution to improve their online presence and suggest the benefits tailored to their business "
                            f"as described: {about}. Focus on making the email compelling and highlighting specific benefits.")
        else:
            email_prompt = (f"Write an introductory email. Introduce me as Leo from Liistudios, a software agency based in East London. "
                            f"Inquire if they would be interested in improving their online presence and optimizing their website ({website}). "
                            f"Tailor it to {name} and include insights based on: {about}. Make it engaging and professional.")

        email = generate_with_retries(email_prompt)
        data.at[idx, 'Email'] = email
        print(f"Email for {name}: {email}")

        # Save the enriched data back to a new Excel file after each row
        data.to_excel(output_path, index=False)
        print(f"Progress saved to {output_path}")

        # Increase rate limit after processing each business
        time.sleep(5)  # Adjust the sleep time as needed (5 to 10 seconds)

    print(f"Output saved to {output_path}")

def generate_with_retries(prompt, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            return generate_ai_response(prompt)
        except Exception as e:
            print(f"Error generating response: {e}")
            retries += 1
            if retries >= max_retries:
                print("Max retries reached. Exiting.")
                raise

# Main function
def main():
    print("Starting the script...")
    # Configure API
    configure_api()

    # Input and output file paths
    input_file_name = input("Enter the input Excel file name (without extension): ")
    output_file_name = input("Enter the output Excel file name (without extension): ")

    # Add extensions to file names
    input_file = f"{input_file_name}.xlsx"
    output_file = f"{output_file_name}.xlsx"

    # Ensure the output directory exists
    output_dir = 'Leads'
    os.makedirs(output_dir, exist_ok=True)

    # Full path for the output file
    output_file = os.path.join(output_dir, output_file)

    # Process the data and generate summaries and emails
    process_excel(input_file, output_file)
    print("Script finished successfully.")

if __name__ == "__main__":
    main()
    try:
        process_excel(input_file, output_file)
        print("Script finished successfully.")
        os.startfile(output_file)  # Open the output file
    except Exception as e:
        print(f"An error occurred: {e}")
        os.startfile(output_file)  # Attempt to open the output file even if there was an error
