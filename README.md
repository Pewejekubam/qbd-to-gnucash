# Modular JSON Mapping Documentation

This project uses modular JSON dictionaries to map QuickBooks list types to GNUCash-compatible hierarchies and attributes.

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
The mapping file for accounts is located at `mappings/accounts_mapping.json` and is dynamically loaded during processing.

## External References
This project aligns with the GNUCash CSV import logic, as detailed in the [GNUCash source code](https://github.com/Gnucash/gnucash/blob/stable/gnucash/import-export/csv-imp/assistant-csv-account-import.c). Key considerations include:
- **Commodity Validation**: Ensuring valid commodities (e.g., `USD`) are associated with accounts.
- **Namespace Mapping**: Using `CURRENCY` as the namespace for currencies like `USD`.
- **Account Hierarchy**: Defining parent accounts before child accounts to maintain a valid hierarchy.

These principles are implemented in the `convert_accounts` function to ensure compatibility with GNUCash.
