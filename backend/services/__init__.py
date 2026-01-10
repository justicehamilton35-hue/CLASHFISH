"""Services module."""
from .clash_royale_api import clash_royale_client, ClashRoyaleClient, ClashRoyaleAPIError
from .deck_classifier import deck_classifier, DeckClassifier
from .strategic_analyzer import StrategicAnalyzer

# Optional computer vision imports
try:
    from .card_detector import CardDetector, CARD_COSTS
    from .replay_analyzer import ReplayAnalyzer
    CV_AVAILABLE = True
except ImportError:
    CardDetector = None
    ReplayAnalyzer = None
    CARD_COSTS = {}
    CV_AVAILABLE = False

__all__ = [
    "clash_royale_client",
    "ClashRoyaleClient",
    "ClashRoyaleAPIError",
    "deck_classifier",
    "DeckClassifier",
    "StrategicAnalyzer",
    "CardDetector",
    "ReplayAnalyzer",
    "CARD_COSTS",
    "CV_AVAILABLE",
]
