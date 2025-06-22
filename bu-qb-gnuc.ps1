# Define source and target locations
$source = (Get-Item -Path ".").FullName
$targetRoot = (Get-Item -Path "\git-root").FullName

# Get Git short commit hash (fallback to 'nogit' if git fails)
try {
    $commitHash = git rev-parse --short HEAD 2>$null
    if (-not $commitHash) {
        $commitHash = "nogit"
    }
} catch {
    $commitHash = "nogit"
}

# Get Git commit message
try {
    $commitMessage = git log -1 --format=%s
} catch {
    $commitMessage = "No commit message available"
}

# Generate timestamp and archive name
$timestamp = Get-Date -Format "yyyyMMddHHmm"
$archiveName = "qbd-to-gnucash-$timestamp-$commitHash.zip"
$target = Join-Path -Path $targetRoot -ChildPath $archiveName
$commitMessageFile = Join-Path -Path $source -ChildPath "commit_message.txt"

# Create commit message file
try {
    $commitMessage | Out-File -FilePath $commitMessageFile -Encoding utf8
} catch {
    Write-Error "Failed to create commit message file: $_"
    exit 1
}

# Check if the source directory exists
if (!(Test-Path $source)) {
    Write-Error "Source directory '$source' does not exist."
    Remove-Item -Path $commitMessageFile -Force -ErrorAction SilentlyContinue
    exit 1
}

# Ensure the target archive does not already exist
if (Test-Path $target) {
    Write-Error "Target archive '$target' already exists and is in use."
    Remove-Item -Path $commitMessageFile -Force -ErrorAction SilentlyContinue
    exit 1
}

# Create the archive, suppressing output
try {
    Compress-Archive -Path $source\* -DestinationPath $target -Force -CompressionLevel Optimal | Out-Null
} catch {
    Write-Error "Failed to create archive: $_"
    Remove-Item -Path $commitMessageFile -Force -ErrorAction SilentlyContinue
    exit 1
}

# Remove commit message file
try {
    Remove-Item -Path $commitMessageFile -Force
} catch {
    Write-Error "Failed to remove commit message file: $_"
}

# Get archive information
try {
    $archive = Get-Item -Path $target
    $archiveSize = $archive.Length
    $folderCount = (Get-ChildItem -Path $source -Recurse -Directory).Count
    $fileCount = (Get-ChildItem -Path $source -Recurse -File).Count + 1 # Include commit message file in count

    # Output the results
    Write-Host "Archive Information:"
    Write-Host "-------------------"
    Write-Host "Git Commit: $commitHash"
    Write-Host "Commit Message: $commitMessage"
    Write-Host "Source Structure: $source"
    Write-Host "Folders: $folderCount"
    Write-Host "Files: $fileCount"
    Write-Host "Size: $(if ($archiveSize -gt 1GB) {'{0:F2} GB' -f ($archiveSize/1GB)} elseif ($archiveSize -gt 1MB) {'{0:F2} MB' -f ($archiveSize/1MB)} else {'{0} KB' -f ($archiveSize/1KB)})"
    Write-Host "Target Location: $target"
} catch {
    Write-Error "Failed to retrieve archive information: $_"
    exit 1
}