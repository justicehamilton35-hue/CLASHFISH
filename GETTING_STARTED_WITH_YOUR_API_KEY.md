# 🎉 You Have a Clash Royale API Key! Here's What to Do

Welcome! You've obtained an official Clash Royale API key. This guide will help you integrate it with ClashFish so you can analyze **real players** instead of sample data.

---

## ⚡ Quick Setup (2 Minutes)

### Step 1: Find Your IP Address
Your API key only works from whitelisted IP addresses. First, find yours:

```bash
curl https://api.ipify.org
```

**Write down this IP address** - you'll need it in the next step.

### Step 2: Whitelist Your IP Address

1. Go to https://developer.clashroyale.com
2. Log in with your Supercell ID
3. Find your API key in "My Keys" or "My Account"
4. Click "Edit" or "Manage"
5. Add your IP address from Step 1 to "Allowed IP Addresses"
6. Save changes
7. **Wait 2-3 minutes** for the changes to take effect

### Step 3: Configure ClashFish

**Option A: Automated Setup (Recommended)**
```bash
./scripts/setup_api_key.sh
```

When prompted, paste your API key (the long JWT token that looks like `eyJ0eXAiOiJKV1QiLCJh...`)

**Option B: Manual Setup**
1. Copy the template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and change these two lines:
   ```env
   CLASH_ROYALE_API_KEY=paste_your_api_key_here
   USE_MOCK_DATA=false
   ```

### Step 4: Test Your Setup
```bash
./scripts/test_api_key.sh
```

If you see "✅ SUCCESS!", you're ready to go!

If you see "❌ FAILED", check the error message - it will tell you exactly what's wrong.

### Step 5: Start ClashFish
```bash
./scripts/start_dev.sh
```

Then open: **http://localhost:8000**

Now you can search for **ANY player** by their tag! 🎮

---

## 🧪 Testing With Real Players

Try these player tags to verify everything works:

- `#2PP` - Surgical Goblin (pro player)
- `#V2QUUQVU8` - Sample player from our mock data
- Your own player tag!

Just enter the tag (with or without the #) in the search box.

---

## 🔐 Security Information

### What We Did to Keep Your API Key Safe:

1. ✅ **Added `.gitignore`** - Your `.env` file (containing the API key) will NEVER be committed to git
2. ✅ **Secure storage** - API key is only stored in `.env` on your local machine
3. ✅ **No logging** - Your API key is never logged or displayed in full
4. ✅ **Environment-based** - Works with environment variables in production

### Important Security Rules:

- ⚠️ **NEVER** commit your `.env` file to git
- ⚠️ **NEVER** share your API key publicly
- ⚠️ **NEVER** post your `.env` file in chat/forums
- ✅ **DO** use different keys for dev/staging/production
- ✅ **DO** regenerate your key if you think it's compromised

### What to Do If Your Key Gets Exposed:

1. Go to https://developer.clashroyale.com
2. Delete the exposed key immediately
3. Create a new key with a different name
4. Update your `.env` file with the new key
5. Re-run `./scripts/test_api_key.sh` to verify

---

## 📋 Your API Key Information

From the developer portal, you should have:

- **Token/Key**: A long string starting with `eyJ...` (this is your actual API key)
- **Name**: The name you gave this key (e.g., "ClashFish Development")
- **Description**: What this key is for
- **Allowed IPs**: The IP addresses that can use this key

**Only the Token/Key is needed for ClashFish** - paste that into `.env`.

---

## 🐛 Common Issues & Solutions

### Issue: "Access denied (403)"

**Cause**: Your IP address is not whitelisted

**Solution**:
```bash
# 1. Check your current IP
curl https://api.ipify.org

# 2. Go to developer.clashroyale.com
# 3. Edit your API key
# 4. Add/update the IP address
# 5. Wait 2-3 minutes
# 6. Test again
./scripts/test_api_key.sh
```

### Issue: My IP address keeps changing

**Cause**: You have a dynamic IP address (common on home networks)

**Solution**:
- Option 1: Use a VPS/server with a static IP for production
- Option 2: Re-whitelist your IP whenever it changes
- Option 3: Some developer portals allow IP ranges (check documentation)

### Issue: "Player not found (404)"

**Cause**: Invalid player tag or player doesn't exist

**Solution**:
- Make sure the player tag is correct
- Player tags are case-insensitive but usually uppercase
- Try with and without the `#` symbol
- Test with a known player like `#2PP`

### Issue: "Rate limit exceeded (429)"

**Cause**: Too many requests in a short time

**Solution**:
- Wait 10-20 seconds
- The Clash Royale API allows ~30 requests per second
- Future versions will add automatic rate limiting

### Issue: Test script fails but API key looks correct

**Cause**: Various network or API issues

**Solution**:
```bash
# Test the API directly with curl
curl -X GET "https://api.clashroyale.com/v1/players/%232PP" \
  -H "Authorization: Bearer YOUR_API_KEY_HERE"

# Check API status at developer.clashroyale.com
# Sometimes the API has downtime
```

---

## 🔄 Switching Between Mock and Real Data

You can toggle between modes by editing `.env`:

### Use Real API (Analyze Real Players):
```env
USE_MOCK_DATA=false
CLASH_ROYALE_API_KEY=your_key_here
```

### Use Mock Data (Development/Testing):
```env
USE_MOCK_DATA=true
```

This is useful for:
- Development without hitting API rate limits
- Testing when the API is down
- Demonstrating features offline
- Saving API quota

---

## 📊 What's Next?

Now that your API is configured, you can:

### 1. Analyze Real Players ✅
- Search any player tag
- View complete battle history
- See real deck classifications
- Get matchup analysis

### 2. Build Advanced Features 🚀
- Win probability with real match data
- Move evaluation on actual gameplay
- AI commentary on real battles
- Performance analytics

### 3. Explore the Data 📈
- Study meta trends
- Analyze deck win rates
- Compare player strategies
- Track your own improvement

---

## 🆘 Need More Help?

- **Detailed Setup**: See `API_SETUP.md`
- **Quick Start**: See `QUICKSTART.md`
- **Full Documentation**: See `DESIGN.md`
- **Test Script**: Run `./scripts/test_api_key.sh`
- **Issues**: Check GitHub Issues

---

## ✅ Checklist

Before you start analyzing:

- [ ] I have my API key from developer.clashroyale.com
- [ ] I know my IP address (`curl https://api.ipify.org`)
- [ ] My IP is whitelisted in the developer portal
- [ ] I've configured `.env` with my API key
- [ ] I've set `USE_MOCK_DATA=false` in `.env`
- [ ] I've run `./scripts/test_api_key.sh` and it shows success
- [ ] I can start the server with `./scripts/start_dev.sh`
- [ ] I can search for real players in the dashboard

---

## 🎉 Congratulations!

You're now ready to analyze **any Clash Royale player in the world**!

Your ClashFish installation can:
- ✅ Fetch real player profiles
- ✅ Retrieve actual battle history
- ✅ Classify real decks
- ✅ Provide matchup analysis
- ✅ Track win/loss statistics
- ✅ And much more...

**Start analyzing**: `./scripts/start_dev.sh` → http://localhost:8000

---

**Security Reminder**: Your `.env` file is gitignored. Never share it or commit it to version control! 🔒
