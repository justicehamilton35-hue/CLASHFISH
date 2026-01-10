"""
Replay Analyzer - Move-by-move analysis similar to chess engines
Analyzes card placements and provides Stockfish-like evaluations.
"""
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import logging


class ReplayAnalyzer:
    """Analyzes replay data to provide move-by-move insights."""

    # Move quality classifications
    MOVE_QUALITY = {
        "brilliant": {"threshold": 2.0, "symbol": "!!"},
        "great": {"threshold": 1.0, "symbol": "!"},
        "good": {"threshold": 0.3, "symbol": ""},
        "inaccuracy": {"threshold": -0.5, "symbol": "?!"},
        "mistake": {"threshold": -1.5, "symbol": "?"},
        "blunder": {"threshold": float('-inf'), "symbol": "??"}
    }

    @staticmethod
    def analyze_replay(
        card_plays: List[Dict[str, Any]],
        battle_result: Dict[str, Any],
        deck_archetype: str
    ) -> Dict[str, Any]:
        """
        Comprehensive replay analysis.

        Args:
            card_plays: List of card play events with timestamps
            battle_result: Final battle outcome data
            deck_archetype: Player's deck archetype

        Returns:
            Complete replay analysis with move evaluations
        """
        # Analyze each move
        move_evaluations = ReplayAnalyzer._evaluate_moves(card_plays, deck_archetype)

        # Calculate accuracy
        accuracy = ReplayAnalyzer._calculate_accuracy(move_evaluations)

        # Find critical moments
        critical_moments = ReplayAnalyzer._find_critical_moments(move_evaluations)

        # Generate insights
        insights = ReplayAnalyzer._generate_insights(
            move_evaluations,
            critical_moments,
            battle_result
        )

        return {
            "move_evaluations": move_evaluations,
            "accuracy": accuracy,
            "critical_moments": critical_moments,
            "insights": insights,
            "summary": ReplayAnalyzer._generate_summary(
                move_evaluations,
                accuracy,
                battle_result
            )
        }

    @staticmethod
    def _evaluate_moves(
        card_plays: List[Dict[str, Any]],
        deck_archetype: str
    ) -> List[Dict[str, Any]]:
        """
        Evaluate each move (card play) in the replay.

        Returns:
            List of move evaluations with quality ratings
        """
        evaluations = []

        for i, play in enumerate(card_plays):
            # Simplified evaluation logic (would be much more complex in production)
            evaluation = {
                "move_number": i + 1,
                "timestamp": play['timestamp'],
                "card": play['card'],
                "position": play['position'],
                "evaluation_score": ReplayAnalyzer._calculate_move_score(
                    play,
                    card_plays[:i],  # Previous moves
                    deck_archetype
                ),
                "is_player": i % 2 == 0  # Alternate between player and opponent
            }

            # Classify move quality
            evaluation["quality"] = ReplayAnalyzer._classify_move_quality(
                evaluation["evaluation_score"]
            )

            # Add context
            evaluation["context"] = ReplayAnalyzer._get_move_context(
                play,
                card_plays[:i]
            )

            evaluations.append(evaluation)

        return evaluations

    @staticmethod
    def _calculate_move_score(
        play: Dict[str, Any],
        previous_plays: List[Dict[str, Any]],
        deck_archetype: str
    ) -> float:
        """
        Calculate evaluation score for a move.
        Positive = good, negative = bad.

        This is simplified - real implementation would be much more sophisticated.
        """
        score = 0.0

        # Timing evaluation
        if previous_plays:
            time_since_last = play['timestamp'] - previous_plays[-1]['timestamp']

            # Punish very slow plays (wasting elixir)
            if time_since_last > 5.0:
                score -= 0.5

            # Reward quick responses
            if time_since_last < 1.0:
                score += 0.3

        # Position evaluation (center vs corners)
        x, y = play['position']['x'], play['position']['y']

        # Reward central positioning for certain cards
        if "Tank" in play['card'] or "Giant" in play['card']:
            center_distance = abs(0.5 - x)  # Assuming normalized 0-1 coordinates
            score += (0.5 - center_distance) * 0.5

        # Context-based evaluation
        if len(previous_plays) > 0:
            last_play = previous_plays[-1]

            # Reward counter-plays
            if ReplayAnalyzer._is_counter(play['card'], last_play['card']):
                score += 1.5

            # Punish redundant plays
            if play['card'] == last_play['card']:
                score -= 0.8

        # Random variation to simulate uncertainty
        import random
        score += random.uniform(-0.3, 0.3)

        return score

    @staticmethod
    def _is_counter(card: str, opponent_card: str) -> bool:
        """Check if card is a good counter to opponent's card."""
        # Simplified counter logic
        counters = {
            "Fireball": ["Barbarians", "Minion Horde", "Wizard"],
            "Zap": ["Minions", "Skeleton Army", "Goblin Gang"],
            "The Log": ["Goblin Barrel", "Princess", "Skeleton Army"],
            "Arrows": ["Minion Horde", "Minions", "Princess"],
            "Lightning": ["Elixir Collector", "Sparky", "Three Musketeers"],
            "P.E.K.K.A": ["Giant", "Golem", "Mega Knight"],
            "Inferno Tower": ["Giant", "Golem", "Lava Hound"],
            "Rocket": ["Elixir Collector", "Sparky", "Three Musketeers"],
        }

        return opponent_card in counters.get(card, [])

    @staticmethod
    def _classify_move_quality(score: float) -> Dict[str, str]:
        """Classify move based on evaluation score."""
        for quality, data in ReplayAnalyzer.MOVE_QUALITY.items():
            if score >= data["threshold"]:
                return {
                    "rating": quality,
                    "symbol": data["symbol"],
                    "score": score
                }
        return {"rating": "good", "symbol": "", "score": score}

    @staticmethod
    def _get_move_context(
        play: Dict[str, Any],
        previous_plays: List[Dict[str, Any]]
    ) -> str:
        """Generate contextual description for move."""
        if not previous_plays:
            return "Opening move"

        last_play = previous_plays[-1]
        time_diff = play['timestamp'] - last_play['timestamp']

        if time_diff < 1.0:
            return f"Quick response to {last_play['card']}"
        elif time_diff > 5.0:
            return "Defensive patience"
        else:
            return "Standard tempo play"

    @staticmethod
    def _calculate_accuracy(move_evaluations: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate player accuracy similar to chess.com.

        Returns:
            Accuracy percentage and move breakdown
        """
        player_moves = [m for m in move_evaluations if m['is_player']]

        if not player_moves:
            return {"overall": 0.0, "move_breakdown": {}}

        quality_counts = {
            "brilliant": 0,
            "great": 0,
            "good": 0,
            "inaccuracy": 0,
            "mistake": 0,
            "blunder": 0
        }

        for move in player_moves:
            rating = move['quality']['rating']
            quality_counts[rating] += 1

        total_moves = len(player_moves)

        # Calculate accuracy (100% = all brilliant/great, decreases with mistakes)
        accuracy = (
            (quality_counts["brilliant"] * 1.0 +
             quality_counts["great"] * 0.9 +
             quality_counts["good"] * 0.8 +
             quality_counts["inaccuracy"] * 0.6 +
             quality_counts["mistake"] * 0.3 +
             quality_counts["blunder"] * 0.0) / total_moves * 100
        )

        return {
            "overall": round(accuracy, 1),
            "move_breakdown": quality_counts,
            "total_moves": total_moves
        }

    @staticmethod
    def _find_critical_moments(move_evaluations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify critical moments in the match."""
        critical_moments = []

        for i, move in enumerate(move_evaluations):
            # Find brilliant moves
            if move['quality']['rating'] == 'brilliant':
                critical_moments.append({
                    "move_number": move['move_number'],
                    "timestamp": move['timestamp'],
                    "type": "brilliant_move",
                    "description": f"Brilliant play: {move['card']} {move['quality']['symbol']}",
                    "card": move['card']
                })

            # Find blunders
            elif move['quality']['rating'] == 'blunder':
                critical_moments.append({
                    "move_number": move['move_number'],
                    "timestamp": move['timestamp'],
                    "type": "blunder",
                    "description": f"Missed opportunity with {move['card']} {move['quality']['symbol']}",
                    "card": move['card']
                })

            # Find turning points (large evaluation swings)
            if i > 0:
                prev_score = move_evaluations[i-1]['evaluation_score']
                curr_score = move['evaluation_score']
                swing = curr_score - prev_score

                if abs(swing) > 2.0:
                    critical_moments.append({
                        "move_number": move['move_number'],
                        "timestamp": move['timestamp'],
                        "type": "turning_point",
                        "description": f"Major momentum shift: {move['card']}",
                        "card": move['card'],
                        "swing": swing
                    })

        return critical_moments

    @staticmethod
    def _generate_insights(
        move_evaluations: List[Dict[str, Any]],
        critical_moments: List[Dict[str, Any]],
        battle_result: Dict[str, Any]
    ) -> List[str]:
        """Generate strategic insights from analysis."""
        insights = []

        # Overall performance
        player_moves = [m for m in move_evaluations if m['is_player']]
        avg_score = sum(m['evaluation_score'] for m in player_moves) / len(player_moves)

        if avg_score > 0.5:
            insights.append("Strong overall performance with consistent good moves")
        elif avg_score < -0.5:
            insights.append("Room for improvement in move selection and timing")

        # Mistake analysis
        mistakes = [m for m in player_moves if m['quality']['rating'] in ['mistake', 'blunder']]
        if len(mistakes) > len(player_moves) * 0.3:
            insights.append(f"High mistake rate: {len(mistakes)} critical errors")

        # Brilliant plays
        brilliant = [m for m in player_moves if m['quality']['rating'] == 'brilliant']
        if brilliant:
            insights.append(f"Excellent plays at moves {', '.join(str(m['move_number']) for m in brilliant)}")

        # Tempo analysis
        slow_moves = [m for m in move_evaluations if m['context'] == 'Defensive patience']
        if len(slow_moves) > 5:
            insights.append("Passive playstyle - consider more aggressive pressure")

        return insights

    @staticmethod
    def _generate_summary(
        move_evaluations: List[Dict[str, Any]],
        accuracy: Dict[str, float],
        battle_result: Dict[str, Any]
    ) -> str:
        """Generate human-readable summary."""
        result = battle_result.get('player1_result', 'unknown')
        accuracy_pct = accuracy.get('overall', 0)

        player_moves = [m for m in move_evaluations if m['is_player']]
        brilliant_count = sum(1 for m in player_moves if m['quality']['rating'] == 'brilliant')
        blunder_count = sum(1 for m in player_moves if m['quality']['rating'] == 'blunder')

        summary = f"You {'won' if result == 'win' else 'lost'} with {accuracy_pct}% accuracy. "
        summary += f"Played {len(player_moves)} moves "

        if brilliant_count > 0:
            summary += f"including {brilliant_count} brilliant play{'s' if brilliant_count > 1 else ''}"

        if blunder_count > 0:
            if brilliant_count > 0:
                summary += " but "
            summary += f"with {blunder_count} blunder{'s' if blunder_count > 1 else ''}"

        summary += "."

        return summary
