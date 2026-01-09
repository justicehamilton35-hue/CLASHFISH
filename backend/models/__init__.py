"""Database models."""
try:
    from .player import Player
    from .match import Match, MatchResult
    from .analysis import MatchAnalysis
    __all__ = ["Player", "Match", "MatchResult", "MatchAnalysis"]
except Exception as e:
    # If models can't be imported (no SQLAlchemy), create dummy classes
    print(f"⚠️  Database models not available: {e}")
    print("   Running without database support")

    class Player:
        pass

    class Match:
        pass

    class MatchResult:
        pass

    class MatchAnalysis:
        pass

    __all__ = ["Player", "Match", "MatchResult", "MatchAnalysis"]
