import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(data, output_file):
    """
    Create a vertical PDF report from the given data.

    Args:
        data (dict): The parsed JSON data containing product information.
        output_file (str): Path to save the generated PDF.
    """
    # Prepare the PDF document in vertical layout
    pdf = SimpleDocTemplate(output_file, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add a title
    title = Paragraph("GDI Hovercam Report", styles["Title"])
    elements.append(title)

    # Add a spacer
    elements.append(Paragraph("<br/>", styles["BodyText"]))

    # Create a table header with word wrapping for column headings
    table_data = [
        [
            Paragraph("Product Name", styles["BodyText"]),
            Paragraph("QTY In<br/>Stock", styles["BodyText"]),
            Paragraph("Price", styles["BodyText"]),
            Paragraph("Inventory<br/>Value", styles["BodyText"]),
            Paragraph("Sales (Week)", styles["BodyText"]),
            Paragraph("Open<br/>Sales<br/>Orders", styles["BodyText"]),
            Paragraph("Open<br/>Purchase<br/>Orders", styles["BodyText"]),
            Paragraph("Current Inventory", styles["BodyText"]),
            Paragraph("Weekly Avg Sales 12M", styles["BodyText"]),
            Paragraph("Run Rate (M)", styles["BodyText"]),
        ]
    ]

    # Add data rows with truncated product names
    for product in data["wd"]:
        table_data.append([
            product["product_name"][:20],  # Truncate to first 20 characters
            product["base_fields"]["QTY_In_Stock"],
            product["base_fields"]["GDI_Purchase_Price"],
            product["base_fields"]["Inventory_Value"],
            product["base_fields"]["Weekly_Sales"],
            product["base_fields"]["Open_Sales_Orders"],
            product["base_fields"]["Open_Purchase_Orders"],
            product["base_fields"]["Current_Inventory"],
            round(product["calculated_fields"]["12m_avg_sales"], 2),
            round(product["calculated_fields"]["run_rate"], 2),
        ])

    # Adjust column widths: Product Name wider, others fixed at ~0.25 inches
    col_widths = [150, 40, 40, 50, 40, 50, 50, 50, 50, 50]  # Wider for product name, ~0.25 inch (~40 points) for others

    # Create the table with specified column widths
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header row
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Body row background
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid
    ]))

    # Add the table to the PDF elements
    elements.append(table)

    # Build the PDF
    pdf.build(elements)
    print(f"PDF report created successfully: {output_file}")


def main():
    # Load the JSON data
    with open("output.json", "r") as json_file:
        data = json.load(json_file)

    # Generate the PDF report
    create_pdf(data, "Product_Weekly_Data_Report.pdf")


if __name__ == "__main__":
    main()
