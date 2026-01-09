# ClashFish - Quick Start Guide

Get your Clash Royale analyzer running in 5 minutes!

## Prerequisites

- **Python 3.10+** installed
- **Git** (already have it!)
- *Optional*: Docker & Docker Compose for full stack

## Option 1: Quick Start (Mock Data Mode) ⚡

**No API keys needed! Uses sample data for immediate testing.**

### Step 1: Run the Startup Script

```bash
./scripts/start_dev.sh
```

That's it! The script will:
- Create a virtual environment
- Install all dependencies
- Start the backend server

### Step 2: Open Your Browser

Visit: **http://localhost:8000**

You should see the ClashFish dashboard with sample player data already loaded.

### What You Can Do Now:

1. **Search for the sample player**: `V2QUUQVU8` (pre-filled)
2. **View battle history** with:
   - Win/Loss records
   - Deck classifications (e.g., "2.6 Hog Cycle", "Golem Beatdown")
   - Matchup ratings
   - Card-by-card deck breakdown
3. **Explore API docs**: http://localhost:8000/docs

---

## Option 2: With Real API (Optional)

To analyze real players, you need a Clash Royale API key.

### Step 1: Get API Key

1. Go to https://developer.clashroyale.com
2. Create an account and generate an API key
3. Note: You need to whitelist your IP address

### Step 2: Configure

Edit `.env` file:
```env
CLASH_ROYALE_API_KEY=your_actual_api_key_here
USE_MOCK_DATA=false
```

### Step 3: Run

```bash
./scripts/start_dev.sh
```

Now you can analyze **any player** by their tag!

---

## Option 3: Full Docker Stack 🐳

Includes PostgreSQL, Redis, and MongoDB for the complete experience.

### Step 1: Start Services

```bash
docker-compose up -d
```

### Step 2: Access

- **Dashboard**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **MongoDB**: localhost:27017

### Step 3: Stop Services

```bash
docker-compose down
```

---

## API Endpoints

Once running, you can use these endpoints:

### Get Player Info
```bash
curl http://localhost:8000/api/v1/players/V2QUUQVU8
```

**Response:**
```json
{
  "player_id": "V2QUUQVU8",
  "player_name": "ClashMaster",
  "current_trophies": 5234,
  "wins": 1247,
  "losses": 1053,
  "win_rate": 54.2
}
```

### Get Player Battles
```bash
curl http://localhost:8000/api/v1/players/V2QUUQVU8/battles
```

**Response:**
```json
[
  {
    "match_id": "...",
    "battle_time": "2026-01-08T14:30:22Z",
    "game_mode": "Ladder_1v1",
    "player1_crowns": 3,
    "player2_crowns": 1,
    "player1_result": "win",
    "deck_archetype": "2.6 Hog Cycle",
    "opponent_archetype": "Golem Beatdown",
    "matchup_rating": "unfavorable",
    "deck_avg_cost": 2.6
  }
]
```

### Get All Archetypes
```bash
curl http://localhost:8000/api/v1/archetypes
```

---

## Sample Players (Mock Data)

Try these player tags in mock mode:

- **V2QUUQVU8** - ClashMaster (2.6 Hog Cycle player)
- Includes 3 sample battles against:
  - Golem Beatdown (3-1 WIN)
  - Log Bait (2-1 WIN)
  - X-Bow Cycle (1-0 WIN)

---

## What's Working Now ✅

- ✅ Player profile fetching
- ✅ Battle history retrieval
- ✅ Deck classification (10 archetypes)
- ✅ Matchup analysis
- ✅ Average elixir cost calculation
- ✅ Win/Loss tracking
- ✅ Beautiful web dashboard
- ✅ REST API with auto-docs

---

## What's Next 🚀

The prototype is working! Next steps from the design doc:

### Phase 1 (Current - MVP)
- ✅ Data ingestion from Clash Royale API
- ✅ Basic deck classification
- ✅ Player and match storage
- ⏳ Win probability model (simple heuristic version)
- ⏳ Move evaluation (basic quality scoring)

### Phase 2 (Coming Soon)
- 🔮 Advanced LSTM win probability model
- 🎯 Move-by-move evaluation with alternatives
- 💬 AI commentary (GPT/Claude integration)
- 📊 Performance analytics dashboard
- 🎬 3D replay viewer (Three.js)

### Phase 3 (Future)
- 📱 Mobile app
- 👥 Multiplayer analysis
- 🏆 Tournament mode
- 📈 Meta tracking

---

## Troubleshooting

### Port 8000 already in use?
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn backend.main:app --port 8001
```

### Python version too old?
```bash
# Check version
python3 --version

# Should be 3.10 or higher
# Install Python 3.10+ if needed
```

### Dependencies not installing?
```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Then retry
pip install -r backend/requirements.txt
```

### Can't find mock data?
```bash
# Ensure you're in the project root
pwd
# Should end with /CLASHFISH

# Check if mock data exists
ls data/mock/
# Should show sample_battles.json and sample_player.json
```

---

## Project Structure

```
CLASHFISH/
├── backend/              # FastAPI backend
│   ├── api/             # API endpoints (future)
│   ├── models/          # Database models ✅
│   ├── services/        # Business logic ✅
│   │   ├── clash_royale_api.py  # API client ✅
│   │   └── deck_classifier.py   # Deck analysis ✅
│   ├── config/          # Configuration ✅
│   ├── database/        # DB setup ✅
│   └── main.py          # FastAPI app ✅
├── data/
│   └── mock/            # Sample data ✅
│       ├── sample_player.json
│       └── sample_battles.json
├── scripts/
│   └── start_dev.sh     # Quick start script ✅
├── .env.example         # Configuration template ✅
├── docker-compose.yml   # Docker setup ✅
├── DESIGN.md           # Full system design ✅
├── README.md           # Project overview ✅
└── QUICKSTART.md       # This file! ✅
```

---

## Testing the System

### 1. Test Health Check
```bash
curl http://localhost:8000/api/v1/health
```

Expected:
```json
{
  "status": "healthy",
  "app_name": "ClashFish",
  "version": "0.1.0",
  "mock_mode": true
}
```

### 2. Test Player Lookup
Visit: http://localhost:8000

Enter: `V2QUUQVU8`

You should see:
- Player name: ClashMaster
- Trophies: 🏆 5234
- Win rate: ~54%
- 3 recent battles with deck analysis

### 3. Test Deck Classification

The system should identify:
- **Battle 1**: 2.6 Hog Cycle vs Golem Beatdown
- **Battle 2**: 2.6 Hog Cycle vs Log Bait
- **Battle 3**: 2.6 Hog Cycle vs X-Bow Cycle

---

## Next Steps

1. **Explore the Dashboard**: Play around with the web interface
2. **Try the API**: Use curl or Postman to test endpoints
3. **Read the Design**: Check `DESIGN.md` for the full architecture
4. **Add Features**: Start implementing win probability or move evaluation
5. **Get Real API Key**: Analyze actual players from the game

---

## Getting Help

- **Issues**: Check GitHub Issues
- **Design Questions**: See DESIGN.md
- **API Reference**: http://localhost:8000/docs (Swagger UI)

---

## Summary

**You now have a working Clash Royale analyzer!** 🎉

It can:
- Fetch player profiles
- Retrieve battle history
- Classify 10+ deck archetypes
- Analyze matchups
- Display results in a beautiful dashboard

This is the foundation. From here, we'll add:
- Win probability tracking
- Move-by-move analysis
- AI commentary
- 3D replay viewer

**Happy analyzing!** ⚔️🏆
