#!/bin/bash

# ClashFish API Key Setup Script
# This script helps you securely configure your Clash Royale API key

echo "🔑 ClashFish API Key Setup"
echo "=========================="
echo ""

# Check if .env already exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists"
    read -p "Do you want to update it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
    echo ""
else
    # Create .env from template
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
fi

# Prompt for API key
echo "Please enter your Clash Royale API key information:"
echo "(You can find this at https://developer.clashroyale.com)"
echo ""

read -p "API Key (Bearer token): " API_KEY

if [ -z "$API_KEY" ]; then
    echo "❌ Error: API key cannot be empty"
    exit 1
fi

# Update .env file
echo ""
echo "Updating .env file..."

# Use sed to update the API key line
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/^CLASH_ROYALE_API_KEY=.*/CLASH_ROYALE_API_KEY=${API_KEY}/" .env
    sed -i '' "s/^USE_MOCK_DATA=.*/USE_MOCK_DATA=false/" .env
else
    # Linux
    sed -i "s/^CLASH_ROYALE_API_KEY=.*/CLASH_ROYALE_API_KEY=${API_KEY}/" .env
    sed -i "s/^USE_MOCK_DATA=.*/USE_MOCK_DATA=false/" .env
fi

echo "✅ API key configured successfully!"
echo ""
echo "⚙️  Configuration updated:"
echo "   - CLASH_ROYALE_API_KEY: ${API_KEY:0:10}... (hidden)"
echo "   - USE_MOCK_DATA: false (using real API)"
echo ""
echo "🎮 You can now analyze real players!"
echo ""
echo "Next steps:"
echo "1. Start the server: ./scripts/start_dev.sh"
echo "2. Visit: http://localhost:8000"
echo "3. Search for any player by their tag (e.g., #V2QUUQVU8)"
echo ""
echo "⚠️  Important: Your API key is stored in .env which is gitignored for security."
echo "   Do not share this file or commit it to version control!"
echo ""
