"""
Deck Classification Service.
Classifies decks into archetypes based on card composition and synergies.
"""
from typing import List, Dict, Tuple, Optional


class DeckClassifier:
    """
    Rule-based deck classifier that identifies deck archetypes.
    """

    # Define signature cards for each archetype
    ARCHETYPES = {
        "hog_cycle": {
            "name": "2.6 Hog Cycle",
            "category": "cycle",
            "signature_cards": ["Hog Rider"],
            "common_cards": ["Musketeer", "Ice Golem", "Cannon", "Ice Spirit", "Skeletons", "Fireball", "The Log"],
            "max_avg_elixir": 3.0,
            "description": "Fast cycle deck centered around Hog Rider",
        },
        "log_bait": {
            "name": "Log Bait",
            "category": "bait",
            "signature_cards": ["Goblin Barrel", "Princess"],
            "common_cards": ["Rocket", "Inferno Tower", "Knight", "Goblin Gang", "Ice Spirit", "The Log"],
            "description": "Bait opponent's log, then punish with Goblin Barrel",
        },
        "xbow_cycle": {
            "name": "X-Bow Cycle",
            "category": "siege",
            "signature_cards": ["X-Bow"],
            "common_cards": ["Tesla", "Archers", "Ice Golem", "Skeletons", "Ice Spirit", "Fireball", "The Log"],
            "max_avg_elixir": 3.5,
            "description": "Siege deck that locks X-Bow onto tower",
        },
        "golem_beatdown": {
            "name": "Golem Beatdown",
            "category": "beatdown",
            "signature_cards": ["Golem"],
            "common_cards": ["Night Witch", "Baby Dragon", "Tornado", "Lightning", "Mega Minion", "Lumberjack"],
            "min_avg_elixir": 4.0,
            "description": "Heavy beatdown with Golem as tank",
        },
        "giant_double_prince": {
            "name": "Giant Double Prince",
            "category": "beatdown",
            "signature_cards": ["Giant", "Prince", "Dark Prince"],
            "common_cards": ["Electro Wizard", "Mega Minion", "Zap", "Fireball"],
            "min_avg_elixir": 4.0,
            "description": "Beatdown deck with Giant and both Princes",
        },
        "pekka_bridge_spam": {
            "name": "Pekka Bridge Spam",
            "category": "bridge_spam",
            "signature_cards": ["P.E.K.K.A", "Battle Ram"],
            "common_cards": ["Bandit", "Electro Wizard", "Magic Archer", "Poison", "Zap"],
            "description": "Aggressive bridge spam with P.E.K.K.A. for defense",
        },
        "lava_hound": {
            "name": "Lava Hound",
            "category": "beatdown",
            "signature_cards": ["Lava Hound"],
            "common_cards": ["Balloon", "Baby Dragon", "Miner", "Mega Minion", "Tombstone", "Fireball", "Zap"],
            "min_avg_elixir": 3.8,
            "description": "Air beatdown centered around Lava Hound",
        },
        "graveyard": {
            "name": "Graveyard",
            "category": "graveyard",
            "signature_cards": ["Graveyard"],
            "common_cards": ["Knight", "Archers", "Ice Wizard", "Tornado", "Poison", "Freeze"],
            "description": "Control deck with Graveyard as win condition",
        },
        "miner_control": {
            "name": "Miner Control",
            "category": "control",
            "signature_cards": ["Miner"],
            "common_cards": ["Poison", "Mini P.E.K.K.A", "Inferno Tower", "Ice Spirit", "Skeletons", "The Log"],
            "max_avg_elixir": 3.3,
            "description": "Control deck with Miner for chip damage",
        },
        "mega_knight": {
            "name": "Mega Knight Control",
            "category": "control",
            "signature_cards": ["Mega Knight"],
            "common_cards": ["Inferno Dragon", "Bats", "Miner", "Poison", "Zap"],
            "description": "Control deck using Mega Knight for defense and counter-push",
        },
    }

    @staticmethod
    def calculate_deck_cost(deck: List[Dict]) -> float:
        """
        Calculate average elixir cost of a deck.

        Args:
            deck: List of card dictionaries with elixir_cost or card names

        Returns:
            Average elixir cost
        """
        # Card elixir costs (hardcoded for now)
        CARD_COSTS = {
            "Skeletons": 1, "Ice Spirit": 1, "Electro Spirit": 1,
            "The Log": 2, "Zap": 2, "Bats": 2, "Ice Golem": 2, "Snowball": 2,
            "Knight": 3, "Archers": 3, "Cannon": 3, "Goblin Gang": 3, "Miner": 3,
            "Hog Rider": 4, "Musketeer": 4, "Fireball": 4, "Mini P.E.K.K.A": 4, "Prince": 4,
            "Giant": 5, "Balloon": 5, "Wizard": 5, "Bowler": 5,
            "P.E.K.K.A": 7, "Golem": 8, "Lava Hound": 7,
            "Graveyard": 5, "Rocket": 6, "Lightning": 6, "Goblin Barrel": 3,
            "X-Bow": 6, "Mortar": 4, "Inferno Tower": 5, "Tesla": 4,
            "Baby Dragon": 4, "Mega Minion": 3, "Night Witch": 4,
            "Dark Prince": 4, "Battle Ram": 4, "Bandit": 3,
            "Electro Wizard": 4, "Ice Wizard": 3, "Princess": 3,
            "Tornado": 3, "Poison": 4, "Freeze": 4, "Lumberjack": 4,
            "Mega Knight": 7, "Inferno Dragon": 4, "Magic Archer": 4,
        }

        total_cost = 0
        count = 0

        for card in deck:
            card_name = card.get('name', '')
            # Try to get elixir cost from card data first
            if 'elixir_cost' in card or 'elixirCost' in card:
                cost = card.get('elixir_cost') or card.get('elixirCost')
                total_cost += cost
                count += 1
            elif card_name in CARD_COSTS:
                total_cost += CARD_COSTS[card_name]
                count += 1

        return round(total_cost / count, 2) if count > 0 else 0.0

    @staticmethod
    def extract_card_names(deck: List[Dict]) -> List[str]:
        """
        Extract card names from deck data.

        Args:
            deck: List of card dictionaries

        Returns:
            List of card names
        """
        return [card.get('name', '') for card in deck]

    def classify_deck(self, deck: List[Dict]) -> Tuple[str, str, float]:
        """
        Classify a deck into an archetype.

        Args:
            deck: List of 8 card dictionaries

        Returns:
            Tuple of (archetype_id, archetype_name, confidence)
        """
        if not deck or len(deck) != 8:
            return ("unknown", "Unknown Deck", 0.0)

        card_names = self.extract_card_names(deck)
        avg_cost = self.calculate_deck_cost(deck)

        best_match = None
        best_score = 0.0

        for archetype_id, archetype_data in self.ARCHETYPES.items():
            score = 0.0

            # Check for signature cards (high weight)
            signature_matches = sum(1 for card in archetype_data['signature_cards'] if card in card_names)
            signature_total = len(archetype_data['signature_cards'])
            if signature_total > 0:
                score += (signature_matches / signature_total) * 50

            # Check for common cards (medium weight)
            common_matches = sum(1 for card in archetype_data['common_cards'] if card in card_names)
            common_total = len(archetype_data['common_cards'])
            if common_total > 0:
                score += (common_matches / common_total) * 30

            # Check elixir cost constraints
            min_cost = archetype_data.get('min_avg_elixir', 0)
            max_cost = archetype_data.get('max_avg_elixir', 10)
            if min_cost <= avg_cost <= max_cost:
                score += 20

            # Update best match
            if score > best_score:
                best_score = score
                best_match = (archetype_id, archetype_data['name'], score / 100)

        # If no good match found, classify as generic
        if not best_match or best_match[2] < 0.4:
            # Try to classify by category based on cards
            if any(card in card_names for card in ["Golem", "Giant", "Lava Hound"]):
                return ("beatdown", "Beatdown", 0.5)
            elif avg_cost < 3.2:
                return ("cycle", "Cycle Deck", 0.5)
            elif any(card in card_names for card in ["X-Bow", "Mortar"]):
                return ("siege", "Siege", 0.5)
            else:
                return ("unknown", "Unknown Deck", 0.3)

        return best_match

    def get_archetype_info(self, archetype_id: str) -> Optional[Dict]:
        """
        Get detailed information about an archetype.

        Args:
            archetype_id: Archetype identifier

        Returns:
            Dictionary with archetype information or None if not found
        """
        return self.ARCHETYPES.get(archetype_id)

    def get_matchup_rating(self, player_archetype: str, opponent_archetype: str) -> str:
        """
        Get matchup rating between two archetypes.
        This is a simplified version; full implementation would use a matchup matrix.

        Args:
            player_archetype: Player's deck archetype
            opponent_archetype: Opponent's deck archetype

        Returns:
            Rating: 'favorable', 'neutral', or 'unfavorable'
        """
        # Simplified matchup table
        MATCHUPS = {
            ("hog_cycle", "golem_beatdown"): "unfavorable",
            ("hog_cycle", "log_bait"): "favorable",
            ("hog_cycle", "xbow_cycle"): "neutral",
            ("log_bait", "hog_cycle"): "unfavorable",
            ("log_bait", "golem_beatdown"): "favorable",
            ("xbow_cycle", "golem_beatdown"): "favorable",
            ("xbow_cycle", "miner_control"): "unfavorable",
            ("golem_beatdown", "hog_cycle"): "favorable",
            ("golem_beatdown", "xbow_cycle"): "unfavorable",
            ("pekka_bridge_spam", "golem_beatdown"): "favorable",
        }

        matchup = (player_archetype, opponent_archetype)
        return MATCHUPS.get(matchup, "neutral")


# Create singleton instance
deck_classifier = DeckClassifier()
