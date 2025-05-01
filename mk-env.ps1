# Create the project directory
$projectDir = "qbd_to_gnucash"
if (!(Test-Path $projectDir)) {
    New-Item -ItemType Directory -Path $projectDir
}

# Create the subdirectories
$subdirs = @("list_converters", "utils")
foreach ($subdir in $subdirs) {
    $path = Join-Path $projectDir $subdir
    if (!(Test-Path $path)) {
        New-Item -ItemType Directory -Path $path
    }
}

# Create the empty script files
$files = @(
    "main.py",
    "iif_parser.py",
    "config.py",
    "list_converters\__init__.py",
    "list_converters\accounts.py",
    "list_converters\customers.py",
    "list_converters\vendors.py",
    "list_converters\employees.py",
    "list_converters\items.py",
    "list_converters\sales_tax_codes.py",
    "utils\__init__.py",
    "utils\csv_writer.py",
    "utils\error_handler.py"
)

foreach ($file in $files) {
    $path = Join-Path $projectDir $file
    if (!(Test-Path $path)) {
        New-Item -ItemType File -Path $path
    }
}