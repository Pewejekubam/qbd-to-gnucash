# Modular JSON Mapping Documentation

This project uses modular JSON dictionaries to map QuickBooks list types to GNUCash-compatible hierarchies and attributes.

## Workflow Overview

The workflow for processing IIF files and generating the accounts CSV file involves the following steps:

1. **Load Configuration**:
   - The `main.py` script loads configuration settings, including the input and output directories, from environment variables or a configuration file.

2. **Identify Input Files**:
   - The script scans the input directory for `.iif` files to process.

3. **Load Baseline Mapping**:
   - The baseline mapping file (`mappings/account_mapping_baseline.json`) is loaded. This file contains predefined mappings for common QuickBooks account types to GNUCash-compatible structures.

4. **Check for Specific Mapping File**:
   - The script checks if the specific mapping file (`account_mapping_specific.json`) exists in the output directory:
     - **If the file exists**:
       - It is loaded and merged with the baseline mapping to complete the account type mappings.
     - **If the file does not exist**:
       - The script identifies all unmapped account types from the input IIF file.
       - A new specific mapping file is created, containing these unmapped account types with default placeholders.
       - The script stops execution to allow the user to review and modify the specific mapping file.

5. **Process Accounts**:
   - The script processes the accounts in the IIF file:
     - It maps each account to its GNUCash-compatible structure using the merged mapping.
     - If an account type is not found in the mapping, the default rules from the baseline mapping are applied.

6. **Generate Accounts CSV**:
   - The processed accounts are written to an `accounts.csv` file in the output directory.
   - The accounts are sorted to ensure parent accounts are written before child accounts, maintaining a valid hierarchy.

7. **Iterative Workflow**:
   - The user can modify the specific mapping file to refine the mappings.
   - The script can be re-run to generate an updated `accounts.csv` file based on the modified mappings.

## File Structure

### Metadata
- `version`: Version of the mapping file.
- `last_updated`: Last modification date.
- `description`: Purpose of the file.

### Account Types
Each account type in QuickBooks is mapped to a GNUCash-compatible structure:
- `gnucash_type`: Corresponds to GNUCash account type (`BANK`, `ASSET`, etc.).
- `destination_hierarchy`: Target hierarchy in GNUCash.
- `placeholder`: Boolean indicating if the account is a parent/grouping account.

### Default Rules
Unmapped accounts are routed to a default hierarchy.

## Modular Approach
Each list type (e.g., accounts, customers, vendors) has its own JSON mapping file under the `mappings` directory. This ensures scalability and easier maintenance.

## Example Usage
The mapping file for accounts is located at `mappings/account_mapping_baseline.json` and is dynamically loaded during processing.

## External References
This project aligns with the GNUCash CSV import logic, as detailed in the [GNUCash source code](https://github.com/Gnucash/gnucash/blob/stable/gnucash/import-export/csv-imp/assistant-csv-account-import.c). Key considerations include:
- **Commodity Validation**: Ensuring valid commodities (e.g., `USD`) are associated with accounts.
- **Namespace Mapping**: Using `CURRENCY` as the namespace for currencies like `USD`.
- **Account Hierarchy**: Defining parent accounts before child accounts to maintain a valid hierarchy.

These principles are implemented in the `convert_accounts` function to ensure compatibility with GNUCash.
