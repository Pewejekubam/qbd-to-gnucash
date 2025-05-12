import csv
import logging

def ensure_all_parents_exist(tree):
    new_entries = {}

    # Start with full list of existing account paths
    account_paths = set(tree.keys())

    # Build set of all required parent paths
    required_paths = set()
    for full_name in account_paths:
        parts = full_name.split(":")
        for i in range(1, len(parts)):
            required_paths.add(":".join(parts[:i]))

    # Add missing parents
    for parent_path in required_paths:
        if parent_path not in tree and parent_path not in new_entries:
            part = parent_path.split(":")[-1]
            new_entries[parent_path] = {
                "Type": "",
                "Account Name": part,
                "Account Code": "",
                "Description": "",
                "Account Color": "",
                "Notes": "",
                "Symbol": "USD",
                "Namespace": "CURRENCY",
                "Hidden": "F",
                "Tax Info": "F",
                "Placeholder": "T",
            }

    tree.update(new_entries)
    return tree

def sort_accounts_hierarchically(tree):
    return dict(sorted(tree.items(), key=lambda item: (item[0].count(":"), item[0])))

def write_gnucash_csv(tree, output_path):
    # ✅ Ensure all parents exist before writing
    tree = ensure_all_parents_exist(tree)
    tree = sort_accounts_hierarchically(tree)

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "Type",
            "Full Account Name",
            "Account Name",
            "Account Code",
            "Description",
            "Account Color",
            "Notes",
            "Symbol",
            "Namespace",
            "Hidden",
            "Tax Info",
            "Placeholder",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for full_name, data in tree.items():
            row = {
                "Type": data.get("Type", ""),
                "Full Account Name": full_name,  # ✅ Always use the key as the full path
                "Account Name": data.get("Account Name", ""),
                "Account Code": data.get("Account Code", ""),
                "Description": data.get("Description", ""),
                "Account Color": data.get("Account Color", ""),
                "Notes": data.get("Notes", ""),
                "Symbol": data.get("Symbol", "USD"),
                "Namespace": data.get("Namespace", "CURRENCY"),
                "Hidden": data.get("Hidden", "F"),
                "Tax Info": data.get("Tax Info", "F"),
                "Placeholder": data.get("Placeholder", "F"),
            }
            writer.writerow(row)
            logging.info(f"Wrote account: {full_name}")
