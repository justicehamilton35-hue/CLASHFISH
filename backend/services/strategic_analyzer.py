"""
Strategic Analysis Module
Provides detailed strategic insights based on battle data.
"""
from typing import Dict, List, Any, Tuple


class StrategicAnalyzer:
    """Analyzes battles and provides strategic insights."""

    # Archetype strengths and weaknesses
    ARCHETYPE_COUNTERS = {
        "hog_cycle": {
            "strong_against": ["golem_beatdown", "lava_hound"],
            "weak_against": ["xbow_siege", "mortar_siege"],
            "strategy": "Apply constant pressure with Hog Rider and cycle cards quickly. Defend with minimal elixir."
        },
        "golem_beatdown": {
            "strong_against": ["xbow_siege", "mortar_siege", "miner_control"],
            "weak_against": ["hog_cycle", "pekka_bridge_spam"],
            "strategy": "Build big pushes behind Golem. Defend lightly and punish opposite lane."
        },
        "log_bait": {
            "strong_against": ["pekka_bridge_spam", "miner_control"],
            "weak_against": ["graveyard", "spell_cycle"],
            "strategy": "Bait out Log/Zap with gang cards, then punish with Goblin Barrel."
        },
        "xbow_siege": {
            "strong_against": ["hog_cycle", "log_bait"],
            "weak_against": ["golem_beatdown", "giant_beatdown"],
            "strategy": "Lock X-Bow on tower, defend with Tesla and cycle cards. Control the tempo."
        },
        "pekka_bridge_spam": {
            "strong_against": ["golem_beatdown", "giant_beatdown"],
            "weak_against": ["hog_cycle", "log_bait"],
            "strategy": "Counter-push with PEKKA, apply opposite lane pressure with Battle Ram."
        },
        "graveyard": {
            "strong_against": ["log_bait", "spell_cycle"],
            "weak_against": ["splash_heavy", "cycle_decks"],
            "strategy": "Tank for Graveyard, time it when opponent is low on elixir."
        },
        "miner_control": {
            "strong_against": ["xbow_siege", "mortar_siege"],
            "weak_against": ["golem_beatdown", "log_bait"],
            "strategy": "Chip damage with Miner, defend efficiently, control the pace."
        },
        "mortar_siege": {
            "strong_against": ["hog_cycle", "log_bait"],
            "weak_against": ["golem_beatdown", "lava_hound"],
            "strategy": "Defensive Mortar, chip damage, cycle quickly."
        },
        "lava_hound": {
            "strong_against": ["xbow_siege", "mortar_siege"],
            "weak_against": ["hog_cycle", "miner_control"],
            "strategy": "Build air pushes, punish opposite lane when opponent commits."
        },
        "giant_beatdown": {
            "strong_against": ["xbow_siege", "mortar_siege"],
            "weak_against": ["pekka_bridge_spam", "hog_cycle"],
            "strategy": "Build pushes behind Giant, support with splash damage."
        },
        "spell_cycle": {
            "strong_against": ["golem_beatdown", "lava_hound"],
            "weak_against": ["fast_cycle", "bridge_spam"],
            "strategy": "Defend efficiently, chip tower with spells, cycle quickly."
        },
    }

    @staticmethod
    def analyze_battle(battle_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive battle analysis.

        Args:
            battle_data: Battle data with decks, result, tower HP, etc.

        Returns:
            Dict with strategic insights
        """
        player_archetype = battle_data.get('deck_archetype', 'unknown')
        opponent_archetype = battle_data.get('opponent_archetype', 'unknown')
        result = battle_data.get('player1_result', 'unknown')

        # Get matchup info
        matchup_info = StrategicAnalyzer._get_matchup_analysis(
            player_archetype,
            opponent_archetype
        )

        # Analyze tower damage
        damage_analysis = StrategicAnalyzer._analyze_tower_damage(battle_data)

        # Get strategic advice
        strategy = StrategicAnalyzer._get_strategy_advice(
            player_archetype,
            opponent_archetype,
            result
        )

        # Performance assessment
        performance = StrategicAnalyzer._assess_performance(
            battle_data,
            damage_analysis
        )

        return {
            "matchup_info": matchup_info,
            "damage_analysis": damage_analysis,
            "strategy": strategy,
            "performance": performance
        }

    @staticmethod
    def _get_matchup_analysis(player_arch: str, opponent_arch: str) -> Dict[str, Any]:
        """Analyze matchup between two archetypes."""
        player_info = StrategicAnalyzer.ARCHETYPE_COUNTERS.get(player_arch, {})

        strong_against = player_info.get('strong_against', [])
        weak_against = player_info.get('weak_against', [])

        if opponent_arch in strong_against:
            matchup_type = "favorable"
            expected_outcome = "You should win this matchup"
        elif opponent_arch in weak_against:
            matchup_type = "unfavorable"
            expected_outcome = "This is a difficult matchup"
        else:
            matchup_type = "neutral"
            expected_outcome = "Even matchup, skill dependent"

        return {
            "type": matchup_type,
            "expected": expected_outcome,
            "player_strategy": player_info.get('strategy', ''),
            "strong_against": strong_against,
            "weak_against": weak_against
        }

    @staticmethod
    def _analyze_tower_damage(battle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze tower damage to assess game closeness."""
        player_team = battle_data.get('team', [{}])[0] if battle_data.get('team') else {}
        opponent_team = battle_data.get('opponent', [{}])[0] if battle_data.get('opponent') else {}

        player_king_hp = player_team.get('kingTowerHitPoints', 0)
        player_princess_hp = player_team.get('princessTowersHitPoints', [0, 0])

        opponent_king_hp = opponent_team.get('kingTowerHitPoints', 0)
        opponent_princess_hp = opponent_team.get('princessTowersHitPoints', [0, 0])

        player_crowns = battle_data.get('player1_crowns', 0)
        opponent_crowns = battle_data.get('player2_crowns', 0)

        # Calculate remaining HP percentages (assuming max HP is 4200 for king, 2534 for princess)
        KING_MAX_HP = 4200
        PRINCESS_MAX_HP = 2534

        player_total_hp = player_king_hp + sum(player_princess_hp)
        opponent_total_hp = opponent_king_hp + sum(opponent_princess_hp)

        # Determine game closeness
        if player_crowns == 3 and opponent_total_hp > 0:
            closeness = "dominant"
            description = "Decisive 3-crown victory"
        elif opponent_crowns == 3 and player_total_hp > 0:
            closeness = "dominated"
            description = "Defeated by 3-crown"
        elif player_crowns - opponent_crowns >= 2:
            closeness = "comfortable"
            description = "Clear victory"
        elif opponent_crowns - player_crowns >= 2:
            closeness = "difficult"
            description = "Clear defeat"
        elif abs(player_crowns - opponent_crowns) == 1:
            if player_total_hp > opponent_total_hp * 1.5:
                closeness = "controlled"
                description = "Won with towers intact"
            elif opponent_total_hp > player_total_hp * 1.5:
                closeness = "pressured"
                description = "Lost while taking heavy damage"
            else:
                closeness = "close"
                description = "Very close match"
        else:
            closeness = "even"
            description = "Evenly matched"

        return {
            "closeness": closeness,
            "description": description,
            "player_hp_remaining": player_total_hp,
            "opponent_hp_remaining": opponent_total_hp,
            "crown_difference": player_crowns - opponent_crowns
        }

    @staticmethod
    def _get_strategy_advice(player_arch: str, opponent_arch: str, result: str) -> Dict[str, Any]:
        """Get strategic advice for matchup."""
        player_info = StrategicAnalyzer.ARCHETYPE_COUNTERS.get(player_arch, {})
        opponent_info = StrategicAnalyzer.ARCHETYPE_COUNTERS.get(opponent_arch, {})

        general_strategy = player_info.get('strategy', 'Play to your deck strengths')

        # Specific advice based on matchup
        advice = []

        if opponent_arch in player_info.get('weak_against', []):
            if result == 'win':
                advice.append("Great job winning a difficult matchup!")
                advice.append("You likely outplayed your opponent or had better card levels.")
            else:
                advice.append("This matchup naturally favors your opponent.")
                advice.append("Focus on defending efficiently and looking for elixir advantages.")
        elif opponent_arch in player_info.get('strong_against', []):
            if result == 'loss':
                advice.append("You lost a favorable matchup - review your gameplay.")
                advice.append("Look for missed opportunities or defensive mistakes.")
            else:
                advice.append("Good execution of a favorable matchup!")

        # Add opponent-specific advice
        opponent_strategy = opponent_info.get('strategy', '')
        if opponent_strategy:
            advice.append(f"Opponent's typical strategy: {opponent_strategy}")

        return {
            "general": general_strategy,
            "specific_advice": advice
        }

    @staticmethod
    def _assess_performance(battle_data: Dict[str, Any], damage_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess player performance in the battle."""
        result = battle_data.get('player1_result', 'unknown')
        closeness = damage_analysis.get('closeness', 'unknown')
        matchup_rating = battle_data.get('matchup_rating', 0.5)

        # Determine performance quality
        if result == 'win':
            if closeness == 'dominant':
                quality = "excellent"
                description = "Outstanding performance"
            elif closeness == 'comfortable':
                quality = "good"
                description = "Solid victory"
            elif closeness == 'close':
                quality = "adequate"
                description = "Narrow victory"
            else:
                quality = "good"
                description = "Well played"
        elif result == 'loss':
            if closeness == 'dominated':
                quality = "poor"
                description = "Significant areas for improvement"
            elif closeness == 'difficult':
                quality = "below_average"
                description = "Could improve execution"
            elif closeness == 'close':
                quality = "decent"
                description = "Close defeat, small mistakes"
            else:
                quality = "below_average"
                description = "Room for improvement"
        else:
            quality = "neutral"
            description = "Draw"

        # Add context based on matchup
        if matchup_rating < 0.45 and result == 'win':
            description += " (won unfavorable matchup)"
        elif matchup_rating > 0.55 and result == 'loss':
            description += " (lost favorable matchup)"

        return {
            "quality": quality,
            "description": description,
            "notes": []
        }

    @staticmethod
    def analyze_deck_synergy(deck: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze synergies within a deck."""
        card_names = [card['name'] for card in deck]

        synergies = []
        weaknesses = []

        # Check for common synergies
        if 'Hog Rider' in card_names and 'Freeze' in card_names:
            synergies.append("Hog + Freeze: Powerful surprise combo")

        if 'Giant' in card_names and 'Sparky' in card_names:
            synergies.append("Giant + Sparky: Classic beatdown combo")

        if 'Miner' in card_names and 'Poison' in card_names:
            synergies.append("Miner + Poison: Control chip damage combo")

        if 'Golem' in card_names and 'Night Witch' in card_names:
            synergies.append("Golem + Night Witch: Strong beatdown synergy")

        # Check for bait mechanics
        bait_cards = sum(1 for card in card_names if card in [
            'Goblin Gang', 'Goblin Barrel', 'Skeleton Army', 'Minion Horde'
        ])
        if bait_cards >= 2:
            synergies.append(f"Spell bait: {bait_cards} cards require same counter")

        # Check for air defense
        air_defense = sum(1 for card in card_names if card in [
            'Musketeer', 'Archers', 'Wizard', 'Baby Dragon', 'Mega Minion',
            'Minions', 'Electro Wizard', 'Hunter', 'Tesla', 'Inferno Tower'
        ])
        if air_defense < 2:
            weaknesses.append("Limited air defense")

        # Check for splash damage
        splash_cards = sum(1 for card in card_names if card in [
            'Wizard', 'Baby Dragon', 'Valkyrie', 'Bomber', 'Executioner',
            'Fireball', 'Poison', 'Rocket', 'Lightning'
        ])
        if splash_cards < 2:
            weaknesses.append("Limited splash damage")

        return {
            "synergies": synergies,
            "weaknesses": weaknesses
        }
