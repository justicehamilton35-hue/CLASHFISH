# Test Clash Royale API Key (Windows PowerShell)
# This script tests if your API key is working correctly

Write-Host "🧪 Testing Clash Royale API Key" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "❌ Error: .env file not found" -ForegroundColor Red
    Write-Host "   Run: Copy-Item .env.example .env"
    Write-Host "   Then add your API key to the .env file"
    exit 1
}

# Load API key from .env
$envContent = Get-Content .env
$apiKey = $null

foreach ($line in $envContent) {
    if ($line -match '^CLASH_ROYALE_API_KEY=(.+)$') {
        $apiKey = $matches[1]
        break
    }
}

if ([string]::IsNullOrWhiteSpace($apiKey) -or $apiKey -eq 'your_api_key_here') {
    Write-Host "❌ Error: CLASH_ROYALE_API_KEY not set in .env" -ForegroundColor Red
    Write-Host "   Edit .env and add your API key"
    exit 1
}

# Check IP address
Write-Host "📍 Your current IP address:" -ForegroundColor Cyan
try {
    $myIp = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing).Content
    Write-Host "   $myIp" -ForegroundColor White
} catch {
    Write-Host "   Unable to determine IP" -ForegroundColor Yellow
    $myIp = "unknown"
}

Write-Host ""
Write-Host "⚠️  Make sure this IP is whitelisted at:" -ForegroundColor Yellow
Write-Host "   https://developer.clashroyale.com"
Write-Host ""

# Test API call with a known player
Write-Host "🎮 Testing API call..." -ForegroundColor Cyan
Write-Host "   Fetching player: #2PP (Surgical Goblin)"
Write-Host ""

try {
    $headers = @{
        "Authorization" = "Bearer $apiKey"
    }

    $response = Invoke-WebRequest `
        -Uri "https://api.clashroyale.com/v1/players/%232PP" `
        -Headers $headers `
        -UseBasicParsing `
        -ErrorAction Stop

    $statusCode = $response.StatusCode

    if ($statusCode -eq 200) {
        Write-Host "✅ SUCCESS! API key is working correctly" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Player data received:" -ForegroundColor Cyan

        # Parse JSON and display key info
        $playerData = $response.Content | ConvertFrom-Json
        Write-Host "   Name: $($playerData.name)" -ForegroundColor White
        Write-Host "   Tag: $($playerData.tag)" -ForegroundColor White
        Write-Host "   Trophies: $($playerData.trophies)" -ForegroundColor White
        Write-Host "   Wins: $($playerData.wins)" -ForegroundColor White
        Write-Host "   Losses: $($playerData.losses)" -ForegroundColor White

        Write-Host ""
        Write-Host "✅ You're all set! Your API key is configured correctly." -ForegroundColor Green
        Write-Host "   Run: .\scripts\start_dev.ps1 to start the server" -ForegroundColor Cyan
    }

} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__

    if ($statusCode -eq 403) {
        Write-Host "❌ FAILED: Access Denied (403)" -ForegroundColor Red
        Write-Host ""
        Write-Host "This usually means:" -ForegroundColor Yellow
        Write-Host "  1. ❌ Your IP address ($myIp) is not whitelisted"
        Write-Host "  2. ❌ Your API key is invalid or expired"
        Write-Host ""
        Write-Host "To fix this:" -ForegroundColor Cyan
        Write-Host "  1. Go to: https://developer.clashroyale.com"
        Write-Host "  2. Edit your API key"
        Write-Host "  3. Add your IP address: $myIp"
        Write-Host "  4. Wait a few minutes for changes to take effect"
        Write-Host "  5. Run this test again"

    } elseif ($statusCode -eq 404) {
        Write-Host "⚠️  Player not found (404)" -ForegroundColor Yellow
        Write-Host "   API key works, but player #2PP not found"
        Write-Host "   This is unusual - the test player should exist"
        Write-Host ""
        Write-Host "✅ Your API key appears to be working!" -ForegroundColor Green

    } elseif ($statusCode -eq 429) {
        Write-Host "⚠️  Rate limit exceeded (429)" -ForegroundColor Yellow
        Write-Host "   Wait a few seconds and try again"
        Write-Host ""
        Write-Host "✅ Your API key appears to be working (just rate limited)" -ForegroundColor Green

    } elseif ($statusCode -eq 503) {
        Write-Host "⚠️  Clash Royale API is temporarily unavailable (503)" -ForegroundColor Yellow
        Write-Host "   Try again in a few minutes"

    } else {
        Write-Host "❌ FAILED: HTTP $statusCode" -ForegroundColor Red
        Write-Host ""
        Write-Host "Error details:" -ForegroundColor Yellow
        Write-Host $_.Exception.Message
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
