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
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f6f7f9;
                min-height: 100vh;
                padding: 0;
            }
            .header {
                background: #262421;
                color: white;
                padding: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .header-content {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 30px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .logo h1 {
                color: white;
                font-size: 24px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            .logo-icon {
                font-size: 28px;
            }
            .tagline {
                color: #a0a0a0;
                font-size: 14px;
                margin-left: 40px;
            }
            .container {
                max-width: 1200px;
                margin: 30px auto;
                padding: 0 30px;
            }
            .search-section {
                background: white;
                border-radius: 8px;
                padding: 24px;
                margin-bottom: 24px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .search-box {
                display: flex;
                gap: 12px;
                max-width: 600px;
            }
            input {
                flex: 1;
                padding: 12px 16px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                font-size: 15px;
                font-family: inherit;
                transition: all 0.2s;
            }
            input:focus {
                outline: none;
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
            button {
                padding: 12px 24px;
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }
            button:hover {
                background: #2563eb;
            }
            button:active {
                background: #1d4ed8;
            }
            .status {
                padding: 12px 16px;
                border-radius: 6px;
                margin-bottom: 16px;
                display: none;
                font-size: 14px;
            }
            .status.success {
                background: #ecfdf5;
                color: #065f46;
                border: 1px solid #a7f3d0;
                display: block;
            }
            .status.error {
                background: #fef2f2;
                color: #991b1b;
                border: 1px solid #fecaca;
                display: block;
            }
            .status.info {
                background: #eff6ff;
                color: #1e40af;
                border: 1px solid #bfdbfe;
                display: block;
            }
            .player-header {
                background: white;
                border-radius: 8px;
                padding: 24px;
                margin-bottom: 24px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .player-header h2 {
                font-size: 28px;
                color: #111827;
                margin-bottom: 8px;
                font-weight: 700;
            }
            .player-info {
                color: #6b7280;
                font-size: 14px;
                margin-bottom: 20px;
            }
            .player-info span {
                margin-right: 20px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 16px;
            }
            .stat-card {
                background: #f9fafb;
                padding: 16px;
                border-radius: 6px;
                border: 1px solid #e5e7eb;
            }
            .stat-value {
                font-size: 28px;
                font-weight: 700;
                color: #111827;
                margin-bottom: 4px;
            }
            .stat-label {
                font-size: 13px;
                color: #6b7280;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-weight: 500;
            }
            .section-title {
                font-size: 20px;
                font-weight: 700;
                color: #111827;
                margin-bottom: 16px;
            }
            .battles-section {
                background: white;
                border-radius: 8px;
                padding: 24px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .battle-card {
                background: #fafafa;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 16px;
                margin-bottom: 12px;
                cursor: pointer;
                transition: all 0.2s;
            }
            .battle-card:hover {
                border-color: #3b82f6;
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
                transform: translateY(-1px);
            }
            .battle-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }
            .battle-result {
                font-weight: 700;
                font-size: 15px;
            }
            .battle-result.win { color: #059669; }
            .battle-result.loss { color: #dc2626; }
            .battle-result.draw { color: #d97706; }
            .battle-mode {
                color: #6b7280;
                font-size: 14px;
                margin-left: 12px;
            }
            .battle-score {
                font-size: 20px;
                font-weight: 700;
                color: #111827;
            }
            .battle-opponent {
                color: #6b7280;
                font-size: 13px;
                margin-bottom: 12px;
            }
            .deck-preview {
                display: flex;
                gap: 6px;
                flex-wrap: wrap;
            }
            .card-badge {
                background: white;
                border: 1px solid #d1d5db;
                color: #374151;
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: 500;
            }
            .archetype {
                display: inline-block;
                background: #3b82f6;
                color: white;
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 8px;
            }
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.6);
                z-index: 1000;
                overflow-y: auto;
                padding: 40px 20px;
            }
            .modal.show {
                display: flex;
                align-items: flex-start;
                justify-content: center;
            }
            .modal-content {
                background: white;
                border-radius: 8px;
                padding: 32px;
                max-width: 1000px;
                width: 100%;
                position: relative;
                box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
            }
            .modal-close {
                position: absolute;
                top: 16px;
                right: 16px;
                font-size: 24px;
                cursor: pointer;
                color: #9ca3af;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 6px;
                transition: all 0.2s;
            }
            .modal-close:hover {
                background: #f3f4f6;
                color: #374151;
            }
            .battle-detail-header {
                text-align: center;
                margin-bottom: 32px;
                padding-bottom: 24px;
                border-bottom: 1px solid #e5e7eb;
            }
            .battle-detail-header h2 {
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 8px;
            }
            .detail-score {
                font-size: 56px;
                font-weight: 800;
                color: #111827;
                margin: 12px 0;
                letter-spacing: -1px;
            }
            .detail-meta {
                color: #6b7280;
                font-size: 14px;
                margin-top: 8px;
            }
            .vs-section {
                display: grid;
                grid-template-columns: 1fr auto 1fr;
                gap: 24px;
                margin: 32px 0;
                align-items: start;
            }
            .player-section {
                background: #fafafa;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 20px;
            }
            .player-section h3 {
                color: #111827;
                margin-bottom: 12px;
                font-size: 16px;
                font-weight: 700;
            }
            .deck-meta {
                color: #6b7280;
                font-size: 13px;
                margin-bottom: 16px;
            }
            .deck-meta strong {
                color: #374151;
                font-weight: 600;
            }
            .deck-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 8px;
            }
            .card-detail {
                background: white;
                padding: 10px 12px;
                border-radius: 6px;
                border: 1px solid #e5e7eb;
                font-size: 13px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-weight: 500;
                color: #374151;
            }
            .card-level {
                background: #3b82f6;
                color: white;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 700;
            }
            .vs-divider {
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                font-weight: 700;
                color: #9ca3af;
            }
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 16px;
                margin-top: 24px;
            }
            .info-item {
                background: #fafafa;
                border: 1px solid #e5e7eb;
                padding: 16px;
                border-radius: 6px;
            }
            .info-label {
                font-size: 12px;
                color: #6b7280;
                margin-bottom: 6px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-weight: 600;
            }
            .info-value {
                font-size: 16px;
                font-weight: 700;
                color: #111827;
            }
            .matchup-indicator {
                padding: 16px;
                border-radius: 6px;
                text-align: center;
                margin: 24px 0;
                font-weight: 600;
                font-size: 14px;
                border: 1px solid;
            }
            .matchup-favorable {
                background: #ecfdf5;
                color: #065f46;
                border-color: #a7f3d0;
            }
            .matchup-neutral {
                background: #fef3c7;
                color: #92400e;
                border-color: #fde68a;
            }
            .matchup-unfavorable {
                background: #fef2f2;
                color: #991b1b;
                border-color: #fecaca;
            }
            .section-divider {
                height: 1px;
                background: #e5e7eb;
                margin: 32px 0;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">⚔️</span>
                    <h1>ClashFish</h1>
                    <span class="tagline">Stockfish for Clash Royale</span>
                </div>
            </div>
        </div>

        <div class="container">
            <div class="search-section">
                <div class="search-box">
                    <input type="text" id="playerTag" placeholder="Enter player tag (e.g., V2QUUQVU8)" value="V2QUUQVU8">
                    <button onclick="analyzePlayer()">Analyze Player</button>
                </div>
                <div id="status" class="status"></div>
            </div>

            <div id="results"></div>
        </div>

        <!-- Battle Detail Modal -->
        <div id="battleModal" class="modal">
            <div class="modal-content">
                <span class="modal-close" onclick="closeModal()">&times;</span>
                <div id="battleDetail"></div>
            </div>
        </div>

        <script>
            let currentBattles = [];  // Store battles for modal access
        </script>
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

                // Store battles for modal access
                currentBattles = battles;

                let html = `
                    <div class="player-header">
                        <h2>${player.player_name}</h2>
                        <div class="player-info">
                            <span><strong>Tag:</strong> ${player.player_tag}</span>
                            <span><strong>Trophies:</strong> ${player.current_trophies} 🏆</span>
                        </div>

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
                    </div>

                    <div class="battles-section">
                        <h3 class="section-title">Recent Battles</h3>
                `;

                battles.forEach((battle, index) => {
                    const resultText = battle.player1_result === 'win' ? 'Victory' : battle.player1_result === 'loss' ? 'Defeat' : 'Draw';
                    const resultClass = battle.player1_result;

                    html += `
                        <div class="battle-card" onclick="showBattleDetail(${index})">
                            <div class="battle-header">
                                <div>
                                    <span class="battle-result ${resultClass}">${resultText}</span>
                                    <span class="battle-mode">${battle.game_mode}</span>
                                </div>
                                <div class="battle-score">${battle.player1_crowns} - ${battle.player2_crowns}</div>
                            </div>
                            <div class="battle-opponent">
                                vs ${battle.opponent_name || 'Opponent'} • ${battle.arena || 'Arena'}
                            </div>
                            ${battle.deck_archetype ? `<span class="archetype">${battle.deck_archetype}</span>` : ''}
                            <div class="deck-preview">
                                ${battle.player1_deck.slice(0, 8).map(card => `<span class="card-badge">${card.name}</span>`).join('')}
                            </div>
                        </div>
                    `;
                });

                html += `</div>`;

                resultsDiv.innerHTML = html;
            }

            function showBattleDetail(battleIndex) {
                const battle = currentBattles[battleIndex];
                const modal = document.getElementById('battleModal');
                const detailDiv = document.getElementById('battleDetail');

                const result = battle.player1_result === 'win' ? 'Victory' : battle.player1_result === 'loss' ? 'Defeat' : 'Draw';
                const resultColor = battle.player1_result === 'win' ? '#059669' : battle.player1_result === 'loss' ? '#dc2626' : '#d97706';

                // Determine matchup indicator
                let matchupClass = 'matchup-neutral';
                let matchupText = 'Neutral Matchup';
                if (battle.matchup_rating > 0.55) {
                    matchupClass = 'matchup-favorable';
                    matchupText = 'Favorable Matchup';
                } else if (battle.matchup_rating < 0.45) {
                    matchupClass = 'matchup-unfavorable';
                    matchupText = 'Unfavorable Matchup';
                }

                let html = `
                    <div class="battle-detail-header">
                        <h2 style="color: ${resultColor};">${result}</h2>
                        <div class="detail-score">${battle.player1_crowns} - ${battle.player2_crowns}</div>
                        <div class="detail-meta">
                            ${battle.game_mode} • ${battle.arena || 'Arena'} • ${new Date(battle.battle_time).toLocaleString()}
                        </div>
                    </div>

                    <div class="matchup-indicator ${matchupClass}">
                        ${matchupText} • Win Probability: ${(battle.matchup_rating * 100).toFixed(0)}%
                    </div>

                    <div class="vs-section">
                        <div class="player-section">
                            <h3>Your Deck</h3>
                            <div class="deck-meta">
                                <strong>Archetype:</strong> ${battle.deck_archetype || 'Unknown'}<br>
                                <strong>Avg Elixir Cost:</strong> ${battle.deck_avg_cost.toFixed(1)}
                            </div>
                            <div class="deck-grid">
                                ${battle.player1_deck.map(card => `
                                    <div class="card-detail">
                                        <span>${card.name}</span>
                                        <span class="card-level">Lv ${card.level}</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>

                        <div class="vs-divider">VS</div>

                        <div class="player-section">
                            <h3>Opponent's Deck</h3>
                            <div class="deck-meta">
                                <strong>Player:</strong> ${battle.opponent_name || 'Unknown'}<br>
                                <strong>Archetype:</strong> ${battle.opponent_archetype || 'Unknown'}<br>
                                <strong>Avg Elixir Cost:</strong> ${battle.opponent_avg_cost.toFixed(1)}
                            </div>
                            <div class="deck-grid">
                                ${battle.player2_deck.map(card => `
                                    <div class="card-detail">
                                        <span>${card.name}</span>
                                        <span class="card-level">Lv ${card.level}</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>

                    <div class="section-divider"></div>

                    <h3 class="section-title">Battle Statistics</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">Game Mode</div>
                            <div class="info-value">${battle.game_mode}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Battle Type</div>
                            <div class="info-value">${battle.battle_type || 'Standard'}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Your Crowns</div>
                            <div class="info-value">${battle.player1_crowns} 👑</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Opponent Crowns</div>
                            <div class="info-value">${battle.player2_crowns} 👑</div>
                        </div>
                    </div>
                `;

                detailDiv.innerHTML = html;
                modal.classList.add('show');
            }

            function closeModal() {
                const modal = document.getElementById('battleModal');
                modal.classList.remove('show');
            }

            // Close modal when clicking outside
            document.addEventListener('click', (e) => {
                const modal = document.getElementById('battleModal');
                if (e.target === modal) {
                    closeModal();
                }
            });

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
