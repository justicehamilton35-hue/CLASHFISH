# Replay Analysis Guide

ClashFish now supports **visual replay analysis** using computer vision to detect cards frame-by-frame and provide Stockfish-style move evaluations!

## Features

### 🎥 Video Analysis
- Upload full match replays (.mp4, .mov, .avi)
- Frame-by-frame card detection using Roboflow models
- Automatic card play extraction
- Elixir usage tracking over time
- Move-by-move timeline analysis

### 📸 Screenshot Analysis
- Quick analysis of single moments
- Detect all visible cards with confidence scores
- Position tracking for strategic insights

### 🎯 Move Evaluation (Like Chess.com)
- **Brilliant (!!)**  - Outstanding plays that gain significant advantage
- **Great (!)**      - Strong moves with clear benefit
- **Good**           - Solid standard plays
- **Inaccuracy (?!)** - Questionable timing or positioning
- **Mistake (?)**    - Clear errors losing advantage
- **Blunder (??)**   - Critical mistakes that lose the game

### 📊 Analysis Metrics
- **Accuracy Score**: Overall performance percentage
- **Move Breakdown**: Count of each move quality
- **Critical Moments**: Turning points and key plays
- **Strategic Insights**: AI-generated advice

## Installation

### 1. Install Computer Vision Dependencies

```bash
pip install inference opencv-python pillow
```

Or for Windows (if you have C compiler issues):
```bash
pip install inference opencv-python-headless pillow
```

### 2. Get Roboflow API Key (Optional)

For best results, sign up at [Roboflow](https://roboflow.com/) and get an API key. Free tier available!

**Available Models:**
- **vision_bot** - 1,187 images, YOLOv8n (default)
- **clashroyale** - 972 images, official dataset
- **angelfire** - 1,792 images, comprehensive model

## Usage

### Via Web Interface

1. Visit http://localhost:8000
2. Scroll to "Replay Analysis" section
3. Click "Choose File" and select your replay video or screenshot
4. Click "Analyze Replay"
5. View move-by-move analysis with evaluations

### Via API

#### Upload Video/Image

```bash
curl -X POST "http://localhost:8000/api/v1/replay/upload" \
  -F "file=@my_replay.mp4" \
  -F "roboflow_api_key=your_key_here"
```

#### Quick Screenshot Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/replay/analyze-image" \
  -F "file=@screenshot.png"
```

#### Check Capabilities

```bash
curl http://localhost:8000/api/v1/replay/capabilities
```

## Example Response

```json
{
  "success": true,
  "file_type": "video",
  "card_plays": [
    {
      "timestamp": 2.5,
      "card": "Hog Rider",
      "position": {"x": 0.5, "y": 0.7},
      "confidence": 0.95
    },
    ...
  ],
  "analysis": {
    "move_evaluations": [
      {
        "move_number": 1,
        "card": "Hog Rider",
        "quality": {
          "rating": "great",
          "symbol": "!",
          "score": 1.2
        },
        "context": "Opening move",
        "timestamp": 2.5
      },
      ...
    ],
    "accuracy": {
      "overall": 87.5,
      "move_breakdown": {
        "brilliant": 2,
        "great": 5,
        "good": 8,
        "inaccuracy": 2,
        "mistake": 1,
        "blunder": 0
      }
    },
    "critical_moments": [
      {
        "move_number": 12,
        "type": "brilliant_move",
        "description": "Brilliant play: Fireball !!",
        "timestamp": 45.2
      }
    ],
    "insights": [
      "Strong overall performance with consistent good moves",
      "Excellent plays at moves 3, 7, 12"
    ],
    "summary": "You won with 87.5% accuracy. Played 18 moves including 2 brilliant plays."
  }
}
```

## How It Works

### 1. Card Detection
- Uses pre-trained Roboflow models specialized for Clash Royale
- YOLOv8n architecture for fast, accurate detection
- Detects cards in spectator view or gameplay
- Tracks position, confidence, and timing

### 2. Move Extraction
- Processes video frame-by-frame
- Identifies new card plays (filters duplicates)
- Tracks timestamps and positions
- Alternates between player and opponent

### 3. Evaluation Engine
- Calculates move quality scores
- Considers timing, position, and context
- Identifies counters and synergies
- Compares to optimal plays

### 4. Strategic Analysis
- Generates accuracy percentage
- Finds critical moments (brilliant/blunders)
- Produces actionable insights
- Provides game summary

## Best Practices

### Recording Replays

1. **Quality**: 720p or higher recommended
2. **Format**: MP4 works best
3. **Duration**: Full matches (3-5 minutes)
4. **View**: Spectator mode or standard gameplay
5. **Clarity**: Ensure cards are clearly visible

### Uploading

- Maximum file size: 100MB
- Longer videos take more time to process
- Screenshots are faster but less detailed
- Use API key for better accuracy

### Interpreting Results

- **80%+ accuracy** = Excellent performance
- **70-80% accuracy** = Good, room for improvement
- **Below 70%** = Review mistakes and blunders
- Focus on critical moments for biggest gains

## Limitations

- Cannot detect cards in hand (only played cards)
- Requires clear visibility of cards
- May miss cards in fast sequences
- Elixir tracking is estimated
- No audio analysis

## Troubleshooting

### "Computer vision features not available"
Install dependencies: `pip install inference opencv-python pillow`

### "No cards detected"
- Check video quality
- Ensure cards are visible
- Try spectator view replays
- Adjust confidence threshold

### Slow processing
- Use screenshot for quick analysis
- Reduce video length
- Increase frame_interval parameter

### Low accuracy
- Get Roboflow API key for better models
- Use higher quality recordings
- Ensure good lighting in recordings

## Future Enhancements

- [ ] Real-time live analysis
- [ ] Multi-player detection (2v2 mode)
- [ ] Tower HP tracking
- [ ] Elixir bar detection
- [ ] Card level detection
- [ ] Audio analysis for spell sounds
- [ ] Win probability curve
- [ ] Opening book analysis
- [ ] Endgame evaluation

## Resources

- [Roboflow Universe - Clash Royale Models](https://universe.roboflow.com/)
- [Vision Bot Model](https://universe.roboflow.com/vision-bot/clash-royale-card-detection-ylzsc)
- [Official Dataset](https://universe.roboflow.com/clashroyale/clash-royale-of3d3)
- [Roboflow Inference Docs](https://inference.roboflow.com/)

## Contributing

Have a better Clash Royale detection model? Improved evaluation algorithm? Submit a PR!

1. Train your model on Roboflow
2. Add model ID to `backend/services/card_detector.py`
3. Update documentation
4. Share results!

---

**Note**: Replay analysis requires additional dependencies not included in base installation. Install with:
```bash
pip install inference opencv-python pillow
```
