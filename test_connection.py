from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Supabase credentials from the .env file
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")

# Initialize Supabase client
supabase = create_client(supabase_url, supabase_key)

# Test: Insert data into the Hovercam_Report table
print("Inserting a row...")
insert_response = supabase.table("Hovercam_Report").insert({
    "Date": "2024-02-01",  # Replace with an actual date
    "Product_Name": "Hovercam X100",  # Replace with a product name
    "Gdi_Purchase_Price": 299.99,  # Replace with a purchase price
    "Qty_In_Stock": 30,  # Replace with quantity
    "Inventory_Value": 14999.50  # Replace with inventory value
}).execute()

print("Insert response:", insert_response)

# Test: Fetch data from the Hovercam_Report table
print("Fetching rows...")
select_response = supabase.table("Hovercam_Report").select("*").execute()
print("Select response:", select_response.data)