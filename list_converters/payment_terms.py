# -----------------------------------------------------------------------------
# MODULE: Payment Terms Converter
# PURPOSE: Convert QuickBooks Payment Terms IIF files to HTML format
# -----------------------------------------------------------------------------

import os

def convert_payment_terms(iif_file_path, output_file_path):
    """
    Convert QuickBooks Payment Terms IIF file to a well-formatted HTML file.

    Args:
        iif_file_path (str): Path to the Payment Terms IIF file.
        output_file_path (str): Path to the output HTML file.
    """
    # Ensure the output file has a .html extension
    if not output_file_path.endswith('.html'):
        output_file_path = os.path.splitext(output_file_path)[0] + '.html'

    try:
        with open(iif_file_path, 'r') as iif_file, open(output_file_path, 'w') as output_file:
            # Write HTML header
            output_file.write("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Payment Terms</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        color: #333;
                        margin: 20px;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 12px;
                        text-align: left;
                    }
                    th {
                        background-color: #4CAF50;
                        color: white;
                        font-size: 1.2em;
                    }
                    tr:nth-child(even) {
                        background-color: #f9f9f9;
                    }
                    tr:hover {
                        background-color: #f1f1f1;
                    }
                    td {
                        font-size: 1.1em;
                    }
                </style>
            </head>
            <body>
                <h1>Payment Terms</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Discount %</th>
                            <th>Net Days</th>
                            <th>Discount Days</th>
                        </tr>
                    </thead>
                    <tbody>
            """)

            # Process the IIF file
            for line in iif_file:
                if line.startswith("TERMS"):
                    parts = line.strip().split('\t')
                    if len(parts) >= 7:
                        name = parts[1]
                        discount_percent = parts[4]
                        net_days = parts[5]
                        discount_days = parts[6]
                        output_file.write(f"""
                        <tr>
                            <td>{name}</td>
                            <td>{discount_percent}</td>
                            <td>{net_days}</td>
                            <td>{discount_days}</td>
                        </tr>
                        """)

            # Write HTML footer
            output_file.write("""
                    </tbody>
                </table>
            </body>
            </html>
            """)
        print(f"Payment Terms converted to {output_file_path}")
    except Exception as e:
        print(f"Error converting Payment Terms: {e}")