

# import streamlit as st
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import re
# import time
# import random
# import urllib3
# import io
# from urllib.parse import urlparse, urljoin

# # Disable SSL warnings
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# def clean_website_url(url):
#     """
#     Clean and validate website URL.
    
#     :param url: Input URL string
#     :return: Cleaned and validated URL or None
#     """
#     # Handle NaN or empty values
#     if pd.isna(url) or not isinstance(url, str):
#         return None
    
#     # Remove leading/trailing whitespace
#     url = url.strip().lower()
    
#     # Skip invalid entries
#     if url in ['nan', 'none', ''] or len(url) < 4:
#         return None
    
#     # Add http/https prefix if missing
#     if not url.startswith(('http://', 'https://')):
#         url = 'https://' + url
    
#     return url

# def extract_email(text):
#     """
#     Extract email addresses from text using multiple regex patterns.
    
#     :param text: Input text to search for emails
#     :return: List of unique email addresses
#     """
#     # Multiple email patterns to catch various formats
#     email_patterns = [
#         r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
#         r'\(at\)', # Catch obfuscated emails
#         r'\[at\]',
#         r'\(dot\)',
#         r'\[dot\]'
#     ]
    
#     # Collect all emails
#     all_emails = []
#     for pattern in email_patterns:
#         all_emails.extend(re.findall(pattern, str(text), re.IGNORECASE))
    
#     # Clean and normalize emails
#     cleaned_emails = []
#     for email in all_emails:
#         # Replace obfuscated patterns
#         email = email.replace('(at)', '@').replace('[at]', '@')
#         email = email.replace('(dot)', '.').replace('[dot]', '.')
        
#         # Validate email format
#         if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email, re.IGNORECASE):
#             cleaned_emails.append(email.lower())
    
#     return list(set(cleaned_emails))

# def comprehensive_website_scrape(url, progress_callback=None, timeout=15):
#     """
#     Comprehensive website scraping strategy.
    
#     :param url: Website URL to scrape
#     :param progress_callback: Optional callback to update progress
#     :param timeout: Request timeout in seconds
#     :return: List of extracted emails
#     """
#     # Validate URL
#     if not url:
#         return []
    
#     try:
#         # Comprehensive user agent list to rotate
#         user_agents = [
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
#             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
#         ]
        
#         headers = {
#             'User-Agent': random.choice(user_agents),
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.5',
#             'Referer': 'https://www.google.com/',
#         }
        
#         # Potential page URLs to check
#         page_urls = [
#             url,  # Main page
#             urljoin(url, '/'),  # Index page
#             urljoin(url, '/contact'),
#             urljoin(url, '/contact-us'),
#             urljoin(url, '/about'),
#             urljoin(url, '/about-us'),
#         ]
        
#         # Ensure unique URLs
#         page_urls = list(dict.fromkeys(page_urls))
        
#         # Collect all emails
#         all_emails = set()
        
#         # Try each URL
#         for page_url in page_urls:
#             try:
#                 # Optional progress update
#                 if progress_callback:
#                     progress_callback(f"Checking {page_url}")
                
#                 # Send request with comprehensive settings
#                 response = requests.get(
#                     page_url, 
#                     headers=headers, 
#                     timeout=timeout, 
#                     verify=False,  # Disable SSL verification
#                     allow_redirects=True
#                 )
                
#                 # Check for successful response
#                 response.raise_for_status()
                
#                 # Parse HTML
#                 soup = BeautifulSoup(response.text, 'html.parser')
                
#                 # Extract text from different parts of the page
#                 full_text = []
                
#                 # Add text from header and footer
#                 if soup.header:
#                     full_text.append(soup.header.get_text())
#                 if soup.footer:
#                     full_text.append(soup.footer.get_text())
                
#                 # Add text from specific common div classes
#                 common_classes = [
#                     'contact', 'contact-info', 'footer', 
#                     'header', 'site-header', 'site-footer',
#                     'top-bar', 'bottom-bar'
#                 ]
                
#                 for cls in common_classes:
#                     for div in soup.find_all(['div', 'section'], class_=re.compile(cls, re.IGNORECASE)):
#                         full_text.append(div.get_text())
                
#                 # Extract from entire page text
#                 full_text.append(soup.get_text())
                
#                 # Combine and extract emails
#                 combined_text = ' '.join(full_text)
#                 page_emails = extract_email(combined_text)
                
#                 # Add to total emails
#                 all_emails.update(page_emails)
            
#             except requests.exceptions.HTTPError as http_err:
#                 # Handle specific HTTP errors
#                 if progress_callback:
#                     progress_callback(f"HTTP Error on {page_url}: {http_err}")
#                 continue
#             except Exception as page_err:
#                 # Silently handle page-specific errors
#                 if progress_callback:
#                     progress_callback(f"Error checking {page_url}: {page_err}")
#                 continue
        
#         return list(all_emails)
    
#     except Exception as e:
#         # Catch-all for any unexpected errors
#         if progress_callback:
#             progress_callback(f"Unexpected error scraping {url}: {str(e)}")
#         return []

# def process_websites(df, website_column):
#     """
#     Process websites and extract emails with enhanced error handling.
    
#     :param df: DataFrame containing websites
#     :param website_column: Column name with website links
#     :return: Updated DataFrame
#     """
#     # Create a copy of the DataFrame to avoid modifying the original
#     working_df = df.copy()
    
#     # Add a new column for emails
#     working_df['Extracted Emails'] = ''
    
#     # Progress tracking
#     progress_bar = st.progress(0)
#     status_text = st.empty()
#     error_container = st.container()
    
#     # Track errors
#     errors = []
    
#     # Scrape emails for each website
#     total_rows = len(working_df)
#     for index, row in working_df.iterrows():
#         # Update progress
#         progress = int((index + 1) / total_rows * 100)
#         progress_bar.progress(progress)
        
#         # Clean website URL
#         website = clean_website_url(row[website_column])
        
#         # Skip invalid websites
#         if not website:
#             continue
        
#         # Update status
#         status_text.text(f"Scraping {website}...")
        
#         # Define progress callback for this website
#         def progress_callback(msg):
#             status_text.text(msg)
        
#         # Extract emails
#         try:
#             emails = comprehensive_website_scrape(website, progress_callback)
            
#             # Store emails in the dataframe
#             if emails:
#                 working_df.at[index, 'Extracted Emails'] = '; '.join(emails)
#             else:
#                 # Log websites with no emails found
#                 errors.append(f"No emails found for {website}")
        
#         except Exception as e:
#             # Capture and log any unexpected errors
#             errors.append(f"Error processing {website}: {str(e)}")
        
#         # Be nice to servers, add random delay
#         time.sleep(random.uniform(0.5, 1.5))
    
#     # Display errors if any
#     if errors:
#         with error_container:
#             with st.expander("Errors and Warnings"):
#                 for error in errors:
#                     st.warning(error)
    
#     # Clear status and progress
#     status_text.empty()
#     progress_bar.empty()
    
#     return working_df

# def main():
#     st.title("Website Email Scraper 🌐📧")
    
#     # File uploader with expanded options
#     uploaded_file = st.file_uploader(
#         "Choose an Excel file", 
#         type=['xlsx', 'xls','csv'],
#         help="Upload an Excel file with website links. Maximum file size: 200MB"
#     )
    
#     if uploaded_file is not None:
#         try:
#             # Read the Excel file
#             df = pd.read_excel(uploaded_file)
            
#             # Display file contents
#             st.subheader("File Contents")
#             st.dataframe(df.head())
            
#             # Column selection
#             website_column = st.selectbox(
#                 "Select the column containing website links",
#                 df.columns
#             )
            
#             # Scrape button
#             if st.button("Scrape Emails"):
#                 # Validate column selection
#                 if website_column not in df.columns:
#                     st.error(f"Column '{website_column}' not found in the file!")
#                     return
                
#                 # Process websites and extract emails
#                 result_df = process_websites(df, website_column)
                
#                 # Display results
#                 st.subheader("Scraped Results")
#                 st.dataframe(result_df)
                
#                 # Download button
#                 # Use in-memory bytes instead of file path
#                 output = io.BytesIO()
#                 with pd.ExcelWriter(output, engine='openpyxl') as writer:
#                     result_df.to_excel(writer, index=False)
#                 output.seek(0)
                
#                 st.download_button(
#                     label="Download Scraped Results",
#                     data=output,
#                     file_name='scraped_emails.xlsx',
#                     mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#                 )
        
#         except Exception as e:
#             st.error(f"An error occurred: {e}")

# # Sidebar with information
# def show_sidebar():
#     st.sidebar.title("About This App")
#     st.sidebar.info("""
#     ### Website Email Scraper
    
#     **Enhanced Features:**
#     - Comprehensive email extraction
#     - Checks multiple page sections
#     - Handles obfuscated emails
#     - Robust error handling
    
#     **Extraction Strategy:**
#     - Main page
#     - Index page
#     - Contact pages
#     - Header and footer
#     - Common information divs
    
#     **Limitations:**
#     - Some websites may block scraping
#     - Not all emails may be found
#     - Respect website terms of service
#     """)
    
#     st.sidebar.warning("⚠️ Ethical Scraping: Always get permission!")

# if __name__ == '__main__':
#     show_sidebar()
#     main()




# import streamlit as st
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import re
# import time
# import random
# import urllib3
# import io
# from urllib.parse import urlparse, urljoin

# # Disable SSL warnings
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# def clean_website_url(url):
#     """
#     Clean and validate website URL.
    
#     :param url: Input URL string
#     :return: Cleaned and validated URL or None
#     """
#     # Handle NaN or empty values
#     if pd.isna(url) or not isinstance(url, str):
#         return None
    
#     # Remove leading/trailing whitespace
#     url = url.strip().lower()
    
#     # Skip invalid entries
#     if url in ['nan', 'none', ''] or len(url) < 4:
#         return None
    
#     # Add http/https prefix if missing
#     if not url.startswith(('http://', 'https://')):
#         url = 'https://' + url
    
#     return url

# def extract_email(text):
#     """
#     Extract email addresses from text using multiple regex patterns.
    
#     :param text: Input text to search for emails
#     :return: List of unique email addresses
#     """
#     # Multiple email patterns to catch various formats
#     email_patterns = [
#         r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
#         r'\(at\)', # Catch obfuscated emails
#         r'\[at\]',
#         r'\(dot\)',
#         r'\[dot\]'
#     ]
    
#     # Collect all emails
#     all_emails = []
#     for pattern in email_patterns:
#         all_emails.extend(re.findall(pattern, str(text), re.IGNORECASE))
    
#     # Clean and normalize emails
#     cleaned_emails = []
#     for email in all_emails:
#         # Replace obfuscated patterns
#         email = email.replace('(at)', '@').replace('[at]', '@')
#         email = email.replace('(dot)', '.').replace('[dot]', '.')
        
#         # Validate email format
#         if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email, re.IGNORECASE):
#             cleaned_emails.append(email.lower())
    
#     return list(set(cleaned_emails))

# def comprehensive_website_scrape(url, progress_callback=None, timeout=15):
#     """
#     Comprehensive website scraping strategy.
    
#     :param url: Website URL to scrape
#     :param progress_callback: Optional callback to update progress
#     :param timeout: Request timeout in seconds
#     :return: List of extracted emails
#     """
#     # Validate URL
#     if not url:
#         return []
    
#     try:
#         # Comprehensive user agent list to rotate
#         user_agents = [
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
#             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
#         ]
        
#         headers = {
#             'User-Agent': random.choice(user_agents),
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.5',
#             'Referer': 'https://www.google.com/',
#         }
        
#         # Potential page URLs to check
#         page_urls = [
#             url,  # Main page
#             urljoin(url, '/'),  # Index page
#             urljoin(url, '/contact'),
#             urljoin(url, '/contact-us'),
#             urljoin(url, '/about'),
#             urljoin(url, '/about-us'),
#         ]
        
#         # Ensure unique URLs
#         page_urls = list(dict.fromkeys(page_urls))
        
#         # Collect all emails
#         all_emails = set()
        
#         # Try each URL
#         for page_url in page_urls:
#             try:
#                 # Optional progress update
#                 if progress_callback:
#                     progress_callback(f"Checking {page_url}")
                
#                 # Send request with comprehensive settings
#                 response = requests.get(
#                     page_url, 
#                     headers=headers, 
#                     timeout=timeout, 
#                     verify=False,  # Disable SSL verification
#                     allow_redirects=True
#                 )
                
#                 # Check for successful response
#                 response.raise_for_status()
                
#                 # Parse HTML
#                 soup = BeautifulSoup(response.text, 'html.parser')
                
#                 # Extract text from different parts of the page
#                 full_text = []
                
#                 # Add text from header and footer
#                 if soup.header:
#                     full_text.append(soup.header.get_text())
#                 if soup.footer:
#                     full_text.append(soup.footer.get_text())
                
#                 # Add text from specific common div classes
#                 common_classes = [
#                     'contact', 'contact-info', 'footer', 
#                     'header', 'site-header', 'site-footer',
#                     'top-bar', 'bottom-bar'
#                 ]
                
#                 for cls in common_classes:
#                     for div in soup.find_all(['div', 'section'], class_=re.compile(cls, re.IGNORECASE)):
#                         full_text.append(div.get_text())
                
#                 # Extract from entire page text
#                 full_text.append(soup.get_text())
                
#                 # Combine and extract emails
#                 combined_text = ' '.join(full_text)
#                 page_emails = extract_email(combined_text)
                
#                 # Add to total emails
#                 all_emails.update(page_emails)
            
#             except requests.exceptions.HTTPError as http_err:
#                 # Handle specific HTTP errors
#                 if progress_callback:
#                     progress_callback(f"HTTP Error on {page_url}: {http_err}")
#                 continue
#             except Exception as page_err:
#                 # Silently handle page-specific errors
#                 if progress_callback:
#                     progress_callback(f"Error checking {page_url}: {page_err}")
#                 continue
        
#         return list(all_emails)
    
#     except Exception as e:
#         # Catch-all for any unexpected errors
#         if progress_callback:
#             progress_callback(f"Unexpected error scraping {url}: {str(e)}")
#         return []

# def process_websites(df, website_column):
#     """
#     Process websites and extract emails with enhanced error handling.
    
#     :param df: DataFrame containing websites
#     :param website_column: Column name with website links
#     :return: Updated DataFrame
#     """
#     # Create a copy of the DataFrame to avoid modifying the original
#     working_df = df.copy()
    
#     # Add a new column for emails
#     working_df['Extracted Emails'] = ''
    
#     # Progress tracking
#     progress_bar = st.progress(0)
#     status_text = st.empty()
#     error_container = st.container()
    
#     # Track errors
#     errors = []
    
#     # Scrape emails for each website
#     total_rows = len(working_df)
#     for index, row in working_df.iterrows():
#         # Update progress
#         progress = int((index + 1) / total_rows * 100)
#         progress_bar.progress(progress)
        
#         # Clean website URL
#         website = clean_website_url(row[website_column])
        
#         # Skip invalid websites
#         if not website:
#             continue
        
#         # Update status
#         status_text.text(f"Scraping {website}...")
        
#         # Define progress callback for this website
#         def progress_callback(msg):
#             status_text.text(msg)
        
#         # Extract emails
#         try:
#             emails = comprehensive_website_scrape(website, progress_callback)
            
#             # Store emails in the dataframe
#             if emails:
#                 working_df.at[index, 'Extracted Emails'] = '; '.join(emails)
#             else:
#                 # Log websites with no emails found
#                 errors.append(f"No emails found for {website}")
        
#         except Exception as e:
#             # Capture and log any unexpected errors
#             errors.append(f"Error processing {website}: {str(e)}")
        
#         # Be nice to servers, add random delay
#         time.sleep(random.uniform(0.5, 1.5))
    
#     # Display errors if any
#     if errors:
#         with error_container:
#             with st.expander("Errors and Warnings"):
#                 for error in errors:
#                     st.warning(error)
    
#     # Clear status and progress
#     status_text.empty()
#     progress_bar.empty()
    
#     return working_df

# def read_file(uploaded_file):
#     """
#     Read uploaded file based on file type.
    
#     :param uploaded_file: Uploaded file object
#     :return: Pandas DataFrame
#     """
#     file_name = uploaded_file.name.lower()
    
#     try:
#         # Handle CSV files
#         if file_name.endswith('.csv'):
#             df = pd.read_csv(uploaded_file)
#         # Handle Excel files
#         elif file_name.endswith(('.xlsx', '.xls')):
#             df = pd.read_excel(uploaded_file)
#         else:
#             st.error(f"Unsupported file format: {file_name}. Please upload a CSV or Excel file.")
#             return None
            
#         return df
#     except Exception as e:
#         st.error(f"Error reading file: {str(e)}")
#         return None

# def main():
#     st.title("Website Email Scraper 🌐📧")
    
#     # File uploader with expanded options
#     uploaded_file = st.file_uploader(
#         "Choose a file", 
#         type=['xlsx', 'xls', 'csv'],
#         help="Upload a file with website links. Maximum file size: 200MB"
#     )
    
#     if uploaded_file is not None:
#         # Read the file based on extension
#         df = read_file(uploaded_file)
        
#         if df is not None:
#             # Display file contents
#             st.subheader("File Contents")
#             st.dataframe(df.head())
            
#             # Column selection
#             website_column = st.selectbox(
#                 "Select the column containing website links",
#                 df.columns
#             )
            
#             # Scrape button
#             if st.button("Scrape Emails"):
#                 # Validate column selection
#                 if website_column not in df.columns:
#                     st.error(f"Column '{website_column}' not found in the file!")
#                     return
                
#                 # Process websites and extract emails
#                 result_df = process_websites(df, website_column)
                
#                 # Display results
#                 st.subheader("Scraped Results")
#                 st.dataframe(result_df)
                
#                 # Download button
#                 # Use in-memory bytes instead of file path
#                 output = io.BytesIO()
                
#                 # Determine output file format based on input
#                 if uploaded_file.name.lower().endswith('.csv'):
#                     # Save as CSV
#                     csv_data = result_df.to_csv(index=False)
#                     output_filename = 'scraped_emails.csv'
#                     mime_type = 'text/csv'
#                     st.download_button(
#                         label="Download Scraped Results (CSV)",
#                         data=csv_data,
#                         file_name=output_filename,
#                         mime=mime_type
#                     )
#                 else:
#                     # Save as Excel
#                     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#                         result_df.to_excel(writer, index=False)
#                     output.seek(0)
                    
#                     st.download_button(
#                         label="Download Scraped Results (Excel)",
#                         data=output,
#                         file_name='scraped_emails.xlsx',
#                         mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#                     )



# if __name__ == '__main__':
   
#     main()



import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import urllib3
import io
from urllib.parse import urlparse, urljoin

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def clean_website_url(url):
    """
    Clean and validate website URL.
    
    :param url: Input URL string
    :return: Cleaned and validated URL or None
    """
    # Handle NaN or empty values
    if pd.isna(url) or not isinstance(url, str):
        return None
    
    # Remove leading/trailing whitespace
    url = url.strip().lower()
    
    # Skip invalid entries
    if url in ['nan', 'none', ''] or len(url) < 4:
        return None
    
    # Add http/https prefix if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url

def extract_email(text):
    """
    Extract email addresses from text using multiple regex patterns.
    
    :param text: Input text to search for emails
    :return: List of unique email addresses
    """
    # Multiple email patterns to catch various formats
    email_patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        r'\(at\)', # Catch obfuscated emails
        r'\[at\]',
        r'\(dot\)',
        r'\[dot\]'
    ]
    
    # Collect all emails
    all_emails = []
    for pattern in email_patterns:
        all_emails.extend(re.findall(pattern, str(text), re.IGNORECASE))
    
    # Clean and normalize emails
    cleaned_emails = []
    for email in all_emails:
        # Replace obfuscated patterns
        email = email.replace('(at)', '@').replace('[at]', '@')
        email = email.replace('(dot)', '.').replace('[dot]', '.')
        
        # Validate email format
        if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email, re.IGNORECASE):
            cleaned_emails.append(email.lower())
    
    return list(set(cleaned_emails))

def comprehensive_website_scrape(url, progress_callback=None, timeout=15):
    """
    Comprehensive website scraping strategy.
    
    :param url: Website URL to scrape
    :param progress_callback: Optional callback to update progress
    :param timeout: Request timeout in seconds
    :return: List of extracted emails
    """
    # Validate URL
    if not url:
        return []
    
    try:
        # Comprehensive user agent list to rotate
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        }
        
        # Potential page URLs to check
        page_urls = [
            url,  # Main page
            urljoin(url, '/'),  # Index page
            urljoin(url, '/contact'),
            urljoin(url, '/contact-us'),
            urljoin(url, '/about'),
            urljoin(url, '/about-us'),
        ]
        
        # Ensure unique URLs
        page_urls = list(dict.fromkeys(page_urls))
        
        # Collect all emails
        all_emails = set()
        
        # Try each URL
        for page_url in page_urls:
            try:
                # Optional progress update
                if progress_callback:
                    progress_callback(f"Checking {page_url}")
                
                # Send request with comprehensive settings
                response = requests.get(
                    page_url, 
                    headers=headers, 
                    timeout=timeout, 
                    verify=False,  # Disable SSL verification
                    allow_redirects=True
                )
                
                # Check for successful response
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract text from different parts of the page
                full_text = []
                
                # Add text from header and footer
                if soup.header:
                    full_text.append(soup.header.get_text())
                if soup.footer:
                    full_text.append(soup.footer.get_text())
                
                # Add text from specific common div classes
                common_classes = [
                    'contact', 'contact-info', 'footer', 
                    'header', 'site-header', 'site-footer',
                    'top-bar', 'bottom-bar'
                ]
                
                for cls in common_classes:
                    for div in soup.find_all(['div', 'section'], class_=re.compile(cls, re.IGNORECASE)):
                        full_text.append(div.get_text())
                
                # Extract from entire page text
                full_text.append(soup.get_text())
                
                # Combine and extract emails
                combined_text = ' '.join(full_text)
                page_emails = extract_email(combined_text)
                
                # Add to total emails
                all_emails.update(page_emails)
            
            except requests.exceptions.HTTPError as http_err:
                # Handle specific HTTP errors
                if progress_callback:
                    progress_callback(f"HTTP Error on {page_url}: {http_err}")
                continue
            except Exception as page_err:
                # Silently handle page-specific errors
                if progress_callback:
                    progress_callback(f"Error checking {page_url}: {page_err}")
                continue
        
        return list(all_emails)
    
    except Exception as e:
        # Catch-all for any unexpected errors
        if progress_callback:
            progress_callback(f"Unexpected error scraping {url}: {str(e)}")
        return []

def process_websites(df, website_column):
    """
    Process websites and extract emails with enhanced error handling.
    
    :param df: DataFrame containing websites
    :param website_column: Column name with website links
    :return: Updated DataFrame
    """
    # Create a copy of the DataFrame to avoid modifying the original
    working_df = df.copy()
    
    # Add a new column for emails
    working_df['Extracted Emails'] = ''
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    error_container = st.container()
    
    # Track errors
    errors = []
    
    # Scrape emails for each website
    total_rows = len(working_df)
    for index, row in working_df.iterrows():
        # Update progress
        progress = int((index + 1) / total_rows * 100)
        progress_bar.progress(progress)
        
        # Clean website URL
        website = clean_website_url(row[website_column])
        
        # Skip invalid websites
        if not website:
            continue
        
        # Update status
        status_text.text(f"Scraping {website}...")
        
        # Define progress callback for this website
        def progress_callback(msg):
            status_text.text(msg)
        
        # Extract emails
        try:
            emails = comprehensive_website_scrape(website, progress_callback)
            
            # Store emails in the dataframe
            if emails:
                working_df.at[index, 'Extracted Emails'] = '; '.join(emails)
            else:
                # Log websites with no emails found
                errors.append(f"No emails found for {website}")
        
        except Exception as e:
            # Capture and log any unexpected errors
            errors.append(f"Error processing {website}: {str(e)}")
        
        # Be nice to servers, add random delay
        time.sleep(random.uniform(0.5, 1.5))
    
    # Display errors if any
    if errors:
        with error_container:
            with st.expander("Errors and Warnings"):
                for error in errors:
                    st.warning(error)
    
    # Clear status and progress
    status_text.empty()
    progress_bar.empty()
    
    return working_df

def read_file(uploaded_file):
    """
    Read uploaded file based on file type.
    
    :param uploaded_file: Uploaded file object
    :return: Pandas DataFrame
    """
    file_name = uploaded_file.name.lower()
    
    try:
        # Handle CSV files
        if file_name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        # Handle Excel files
        elif file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file format: {file_name}. Please upload a CSV or Excel file.")
            return None
            
        return df
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

def main():
    # Create a two-column layout for the header
    header_col1, header_col2 = st.columns([1, 4])
    
    # Add logo in the first column
    with header_col1:
        st.image("https://nec-codes.s3.us-east-1.amazonaws.com/logo+_sk.png", width=100)
    
    # Add title in the second column
    with header_col2:
        
        st.title("Website Email Scraper 🌐📧")
    
    # File uploader with expanded options
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=['xlsx', 'xls', 'csv'],
        help="Upload a file with website links. Maximum file size: 200MB"
    )
    
    if uploaded_file is not None:
        # Read the file based on extension
        df = read_file(uploaded_file)
        
        if df is not None:
            # Display file contents
            st.subheader("File Contents")
            st.dataframe(df.head())
            
            # Column selection
            website_column = st.selectbox(
                "Select the column containing website links",
                df.columns
            )
            
            # Scrape button
            if st.button("Scrape Emails"):
                # Validate column selection
                if website_column not in df.columns:
                    st.error(f"Column '{website_column}' not found in the file!")
                    return
                
                # Process websites and extract emails
                result_df = process_websites(df, website_column)
                
                # Display results
                st.subheader("Scraped Results")
                st.dataframe(result_df)
                
                # Download button
                # Use in-memory bytes instead of file path
                output = io.BytesIO()
                
                # Determine output file format based on input
                if uploaded_file.name.lower().endswith('.csv'):
                    # Save as CSV
                    csv_data = result_df.to_csv(index=False)
                    output_filename = 'scraped_emails.csv'
                    mime_type = 'text/csv'
                    st.download_button(
                        label="Download Scraped Results (CSV)",
                        data=csv_data,
                        file_name=output_filename,
                        mime=mime_type
                    )
                else:
                    # Save as Excel
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        result_df.to_excel(writer, index=False)
                    output.seek(0)
                    
                    st.download_button(
                        label="Download Scraped Results (Excel)",
                        data=output,
                        file_name='scraped_emails.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )



if __name__ == '__main__':
  
    main()