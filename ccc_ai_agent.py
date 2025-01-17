#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import json
import os

# Load API keys from config.json
try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        os.environ["ANTHROPIC_API_KEY"] = config["ANTHROPIC_API_KEY"]
except FileNotFoundError:
    print("Error: config.json file not found. Please create one with your API keys.")
    exit(1)
except KeyError as e:
    print(f"Error: Missing key in config.json: {e}")
    exit(1)

#Imports
from typing import Literal, TypedDict
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from PIL import Image
from IPython.display import Image, display, HTML
import logging
import re
import requests
import pdfplumber
import io
import streamlit as st
import base64

#TOOLS
@tool
def webstaurantstore(query: str = None, product_limit: int = 10) -> str:
    """
    Scrapes the WebstaurantStore website for product data based on the search term with a user-defined product limit.

    Args:
    - query (str): The search term used to find products. Default is None.
    - product_limit (int): The maximum number of products to retrieve. Defaults to 10.

    Returns:
    - str: A string representation of the products found, including price, URL, and description.
    """
    import traceback
    import time 

    # Setup Edge WebDriver for Web Scraping
    options = Options()
    options.use_chromium = True
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    try:
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    except Exception as e:
        return f"Error initializing WebDriver: {e}"

    try:
        if not query:
            raise ValueError("Query term cannot be None or empty.")

        url = f"https://www.webstaurantstore.com/search/{query.replace(' ', '-')}.html"
        print(f"Navigating to URL: {url}")
        driver.get(url)

        # Retry logic if elements are not loaded within 10 seconds
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-box-container'))
                )
                break
            except Exception as wait_exception:
                retry_count += 1
                print(f"Retry {retry_count}/{max_retries} due to timeout: {wait_exception}")
                if retry_count >= max_retries:
                    raise TimeoutError("Failed to load product elements after multiple retries.")
                time.sleep(3)

        # Extract product details
        product_elements = driver.find_elements(By.CLASS_NAME, 'product-box-container')
        products = []

        for item in product_elements:
            try:
                description = item.find_element(By.CSS_SELECTOR, 'span[data-testid="itemDescription"]').text.strip()
                price = item.find_element(By.CSS_SELECTOR, '[data-testid="price"]').text.strip()
                product_link = item.find_element(By.CSS_SELECTOR, "a[data-testid='itemLink']").get_attribute('href')

                products.append({
                    'description': description,
                    'price': price,
                    'product_link': product_link
                })

                if len(products) >= product_limit:
                    break
            except Exception as detail_exception:
                print(f"Error extracting product details: {detail_exception}")
                traceback.print_exc()

        if not products:
            return "No products found. Please check the query or website structure."

        return str(products)

    except Exception as main_exception:
        print(f"Error during scraping: {main_exception}")
        traceback.print_exc()
        return f"Error during scraping: {main_exception}"

    finally:
        try:
            driver.quit()
            print("WebDriver closed successfully.")
        except Exception as quit_exception:
            print(f"Error closing WebDriver: {quit_exception}")


@tool
def icecastlefh(vehicle_name: str = None) -> str:
    """
    Fetches standard options from IceCastleFH based on the provided vehicle name, attempts to match the closest product page,
    and extracts floor plan information if available.

    Args:
    - vehicle_name (str): The name of the vehicle to search for. Default is None.

    Returns:
    - str: A string containing the extracted floor plan details along with the URL used to fetch the product information.
            If an error occurs, an appropriate error message is returned.
    """
    # Helper function to create a URL-friendly slug
    def create_slug(product_name):
        product_name = product_name.lower()
        product_name = product_name.replace('.', '-')
        product_name = re.sub(r"′\s*x\s*", '-x-', product_name)
        product_name = product_name.replace("'", '')
        product_name = re.sub(r'\s+x\s+', 'x', product_name)
        product_name = product_name.replace(' ', '-')
        product_name = re.sub(r'[^a-z0-9\-]', '', product_name)
        roduct_name = re.sub(r'-{2,}', '-', product_name)
        return product_name.strip('-')

    try:
        # Step 1: Create product slug
        slug = create_slug(vehicle_name)
        product_url = f"https://icecastlefh.com/product/{slug}"
        print(f"Fetching data from: {product_url}")

        # Step 2: Fetch product page
        response = requests.get(product_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 3: Find the PDF link
        pdf_link_tag = soup.find('a', href=lambda href: href and '/wp-content/uploads/' in href, 
                                 string=lambda text: text and 'Floor Plan' in text)
        
        if not pdf_link_tag or 'href' not in pdf_link_tag.attrs:
            return f"PDF link not found on the product page. URL: {product_url}"

        href = pdf_link_tag['href']
        pdf_url = href if href.startswith("http") else f"https://icecastlefh.com{href}"
        print(f"PDF URL found: {pdf_url}")

        # Step 4: Fetch PDF content
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()

        # Step 5: Extract text from PDF
        with pdfplumber.open(io.BytesIO(pdf_response.content)) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n\n"

        return f"Product URL: {product_url}\n\n{full_text.strip() if full_text.strip() else 'No text found in the PDF.'}"

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}\nURL: {product_url}"
    except Exception as e:
        return f"An unexpected error occurred: {e}\nURL: {product_url}"

 
tools = [webstaurantstore, icecastlefh]

tool_node = ToolNode(tools)

# Initialize model
model = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0).bind_tools(tools)

# Define the function that determines whether to continue or not
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Define the function that calls the model
def call_model(state: MessagesState):
    """
    Ensures the LLM always adheres to the format by using a system message.
    """
    system_message = """ 
You are a helpful assistant that only provides factual product information. 
Do not include any opinions, summaries, or extra commentary. 
Always present product data in a well-formatted table, regardless of the number of products returned, even if it's just one product.

Example Queries by the user:
'webstaurantstore' tool
1. Top 3 results for 2 compartment sinks
2. Top 5 results for reach-in refrigerators

`icecastlefh` tool
1. Does the 8′ x 17′ RV American Eagle have a full-size kitchen (or any products within the vehicle) - in case of questions specific to a vehicle, use the tool first to get the data and then use the extracted data to answer the question.
2. Is there a bunk bed in the 6.5′ x 14′ Hunter's Haven
3. Standard options for 8′ x 17′ Mille Lacs Hybrid

Instructions:
1. Present the output from the `webstaurantstore` tool as a well-formatted table, including columns for Description, Price, and Product Link. 
2. If any of the tools return error messages instead of product data, display the error message directly.
3. If you are using the `icecastlefh` tool, always display the URL along with the extracted details in a clear format.
4. Ensure the output is concise, easy to read, and visually clear for the user.

 
"""
    # Prepend the system message
    messages = [HumanMessage(role="system", content=system_message)] + state['messages']
    
    response = model.invoke(messages)
    
    return {"messages": [response]}

# Define the workflow graph
workflow = StateGraph(MessagesState)

#Nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

#Edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

# Initialize memory to persist state
checkpointer = MemorySaver()

# Compiling Graph
app = workflow.compile(checkpointer=checkpointer)

# Function to convert images to Base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Set the main page background to white */
        body, .stApp {
            background-color: white;
            color: black;
        }
        /* Align logos and title in a row */
        .logo-title-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px; /* Adjust spacing between logos and title */
        }
        .logo {
            width: 100px;  /* Confined width for logos */
            height: auto; /* Maintain aspect ratio */
            max-height: 100px; /* Prevent very tall images */
        }
        .title {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            background: linear-gradient(to right, #FF4B4B, #0073e6);
            -webkit-background-clip: text;
            color: transparent;
        }
        .subtitle {
            text-align: center;
            color: gray;
            font-size: 18px;
        }
        .stButton button {
            position: relative;
            visibility: visible !important; /* Ensure the button is always visible */
            opacity: 1 !important; /* Full opacity */
            background-color: black; /* Black button color */
            color: white; /* White text color for the button */
            font-size: 16px; /* Text size */
            border-radius: 5px; /* Rounded corners for the button */
            padding: 10px 20px; /* Button padding */
            border: none; /* Remove button border */
            cursor: pointer; /* Pointer cursor on hover */
            transition: transform 0.1s ease, background-color 0.2s ease; /* Add smooth animations */
        }
        .stButton button:active {
            transform: scale(0.95); /* Slightly shrink the button when clicked */
            background-color: #333; /* Slightly lighter black for a feedback effect */
        }

        /* Add hover effect for better interactivity */
        .stButton button:hover {
            background-color: #444; /* Dark gray on hover */
        }
    </style>
    """,
    unsafe_allow_html=True
)

def run_chatbot_streamlit():
    # Initialize state for the current chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Title and Logos
    uic_logo_base64 = image_to_base64("uic_logo.png")
    ccc_logo_base64 = image_to_base64("ccc_logo.png")
    st.markdown(
        f"""
        <div class="logo-title-container">
            <img src="data:image/png;base64,{uic_logo_base64}" class="logo">
            <div>
                <h1 class="title">LLM Powered AI Agent for Vehicle Data Workflow</h1>
                <p class="subtitle">Ask me about product details and I'll fetch them for you!</p>
            </div>
            <img src="data:image/png;base64,{ccc_logo_base64}" class="logo">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Current Chat Input
    user_input = st.text_input("You:", key="input", placeholder="Type your query here...")
    col1, col2 = st.columns([4, 1])
    with col2:
        submit_button = st.button("Submit", key="submit_button")

    # If a new query is passed
    if user_input:
        # Clear current messages for the new query
        st.session_state.messages = []

        # Add new user input to messages
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            st.write("Processing user input...")
            final_state = app.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config={"configurable": {"thread_id": 42}}
            )
            st.write("Response received!")
            response = final_state["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Display only the current chat
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div style='background-color: #e8f4ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; float: right; max-width: 70%; text-align: right;'>
                        <strong style='color: #0056b3;'>You:</strong> {msg["content"]}</div>
                    <div style='clear: both;'></div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style='background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px; max-width: 70%;'>
                        <strong style='color: #4CAF50;'>AI Assistant:</strong> {msg["content"]}</div>
                    """,
                    unsafe_allow_html=True,
                )

# Start Streamlit
if __name__ == "__main__":
    run_chatbot_streamlit()




