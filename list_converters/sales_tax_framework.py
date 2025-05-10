# -----------------------------------------------------------------------------
# MODULE: Sales Tax Framework Parser
# PURPOSE: Parse and process Sales Tax Codes and Items from QuickBooks IIF files
# -----------------------------------------------------------------------------

import os

def parse_sales_tax_files(codes_file_path, items_file_path):
    """
    Parse the Sales Tax Codes and Items IIF files to extract relevant data.

    Args:
        codes_file_path (str): Path to the Sales Tax Codes IIF file.
        items_file_path (str): Path to the Sales Tax Items IIF file.

    Returns:
        dict: Extracted sales tax data including codes and items.
    """
    sales_tax_data = {"codes": [], "items": []}

    try:
        # Parse Sales Tax Codes
        with open(codes_file_path, 'r') as codes_file:
            for line in codes_file:
                if line.startswith("SALESTAXCODE"):
                    parts = line.strip().split('\t')
                    if len(parts) >= 7:
                        sales_tax_data["codes"].append({
                            "code": parts[1],
                            "description": parts[5],
                            "taxable": "Yes" if parts[6] == "Y" else "No"
                        })

        # Parse Sales Tax Items
        with open(items_file_path, 'r') as items_file:
            for line in items_file:
                if line.startswith("INVITEM") and "COMPTAX" in line:
                    parts = line.strip().split('\t')
                    if len(parts) >= 6:
                        sales_tax_data["items"].append({
                            "name": parts[1],
                            "rate": parts[5],
                            "account": parts[4]
                        })

    except Exception as e:
        print(f"Error parsing sales tax files: {e}")

    return sales_tax_data


def generate_sales_tax_html(output_file_path, sales_tax_data):
    """
    Generate an HTML guide for setting up the sales tax framework in GnuCash.

    Args:
        output_file_path (str): Path to the output HTML file.
        sales_tax_data (dict): Extracted sales tax data.
    """
    try:
        with open(output_file_path, 'w') as file:
            file.write("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sales Tax Framework Setup Guide</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
                    h1, h2 { color: #2c3e50; }
                    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                    table, th, td { border: 1px solid #ddd; }
                    th, td { padding: 10px; text-align: left; }
                    th { background-color: #f4f4f4; }
                    ul { margin: 10px 0; padding-left: 20px; }
                    .note { font-style: italic; color: #7f8c8d; }
                </style>
            </head>
            <body>
                <h1>Sales Tax Framework Setup Guide for GnuCash</h1>
                <p>This guide provides step-by-step instructions for manually setting up the sales tax framework in GnuCash based on extracted data from QuickBooks IIF files.</p>
            """)

            # Step 1: Liability Accounts
            file.write("<h2>Step 1: Create Sales Tax Liability Accounts</h2>")
            file.write("<p>Follow these steps to create liability accounts for each tax jurisdiction:</p>")
            file.write("<ol><li>Open GnuCash and navigate to <strong>Accounts</strong>.</li>")
            file.write("<li>Create a new account under <strong>Liabilities</strong> for each tax jurisdiction.</li></ol>")
            file.write("<table><thead><tr><th>Tax Jurisdiction</th><th>Account Name</th><th>Account Type</th></tr></thead><tbody>")
            for item in sales_tax_data["items"]:
                file.write(f"<tr><td>{item['name']}</td><td>Liabilities:Sales Tax:{item['name']}</td><td>Liability</td></tr>")
            file.write("</tbody></table>")

            # Step 2: Tax Tables
            file.write("<h2>Step 2: Set Up Tax Tables</h2>")
            file.write("<p>Define tax tables to link tax rates to the liability accounts:</p>")
            file.write("<ol><li>Navigate to <strong>Business &gt; Tax Tables</strong> in GnuCash.</li>")
            file.write("<li>Create a new tax table for each jurisdiction and assign the corresponding liability account.</li></ol>")
            file.write("<table><thead><tr><th>Tax Table Name</th><th>Tax Rate (%)</th><th>Linked Account</th></tr></thead><tbody>")
            for item in sales_tax_data["items"]:
                file.write(f"<tr><td>{item['name']} Tax Table</td><td>{item['rate']}</td><td>Liabilities:Sales Tax:{item['name']}</td></tr>")
            file.write("</tbody></table>")

            # Step 3: Taxable vs. Non-Taxable
            file.write("<h2>Step 3: Define Taxable vs. Non-Taxable Categories</h2>")
            file.write("<p>Classify items as taxable or non-taxable based on the sales tax codes:</p>")
            file.write("<ol><li>Review the sales tax codes extracted from the IIF files.</li>")
            file.write("<li>Assign each code to either <strong>Taxable</strong> or <strong>Non-Taxable</strong>.</li></ol>")
            file.write("<table><thead><tr><th>Sales Tax Code</th><th>Category</th></tr></thead><tbody>")
            for code in sales_tax_data["codes"]:
                file.write(f"<tr><td>{code['code']}</td><td>{code['taxable']}</td></tr>")
            file.write("</tbody></table>")

            file.write('<p class="note">Note: If the sales tax items file is missing, log an entry and skip this setup.</p>')
            file.write("</body></html>")
        print(f"Sales Tax Framework HTML generated at {output_file_path}")
    except Exception as e:
        print(f"Error generating HTML file: {e}")


def process_sales_tax_framework(codes_file_path, items_file_path, output_file_path):
    """
    Process the sales tax framework setup from IIF files and generate an HTML guide.

    Args:
        codes_file_path (str): Path to the Sales Tax Codes IIF file.
        items_file_path (str): Path to the Sales Tax Items IIF file.
        output_file_path (str): Path to the output HTML file.
    """
    sales_tax_data = parse_sales_tax_files(codes_file_path, items_file_path)
    generate_sales_tax_html(output_file_path, sales_tax_data)


if __name__ == "__main__":
    # Example usage
    codes_file = "c:\\git-root\\qbd-to-gnucash\\input\\sample-qbd-sales-tax-codes.IIF"
    items_file = "c:\\git-root\\qbd-to-gnucash\\input\\sample-qbd-sales-tax-items.IIF"
    output_file = "c:\\git-root\\qbd-to-gnucash\\sales_tax_framework_setup.html"
    process_sales_tax_framework(codes_file, items_file, output_file)
