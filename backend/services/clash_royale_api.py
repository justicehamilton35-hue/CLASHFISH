"""
Clash Royale API client service.
Handles fetching player and battle data from the official Clash Royale API,
with fallback to mock data for development.
"""
import json
import httpx
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta

from backend.config import settings


class ClashRoyaleAPIError(Exception):
    """Custom exception for Clash Royale API errors."""
    pass


class ClashRoyaleClient:
    """Client for interacting with Clash Royale API."""

    def __init__(self, api_key: Optional[str] = None, use_mock: Optional[bool] = None):
        """
        Initialize the Clash Royale API client.

        Args:
            api_key: API key for Clash Royale API (optional, uses settings if not provided)
            use_mock: Whether to use mock data (optional, uses settings if not provided)
        """
        self.api_key = api_key or settings.clash_royale_api_key
        self.base_url = settings.clash_royale_api_url
        self.use_mock = use_mock if use_mock is not None else settings.use_mock_data

        # Load mock data if in mock mode
        if self.use_mock:
            self._load_mock_data()

    def _load_mock_data(self):
        """Load mock data from JSON files."""
        mock_dir = Path("data/mock")

        # Load sample player
        player_file = mock_dir / "sample_player.json"
        if player_file.exists():
            with open(player_file, "r") as f:
                self.mock_player = json.load(f)
        else:
            self.mock_player = None

        # Load sample battles
        battles_file = mock_dir / "sample_battles.json"
        if battles_file.exists():
            with open(battles_file, "r") as f:
                self.mock_battles = json.load(f)
        else:
            self.mock_battles = []

    async def get_player(self, player_tag: str) -> Dict[str, Any]:
        """
        Get player information by player tag.

        Args:
            player_tag: Player tag (e.g., '#V2QUUQVU8' or 'V2QUUQVU8')

        Returns:
            Dictionary containing player data

        Raises:
            ClashRoyaleAPIError: If API request fails
        """
        # Clean player tag (remove # if present)
        player_tag = player_tag.lstrip('#').upper()

        if self.use_mock:
            # Return mock data
            if self.mock_player and self.mock_player.get('tag', '').lstrip('#') == player_tag:
                return self.mock_player
            else:
                raise ClashRoyaleAPIError(f"Mock player {player_tag} not found")

        # Make real API request
        url = f"{self.base_url}/players/%23{player_tag}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ClashRoyaleAPIError(f"Player {player_tag} not found")
            elif e.response.status_code == 403:
                raise ClashRoyaleAPIError("Invalid API key or access denied")
            else:
                raise ClashRoyaleAPIError(f"API error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise ClashRoyaleAPIError(f"Network error: {str(e)}")

    async def get_player_battles(self, player_tag: str) -> List[Dict[str, Any]]:
        """
        Get recent battles for a player.

        Args:
            player_tag: Player tag (e.g., '#V2QUUQVU8' or 'V2QUUQVU8')

        Returns:
            List of battle dictionaries

        Raises:
            ClashRoyaleAPIError: If API request fails
        """
        # Clean player tag
        player_tag = player_tag.lstrip('#').upper()

        if self.use_mock:
            # Return mock battles
            return self.mock_battles

        # Make real API request
        url = f"{self.base_url}/players/%23{player_tag}/battlelog"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ClashRoyaleAPIError(f"Player {player_tag} not found")
            elif e.response.status_code == 403:
                raise ClashRoyaleAPIError("Invalid API key or access denied")
            else:
                raise ClashRoyaleAPIError(f"API error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise ClashRoyaleAPIError(f"Network error: {str(e)}")

    def parse_player_data(self, api_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse player data from API response into our internal format.

        Args:
            api_data: Raw API response data

        Returns:
            Parsed player data
        """
        return {
            "player_id": api_data['tag'].lstrip('#'),
            "player_tag": api_data['tag'],
            "player_name": api_data['name'],
            "current_trophies": api_data.get('trophies', 0),
            "best_trophies": api_data.get('bestTrophies', 0),
            "level": api_data.get('expLevel', 1),
            "clan_id": api_data.get('clan', {}).get('tag', '').lstrip('#') if 'clan' in api_data else None,
            "clan_name": api_data.get('clan', {}).get('name') if 'clan' in api_data else None,
            "wins": api_data.get('wins', 0),
            "losses": api_data.get('losses', 0),
            "three_crown_wins": api_data.get('threeCrownWins', 0),
            "cards_discovered": len(api_data.get('cards', [])),
            "favorite_card": api_data.get('currentFavouriteCard', {}).get('name'),
            "profile_data": api_data,  # Store full profile as JSON
        }

    def parse_battle_data(self, battle_data: Dict[str, Any], player_tag: str) -> Dict[str, Any]:
        """
        Parse battle data from API response into our internal format.

        Args:
            battle_data: Raw battle data from API
            player_tag: Tag of the player we're analyzing (to determine player1 vs player2)

        Returns:
            Parsed match data
        """
        player_tag = player_tag.lstrip('#').upper()

        # Find which team the player is on
        team = battle_data.get('team', [])[0] if battle_data.get('team') else {}
        opponent = battle_data.get('opponent', [])[0] if battle_data.get('opponent') else {}

        # Determine if player is player1 or player2
        is_player1 = team.get('tag', '').lstrip('#').upper() == player_tag

        if is_player1:
            player1_data = team
            player2_data = opponent
        else:
            player1_data = opponent
            player2_data = team

        # Parse battle time
        battle_time_str = battle_data.get('battleTime', '')
        try:
            battle_time = datetime.strptime(battle_time_str, '%Y%m%dT%H%M%S.%fZ')
        except:
            battle_time = datetime.utcnow()

        # Generate match ID from battle time and player tags
        match_id = f"{player1_data.get('tag', '').lstrip('#')}_{player2_data.get('tag', '').lstrip('#')}_{battle_time_str}"

        # Determine results
        player1_crowns = player1_data.get('crowns', 0)
        player2_crowns = player2_data.get('crowns', 0)

        if player1_crowns > player2_crowns:
            player1_result = "win"
            player2_result = "loss"
        elif player1_crowns < player2_crowns:
            player1_result = "loss"
            player2_result = "win"
        else:
            player1_result = "draw"
            player2_result = "draw"

        return {
            "match_id": match_id,
            "battle_time": battle_time,
            "game_mode": battle_data.get('gameMode', {}).get('name', 'Unknown'),
            "match_type": battle_data.get('type', 'PvP'),
            "arena": battle_data.get('arena', {}).get('name'),
            "duration_seconds": None,  # Not provided by API
            # Player 1
            "player1_id": player1_data.get('tag', '').lstrip('#'),
            "player1_deck": [
                {
                    "name": card.get('name'),
                    "id": card.get('id'),
                    "level": card.get('level'),
                    "max_level": card.get('maxLevel'),
                }
                for card in player1_data.get('cards', [])
            ],
            "player1_crowns": player1_crowns,
            "player1_king_tower_hp": player1_data.get('kingTowerHitPoints'),
            "player1_princess_towers_hp": player1_data.get('princessTowersHitPoints'),
            "player1_elixir_leaked": 0.0,  # Not provided by API
            "player1_result": player1_result,
            # Player 2
            "player2_id": player2_data.get('tag', '').lstrip('#'),
            "player2_deck": [
                {
                    "name": card.get('name'),
                    "id": card.get('id'),
                    "level": card.get('level'),
                    "max_level": card.get('maxLevel'),
                }
                for card in player2_data.get('cards', [])
            ],
            "player2_crowns": player2_crowns,
            "player2_king_tower_hp": player2_data.get('kingTowerHitPoints'),
            "player2_princess_towers_hp": player2_data.get('princessTowersHitPoints'),
            "player2_elixir_leaked": 0.0,  # Not provided by API
            "player2_result": player2_result,
            # Meta
            "replay_available": False,
            "replay_url": None,
            "raw_data": battle_data,
            "processed": False,
        }


# Create a singleton instance
clash_royale_client = ClashRoyaleClient()
