"""
Match database model.
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, ForeignKey, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from backend.database.base import Base
import enum


class MatchResult(str, enum.Enum):
    """Match result enumeration."""
    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"


class Match(Base):
    """Match model representing a Clash Royale battle."""

    __tablename__ = "matches"

    match_id = Column(String, primary_key=True, index=True)
    battle_time = Column(DateTime(timezone=True), nullable=False, index=True)
    game_mode = Column(String, nullable=False)  # 1v1, 2v2, challenge, etc.
    match_type = Column(String, nullable=True)  # PvP, friendly, etc.
    arena = Column(String, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    # Player 1 data
    player1_id = Column(String, ForeignKey("players.player_id"), nullable=False, index=True)
    player1_deck = Column(JSON, nullable=False)  # Array of 8 cards
    player1_crowns = Column(Integer, default=0)
    player1_king_tower_hp = Column(Integer, nullable=True)
    player1_princess_towers_hp = Column(JSON, nullable=True)  # [left, right]
    player1_elixir_leaked = Column(Float, default=0.0)
    player1_result = Column(SQLEnum(MatchResult), nullable=False)

    # Player 2 data
    player2_id = Column(String, ForeignKey("players.player_id"), nullable=False, index=True)
    player2_deck = Column(JSON, nullable=False)
    player2_crowns = Column(Integer, default=0)
    player2_king_tower_hp = Column(Integer, nullable=True)
    player2_princess_towers_hp = Column(JSON, nullable=True)
    player2_elixir_leaked = Column(Float, default=0.0)
    player2_result = Column(SQLEnum(MatchResult), nullable=False)

    # Replay data
    replay_available = Column(Boolean, default=False)
    replay_url = Column(String, nullable=True)

    # Raw data from API
    raw_data = Column(JSON, nullable=True)

    # Processing status
    processed = Column(Boolean, default=False, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default="now()")

    # Relationships
    player1 = relationship("Player", foreign_keys=[player1_id], lazy="joined")
    player2 = relationship("Player", foreign_keys=[player2_id], lazy="joined")

    def __repr__(self):
        return f"<Match {self.match_id} {self.player1_id} vs {self.player2_id}>"

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "match_id": self.match_id,
            "battle_time": self.battle_time.isoformat() if self.battle_time else None,
            "game_mode": self.game_mode,
            "match_type": self.match_type,
            "arena": self.arena,
            "duration_seconds": self.duration_seconds,
            "player1": {
                "player_id": self.player1_id,
                "deck": self.player1_deck,
                "crowns": self.player1_crowns,
                "king_tower_hp": self.player1_king_tower_hp,
                "princess_towers_hp": self.player1_princess_towers_hp,
                "elixir_leaked": self.player1_elixir_leaked,
                "result": self.player1_result.value if self.player1_result else None,
            },
            "player2": {
                "player_id": self.player2_id,
                "deck": self.player2_deck,
                "crowns": self.player2_crowns,
                "king_tower_hp": self.player2_king_tower_hp,
                "princess_towers_hp": self.player2_princess_towers_hp,
                "elixir_leaked": self.player2_elixir_leaked,
                "result": self.player2_result.value if self.player2_result else None,
            },
            "replay_available": self.replay_available,
            "processed": self.processed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
