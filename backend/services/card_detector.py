"""
Card Detection Service using Roboflow Inference
Detects Clash Royale cards from images and video frames.
"""
from typing import List, Dict, Any, Tuple, Optional
import logging

try:
    from inference_sdk import InferenceHTTPClient
    import cv2
    import numpy as np
    from PIL import Image
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    logging.warning("Computer vision libraries not available. Install: inference, opencv-python, pillow")


class CardDetector:
    """Detects Clash Royale cards using Roboflow models."""

    # Roboflow model IDs for Clash Royale card detection
    MODELS = {
        "vision_bot": "clash-royale-card-detection-ylzsc/4",  # Vision Bot's model
        "clashroyale": "clash-royale-of3d3/1",  # Official ClashRoyale dataset
        "angelfire": "clash-royale-cylln/1",  # AngelFire's comprehensive model
    }

    def __init__(self, api_key: Optional[str] = None, model_id: Optional[str] = None):
        """
        Initialize card detector.

        Args:
            api_key: Roboflow API key (optional for Universe models)
            model_id: Which model to use (defaults to vision_bot)
        """
        if not VISION_AVAILABLE:
            raise RuntimeError("Computer vision libraries not installed")

        self.api_key = api_key
        self.model_id = model_id or self.MODELS["vision_bot"]

        # Initialize Roboflow client
        self.client = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=api_key
        )

    def detect_cards_from_image(
        self,
        image_path: str,
        confidence_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Detect cards from a single image.

        Args:
            image_path: Path to image file
            confidence_threshold: Minimum confidence for detections

        Returns:
            List of detected cards with positions and confidence
        """
        try:
            # Run inference
            result = self.client.infer(image_path, model_id=self.model_id)

            # Parse predictions
            detections = []
            for prediction in result.get('predictions', []):
                if prediction.get('confidence', 0) >= confidence_threshold:
                    detections.append({
                        'card_name': prediction.get('class'),
                        'confidence': prediction.get('confidence'),
                        'x': prediction.get('x'),
                        'y': prediction.get('y'),
                        'width': prediction.get('width'),
                        'height': prediction.get('height'),
                        'bbox': self._get_bbox(prediction)
                    })

            return detections

        except Exception as e:
            logging.error(f"Error detecting cards from image: {e}")
            return []

    def detect_cards_from_video(
        self,
        video_path: str,
        frame_interval: int = 30,
        confidence_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Detect cards from video file, processing every N frames.

        Args:
            video_path: Path to video file
            frame_interval: Process every N frames (30 = 1 per second at 30fps)
            confidence_threshold: Minimum confidence for detections

        Returns:
            List of frame-by-frame detections with timestamps
        """
        if not VISION_AVAILABLE:
            return []

        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = 0
            detections_timeline = []

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Process every N frames
                if frame_count % frame_interval == 0:
                    timestamp = frame_count / fps

                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Save temp frame
                    temp_path = f"/tmp/frame_{frame_count}.jpg"
                    cv2.imwrite(temp_path, frame)

                    # Detect cards
                    detections = self.detect_cards_from_image(
                        temp_path,
                        confidence_threshold
                    )

                    if detections:
                        detections_timeline.append({
                            'timestamp': timestamp,
                            'frame_number': frame_count,
                            'detections': detections
                        })

                frame_count += 1

            cap.release()
            return detections_timeline

        except Exception as e:
            logging.error(f"Error detecting cards from video: {e}")
            return []

    def extract_card_plays(
        self,
        detections_timeline: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extract distinct card plays from detection timeline.
        Filters out duplicate detections of same card across frames.

        Args:
            detections_timeline: Timeline from detect_cards_from_video

        Returns:
            List of card play events
        """
        card_plays = []
        last_cards = set()

        for frame_data in detections_timeline:
            current_cards = set()

            for detection in frame_data['detections']:
                card_name = detection['card_name']
                current_cards.add(card_name)

                # New card play detected
                if card_name not in last_cards:
                    card_plays.append({
                        'timestamp': frame_data['timestamp'],
                        'card': card_name,
                        'position': {
                            'x': detection['x'],
                            'y': detection['y']
                        },
                        'confidence': detection['confidence']
                    })

            last_cards = current_cards

        return card_plays

    def analyze_elixir_usage(
        self,
        card_plays: List[Dict[str, Any]],
        card_costs: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """
        Analyze elixir usage over time.

        Args:
            card_plays: List of card play events
            card_costs: Dictionary mapping card names to elixir costs

        Returns:
            Elixir timeline with accumulated usage
        """
        ELIXIR_REGEN_RATE = 1.0  # 1 elixir per second (normal time)
        MAX_ELIXIR = 10

        elixir_timeline = []
        current_elixir = MAX_ELIXIR

        for i, play in enumerate(card_plays):
            card = play['card']
            timestamp = play['timestamp']

            # Calculate elixir regenerated since last play
            if i > 0:
                time_diff = timestamp - card_plays[i-1]['timestamp']
                elixir_regen = min(time_diff * ELIXIR_REGEN_RATE, MAX_ELIXIR - current_elixir)
                current_elixir = min(current_elixir + elixir_regen, MAX_ELIXIR)

            # Spend elixir for this card
            card_cost = card_costs.get(card, 0)
            current_elixir -= card_cost

            elixir_timeline.append({
                'timestamp': timestamp,
                'card': card,
                'cost': card_cost,
                'elixir_after': current_elixir,
                'elixir_before': current_elixir + card_cost
            })

        return elixir_timeline

    @staticmethod
    def _get_bbox(prediction: Dict[str, Any]) -> Tuple[int, int, int, int]:
        """Convert prediction to bounding box coordinates."""
        x = prediction.get('x', 0)
        y = prediction.get('y', 0)
        width = prediction.get('width', 0)
        height = prediction.get('height', 0)

        x1 = int(x - width / 2)
        y1 = int(y - height / 2)
        x2 = int(x + width / 2)
        y2 = int(y + height / 2)

        return (x1, y1, x2, y2)

    def visualize_detections(
        self,
        image_path: str,
        detections: List[Dict[str, Any]],
        output_path: str
    ) -> None:
        """
        Draw bounding boxes on image.

        Args:
            image_path: Input image path
            detections: List of detections
            output_path: Where to save annotated image
        """
        if not VISION_AVAILABLE:
            return

        img = cv2.imread(image_path)

        for detection in detections:
            bbox = detection['bbox']
            card_name = detection['card_name']
            confidence = detection['confidence']

            # Draw bounding box
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

            # Add label
            label = f"{card_name} ({confidence:.2f})"
            cv2.putText(
                img,
                label,
                (bbox[0], bbox[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        cv2.imwrite(output_path, img)


# Card costs mapping (elixir cost for each card)
CARD_COSTS = {
    "Arrows": 3,
    "Fireball": 4,
    "Zap": 2,
    "The Log": 2,
    "Rocket": 6,
    "Lightning": 6,
    "Poison": 4,
    "Freeze": 4,
    "Tornado": 3,
    "Rage": 2,
    "Clone": 3,
    "Mirror": 1,  # Variable
    "Heal Spirit": 1,
    "Ice Spirit": 1,
    "Fire Spirit": 1,
    "Electro Spirit": 1,
    "Skeletons": 1,
    "Ice Golem": 2,
    "Knight": 3,
    "Archers": 3,
    "Goblins": 2,
    "Spear Goblins": 2,
    "Minions": 3,
    "Minion Horde": 5,
    "Skeleton Army": 3,
    "Goblin Gang": 3,
    "Barbarians": 5,
    "Elite Barbarians": 6,
    "Royal Recruits": 7,
    "Bats": 2,
    "Guards": 3,
    "Princess": 3,
    "Miner": 3,
    "Mega Knight": 7,
    "P.E.K.K.A": 7,
    "Giant": 5,
    "Royal Giant": 6,
    "Golem": 8,
    "Lava Hound": 7,
    "Balloon": 5,
    "Hog Rider": 4,
    "Battle Ram": 4,
    "Ram Rider": 5,
    "Musketeer": 4,
    "Wizard": 5,
    "Witch": 5,
    "Baby Dragon": 4,
    "Valkyrie": 4,
    "Mini P.E.K.K.A": 4,
    "Prince": 5,
    "Dark Prince": 4,
    "Lumberjack": 4,
    "Sparky": 6,
    "Inferno Dragon": 4,
    "Electro Dragon": 5,
    "Mother Witch": 4,
    "Executioner": 5,
    "Bowler": 5,
    "Cannon Cart": 5,
    "Mega Minion": 3,
    "Dart Goblin": 3,
    "Flying Machine": 4,
    "Hunter": 4,
    "Zappies": 4,
    "Rascals": 5,
    "Cannon": 3,
    "Tesla": 4,
    "Inferno Tower": 5,
    "Bomb Tower": 4,
    "X-Bow": 6,
    "Mortar": 4,
    "Elixir Collector": 6,
    "Goblin Hut": 5,
    "Barbarian Hut": 7,
    "Tombstone": 3,
    "Furnace": 4,
    "Goblin Drill": 4,
    "Goblin Barrel": 3,
    "Graveyard": 5,
    "Skeleton Barrel": 3,
    "Wall Breakers": 2,
    "Royal Hogs": 5,
    "Firecracker": 3,
    "Electro Giant": 8,
    "Electro Wizard": 4,
    "Night Witch": 4,
    "Bandit": 3,
    "Fisherman": 3,
    "Magic Archer": 4,
    "Royal Ghost": 3,
    "Ice Wizard": 3,
}
