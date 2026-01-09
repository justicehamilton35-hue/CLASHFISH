"""
Match Analysis database model.
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.base import Base
from datetime import datetime


class MatchAnalysis(Base):
    """Match analysis model storing computed analysis results."""

    __tablename__ = "match_analysis"

    analysis_id = Column(String, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.match_id"), unique=True, nullable=False, index=True)
    player_id = Column(String, ForeignKey("players.player_id"), nullable=False, index=True)

    # Win probability
    final_win_probability = Column(Float, nullable=True)
    win_probability_curve = Column(JSON, nullable=True)  # [{timestamp_ms, probability}]

    # Deck information
    deck_archetype = Column(String, nullable=True)
    opponent_deck_archetype = Column(String, nullable=True)

    # Move statistics
    total_moves = Column(Integer, default=0)
    mistakes = Column(Integer, default=0)
    blunders = Column(Integer, default=0)
    great_moves = Column(Integer, default=0)
    brilliant_moves = Column(Integer, default=0)
    average_move_quality = Column(Float, default=0.0)

    # Performance metrics
    elixir_efficiency = Column(Float, default=0.0)  # 0-100
    cycle_speed = Column(Float, default=0.0)  # avg seconds per card cycle
    pressure_score = Column(Float, default=0.0)  # offensive pressure rating
    defense_rating = Column(Float, default=0.0)  # defensive effectiveness

    # Key moments and evaluations
    key_moments = Column(JSON, nullable=True)  # Array of critical events
    move_evaluations = Column(JSON, nullable=True)  # Array of move evaluations

    # Strategy
    strategy_followed = Column(String, nullable=True)
    recommended_strategy = Column(String, nullable=True)
    strategic_mistakes = Column(JSON, nullable=True)

    # AI commentary
    commentary = Column(String, nullable=True)  # Full text commentary
    improvement_tips = Column(JSON, nullable=True)  # Array of tips

    # Model metadata
    computed_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    model_version = Column(String, nullable=True)

    # Relationships
    match = relationship("Match", foreign_keys=[match_id], lazy="joined")
    player = relationship("Player", foreign_keys=[player_id], lazy="joined")

    def __repr__(self):
        return f"<MatchAnalysis {self.analysis_id} for match {self.match_id}>"

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "analysis_id": self.analysis_id,
            "match_id": self.match_id,
            "player_id": self.player_id,
            "final_win_probability": self.final_win_probability,
            "win_probability_curve": self.win_probability_curve,
            "deck_archetype": self.deck_archetype,
            "opponent_deck_archetype": self.opponent_deck_archetype,
            "total_moves": self.total_moves,
            "mistakes": self.mistakes,
            "blunders": self.blunders,
            "great_moves": self.great_moves,
            "brilliant_moves": self.brilliant_moves,
            "average_move_quality": self.average_move_quality,
            "elixir_efficiency": self.elixir_efficiency,
            "cycle_speed": self.cycle_speed,
            "pressure_score": self.pressure_score,
            "defense_rating": self.defense_rating,
            "key_moments": self.key_moments,
            "move_evaluations": self.move_evaluations,
            "strategy_followed": self.strategy_followed,
            "recommended_strategy": self.recommended_strategy,
            "strategic_mistakes": self.strategic_mistakes,
            "commentary": self.commentary,
            "improvement_tips": self.improvement_tips,
            "computed_at": self.computed_at.isoformat() if self.computed_at else None,
            "model_version": self.model_version,
        }

    @property
    def accuracy_percentage(self) -> float:
        """Calculate accuracy as percentage of good moves."""
        if self.total_moves == 0:
            return 0.0
        good_moves = self.total_moves - self.mistakes - self.blunders
        return (good_moves / self.total_moves) * 100
