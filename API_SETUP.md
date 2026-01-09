# Clash Royale API Setup Guide

This guide will help you configure your Clash Royale API key to analyze real player data.

---

## Getting Your API Key

1. **Visit**: https://developer.clashroyale.com
2. **Log in** with your Supercell ID
3. **Create an API Key**:
   - Click "My Account" or "Create New Key"
   - Fill in the required information:
     - **Name**: ClashFish Development (or any name)
     - **Description**: Clash Royale Game Analyzer
     - **Allowed IP addresses**: Add your server's IP address

---

## Finding Your IP Address

### Your Current IP Address:
You need to whitelist the IP address where your server runs.

**For local development:**
```bash
# Get your public IP
curl https://api.ipify.org
```

**For server deployment:**
- Use your server's public IP address
- For cloud services (AWS, GCP, Azure), find it in the console

### Important Notes:
- ⚠️ **IP address must be whitelisted** on the Clash Royale Developer Portal
- Your IP may change if you're on a home network (dynamic IP)
- If API calls fail with 403, check your IP hasn't changed

---

## Option 1: Automated Setup (Recommended)

Run the setup script and follow the prompts:

```bash
./scripts/setup_api_key.sh
```

The script will:
1. Create/update your `.env` file
2. Prompt for your API key
3. Configure the application to use real data
4. Verify the setup

---

## Option 2: Manual Setup

### Step 1: Create `.env` file

If you don't have a `.env` file:
```bash
cp .env.example .env
```

### Step 2: Add Your API Key

Open `.env` in a text editor and update these lines:

```env
# Change this line - paste your actual API key
CLASH_ROYALE_API_KEY=your_actual_api_key_here

# Change this line - enable real API mode
USE_MOCK_DATA=false
```

**Example:**
```env
CLASH_ROYALE_API_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3...
USE_MOCK_DATA=false
```

### Step 3: Verify Configuration

Your `.env` should look like this:

```env
# Application Settings
APP_NAME=ClashFish
DEBUG=true
ENVIRONMENT=development

# Clash Royale API - CONFIGURED
CLASH_ROYALE_API_KEY=eyJ0eXAiOiJKV1QiLCJhbGc...  # Your actual key
CLASH_ROYALE_API_URL=https://api.clashroyale.com/v1
USE_MOCK_DATA=false  # Changed to false

# Database (optional for now)
DATABASE_URL=postgresql://clashfish:clashfish@localhost:5432/clashfish

# ... rest of config
```

---

## Testing Your API Key

### Method 1: Using the Web Dashboard

1. Start the server:
   ```bash
   ./scripts/start_dev.sh
   ```

2. Open: http://localhost:8000

3. Enter a **real player tag** (e.g., `#2PP` or `#V2QUUQVU8`)

4. If successful, you'll see:
   - Real player profile data
   - Actual battle history
   - Live deck analysis

### Method 2: Using curl

Test the API directly:

```bash
# Test with a real player tag
curl http://localhost:8000/api/v1/players/2PP
```

**Expected response:**
```json
{
  "player_id": "2PP",
  "player_name": "Surgical Goblin",
  "current_trophies": 8000,
  "wins": 5000,
  ...
}
```

### Method 3: Test API Key Directly

Test the Clash Royale API directly:

```bash
# Replace YOUR_API_KEY with your actual key
curl -X GET "https://api.clashroyale.com/v1/players/%232PP" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## Troubleshooting

### Error: "Invalid API key or access denied"

**Cause**: API key is incorrect or IP address not whitelisted

**Solution**:
1. Verify your API key is correct in `.env`
2. Check your IP address: `curl https://api.ipify.org`
3. Go to https://developer.clashroyale.com
4. Edit your API key and add/update the allowed IP address
5. Wait a few minutes for changes to propagate

### Error: "Player not found"

**Cause**: Invalid player tag format

**Solution**:
- Player tags can include or exclude the `#` symbol
- Both `#V2QUUQVU8` and `V2QUUQVU8` work
- Tags are case-insensitive but usually uppercase

### Error: "Network error"

**Cause**: Cannot reach Clash Royale API

**Solution**:
1. Check your internet connection
2. Verify the API URL: `https://api.clashroyale.com/v1`
3. Test API connectivity:
   ```bash
   curl https://api.clashroyale.com/v1/cards
   ```

### API Key Expired

Clash Royale API keys can expire or be revoked.

**Solution**:
1. Go to https://developer.clashroyale.com
2. Check if your key is still active
3. Create a new key if needed
4. Update `.env` with the new key

### Rate Limiting

The Clash Royale API has rate limits (typically 30 requests per second).

**Current behavior**:
- ClashFish doesn't implement rate limiting yet
- If you hit limits, you'll get 429 errors

**Solution**:
- Avoid making too many requests quickly
- Wait a few seconds between requests
- Future versions will add automatic rate limiting

---

## API Key Information

### What We Store:
- ✅ API key is stored in `.env` (gitignored)
- ✅ Never logged or displayed in full
- ✅ Never committed to version control

### Security Best Practices:
- ⚠️ **Never** share your `.env` file
- ⚠️ **Never** commit `.env` to git (it's in `.gitignore`)
- ⚠️ **Never** post your API key in public channels
- ✅ Regenerate your key if you think it's compromised
- ✅ Use different keys for dev/staging/production

---

## Switching Between Mock and Real Data

You can toggle between mock data and real API:

### Use Real API:
```env
USE_MOCK_DATA=false
CLASH_ROYALE_API_KEY=your_key_here
```

### Use Mock Data (Development):
```env
USE_MOCK_DATA=true
```

**When to use mock data:**
- Initial development
- Testing without API limits
- When API is down
- Demonstrating features offline

**When to use real API:**
- Production deployment
- Analyzing real players
- Testing with live data
- Full feature validation

---

## Next Steps After Setup

Once your API key is configured:

1. **Analyze Real Players**:
   - Search for any player tag
   - View their complete battle history
   - Get real-time deck analysis

2. **Build Advanced Features**:
   - Win probability calculation with real matches
   - Move evaluation on actual gameplay
   - AI commentary on real battles

3. **Deploy to Production**:
   - Use environment variables for API key
   - Set up proper IP whitelisting
   - Implement rate limiting

---

## Support

### Official Resources:
- **Clash Royale API Docs**: https://developer.clashroyale.com/api-docs
- **Developer Portal**: https://developer.clashroyale.com
- **API Status**: Check the developer portal for outages

### ClashFish Resources:
- **Quick Start**: See `QUICKSTART.md`
- **Full Design**: See `DESIGN.md`
- **Issues**: Check GitHub issues

---

## Example: Complete Setup

Here's a complete example of setting up ClashFish with a real API key:

```bash
# 1. Get your IP
MY_IP=$(curl -s https://api.ipify.org)
echo "My IP: $MY_IP"

# 2. Go to https://developer.clashroyale.com
#    Create a key and whitelist your IP: $MY_IP

# 3. Run setup script
./scripts/setup_api_key.sh
# Enter your API key when prompted

# 4. Start the server
./scripts/start_dev.sh

# 5. Open browser
open http://localhost:8000

# 6. Search for a real player (e.g., "2PP")
# You should see real, live data!
```

---

## Summary

✅ **Get API key**: https://developer.clashroyale.com
✅ **Find your IP**: `curl https://api.ipify.org`
✅ **Whitelist IP**: On developer portal
✅ **Configure**: Run `./scripts/setup_api_key.sh` or edit `.env`
✅ **Test**: `curl http://localhost:8000/api/v1/players/2PP`
✅ **Enjoy**: Analyze real players! 🎉

---

**Security Reminder**: Your `.env` file contains secrets. Never commit it to git, never share it publicly, and regenerate your key if it's ever exposed.
