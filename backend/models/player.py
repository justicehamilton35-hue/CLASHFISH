"""
Player database model.
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, func
from backend.database.base import Base


class Player(Base):
    """Player model representing a Clash Royale player."""

    __tablename__ = "players"

    player_id = Column(String, primary_key=True, index=True)
    player_tag = Column(String, unique=True, nullable=False, index=True)
    player_name = Column(String, nullable=False)

    # Stats
    current_trophies = Column(Integer, default=0)
    best_trophies = Column(Integer, default=0)
    level = Column(Integer, default=1)

    # Clan
    clan_id = Column(String, nullable=True)
    clan_name = Column(String, nullable=True)

    # Game stats
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    three_crown_wins = Column(Integer, default=0)
    cards_discovered = Column(Integer, default=0)
    favorite_card = Column(String, nullable=True)

    # Additional profile data stored as JSON
    profile_data = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Player {self.player_name} ({self.player_tag})>"

    @property
    def win_rate(self) -> float:
        """Calculate win rate percentage."""
        total_games = self.wins + self.losses
        if total_games == 0:
            return 0.0
        return (self.wins / total_games) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "player_id": self.player_id,
            "player_tag": self.player_tag,
            "player_name": self.player_name,
            "current_trophies": self.current_trophies,
            "best_trophies": self.best_trophies,
            "level": self.level,
            "clan_id": self.clan_id,
            "clan_name": self.clan_name,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": self.win_rate,
            "three_crown_wins": self.three_crown_wins,
            "cards_discovered": self.cards_discovered,
            "favorite_card": self.favorite_card,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
