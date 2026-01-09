# ClashFish - Clash Royale Game Analyzer

**"Stockfish for Clash Royale"** - A comprehensive game analyzer that provides deep insights into your Clash Royale matches.

## Features

- 🎯 **Win Probability Tracking** - Live probability calculations throughout the match
- 📊 **Move-by-Move Analysis** - Evaluate every card play (Brilliant, Great, Mistake, Blunder)
- 🧠 **AI Commentary** - GPT/Claude-powered insights explaining key moments
- 📈 **Performance Analytics** - Track your improvement over time
- 🎮 **3D Replay Viewer** - Visualize matches with interactive 3D replays
- ⚔️ **Deck Classification** - Automatic archetype detection and matchup analysis
- 💡 **Strategic Advice** - Real-time suggestions based on game state

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/clashfish.git
cd clashfish

# Set up backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database
cd ../scripts
./setup_db.sh

# Set up frontend
cd ../frontend
npm install

# Run with Docker (recommended)
cd ..
docker-compose up
```

### Configuration

Create a `.env` file in the root directory:

```env
# API Keys
CLASH_ROYALE_API_KEY=your_api_key_here
OPENAI_API_KEY=your_openai_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/clashfish
REDIS_URL=redis://localhost:6379
MONGODB_URL=mongodb://localhost:27017/clashfish

# App Settings
DEBUG=true
API_PORT=8000
FRONTEND_PORT=3000
```

## Usage

### Analyze a Player

```bash
# Using the CLI
python -m backend.cli analyze-player V2QUUQVU8

# Or via API
curl -X POST http://localhost:8000/api/v1/players/V2QUUQVU8/analyze
```

### View Analysis Dashboard

Open your browser to `http://localhost:3000` and search for a player.

## Project Structure

```
clashfish/
├── backend/              # Python FastAPI backend
│   ├── api/             # API endpoints
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── database/        # Database schemas & migrations
│   └── utils/           # Utilities
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   └── services/    # API clients
│   └── public/          # Static assets
├── ml/                  # Machine learning models
│   ├── models/          # Trained models
│   ├── training/        # Training scripts
│   └── inference/       # Inference services
├── data/                # Data storage
│   ├── mock/            # Mock data for development
│   ├── raw/             # Raw API responses
│   └── processed/       # Processed data
├── docs/                # Documentation
├── scripts/             # Utility scripts
└── tests/               # Test suite
```

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Mock Data Mode

No API key? No problem! ClashFish works with mock data:

```bash
# Set mock mode in .env
USE_MOCK_DATA=true

# Run the app
python -m backend.main
```

## Architecture

See [DESIGN.md](./DESIGN.md) for comprehensive system architecture.

**Key Components:**
- **Data Ingestion**: Clash Royale API → Database
- **Analysis Engine**: Win probability, move evaluation, deck classification
- **ML Models**: LSTM for win probability, XGBoost for move quality
- **Commentary Service**: LLM integration for narrative analysis
- **3D Viewer**: Three.js-based replay visualization

## Roadmap

- [x] System design document
- [ ] MVP with basic analysis
- [ ] Win probability model
- [ ] Move evaluation system
- [ ] AI commentary
- [ ] 3D replay viewer
- [ ] Mobile app

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

## License

MIT License - see [LICENSE](./LICENSE)

## Links

- **Official API**: https://developer.clashroyale.com
- **Documentation**: https://docs.clashfish.io
- **Discord**: https://discord.gg/clashfish

---

Built with ❤️ for the Clash Royale community
