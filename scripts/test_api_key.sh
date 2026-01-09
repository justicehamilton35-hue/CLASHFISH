#!/bin/bash

# Test Clash Royale API Key
# This script tests if your API key is working correctly

echo "🧪 Testing Clash Royale API Key"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "   Run: cp .env.example .env"
    echo "   Then add your API key to the .env file"
    exit 1
fi

# Load API key from .env
source .env

if [ -z "$CLASH_ROYALE_API_KEY" ]; then
    echo "❌ Error: CLASH_ROYALE_API_KEY not set in .env"
    echo "   Edit .env and add your API key"
    exit 1
fi

# Check IP address
echo "📍 Your current IP address:"
MY_IP=$(curl -s https://api.ipify.org)
echo "   $MY_IP"
echo ""
echo "⚠️  Make sure this IP is whitelisted at:"
echo "   https://developer.clashroyale.com"
echo ""

# Test API call with a known player
echo "🎮 Testing API call..."
echo "   Fetching player: #2PP (Surgical Goblin)"
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" -X GET \
    "https://api.clashroyale.com/v1/players/%232PP" \
    -H "Authorization: Bearer $CLASH_ROYALE_API_KEY")

# Extract HTTP code and body
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ SUCCESS! API key is working correctly"
    echo ""
    echo "📊 Player data received:"
    # Pretty print JSON if jq is available
    if command -v jq &> /dev/null; then
        echo "$BODY" | jq '{name: .name, tag: .tag, trophies: .trophies, wins: .wins, losses: .losses}'
    else
        echo "$BODY" | head -c 200
        echo "..."
    fi
    echo ""
    echo "✅ You're all set! Your API key is configured correctly."
    echo "   Run: ./scripts/start_dev.sh to start the server"
elif [ "$HTTP_CODE" = "403" ]; then
    echo "❌ FAILED: Access Denied (403)"
    echo ""
    echo "This usually means:"
    echo "  1. ❌ Your IP address ($MY_IP) is not whitelisted"
    echo "  2. ❌ Your API key is invalid or expired"
    echo ""
    echo "To fix this:"
    echo "  1. Go to: https://developer.clashroyale.com"
    echo "  2. Edit your API key"
    echo "  3. Add your IP address: $MY_IP"
    echo "  4. Wait a few minutes for changes to take effect"
    echo "  5. Run this test again"
elif [ "$HTTP_CODE" = "404" ]; then
    echo "⚠️  Player not found (404)"
    echo "   API key works, but player #2PP not found"
    echo "   This is unusual - the test player should exist"
    echo ""
    echo "✅ Your API key appears to be working!"
elif [ "$HTTP_CODE" = "429" ]; then
    echo "⚠️  Rate limit exceeded (429)"
    echo "   Wait a few seconds and try again"
    echo ""
    echo "✅ Your API key appears to be working (just rate limited)"
elif [ "$HTTP_CODE" = "503" ]; then
    echo "⚠️  Clash Royale API is temporarily unavailable (503)"
    echo "   Try again in a few minutes"
else
    echo "❌ FAILED: HTTP $HTTP_CODE"
    echo ""
    echo "Response:"
    echo "$BODY" | head -c 500
    echo ""
fi

echo ""
echo "================================"
