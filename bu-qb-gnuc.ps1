# Define source and target locations
$source = (Get-Item -Path ".\qbd-to-gnucash").FullName
$targetRoot = (Get-Item -Path "\git-root").FullName
$timestamp = Get-Date -Format "yyyyMMddHHmm"
$archiveName = "qbd-to-gnucash-archive-$timestamp.zip"
$target = Join-Path -Path $targetRoot -ChildPath $archiveName

# Create the archive, suppressing output
Compress-Archive -Path $source\* -DestinationPath $target -Force -CompressionLevel Optimal | Out-Null

# Get archive information
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