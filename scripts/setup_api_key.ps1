# ClashFish API Key Setup Script (Windows PowerShell)
# This script helps you securely configure your Clash Royale API key

Write-Host "🔑 ClashFish API Key Setup" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""

# Check if .env already exists
if (Test-Path .env) {
    Write-Host "⚠️  .env file already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to update it? (y/n)"
    if ($response -ne 'y' -and $response -ne 'Y') {
        Write-Host "Setup cancelled."
        exit 0
    }
    Write-Host ""
} else {
    # Create .env from template
    Copy-Item .env.example .env
    Write-Host "✅ Created .env file from template" -ForegroundColor Green
    Write-Host ""
}

# Prompt for API key
Write-Host "Please enter your Clash Royale API key information:"
Write-Host "(You can find this at https://developer.clashroyale.com)"
Write-Host ""

$apiKey = Read-Host "API Key (Bearer token)"

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host "❌ Error: API key cannot be empty" -ForegroundColor Red
    exit 1
}

# Update .env file
Write-Host ""
Write-Host "Updating .env file..." -ForegroundColor Yellow

# Read the file content
$envContent = Get-Content .env -Raw

# Replace the API key line
$envContent = $envContent -replace 'CLASH_ROYALE_API_KEY=.*', "CLASH_ROYALE_API_KEY=$apiKey"
$envContent = $envContent -replace 'USE_MOCK_DATA=.*', 'USE_MOCK_DATA=false'

# Write back to file
Set-Content -Path .env -Value $envContent -NoNewline

Write-Host "✅ API key configured successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "⚙️  Configuration updated:" -ForegroundColor Cyan
Write-Host "   - CLASH_ROYALE_API_KEY: $($apiKey.Substring(0, [Math]::Min(10, $apiKey.Length)))... (hidden)"
Write-Host "   - USE_MOCK_DATA: false (using real API)"
Write-Host ""
Write-Host "🎮 You can now analyze real players!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Start the server: .\scripts\start_dev.ps1"
Write-Host "2. Visit: http://localhost:8000"
Write-Host "3. Search for any player by their tag (e.g., #V2QUUQVU8)"
Write-Host ""
Write-Host "⚠️  Important: Your API key is stored in .env which is gitignored for security." -ForegroundColor Yellow
Write-Host "   Do not share this file or commit it to version control!"
Write-Host ""
