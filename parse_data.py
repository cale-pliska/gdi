import json
from typing import List, Dict, Any
from datetime import datetime

def parse_data(data: List[List[Any]]) -> List[Dict[str, Any]]:
    """
    Parse raw spreadsheet data into a list of dictionaries.
    Assumes the first row contains headers.
    """
    headers = data[0]
    return [dict(zip(headers, row)) for row in data[1:]]

def get_most_recent_week(data: List[Dict[str, Any]]) -> str:
    """
    Get the most recent 'Week_Starting_Date' from the dataset.
    """
    return max(data, key=lambda x: datetime.strptime(x['Week_Starting_Date'], '%m/%d/%Y'))['Week_Starting_Date']

def calculate_12m_avg_sales(product_data: List[Dict[str, Any]]) -> float:
    """
    Calculate the 12-month average sales for a product.
    """
    sales = [float(row['Weekly_Sales']) for row in product_data]
    return sum(sales) / len(sales) if sales else 0.0

def calculate_run_rate(qty_in_stock: int, avg_sales: float) -> float:
    """
    Calculate the run rate (months of inventory left) for a product.
    """
    return qty_in_stock / avg_sales if avg_sales > 0 else 0.0

def process_data(data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Process the data to create a list of dictionaries for each product's weekly data.
    The final structure will be { 'wd': [ {}, {}, ... {} ] }.
    """
    most_recent_week = get_most_recent_week(data)
    weekly_data = []

    # Process data for each unique product
    unique_products = set(row['Product_Name'] for row in data)
    for product_name in unique_products:
        # Filter data for the specific product
        product_data = [row for row in data if row['Product_Name'] == product_name]

        # Get data for the most recent week
        most_recent_row = next(row for row in product_data if row['Week_Starting_Date'] == most_recent_week)

        # Calculate 12m avg sales and run rate
        avg_sales = calculate_12m_avg_sales(product_data)
        run_rate = calculate_run_rate(int(most_recent_row['QTY_In_Stock']), avg_sales)

        # Add product data to weekly data list
        weekly_data.append({
            "product_name": product_name,
            "base_fields": {
                "QTY_In_Stock": most_recent_row['QTY_In_Stock'],
                "GDI_Purchase_Price": most_recent_row['GDI_Purchase_Price'],
                "Inventory_Value": most_recent_row['Inventory_Value'],
                "Weekly_Sales": most_recent_row['Weekly_Sales'],
                "Open_Sales_Orders": most_recent_row['Open_Sales_Orders'],
                "Open_Purchase_Orders": most_recent_row['Open_Purchase_Orders'],
                "Current_Inventory": most_recent_row['Current_Inventory']
            },
            "calculated_fields": {
                "12m_avg_sales": avg_sales,
                "run_rate": run_rate
            }
        })

    # Return the final structure with 'wd' as the top-level key
    return {"wd": weekly_data}


def main():
    # Example input: Replace this with the actual data from your source
    raw_data = [
        # Header row
        ["Edit_Timestamp", "Week_Starting_Date", "Week_Ending_Date", "Product_Name", 
         "QTY_In_Stock", "GDI_Purchase_Price", "Inventory_Value", "Weekly_Sales", 
         "Open_Sales_Orders", "Open_Purchase_Orders", "Current_Inventory"],
        # Data rows
        ["11/23/2024 18:29:50", "9/29/2024", "10/5/2024", "HCS8+ (HOVERCAM SOLO 8 PLUS)", 3179, 252.41, 802304.39, 206, 0, 0, 3179],
        ["11/23/2024 18:35:27", "10/6/2024", "10/12/2024", "HCS8+ (HOVERCAM SOLO 8 PLUS)", 3171, 252.41, 799917.11, 8, 0, 1000, 3171],
        # Add more rows as needed
    ]

    # Parse and process data
    parsed_data = parse_data(raw_data)
    processed_data = process_data(parsed_data)

    # Save to JSON or use as needed
    with open('processed_output.json', 'w') as json_file:
        json.dump(processed_data, json_file, indent=2)

    # Print for debugging/logging
    print(json.dumps(processed_data, indent=2))

if __name__ == '__main__':
    main()
