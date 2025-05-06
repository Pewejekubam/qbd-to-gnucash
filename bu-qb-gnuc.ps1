# Define source and target locations
$source = (Get-Item -Path ".").FullName
$targetRoot = (Get-Item -Path "\git-root").FullName
$timestamp = Get-Date -Format "yyyyMMddHHmm"
$archiveName = "qbd-to-gnucash-archive-$timestamp.zip"
$target = Join-Path -Path $targetRoot -ChildPath $archiveName

# Check if the source directory exists
if (!(Test-Path $source)) {
    Write-Error "Source directory '$source' does not exist."
    exit 1
}

# Ensure the target archive does not already exist
if (Test-Path $target) {
    Write-Error "Target archive '$target' already exists and is in use."
    exit 1
}

# Create the archive, suppressing output
try {
    Compress-Archive -Path $source\* -DestinationPath $target -Force -CompressionLevel Optimal | Out-Null
} catch {
    Write-Error "Failed to create archive: $_"
    exit 1
}

# Get archive information
try {
    $archive = Get-Item -Path $target
    $archiveSize = $archive.Length
    $folderCount = (Get-ChildItem -Path $source -Recurse -Directory).Count
    $fileCount = (Get-ChildItem -Path $source -Recurse -File).Count

    # Output the results
    Write-Host "Archive Information:"
    Write-Host "-------------------"
    Write-Host "Source Structure: $source"
    Write-Host "Folders: $folderCount"
    Write-Host "Files: $fileCount"
    Write-Host "Size: $(if ($archiveSize -gt 1GB) {'{0:F2} GB' -f ($archiveSize/1GB)} elseif ($archiveSize -gt 1MB) {'{0:F2} MB' -f ($archiveSize/1MB)} else {'{0} KB' -f ($archiveSize/1KB)})"
    Write-Host "Target Location: $target"
} catch {
    Write-Error "Failed to retrieve archive information: $_"
    exit 1
}