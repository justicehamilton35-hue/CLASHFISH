"""
ClashFish API - Main application entry point.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uvicorn

from backend.config import settings
from backend.database import get_db, init_db
from backend.models import Player, Match, MatchAnalysis
from backend.services import clash_royale_client, ClashRoyaleAPIError, deck_classifier

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Clash Royale Game Analyzer - Stockfish for Clash Royale",
    debug=settings.debug,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📊 Environment: {settings.environment}")
    print(f"🎮 Mock Data Mode: {settings.use_mock_data}")

    # Initialize database (will skip if not available)
    init_db()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic web interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ClashFish - Clash Royale Analyzer</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 36px;
            }
            .tagline {
                color: #666;
                margin-bottom: 30px;
                font-size: 18px;
            }
            .search-box {
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
            }
            input {
                flex: 1;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 16px;
            }
            input:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                padding: 15px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            button:active {
                transform: translateY(0);
            }
            .status {
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                display: none;
            }
            .status.success {
                background: #d4edda;
                color: #155724;
                display: block;
            }
            .status.error {
                background: #f8d7da;
                color: #721c24;
                display: block;
            }
            .status.info {
                background: #d1ecf1;
                color: #0c5460;
                display: block;
            }
            .results {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
                display: none;
            }
            .results.show {
                display: block;
            }
            .battle-card {
                background: white;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 10px;
                border-left: 4px solid #667eea;
            }
            .deck-preview {
                display: flex;
                gap: 5px;
                margin-top: 10px;
                flex-wrap: wrap;
            }
            .card-badge {
                background: #667eea;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            .archetype {
                display: inline-block;
                background: #764ba2;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
                margin-top: 5px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin-top: 20px;
            }
            .stat-card {
                background: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
            }
            .stat-value {
                font-size: 24px;
                font-weight: bold;
                color: #667eea;
            }
            .stat-label {
                font-size: 12px;
                color: #666;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚔️ ClashFish</h1>
            <p class="tagline">Stockfish for Clash Royale - Analyze your battles like never before</p>

            <div class="search-box">
                <input type="text" id="playerTag" placeholder="Enter player tag (e.g., V2QUUQVU8)" value="V2QUUQVU8">
                <button onclick="analyzePlayer()">Analyze</button>
            </div>

            <div id="status" class="status"></div>

            <div id="results" class="results"></div>
        </div>

        <script>
            async function analyzePlayer() {
                const playerTag = document.getElementById('playerTag').value.replace('#', '');
                const statusDiv = document.getElementById('status');
                const resultsDiv = document.getElementById('results');

                if (!playerTag) {
                    showStatus('Please enter a player tag', 'error');
                    return;
                }

                showStatus('🔍 Fetching player data...', 'info');
                resultsDiv.classList.remove('show');

                try {
                    // Fetch player data
                    const playerResponse = await fetch(`/api/v1/players/${playerTag}`);
                    if (!playerResponse.ok) throw new Error('Player not found');
                    const player = await playerResponse.json();

                    // Fetch battles
                    const battlesResponse = await fetch(`/api/v1/players/${playerTag}/battles`);
                    if (!battlesResponse.ok) throw new Error('Could not fetch battles');
                    const battles = await battlesResponse.json();

                    // Display results
                    displayResults(player, battles);
                    showStatus('✅ Analysis complete!', 'success');

                } catch (error) {
                    showStatus(`❌ Error: ${error.message}`, 'error');
                }
            }

            function showStatus(message, type) {
                const statusDiv = document.getElementById('status');
                statusDiv.textContent = message;
                statusDiv.className = `status ${type}`;
            }

            function displayResults(player, battles) {
                const resultsDiv = document.getElementById('results');
                const winRate = ((player.wins / (player.wins + player.losses)) * 100).toFixed(1);

                let html = `
                    <h2>${player.player_name}</h2>
                    <p><strong>Tag:</strong> ${player.player_tag} | <strong>Trophies:</strong> 🏆 ${player.current_trophies}</p>

                    <div class="stats">
                        <div class="stat-card">
                            <div class="stat-value">${player.wins}</div>
                            <div class="stat-label">Wins</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${player.losses}</div>
                            <div class="stat-label">Losses</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${winRate}%</div>
                            <div class="stat-label">Win Rate</div>
                        </div>
                    </div>

                    <h3 style="margin-top: 30px; margin-bottom: 15px;">Recent Battles (${battles.length})</h3>
                `;

                battles.forEach((battle, index) => {
                    const result = battle.player1_result === 'win' ? '🏆 WIN' : battle.player1_result === 'loss' ? '❌ LOSS' : '🤝 DRAW';
                    const resultColor = battle.player1_result === 'win' ? '#28a745' : battle.player1_result === 'loss' ? '#dc3545' : '#ffc107';

                    html += `
                        <div class="battle-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong style="color: ${resultColor};">${result}</strong>
                                    <span style="color: #666; margin-left: 10px;">${battle.game_mode}</span>
                                </div>
                                <div style="font-size: 24px; font-weight: bold;">
                                    ${battle.player1_crowns} - ${battle.player2_crowns}
                                </div>
                            </div>
                            <div style="margin-top: 5px; color: #666; font-size: 14px;">
                                vs ${battle.opponent_name || 'Opponent'} | ${battle.arena || 'Arena'}
                            </div>
                            ${battle.deck_archetype ? `<span class="archetype">${battle.deck_archetype}</span>` : ''}
                            <div class="deck-preview">
                                ${battle.player1_deck.slice(0, 8).map(card => `<span class="card-badge">${card.name}</span>`).join('')}
                            </div>
                        </div>
                    `;
                });

                resultsDiv.innerHTML = html;
                resultsDiv.classList.add('show');
            }

            // Auto-analyze on page load if default tag is present
            window.onload = () => {
                if (document.getElementById('playerTag').value) {
                    analyzePlayer();
                }
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "mock_mode": settings.use_mock_data,
    }


@app.get("/api/v1/players/{player_tag}")
async def get_player(player_tag: str, db: Session = Depends(get_db)):
    """
    Get player information.
    """
    try:
        # Fetch from API
        api_data = await clash_royale_client.get_player(player_tag)
        player_data = clash_royale_client.parse_player_data(api_data)

        # Store/update in database (if available)
        if db is not None:
            try:
                player = db.query(Player).filter(Player.player_id == player_data['player_id']).first()
                if player:
                    # Update existing player
                    for key, value in player_data.items():
                        setattr(player, key, value)
                else:
                    # Create new player
                    player = Player(**player_data)
                    db.add(player)

                db.commit()
                db.refresh(player)
            except Exception as e:
                print(f"⚠️  Database operation failed: {e}")
                # Continue without database

        return player_data

    except ClashRoyaleAPIError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/v1/players/{player_tag}/battles")
async def get_player_battles(player_tag: str, db: Session = Depends(get_db)):
    """
    Get recent battles for a player with analysis.
    """
    try:
        # Fetch battles from API
        battles_data = await clash_royale_client.get_player_battles(player_tag)

        results = []
        for battle_data in battles_data:
            # Parse battle
            parsed_battle = clash_royale_client.parse_battle_data(battle_data, player_tag)

            # Classify deck
            player1_deck = parsed_battle['player1_deck']
            player2_deck = parsed_battle['player2_deck']

            player1_archetype_id, player1_archetype_name, player1_confidence = deck_classifier.classify_deck(player1_deck)
            player2_archetype_id, player2_archetype_name, player2_confidence = deck_classifier.classify_deck(player2_deck)

            # Calculate deck cost
            player1_avg_cost = deck_classifier.calculate_deck_cost(player1_deck)
            player2_avg_cost = deck_classifier.calculate_deck_cost(player2_deck)

            # Get matchup rating
            matchup_rating = deck_classifier.get_matchup_rating(player1_archetype_id, player2_archetype_id)

            # Add to results
            results.append({
                **parsed_battle,
                "deck_archetype": player1_archetype_name,
                "deck_avg_cost": player1_avg_cost,
                "opponent_archetype": player2_archetype_name,
                "opponent_avg_cost": player2_avg_cost,
                "matchup_rating": matchup_rating,
                "opponent_name": battle_data.get('opponent', [{}])[0].get('name') if battle_data.get('opponent') else None,
            })

        return results

    except ClashRoyaleAPIError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/v1/archetypes")
async def get_archetypes():
    """Get all deck archetypes."""
    return {
        archetype_id: {
            "id": archetype_id,
            "name": data["name"],
            "category": data["category"],
            "description": data["description"],
            "signature_cards": data["signature_cards"],
        }
        for archetype_id, data in deck_classifier.ARCHETYPES.items()
    }


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
