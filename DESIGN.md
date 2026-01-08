# Clash Royale Game Analyzer - Complete System Design

## Executive Summary

This document outlines the architecture for **ClashFish** - a comprehensive Clash Royale game analyzer that provides:
- Real-time win probability calculation (0-100% throughout the match)
- Move evaluation (mistakes, blunders, great moves, brilliant plays)
- Deck classification and meta analysis
- Strategic recommendations based on game state
- 3D replay visualization with troop interactions
- AI-powered narrative commentary on key moments
- Historical performance analytics and player statistics

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Data Model & Requirements](#2-data-model--requirements)
3. [Win Probability Model](#3-win-probability-model)
4. [Move Evaluation System](#4-move-evaluation-system)
5. [Deck Classification Engine](#5-deck-classification-engine)
6. [Strategy Suggestion System](#6-strategy-suggestion-system)
7. [3D Replay Viewer](#7-3d-replay-viewer)
8. [AI Narrative Analysis](#8-ai-narrative-analysis)
9. [Data Pipeline](#9-data-pipeline)
10. [API Design](#10-api-design)
11. [Example Output](#11-example-output)
12. [Implementation Roadmap](#12-implementation-roadmap)

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │  Web Dashboard   │  │  3D Replay       │  │  Mobile App   │ │
│  │  (React/Next.js) │  │  (Three.js/WebGL)│  │  (Optional)   │ │
│  └──────────────────┘  └──────────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↕ REST/GraphQL/WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                         API GATEWAY                              │
│  (Load Balancing, Rate Limiting, Authentication, Caching)       │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      MICROSERVICES LAYER                         │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Ingestion  │  │   Analysis   │  │   Replay     │          │
│  │   Service    │  │   Engine     │  │   Service    │          │
│  │              │  │              │  │              │          │
│  │ - RoyaleAPI  │  │ - Win Prob   │  │ - 3D Data    │          │
│  │ - Data Pull  │  │ - Move Eval  │  │ - Timeline   │          │
│  │ - Validation │  │ - Deck Class │  │ - Events     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Strategy    │  │  Commentary  │  │  Statistics  │          │
│  │  Service     │  │  Service     │  │  Service     │          │
│  │              │  │              │  │              │          │
│  │ - Advice     │  │ - AI/LLM     │  │ - Aggregates │          │
│  │ - Counter    │  │ - Narrative  │  │ - Rankings   │          │
│  │ - Timing     │  │ - Insights   │  │ - Trends     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      ML/AI MODEL LAYER                           │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Win Prob     │  │ Move Quality │  │ Deck Type    │          │
│  │ Model        │  │ Classifier   │  │ Classifier   │          │
│  │ (LSTM/GRU)   │  │ (XGBoost)    │  │ (Random Forest│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Elixir Flow  │  │ Positioning  │  │ LLM Service  │          │
│  │ Predictor    │  │ Analyzer     │  │ (GPT/Claude) │          │
│  │ (Regression) │  │ (CV/Rules)   │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                 │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  PostgreSQL  │  │    Redis     │  │   MongoDB    │          │
│  │              │  │              │  │              │          │
│  │ - Players    │  │ - Cache      │  │ - Raw Battles│          │
│  │ - Matches    │  │ - Sessions   │  │ - Logs       │          │
│  │ - Analysis   │  │ - Real-time  │  │ - Unstructured│         │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  ClickHouse  │  │   S3/Blob    │  │   Vector DB  │          │
│  │              │  │              │  │  (Pinecone)  │          │
│  │ - Time Series│  │ - Replays    │  │ - Embeddings │          │
│  │ - Analytics  │  │ - 3D Assets  │  │ - Similarity │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  RoyaleAPI   │  │  Monitoring  │  │  CDN         │          │
│  │  (Data Src)  │  │  (DataDog)   │  │  (CloudFlare)│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack

#### Frontend
- **Web Dashboard**: React/Next.js, TypeScript, TailwindCSS
- **3D Viewer**: Three.js, React Three Fiber (R3F), WebGL
- **State Management**: Zustand or Redux Toolkit
- **Data Visualization**: D3.js, Recharts, Victory
- **Real-time Updates**: Socket.io client

#### Backend
- **API Gateway**: Kong or AWS API Gateway
- **Services**: Node.js (Express/Fastify) or Python (FastAPI)
- **Message Queue**: RabbitMQ or Apache Kafka
- **Task Queue**: Celery (Python) or Bull (Node.js)
- **WebSocket**: Socket.io

#### ML/AI
- **Training**: Python, PyTorch, scikit-learn, XGBoost
- **Serving**: TensorFlow Serving, TorchServe, or MLflow
- **Feature Store**: Feast or Tecton
- **LLM Integration**: OpenAI API / Anthropic Claude API

#### Data Storage
- **Relational**: PostgreSQL 14+ with TimescaleDB extension
- **Cache**: Redis 7+
- **Document**: MongoDB 6+
- **Analytics**: ClickHouse
- **Object Storage**: AWS S3 or MinIO
- **Vector Search**: Pinecone or Qdrant

#### Infrastructure
- **Container Orchestration**: Kubernetes (EKS/GKE/AKS)
- **CI/CD**: GitHub Actions, ArgoCD
- **Monitoring**: Prometheus, Grafana, DataDog
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

---

## 2. Data Model & Requirements

### 2.1 Core Data Entities

#### Player
```
Player {
  player_id: string (primary key, from RoyaleAPI)
  player_tag: string (unique, e.g., "#V2QUUQVU8")
  player_name: string
  current_trophies: integer
  best_trophies: integer
  level: integer
  clan_id: string (nullable)
  clan_name: string (nullable)
  wins: integer
  losses: integer
  three_crown_wins: integer
  cards_discovered: integer
  favorite_card: string
  profile_data: jsonb
  created_at: timestamp
  updated_at: timestamp
}
```

#### Match
```
Match {
  match_id: string (primary key)
  battle_time: timestamp
  game_mode: enum (1v1, 2v2, challenge, tournament, etc.)
  match_type: string (PvP, friendly, etc.)
  arena: string
  duration_seconds: integer

  player1_id: string (foreign key)
  player1_deck: jsonb (array of 8 cards)
  player1_crowns: integer (0-3)
  player1_king_tower_hp: integer
  player1_princess_towers_hp: jsonb
  player1_elixir_leaked: float
  player1_result: enum (win, loss, draw)

  player2_id: string (foreign key)
  player2_deck: jsonb
  player2_crowns: integer
  player2_king_tower_hp: integer
  player2_princess_towers_hp: jsonb
  player2_elixir_leaked: float
  player2_result: enum (win, loss, draw)

  replay_available: boolean
  replay_url: string (nullable)
  raw_data: jsonb
  processed: boolean
  created_at: timestamp
}
```

#### MatchEvent
```
MatchEvent {
  event_id: uuid (primary key)
  match_id: string (foreign key)
  player_id: string (which player made the move)
  timestamp_ms: integer (milliseconds from match start)
  event_type: enum (card_play, tower_damage, tower_destroy, spell_cast, troop_death, elixir_milestone)

  card_id: string (nullable)
  card_level: integer (nullable)
  position_x: float (0-18, arena coordinates)
  position_y: float (0-32, arena coordinates)
  lane: enum (left, center, right, nullable)
  elixir_cost: integer
  elixir_available: float (at time of play)

  target_type: enum (tower, troop, area, nullable)
  damage_dealt: integer (nullable)
  troops_spawned: integer (nullable)

  context: jsonb (additional event data)
  created_at: timestamp
}
```

#### MatchAnalysis
```
MatchAnalysis {
  analysis_id: uuid (primary key)
  match_id: string (foreign key, unique)
  player_id: string (which player's perspective)

  final_win_probability: float (0-1)
  win_probability_curve: jsonb (array of {timestamp_ms, probability})

  deck_archetype: string (e.g., "Hog Cycle", "Golem Beatdown")
  opponent_deck_archetype: string

  total_moves: integer
  mistakes: integer
  blunders: integer
  great_moves: integer
  brilliant_moves: integer

  average_move_quality: float (-3 to +3)
  elixir_efficiency: float (0-100)
  cycle_speed: float (avg seconds per card cycle)
  pressure_score: float (offensive pressure rating)
  defense_rating: float (defensive effectiveness)

  key_moments: jsonb (array of critical events)
  move_evaluations: jsonb (array of {event_id, quality, category, explanation})

  strategy_followed: string
  recommended_strategy: string
  strategic_mistakes: jsonb

  commentary: text (AI-generated narrative)
  improvement_tips: jsonb (array of suggestions)

  computed_at: timestamp
  model_version: string
}
```

#### DeckArchetype
```
DeckArchetype {
  archetype_id: string (primary key, e.g., "hog_cycle")
  archetype_name: string (e.g., "2.6 Hog Cycle")
  category: enum (beatdown, siege, control, cycle, bait, bridge_spam)
  description: text

  signature_cards: jsonb (array of card IDs)
  common_cards: jsonb (array of card IDs with frequency)

  avg_elixir_cost: float
  playstyle: text
  win_conditions: jsonb (array of card IDs)

  strengths: jsonb (array of strings)
  weaknesses: jsonb (array of strings)
  counters: jsonb (array of archetype_ids)
  countered_by: jsonb (array of archetype_ids)

  popularity: float (0-100)
  win_rate: float (0-100)
  meta_tier: enum (S, A, B, C, D)

  created_at: timestamp
  updated_at: timestamp
}
```

#### Card
```
Card {
  card_id: string (primary key, e.g., "knight")
  card_name: string
  rarity: enum (common, rare, epic, legendary, champion)
  type: enum (troop, building, spell)
  elixir_cost: integer

  max_level: integer
  base_stats: jsonb (hp, damage, speed, range, etc.)

  description: text
  icon_url: string
  model_3d_url: string (nullable)

  synergies: jsonb (array of card_ids that work well together)
  counters: jsonb (array of card_ids that counter this card)
  countered_by: jsonb (array of card_ids)

  usage_rate: float (0-100)
  win_rate: float (0-100)

  created_at: timestamp
  updated_at: timestamp
}
```

### 2.2 Time-Series Data (ClickHouse)

#### WinProbabilityTimeSeries
```
{
  match_id: string
  player_id: string
  timestamp_ms: integer
  win_probability: float
  elixir_advantage: float
  tower_hp_advantage: float
  crown_difference: integer
  pressure_score: float
  event_id: string (nullable, if triggered by event)
  computed_at: timestamp
}
```

#### PlayerPerformanceMetrics
```
{
  player_id: string
  date: date
  hour: integer (0-23)

  matches_played: integer
  wins: integer
  losses: integer
  win_rate: float

  avg_win_probability: float
  avg_elixir_efficiency: float
  avg_move_quality: float

  mistakes_per_game: float
  blunders_per_game: float
  great_moves_per_game: float

  most_played_deck: string
  most_successful_deck: string

  timestamp: timestamp
}
```

### 2.3 Data Requirements from RoyaleAPI

To build this analyzer, we need the following data from each battle:

1. **Match Metadata**
   - Battle time
   - Game mode (1v1, 2v2, challenge, etc.)
   - Arena/league
   - Match duration
   - Result (win/loss/draw)

2. **Player Information**
   - Player tags and names
   - Trophy levels
   - Card levels
   - Clan information

3. **Deck Composition**
   - 8 cards per player
   - Card levels
   - Average elixir cost

4. **Match Outcome**
   - Crown count
   - Tower HP remaining
   - Damage dealt/received

5. **Event Stream (CRITICAL)**
   - **Timestamp** for each action
   - **Card played** (which card)
   - **Position** (x, y coordinates on arena)
   - **Elixir state** (current elixir at time of play)
   - **Tower damage events**
   - **Troop deaths**
   - **Spell impacts**

**Note**: RoyaleAPI may not provide detailed event streams by default. If not available:
- Option A: Use RoyaleBattleAPI or direct game client integration
- Option B: Estimate events from replay analysis (if replay files are available)
- Option C: Build a computer vision system to extract events from replay videos

---

## 3. Win Probability Model

### 3.1 Model Architecture

**Type**: Sequence-to-sequence LSTM/GRU with attention mechanism

**Input Features** (per time step):
- **Time-based**:
  - Seconds elapsed (0-300+)
  - Game phase: early (0-60s), mid (60-180s), late (180s+), overtime
  - Time remaining in sudden death

- **Elixir State**:
  - Player elixir (0-10)
  - Opponent elixir (0-10, estimated)
  - Elixir advantage (-10 to +10)
  - Elixir generation rate

- **Tower Health**:
  - Player king tower HP (0-100%)
  - Player left princess tower HP (0-100%)
  - Player right princess tower HP (0-100%)
  - Opponent king tower HP (0-100%)
  - Opponent left princess tower HP (0-100%)
  - Opponent right princess tower HP (0-100%)
  - Tower HP differential

- **Crown State**:
  - Player crowns (0-3)
  - Opponent crowns (0-3)
  - Crown differential (-3 to +3)

- **Card State**:
  - Cards in hand (4 one-hot encoded vectors)
  - Next card in cycle (one-hot)
  - Cards remaining in deck cycle
  - Opponent cards played so far (cumulative one-hot)
  - Opponent cards not yet seen

- **Deck Characteristics**:
  - Average elixir cost
  - Deck archetype (one-hot encoded)
  - Opponent deck archetype (one-hot, updated as revealed)
  - Win condition cards played/remaining

- **Positional State**:
  - Number of player troops on field
  - Number of opponent troops on field
  - Player buildings active
  - Opponent buildings active
  - Lane pressure: left (0-1), center (0-1), right (0-1)

- **Recent Actions** (last 5 seconds):
  - Cards played by player (sequence)
  - Cards played by opponent (sequence)
  - Damage dealt
  - Damage received
  - Elixir spent

- **Meta Context**:
  - Player trophy level
  - Opponent trophy level
  - Card level advantage (-5 to +5 avg)

**Architecture**:
```
Input Layer (feature vector at time t)
    ↓
Embedding Layer (for categorical features)
    ↓
LSTM Layer 1 (256 units, return sequences)
    ↓
Dropout (0.3)
    ↓
LSTM Layer 2 (128 units, return sequences)
    ↓
Attention Layer (temporal attention over sequence)
    ↓
Dense Layer (64 units, ReLU)
    ↓
Dropout (0.2)
    ↓
Dense Layer (32 units, ReLU)
    ↓
Output Layer (1 unit, Sigmoid) → Win Probability (0-1)
```

### 3.2 Training Strategy

**Dataset Construction**:
- Collect 1M+ matches from RoyaleAPI
- Sequence data: sample game state every 1-5 seconds
- Label: final outcome (0 = loss, 1 = win)
- Create sequences of variable length (time-series)

**Loss Function**:
- Binary cross-entropy with temporal weighting
- Early game errors weighted less (uncertainty is natural)
- Late game predictions weighted more (should be accurate)

**Training Process**:
1. **Phase 1**: Train on complete matches (final outcome)
2. **Phase 2**: Fine-tune with intermediate feedback (e.g., if a player loses after leading, penalize overconfident predictions)
3. **Phase 3**: Calibration - adjust probabilities to match actual win rates at each probability bucket

**Evaluation Metrics**:
- Log loss (primary)
- Calibration plot (predicted prob vs actual win rate)
- ROC-AUC
- Brier score
- Accuracy at key thresholds (50%, 75%, 90%)

**Update Frequency**:
- Retrain monthly with new meta data
- Online learning for minor adjustments

### 3.3 Real-time Probability Updates

**Update Triggers**:
- Every card play
- Every tower damage event
- Every 5 seconds (even if no action)
- Every troop death
- Elixir advantage changes > 2

**Calculation Speed**:
- Target: < 50ms per update
- Use model serving infrastructure (TensorFlow Serving)
- Batch predictions when possible

**Confidence Intervals**:
- Provide uncertainty estimates (5%-95% confidence range)
- Higher uncertainty early game, lower late game

---

## 4. Move Evaluation System

### 4.1 Move Quality Categories

| Category | Quality Score | Description | Criteria |
|----------|--------------|-------------|----------|
| **Brilliant!!** | +3.0 to +4.0 | Exceptional play that significantly shifts win probability | Win prob increase > 8% |
| **Great Move** | +1.5 to +3.0 | Strong play that improves position meaningfully | Win prob increase 4-8% |
| **Good** | +0.5 to +1.5 | Solid play, correct decision | Win prob increase 1-4% |
| **Neutral** | -0.5 to +0.5 | Acceptable play, neutral impact | Win prob change -1% to +1% |
| **Inaccuracy** | -1.5 to -0.5 | Suboptimal play, minor negative impact | Win prob decrease 1-3% |
| **Mistake** | -3.0 to -1.5 | Clear error that worsens position | Win prob decrease 3-6% |
| **Blunder** | -4.0 to -3.0 | Major error with significant negative impact | Win prob decrease > 6% |

### 4.2 Move Evaluation Algorithm

**Step 1: Calculate Actual Impact**
- Win probability before move: P_before
- Win probability after move: P_after
- Actual impact: ΔP_actual = P_after - P_before

**Step 2: Calculate Expected Impact**
- Run simulation/model with alternative moves
- For each alternative card play at that moment:
  - Simulate game state after that move
  - Calculate win probability P_alternative
- Best alternative: P_best = max(P_alternative for all alternatives)

**Step 3: Evaluate Quality**
- Expected impact: ΔP_expected = P_best - P_before
- Quality score: ΔP_actual - ΔP_expected
- If actual move was best: quality = ΔP_actual
- If alternative was better: quality = ΔP_actual - ΔP_best (negative)

**Step 4: Classify Move**
- Map quality score to category (see table above)

### 4.3 Alternative Move Analysis

For each move evaluation, we need to consider:

**Alternative Cards** (3 other cards in hand):
- What if player played card A instead?
- What if player played card B at different position?
- What if player cycled a cheap card?

**Alternative Timing**:
- What if player waited 2 seconds (more elixir)?
- What if player played immediately vs delayed?

**Alternative Positioning**:
- What if card was placed in different lane?
- What if card was placed defensively vs offensively?
- What if card was placed to kite vs tank?

**Complexity Challenge**:
- Evaluating all alternatives is computationally expensive
- **Solution**: Use a heuristic search + neural network
  1. Pre-filter obviously bad moves (e.g., spell on empty lane)
  2. Evaluate top 5-10 plausible alternatives with win prob model
  3. Use a fast "move quality predictor" model (see below)

### 4.4 Move Quality Predictor Model

**Type**: XGBoost Classifier

**Input Features**:
- All game state features (same as win prob model)
- Proposed move: card_id, position_x, position_y, timing
- Context: what opponent just played, current lane pressure
- Tactical features:
  - Is this a counter to opponent's last play?
  - Elixir trade potential
  - Will this card reach tower?
  - Does this defend against active threats?
  - Cycle efficiency (does this card advance win condition?)

**Output**:
- Quality score (-4 to +4)
- Confidence (0-1)
- Move type classification: defensive, offensive, cycle, spell, support

**Training**:
- Use historical matches where we know:
  - Actual move played
  - Actual win probability change
  - Final outcome
- Label moves based on win probability delta
- Train XGBoost to predict quality score

**Advantages**:
- Fast inference (< 10ms)
- Can evaluate many alternative moves quickly
- Can be used to suggest best moves

---

## 5. Deck Classification Engine

### 5.1 Deck Archetypes

**Primary Categories**:

1. **Beatdown**: Heavy tanks (Golem, Giant, Lava Hound) with support
   - Playstyle: Build large pushes, tank for damage dealers
   - Examples: Golem Beatdown, Giant Double Prince, Lava Hound Balloon

2. **Control**: Defensive decks with strong counters and spells
   - Playstyle: Defend efficiently, counter-push, spell chip damage
   - Examples: Pekka BS Control, Mega Knight Control

3. **Siege**: Win conditions that attack from own side (X-Bow, Mortar)
   - Playstyle: Lock onto tower from distance, defend the siege building
   - Examples: X-Bow Cycle, Mortar Cycle

4. **Cycle**: Low-cost cards (avg < 3.0 elixir), fast cycling
   - Playstyle: Outcycle opponent's counters, constant pressure
   - Examples: 2.6 Hog Cycle, 2.9 Miner Cycle, 2.8 Hog EQ

5. **Bait**: Multiple cards that bait out same counter
   - Playstyle: Force opponent to waste spell, then punish
   - Examples: Log Bait, Goblin Drill Bait, Skeleton Barrel Bait

6. **Bridge Spam**: Fast, aggressive units at bridge
   - Playstyle: Immediate pressure, deny elixir trades
   - Examples: Pekka Bridge Spam, Bandit Bridge Spam, Royal Ghost

7. **Graveyard**: Graveyard as primary win condition
   - Playstyle: Tank for Graveyard, spell support
   - Examples: Graveyard Freeze, Graveyard Poison

8. **Miner Chip**: Miner + cycle cards for consistent chip damage
   - Playstyle: Constant chip damage, spell cycling, defensive play

### 5.2 Classification Model

**Type**: Ensemble of Random Forest + Neural Network

**Features**:
- Card composition (8 cards, one-hot encoded)
- Average elixir cost
- Presence of signature cards
- Card synergy scores
- Win condition cards present
- Spell composition
- Building presence
- Cycle speed potential (count of 1-2 cost cards)

**Process**:
1. **Signature Matching**: Check for presence of archetype-defining cards
2. **Similarity Scoring**: Compare deck to known archetypes
3. **ML Classification**: Random Forest predicts archetype probabilities
4. **Rule-based Refinement**: Apply game knowledge rules
5. **Output**: Primary archetype + confidence + secondary archetype

**Example**:
```
Deck: Hog Rider, Musketeer, Ice Golem, Skeletons, Ice Spirit, Cannon, Fireball, Log
→ Classification: "2.6 Hog Cycle" (98% confidence)
→ Category: Cycle
→ Win Condition: Hog Rider
```

### 5.3 Meta Analysis

Track deck archetype popularity and performance:
- Win rates by archetype
- Usage rates over time
- Matchup win rates (archetype A vs archetype B)
- Counter relationships
- Meta shifts detection

Store in time-series database for trend analysis.

---

## 6. Strategy Suggestion System

### 6.1 Strategy Framework

**Components**:

1. **Matchup Database**: Pre-computed strategies for archetype vs archetype
2. **Game State Analyzer**: Real-time game state assessment
3. **Tactical Advisor**: Specific card play suggestions
4. **Strategic Advisor**: High-level game plan recommendations

### 6.2 Matchup Strategy Database

For each archetype pair, define:

```json
{
  "your_deck": "2.6 Hog Cycle",
  "opponent_deck": "Golem Beatdown",
  "matchup_rating": "unfavorable",
  "win_rate": 45,

  "overall_strategy": "Apply constant opposite-lane pressure when opponent plays Golem in back. Defend efficiently with Cannon + Musketeer. Spell cycle Fireball on tower late game.",

  "early_game": {
    "strategy": "Play passively, defend with minimal elixir, keep Cannon for Golem. Apply light pressure to prevent opponent from building big push.",
    "key_cards": ["Cannon", "Ice Golem", "Skeletons"],
    "avoid": "Don't overcommit on offense. Save Fireball for Night Witch."
  },

  "mid_game": {
    "strategy": "When opponent plays Golem in back, rush opposite lane with Hog + Ice Spirit. Force them to split elixir. Defend Golem push with Cannon + Musketeer + kiting.",
    "key_cards": ["Hog Rider", "Cannon", "Musketeer"],
    "timing": "Opposite lane pressure immediately after Golem is played"
  },

  "late_game": {
    "strategy": "If ahead, defend and spell cycle. If behind, apply aggressive dual-lane pressure. Defend Golem with Cannon center, kite support troops with Ice Golem.",
    "key_cards": ["Fireball", "Log", "Cannon"],
    "win_condition": "Spell cycle Fireball + Log on tower"
  },

  "key_interactions": [
    "Cannon + Ice Golem full counters Golem",
    "Musketeer kills Night Witch",
    "Fireball on Night Witch + Bats",
    "Ice Golem kites Baby Dragon"
  ],

  "card_timing": {
    "Hog Rider": "Opposite lane when opponent commits Golem in back (8+ elixir)",
    "Cannon": "Reactive placement 4 tiles from river, centered",
    "Fireball": "Night Witch + support troops, or spell cycle if winning"
  },

  "common_mistakes": [
    "Playing Hog Rider same lane as Golem push",
    "Using Fireball too early (save for Night Witch)",
    "Overdefending - minimize elixir spent on defense"
  ]
}
```

**Database Size**: ~100 archetypes × ~100 archetypes = 10,000 matchups

### 6.3 Real-time Strategy Updates

**During match analysis**, provide dynamic suggestions:

**Turn 1** (First 30 seconds):
```
Phase: Opening / Scouting
Recommended: Play Ice Spirit at bridge to cycle and scout opponent's first card
Avoid: Don't play Hog Rider blind - opponent may have building
Elixir: Start conservative, maintain 7+ elixir
```

**Turn 5** (Opponent plays Golem in back):
```
CRITICAL MOMENT: Opponent committed 8 elixir on Golem
✓ RECOMMENDED: Rush opposite lane with Hog Rider + Ice Spirit immediately
  Expected outcome: Force opponent to defend, prevent big push
  Win probability impact: +12% if executed now

✗ MISTAKE: Defending same lane or waiting
  This allows opponent to build unstoppable push
  Win probability impact: -8%
```

**Turn 12** (Player's move played):
```
Move played: Cannon (center placement)
Evaluation: ✓ Great Move (+2.5)
Reasoning: Perfect Cannon placement to pull Golem and activate King Tower.
Expected elixir trade: +4 elixir
Alternative: Playing Musketeer would have been overcommit (-1 elixir)
```

### 6.4 Strategic Mistake Detection

Detect and flag strategic errors:

1. **Wrong Lane Pressure**: Attacking same lane as opponent's heavy push
2. **Overcommitment**: Spending too much elixir on offense when defense is needed
3. **Spell Waste**: Using spell on low-value targets
4. **Poor Cycling**: Not cycling to get to key cards when needed
5. **Timing Errors**: Playing win condition when opponent has hard counter in rotation
6. **Elixir Leaks**: Staying at 10 elixir for extended periods
7. **Tower Trading**: Taking bad crown trades

---

## 7. 3D Replay Viewer

### 7.1 Overview

The 3D replay viewer visualizes the match from a bird's-eye view, showing:
- Arena terrain (grass, river, bridges)
- Towers (King, Princess × 2)
- Troops moving and attacking
- Spells landing with visual effects
- Health bars and elixir bars
- Timeline scrubber with annotations

### 7.2 Technology Choice

**Recommended: Three.js with React Three Fiber**

**Reasons**:
- Web-based, no installation required
- Excellent performance with WebGL
- Rich ecosystem (libraries for animations, physics)
- React integration for UI controls
- Mobile browser support

**Alternative: Unity WebGL**
- More powerful for complex graphics
- Larger bundle size
- Requires more resources

**For mobile apps**: Unity or Unreal Engine

### 7.3 Data Requirements

#### Arena Model
```json
{
  "arena_id": "arena_12",
  "arena_name": "Legendary Arena",
  "dimensions": {
    "width": 18,
    "height": 32,
    "units": "tiles"
  },
  "terrain": {
    "model_url": "/models/arena_12.glb",
    "texture_url": "/textures/arena_12_diffuse.png"
  },
  "towers": [
    {
      "id": "player_king",
      "type": "king_tower",
      "position": {"x": 9, "y": 2, "z": 0},
      "model_url": "/models/king_tower.glb"
    },
    {
      "id": "player_left_princess",
      "type": "princess_tower",
      "position": {"x": 3.5, "y": 5, "z": 0},
      "model_url": "/models/princess_tower.glb"
    },
    {
      "id": "player_right_princess",
      "type": "princess_tower",
      "position": {"x": 14.5, "y": 5, "z": 0},
      "model_url": "/models/princess_tower.glb"
    },
    // Opponent towers (mirrored)
  ]
}
```

#### Troop Models
For each card in game, we need:
```json
{
  "card_id": "knight",
  "model_url": "/models/troops/knight.glb",
  "animation_urls": {
    "idle": "/animations/knight_idle.glb",
    "walk": "/animations/knight_walk.glb",
    "attack": "/animations/knight_attack.glb",
    "death": "/animations/knight_death.glb"
  },
  "scale": 1.0,
  "hitbox_radius": 0.5,
  "visual_effects": {
    "spawn": "particle_spawn.json",
    "attack_impact": "particle_slash.json"
  }
}
```

#### Replay Event Stream
```json
{
  "match_id": "abc123",
  "duration_ms": 180000,
  "events": [
    {
      "event_id": "evt_001",
      "timestamp_ms": 1500,
      "type": "card_play",
      "player": "player1",
      "card_id": "knight",
      "card_level": 11,
      "position": {"x": 9, "y": 14},
      "elixir_spent": 3,
      "elixir_remaining": 7
    },
    {
      "event_id": "evt_002",
      "timestamp_ms": 1500,
      "type": "troop_spawn",
      "troop_id": "troop_001",
      "card_id": "knight",
      "position": {"x": 9, "y": 14},
      "owner": "player1",
      "hp": 1500,
      "target": null
    },
    {
      "event_id": "evt_003",
      "timestamp_ms": 2000,
      "type": "troop_move",
      "troop_id": "troop_001",
      "from": {"x": 9, "y": 14},
      "to": {"x": 9, "y": 15.5},
      "speed": 1.0,
      "animation": "walk"
    },
    {
      "event_id": "evt_004",
      "timestamp_ms": 3200,
      "type": "troop_attack",
      "troop_id": "troop_001",
      "target_id": "opponent_left_princess",
      "target_type": "tower",
      "damage": 150,
      "animation": "attack"
    },
    {
      "event_id": "evt_005",
      "timestamp_ms": 3200,
      "type": "tower_damage",
      "tower_id": "opponent_left_princess",
      "damage": 150,
      "hp_remaining": 2350,
      "visual_effect": "tower_hit"
    },
    {
      "event_id": "evt_006",
      "timestamp_ms": 5000,
      "type": "spell_cast",
      "player": "player2",
      "card_id": "fireball",
      "position": {"x": 9, "y": 14},
      "radius": 2.5,
      "damage": 572,
      "affected_troops": ["troop_001"],
      "visual_effect": "fireball_explosion"
    },
    {
      "event_id": "evt_007",
      "timestamp_ms": 5000,
      "type": "troop_death",
      "troop_id": "troop_001",
      "position": {"x": 9, "y": 15.5},
      "animation": "death",
      "visual_effect": "death_particle"
    }
  ]
}
```

### 7.4 Replay Construction Algorithm

**Challenge**: RoyaleAPI may not provide detailed positional data.

**Solution Approaches**:

#### Option A: Simulation-based Reconstruction
1. Use card play events (card, timestamp, position)
2. Simulate troop behavior based on game rules:
   - Movement: troops move toward nearest target (tower or enemy troop)
   - Speed: use known movement speeds from card data
   - Range: use known attack ranges
   - Targeting: implement targeting logic (ground, air, buildings, lowest HP)
3. Generate interpolated positions every 100ms
4. Output full event stream with positions

**Game Logic Simulation**:
```
For each time step (dt = 100ms):
  For each active troop:
    - Find valid targets within range
    - If target in range: attack (apply damage, play animation)
    - Else: move toward target (update position based on speed × dt)
    - Check if troop reached tower
    - Update HP if taking damage
    - Remove if HP <= 0

  For each spell:
    - Apply area damage at cast time
    - Remove troops in radius with HP <= 0

  For each building:
    - Lifetime countdown
    - Attack if troops in range

  Update elixir (regenerate over time)
  Update tower HP
```

#### Option B: Official Replay File Parsing
- If Clash Royale provides replay files (.replay format)
- Reverse-engineer or use existing parsers
- Extract full event stream with positions

#### Option C: Computer Vision from Replay Videos
- Download replay video from game
- Use object detection (YOLO, Detectron2) to identify troops
- Track positions frame-by-frame
- More complex, but accurate

**Recommended**: Start with Option A (simulation), refine with Option B if possible.

### 7.5 3D Viewer Implementation

#### Component Structure (React Three Fiber)

```jsx
<Canvas>
  <Scene>
    <Lighting />
    <ArenaModel />
    <Towers />
    <Troops replayEvents={events} currentTime={currentTime} />
    <Spells replayEvents={events} currentTime={currentTime} />
    <HealthBars />
    <ElixirBars />
    <Effects />
    <Camera />
  </Scene>
</Canvas>

<ReplayControls>
  <Timeline events={annotatedEvents} />
  <PlayPauseButton />
  <SpeedControl />
  <EventMarkers />
</ReplayControls>

<AnalysisOverlay>
  <WinProbabilityGraph currentTime={currentTime} />
  <MoveEvaluation currentTime={currentTime} />
  <ElixirAdvantage currentTime={currentTime} />
</AnalysisOverlay>
```

#### Animation System

**Interpolation**: Smooth movement between event positions
```javascript
// Linear interpolation for position
function interpolateTroopPosition(troop, currentTime) {
  const events = troop.movementEvents;
  const current = events.find(e => e.timestamp <= currentTime);
  const next = events.find(e => e.timestamp > currentTime);

  if (!next) return current.position;

  const t = (currentTime - current.timestamp) / (next.timestamp - current.timestamp);
  return {
    x: lerp(current.position.x, next.position.x, t),
    y: lerp(current.position.y, next.position.y, t)
  };
}
```

**Animation States**:
- Idle: when not moving
- Walk: when moving to target
- Attack: when attacking
- Death: when HP reaches 0
- Spawn: when first deployed

#### Performance Optimization

- **LOD (Level of Detail)**: Use lower-poly models when zoomed out
- **Instancing**: Reuse geometries for same troop types
- **Culling**: Don't render off-screen objects
- **Texture atlasing**: Combine textures to reduce draw calls
- **Animation sampling**: Lower frame rate for distant troops

#### Visual Effects

- **Card deployment**: Glowing circle at spawn position
- **Spell impacts**: Explosions, fire, lightning
- **Tower destruction**: Dramatic explosion, debris
- **Damage numbers**: Floating text showing damage dealt
- **Range indicators**: Circles showing attack/aggro ranges (toggle)

### 7.6 Timeline & Annotations

**Timeline Features**:
- Horizontal timeline showing match duration (0 - 6 minutes)
- Markers for key events:
  - Card plays (icons at exact timestamp)
  - Tower damage (red markers)
  - Crown destroyed (crown icons)
  - Mistakes/blunders (red flags)
  - Great moves (green stars)
- Win probability graph overlaid
- Hover to see event details
- Click to jump to that moment

**Event Annotations**:
```
[00:15] Knight placed by Player1
[00:18] ✓ Great Move: Perfect counter to opponent's Goblin Gang
[00:32] Fireball by Player2 → 572 damage to Knight
[00:45] ✗ Mistake: Overcommitted with Giant in back, elixir disadvantage
[01:20] 🏆 Crown! Left Princess Tower destroyed
[02:35] ⚠️ Critical Moment: Win probability swung from 35% → 68%
```

---

## 8. AI Narrative Analysis

### 8.1 Integration with LLMs

Use GPT-4, Claude Opus 4.5, or similar for generating:
- Match summaries
- Move explanations
- Strategic insights
- Player performance reports

### 8.2 Prompt Engineering

#### Match Commentary Prompt
```
You are a professional Clash Royale analyst providing commentary on a match replay.

Match Context:
- Player: {player_name} (Trophies: {trophies})
- Deck: {deck_archetype} - {card_list}
- Opponent: {opponent_name} (Trophies: {opponent_trophies})
- Opponent Deck: {opponent_archetype} - {opponent_card_list}
- Result: {result} ({player_crowns}-{opponent_crowns})
- Duration: {duration}

Key Statistics:
- Final win probability: {final_win_prob}%
- Move quality: {mistakes} mistakes, {blunders} blunders, {great_moves} great moves
- Elixir efficiency: {elixir_efficiency}%
- Deck matchup: {matchup_rating}

Critical Moments:
{critical_moments_json}

Move Evaluations:
{move_evaluations_json}

Please provide:

1. **Match Summary** (2-3 sentences): Overview of how the match played out, key turning points, final outcome.

2. **Opening Analysis**: How did each player start? Was the opening strategy appropriate for the matchup?

3. **Key Moments** (3-5 moments): Describe the most important plays that shaped the match. For each moment:
   - What happened (card played, position, timing)
   - Why it was significant (win probability change, strategic impact)
   - What the alternative could have been

4. **Mistakes & Blunders**: Explain the biggest errors made. What should the player have done instead?

5. **Strategic Assessment**:
   - Did the player follow the correct strategy for this matchup?
   - What was the game plan, and was it executed well?
   - How did elixir management affect the outcome?

6. **Improvement Recommendations** (3-5 specific tips): What should the player focus on improving?

Write in a professional but engaging tone, similar to chess.com analysis. Use specific card names and tactical terminology.
```

#### Move Explanation Prompt
```
Explain the following move in a Clash Royale match:

Game State (before move):
- Time: {timestamp}s
- Player Elixir: {elixir}
- Opponent Elixir: {opponent_elixir} (estimated)
- Crown Score: {player_crowns} - {opponent_crowns}
- Tower HP: Player {player_tower_hp}%, Opponent {opponent_tower_hp}%
- Win Probability: {win_prob_before}%

Move Played:
- Card: {card_name} (Level {level})
- Position: {position} ({lane} lane)
- Elixir Cost: {cost}

Result (after move):
- Win Probability: {win_prob_after}% (Δ{win_prob_change}%)
- Move Quality: {move_quality} ({quality_category})

Context:
- Opponent's last play: {opponent_last_card}
- Active troops on field: {troops_on_field}
- Deck archetype: {player_archetype} vs {opponent_archetype}

Alternative moves considered:
{alternatives_json}

Please explain in 2-3 sentences:
1. Why this move was strong/weak
2. What impact it had on the game
3. What alternative would have been better (if applicable)
```

### 8.3 Commentary Generation Pipeline

```
Match Data → Feature Extraction → Critical Moments Detection → LLM Prompt Construction → LLM API Call → Post-Processing → Store Commentary
```

**Critical Moments Detection**:
- Win probability swings > 10%
- Blunders and brilliant moves
- Crown destruction
- Overtime
- Elixir advantage > 5
- Successful/failed pushes

**Caching Strategy**:
- Cache commentary by (match_id, model_version)
- Regenerate if model updated or user requests

**Cost Optimization**:
- Use cheaper models for simple explanations
- Reserve GPT-4/Opus for full match commentary
- Batch process matches during off-peak

---

## 9. Data Pipeline

### 9.1 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA PIPELINE                               │
│                                                                   │
│  [1] Ingestion        [2] Validation     [3] Enrichment         │
│  ┌─────────────┐     ┌─────────────┐    ┌─────────────┐        │
│  │ RoyaleAPI   │────▶│ Schema      │───▶│ Deck Class  │        │
│  │ Polling     │     │ Validation  │    │ Card Data   │        │
│  │ Webhooks    │     │ Deduplication│   │ Meta Info   │        │
│  └─────────────┘     └─────────────┘    └─────────────┘        │
│         │                    │                   │               │
│         ▼                    ▼                   ▼               │
│  [4] Storage          [5] Processing     [6] Model Inference    │
│  ┌─────────────┐     ┌─────────────┐    ┌─────────────┐        │
│  │ Raw Match   │     │ Event       │───▶│ Win Prob    │        │
│  │ Data        │     │ Extraction  │    │ Calculation │        │
│  │ (MongoDB)   │     │ Simulation  │    │ Move Eval   │        │
│  └─────────────┘     └─────────────┘    └─────────────┘        │
│         │                    │                   │               │
│         ▼                    ▼                   ▼               │
│  [7] Analysis         [8] Commentary     [9] Storage            │
│  ┌─────────────┐     ┌─────────────┐    ┌─────────────┐        │
│  │ Aggregate   │     │ LLM         │───▶│ PostgreSQL  │        │
│  │ Statistics  │     │ Generation  │    │ ClickHouse  │        │
│  │ Trends      │     │ (OpenAI)    │    │ Redis Cache │        │
│  └─────────────┘     └─────────────┘    └─────────────┘        │
│         │                    │                   │               │
│         └────────────────────┴───────────────────┘               │
│                              ▼                                    │
│                      [10] API Layer                              │
│                      User Queries & Dashboard                    │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Detailed Pipeline Stages

#### Stage 1: Data Ingestion

**Sources**:
- RoyaleAPI REST API (polling every 5 minutes per player)
- RoyaleAPI Webhooks (if available, for real-time updates)
- User manual uploads (paste match URL or replay file)

**Ingestion Service**:
```python
# Pseudocode
class IngestionService:
    def poll_player_battles(player_tag):
        # Fetch latest battles from RoyaleAPI
        response = royale_api.get(f"/player/{player_tag}/battlelog")
        battles = response.json()

        for battle in battles:
            # Check if already processed
            if not exists(battle['battleTime']):
                queue.publish('raw_battles', battle)

    def handle_webhook(webhook_data):
        # Real-time push from RoyaleAPI
        queue.publish('raw_battles', webhook_data)
```

**Data Format** (from RoyaleAPI):
```json
{
  "type": "PvP",
  "battleTime": "20260108T120000.000Z",
  "isLadderTournament": false,
  "arena": {
    "id": 54000022,
    "name": "Legendary Arena"
  },
  "gameMode": {
    "id": 72000006,
    "name": "Ladder"
  },
  "deckSelection": "collection",
  "team": [
    {
      "tag": "#V2QUUQVU8",
      "name": "Player1",
      "startingTrophies": 5234,
      "crowns": 3,
      "kingTowerHitPoints": 4200,
      "princessTowersHitPoints": [0, 0],
      "cards": [
        {"name": "Hog Rider", "id": 26000009, "level": 11, "maxLevel": 14},
        // ... 7 more cards
      ]
    }
  ],
  "opponent": [
    {
      "tag": "#ABC123",
      "name": "Opponent",
      "startingTrophies": 5198,
      "crowns": 1,
      "kingTowerHitPoints": 2100,
      "princessTowersHitPoints": [0, 1450],
      "cards": [...]
    }
  ]
}
```

#### Stage 2: Validation & Deduplication

**Validation**:
- Check required fields present
- Validate data types
- Ensure card IDs exist in card database
- Check trophy counts reasonable
- Verify timestamp format

**Deduplication**:
- Generate match fingerprint: hash(player_tag + opponent_tag + battleTime)
- Check if match already processed
- If duplicate, skip or update if data changed

#### Stage 3: Enrichment

**Add metadata**:
- Classify decks (both player and opponent)
- Fetch player profile data (current stats)
- Add card metadata (rarity, type, cost)
- Calculate deck statistics (avg cost, card synergies)
- Determine meta relevance

**Output**: Enriched match object ready for analysis

#### Stage 4: Storage (Raw Data)

Store raw and enriched data in MongoDB:
```javascript
{
  _id: "match_abc123",
  match_id: "abc123",
  battleTime: ISODate("2026-01-08T12:00:00Z"),
  gameMode: "Ladder",
  arena: "Legendary Arena",

  player: { /* full player data */ },
  opponent: { /* full opponent data */ },

  enrichment: {
    player_deck_archetype: "2.6 Hog Cycle",
    opponent_deck_archetype: "Golem Beatdown",
    matchup_rating: "unfavorable",
    meta_relevance: 0.87
  },

  processed: false,
  ingested_at: ISODate("2026-01-08T12:05:00Z")
}
```

#### Stage 5: Event Extraction & Simulation

**Goal**: Generate detailed event stream from limited data

**Approach**:
1. Extract known events from RoyaleAPI (if available)
2. Simulate missing events using game logic
3. Generate time-series data (every 100ms)

**Simulation Logic**:
- Use final state (crowns, HP) as constraints
- Estimate card play timings (distribute across match duration)
- Simulate troop movements and interactions
- Calculate damage events
- Track elixir over time

**Output**: Detailed event stream (MatchEvent table)

#### Stage 6: Model Inference

**Win Probability Calculation**:
```python
# For each time step (every 1 second)
for t in range(0, match_duration_seconds):
    game_state = get_game_state_at_time(match_id, t)
    features = extract_features(game_state)
    win_prob = win_prob_model.predict(features)

    store_win_prob(match_id, t, win_prob)
```

**Move Evaluation**:
```python
# For each card play event
for event in card_play_events:
    # Get win prob before and after
    win_prob_before = get_win_prob(event.timestamp - 1)
    win_prob_after = get_win_prob(event.timestamp + 5)  # 5s after

    actual_impact = win_prob_after - win_prob_before

    # Evaluate alternatives
    alternatives = generate_alternative_moves(event)
    best_alternative = max(alternatives, key=lambda x: x.expected_win_prob)

    quality_score = actual_impact - best_alternative.expected_impact
    category = classify_move(quality_score)

    store_move_evaluation(event.event_id, quality_score, category)
```

**Batching**: Process in batches for efficiency (10-100 matches at once)

#### Stage 7: Aggregation & Statistics

Calculate player-level statistics:
```python
def compute_player_stats(player_id, time_period):
    matches = get_matches(player_id, time_period)

    stats = {
        'matches_played': len(matches),
        'wins': count_wins(matches),
        'win_rate': count_wins(matches) / len(matches),
        'avg_crowns': mean([m.crowns for m in matches]),

        'avg_win_probability': mean([m.final_win_prob for m in matches]),
        'avg_elixir_efficiency': mean([m.elixir_efficiency for m in matches]),

        'mistakes_per_game': mean([m.mistakes for m in matches]),
        'blunders_per_game': mean([m.blunders for m in matches]),
        'great_moves_per_game': mean([m.great_moves for m in matches]),

        'most_played_deck': mode([m.deck_archetype for m in matches]),
        'best_deck_archetype': get_best_performing_deck(matches),
        'worst_matchup': get_worst_matchup(matches)
    }

    store_player_stats(player_id, time_period, stats)
```

Store in ClickHouse for fast analytics queries.

#### Stage 8: AI Commentary Generation

```python
def generate_commentary(match_id):
    match = get_match(match_id)
    analysis = get_analysis(match_id)

    # Extract critical moments
    critical_moments = [
        event for event in match.events
        if abs(event.win_prob_change) > 0.10 or event.move_quality in ['blunder', 'brilliant']
    ]

    # Build prompt
    prompt = build_commentary_prompt(match, analysis, critical_moments)

    # Call LLM
    commentary = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    # Store
    store_commentary(match_id, commentary)
```

**Async Processing**: Queue commentary generation as background job

#### Stage 9: Final Storage

Store all analysis results:
- **PostgreSQL**: Structured analysis (MatchAnalysis table)
- **ClickHouse**: Time-series data (win probability, events)
- **Redis**: Cache frequently accessed analyses
- **S3**: Store replay data, 3D models

#### Stage 10: API Layer

Expose data via REST/GraphQL APIs for frontend consumption.

### 9.3 Scalability Considerations

**Throughput**:
- Target: 1000+ matches/hour
- Use horizontal scaling for microservices
- Distribute model inference across GPU instances
- Use message queues (Kafka) for async processing

**Storage**:
- Partition PostgreSQL by date
- Use ClickHouse for historical analytics (100M+ records)
- Archive old matches to cold storage (S3 Glacier)

**Caching**:
- Cache player profiles (5 min TTL)
- Cache deck archetypes (1 hour TTL)
- Cache match analyses (infinite TTL, invalidate on reprocess)

---

## 10. API Design

### 10.1 RESTful API Endpoints

#### Player Endpoints

```
GET /api/v1/players/{playerTag}
Response: Player profile with statistics

GET /api/v1/players/{playerTag}/matches
Query params: limit, offset, gameMode, dateFrom, dateTo
Response: List of matches for player

GET /api/v1/players/{playerTag}/statistics
Query params: period (day, week, month, all)
Response: Aggregated statistics
```

#### Match Endpoints

```
GET /api/v1/matches/{matchId}
Response: Full match data with basic info

GET /api/v1/matches/{matchId}/analysis
Query params: playerId (for perspective)
Response: Complete analysis (win prob, move evals, strategy)

GET /api/v1/matches/{matchId}/replay
Response: Event stream for 3D replay

GET /api/v1/matches/{matchId}/commentary
Response: AI-generated commentary
```

#### Analysis Endpoints

```
GET /api/v1/analysis/win-probability/{matchId}
Query params: playerId, resolution (1s, 5s, 10s)
Response: Time-series of win probability

GET /api/v1/analysis/moves/{matchId}
Response: All moves with evaluations

GET /api/v1/analysis/timeline/{matchId}
Response: Annotated timeline of events
```

#### Search & Discovery

```
GET /api/v1/search/players
Query params: name, minTrophies, maxTrophies
Response: List of players

GET /api/v1/search/matches
Query params: deckArchetype, opponentArchetype, minWinProb, dateFrom
Response: List of matches matching criteria

GET /api/v1/decks/archetypes
Response: List of all deck archetypes with metadata

GET /api/v1/decks/archetypes/{archetypeId}/matchups
Response: Matchup table for this archetype
```

### 10.2 GraphQL Schema

```graphql
type Player {
  playerTag: String!
  playerName: String!
  currentTrophies: Int!
  wins: Int!
  losses: Int!
  winRate: Float!
  statistics(period: TimePeriod!): PlayerStatistics!
  matches(limit: Int, offset: Int): [Match!]!
  favoriteCard: Card
}

type Match {
  matchId: ID!
  battleTime: DateTime!
  gameMode: String!
  duration: Int!

  player: MatchPlayer!
  opponent: MatchPlayer!

  analysis(playerId: String!): MatchAnalysis
  replay: ReplayData
  commentary: Commentary
}

type MatchPlayer {
  player: Player!
  deck: [Card!]!
  crowns: Int!
  kingTowerHP: Int!
  result: MatchResult!
}

type MatchAnalysis {
  finalWinProbability: Float!
  winProbabilityCurve: [WinProbPoint!]!

  deckArchetype: DeckArchetype!
  opponentDeckArchetype: DeckArchetype!

  totalMoves: Int!
  mistakes: Int!
  blunders: Int!
  greatMoves: Int!

  moveEvaluations: [MoveEvaluation!]!
  keyMoments: [KeyMoment!]!
  strategyAdvice: StrategyAdvice!
}

type WinProbPoint {
  timestampMs: Int!
  probability: Float!
  eventId: String
}

type MoveEvaluation {
  eventId: ID!
  timestampMs: Int!
  card: Card!
  position: Position!

  qualityScore: Float!
  category: MoveCategory!
  explanation: String!

  winProbBefore: Float!
  winProbAfter: Float!
  winProbChange: Float!

  alternatives: [AlternativeMove!]
}

type AlternativeMove {
  card: Card!
  position: Position
  expectedWinProb: Float!
  explanation: String!
}

enum MoveCategory {
  BRILLIANT
  GREAT_MOVE
  GOOD
  NEUTRAL
  INACCURACY
  MISTAKE
  BLUNDER
}

type DeckArchetype {
  archetypeId: ID!
  name: String!
  category: String!
  signatureCards: [Card!]!
  avgElixirCost: Float!
  winRate: Float!
  popularity: Float!

  matchups: [Matchup!]!
}

type Matchup {
  opponentArchetype: DeckArchetype!
  winRate: Float!
  rating: String!
  strategy: StrategyAdvice!
}

type StrategyAdvice {
  overallStrategy: String!
  earlyGame: String!
  midGame: String!
  lateGame: String!
  keyInteractions: [String!]!
  commonMistakes: [String!]!
}

type Query {
  player(playerTag: String!): Player
  match(matchId: ID!): Match
  searchPlayers(name: String, minTrophies: Int): [Player!]!
  deckArchetypes: [DeckArchetype!]!
}
```

### 10.3 WebSocket API (Real-time Updates)

For live match analysis (if analyzing ongoing matches):

```javascript
// Client connects
socket.emit('subscribe_match', { matchId: 'abc123', playerId: 'player1' });

// Server pushes updates
socket.on('win_prob_update', (data) => {
  // { timestampMs: 45000, probability: 0.62 }
});

socket.on('move_evaluation', (data) => {
  // { eventId: 'evt_123', category: 'great_move', ... }
});

socket.on('key_moment', (data) => {
  // { timestampMs: 98000, description: 'Critical tower defense' }
});
```

---

## 11. Example Output

### 11.1 Sample Match Analysis

**Match Overview**:
```
Match ID: CR_20260108_001
Date: January 8, 2026, 12:15 PM
Duration: 3m 42s
Arena: Legendary Arena

Player: ClashMaster (#V2QUUQVU8) - 5234 🏆
Deck: 2.6 Hog Cycle (Avg Cost: 2.6)
Cards: Hog Rider, Musketeer, Ice Golem, Skeletons, Ice Spirit, Cannon, Fireball, Log

Opponent: GiantKiller (#ABC123) - 5198 🏆
Deck: Golem Beatdown (Avg Cost: 4.1)
Cards: Golem, Night Witch, Baby Dragon, Tornado, Lightning, Mega Minion, Lumberjack, Bats

Result: ClashMaster WINS 3-1 👑
Final Win Probability: 76%
```

### 11.2 Win Probability Graph

```
Win Probability Over Time

100% ┤                                                    ╭──────────
  90%┤                                              ╭────╯
  80%┤                                        ╭─────╯
  70%┤                                   ╭────╯
  60%┤                           ╭───────╯
  50%┤ ━━━━━━━━━━━━━━━━╮   ╭────╯
  40%┤                 ╰───╯
  30%┤
  20%┤
  10%┤
   0%┤
     └────────────────────────────────────────────────────────────
     0s        1m        2m        3m        3m42s

Key Moments:
⭐ 0:32 - Brilliant!! Opposite lane Hog rush (+12%)
🔴 1:15 - Opponent's mistake: Lightning on single Musketeer (-8%)
⭐ 2:08 - Great Move: Perfect Cannon placement vs Golem (+6%)
🏆 2:45 - Crown! Left Princess Tower destroyed
🏆 3:22 - Crown! Right Princess Tower destroyed
```

### 11.3 Timeline of Card Plays

```
Timeline (ClashMaster's Perspective)

00:05 | Ice Spirit → Bridge (Center)
      | Neutral - Cycle and scout

00:12 | Opponent: Golem → Back (Right)
      | ⚠️ CRITICAL MOMENT: Opponent committed 8 elixir

00:14 | Hog Rider + Ice Spirit → Opposite lane (Left)
      | ⭐ BRILLIANT!! Perfect punish on opposite lane
      | Win Prob: 48% → 60% (+12%)
      | Explanation: Forced opponent to defend, prevented massive Golem push
      | Alternative: Defending same lane would have been -8% win prob

00:28 | Cannon → Center (Defensive)
      | ✓ Good - Prepared for Golem push

00:35 | Opponent: Night Witch → Behind Golem
      | Opponent building big push...

00:38 | Musketeer → Right lane (Defensive)
      | ✓ Great Move - Targets Night Witch, good placement

00:45 | Skeletons → Center
      | ✓ Good - Cycle and distract

00:52 | Fireball → Night Witch + Bats
      | ⭐ GREAT MOVE! High-value Fireball, killed Night Witch
      | Win Prob: 56% → 64% (+8%)

01:05 | Ice Golem → Center (Kiting)
      | ✓ Great Move - Perfect kiting of Baby Dragon

01:15 | Opponent: Lightning → Single Musketeer
      | 🔴 Opponent MISTAKE: Wasted Lightning on low-value target
      | Opponent Win Prob: 36% → 28% (-8%)

01:28 | Hog Rider → Right lane
      | ✓ Good - Counter push with cycle advantage

... [continues]

02:45 | Fireball → Opponent Left Tower (1200 HP remaining)
      | 🏆 CROWN! Tower destroyed
      | Win Prob: 70% → 85% (+15%)

03:22 | Log → Opponent Right Tower (450 HP)
      | 🏆 CROWN! Tower destroyed
      | VICTORY! 3-1

03:42 | Match End
```

### 11.4 Mistakes & Great Moves Summary

```
Move Quality Analysis

Brilliant Moves (2):
1. [00:14] Hog Rider + Ice Spirit opposite lane rush
   → Perfect timing after opponent played Golem in back
   → Forced elixir split, prevented big push
   → +12% win probability

2. [02:08] Cannon center placement for Golem pull
   → Activated King Tower
   → Created +4 elixir advantage on defense

Great Moves (5):
- [00:52] Fireball on Night Witch + Bats (+8%)
- [01:05] Ice Golem kite on Baby Dragon (+4%)
- [01:48] Musketeer to snipe Mega Minion (+5%)
- [02:30] Log to finish left tower (+3%)
- [03:10] Spell cycle to finish right tower (+4%)

Good Moves (18):
- Consistent cycling and efficient trades

Mistakes (2):
1. [01:55] Playing Hog Rider with only 4 elixir
   → Opponent easily defended with Bats
   → -3% win probability
   → Better: Wait for 6+ elixir for proper support

2. [02:15] Fireball on lone Baby Dragon
   → Low-value spell usage
   → -2% win probability
   → Better: Save Fireball for Night Witch or spell cycle

Blunders (0):
- No major blunders! Clean game.

Overall Move Quality: +2.4 (Excellent)
Elixir Efficiency: 92%
```

### 11.5 Strategic Insights

```
Strategic Analysis

Matchup: 2.6 Hog Cycle vs Golem Beatdown
Rating: Unfavorable (45% expected win rate)
Actual Result: WIN (outperformed expectation by 55%)

✓ Strategy Followed Correctly:
- Applied opposite-lane pressure when opponent played Golem
- Defended efficiently with Cannon + Musketeer + kiting
- Transitioned to spell cycling in late game
- Minimized elixir leaks (< 5 total)

Key to Victory:
Your opponent made several mistakes that shifted the game in your favor:
1. Overcommitting with Lightning on single Musketeer
2. Not defending your Hog rushes efficiently
3. Building predictable Golem pushes (easy to counter)

What You Did Well:
✓ Excellent opposite-lane pressure timing
✓ Efficient defense (avg 3.2 elixir to defend 6+ elixir pushes)
✓ Perfect Cannon placements for King Tower activation
✓ Smart spell cycling to finish towers
✓ Fast card cycling kept Cannon available

Areas for Improvement:
⚠️ Be more patient with Hog Rider - wait for 6+ elixir
⚠️ Don't waste Fireball on lone troops in mid-game
⚠️ Consider Ice Golem + Musketeer for better kiting

Recommended Practice:
- Practice defending Golem + Night Witch pushes
- Work on spell cycling decisions in late game
- Study Cannon + kiting techniques for Beatdown matchups
```

### 11.6 AI Commentary (Generated by LLM)

```
Match Commentary

This was a textbook example of how to play 2.6 Hog Cycle against Golem Beatdown,
one of Cycle's most challenging matchups. ClashMaster demonstrated excellent
understanding of the matchup strategy and executed it nearly flawlessly.

Opening Phase (0:00 - 1:00):
The game started cautiously with an Ice Spirit cycle. When the opponent committed
Golem in the back at 0:12, ClashMaster immediately recognized the opportunity and
launched a devastating opposite-lane Hog Rider rush. This brilliant play forced
the opponent to split their elixir between defending the Hog and supporting the
Golem, completely disrupting their game plan. This single decision swung the win
probability from 48% to 60% and set the tone for the entire match.

Mid Game (1:00 - 2:30):
ClashMaster defended the subsequent Golem pushes with impressive efficiency. The
Cannon placements were perfect - pulling the Golem to activate the King Tower and
buying time for the Princess Towers to chip away at it. The Musketeer was well-
positioned to snipe the Night Witch before she could spawn Bats. The Fireball at
0:52 was particularly strong, eliminating the Night Witch and Bats for a massive
elixir advantage.

The opponent made a critical error at 1:15 by using Lightning on a single
Musketeer. This 6-for-4 negative elixir trade gave ClashMaster full control of
the tempo. From this point forward, ClashMaster cycled Hog Riders and maintained
constant pressure while defending efficiently.

Closing (2:30 - 3:42):
With a commanding lead and strong elixir management, ClashMaster transitioned to
spell cycling - a classic 2.6 Hog Cycle finish. The Fireball and Log were saved
for tower damage rather than troop eliminations. The left Princess Tower fell at
2:45, followed by the right tower at 3:22, securing a dominant 3-1 victory.

Final Thoughts:
This game showcased the power of opposite-lane pressure against Beatdown decks.
ClashMaster's decision-making was sharp, with only two minor mistakes that had
minimal impact. The 92% elixir efficiency and fast cycling kept the pressure
relentless. Against a more skilled opponent, those two Fireball/Hog timing
mistakes could have been costlier, but overall this was an excellent performance
that turned an unfavorable matchup into a convincing win.

Rating: 9/10 - Nearly perfect execution of matchup strategy.
```

### 11.7 3D Replay Preview Description

```
3D Replay Viewer

Camera View: Bird's eye, angled 30° from horizontal, centered on arena

Scene:
- Legendary Arena with flowing river and stone bridges
- Four towers visible: King and two Princess towers for each player
- Health bars above each tower, updating in real-time
- Elixir bars at bottom of screen for both players

Timeline Scrubber:
- Full match duration (0:00 - 3:42) displayed horizontally
- Win probability graph overlaid (green line)
- Event markers (card plays, crowns, key moments)
- Current timestamp indicator (draggable)

Key Animated Moments:

[00:14 - Brilliant Rush]
- Hog Rider spawns on left side with glowing circle
- Ice Spirit spawns simultaneously
- Both troops sprint toward opponent's left tower
- Camera pans to follow Hog Rider
- Opponent tower targets Hog, deals damage (health bar drops)
- Hog delivers several hammer swings (damage numbers float up)
- Annotation appears: "⭐ BRILLIANT!! Opposite lane pressure +12%"

[00:52 - Fireball Strike]
- Opponent's Night Witch and Bats cluster behind Golem
- Fireball projectile arcs across arena
- Explosion particle effect at impact point
- Night Witch and Bats disappear (death animations)
- Damage numbers appear: -572 HP
- Annotation: "⭐ GREAT MOVE! High-value Fireball +8%"

[02:45 - Crown Earned]
- Fireball hits left Princess Tower (HP bar at 1200)
- Tower explodes dramatically, rubble falls
- Crown icon appears above arena
- Victory sound effect
- Annotation: "🏆 CROWN! Left Tower destroyed"

Playback Controls:
- Play/Pause button
- Speed control: 0.5x, 1x, 2x, 4x
- Jump to previous/next key moment
- Toggle camera angles: bird's eye, player perspective, opponent perspective
- Toggle overlays: health bars, elixir, range indicators, troop paths

Interactive Elements:
- Click on any troop to see its stats (HP, damage, target)
- Hover over card play to see analysis
- Click on timeline events to jump to that moment
- Toggle "analysis mode" to see suggested plays at any point

Technical Details:
- 60 FPS playback
- Smooth interpolation between events
- Particle effects for spells and impacts
- Authentic troop animations from game assets
- Dynamic lighting and shadows
```

---

## 12. Implementation Roadmap

### Phase 1: MVP (8-12 weeks)

**Weeks 1-2: Foundation**
- [ ] Set up development environment
- [ ] Database schema design (PostgreSQL, MongoDB)
- [ ] RoyaleAPI integration (fetch player battles)
- [ ] Basic data ingestion pipeline
- [ ] Player and Match models

**Weeks 3-4: Core Analysis**
- [ ] Deck classification model (rule-based + ML)
- [ ] Basic win probability model (simpler version)
- [ ] Move evaluation heuristics (without full simulation)
- [ ] Storage of analysis results

**Weeks 5-6: Basic UI**
- [ ] Player search and profile page
- [ ] Match list view
- [ ] Simple match analysis page:
  - Match overview
  - Win probability graph (simple)
  - Card play timeline
- [ ] Basic styling

**Weeks 7-8: API Development**
- [ ] RESTful API endpoints
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Caching layer (Redis)
- [ ] Rate limiting

**Weeks 9-10: AI Commentary (Basic)**
- [ ] LLM integration (OpenAI/Claude API)
- [ ] Basic prompt templates
- [ ] Commentary generation for matches
- [ ] Display in UI

**Weeks 11-12: Testing & Deployment**
- [ ] Unit and integration tests
- [ ] Load testing
- [ ] Deploy to staging
- [ ] Deploy to production (beta)
- [ ] User feedback collection

**MVP Deliverables**:
- Player search
- Match history with basic analysis
- Win probability graph
- Card play timeline
- Move evaluations (simplified)
- AI-generated commentary
- No 3D replay viewer yet

### Phase 2: Advanced Features (12-16 weeks)

**Weeks 13-16: Enhanced Analysis**
- [ ] Advanced win probability model (LSTM)
- [ ] Detailed move evaluation with alternatives
- [ ] Strategy suggestion system
- [ ] Matchup database with recommendations
- [ ] Historical performance analytics

**Weeks 17-20: 3D Replay Viewer**
- [ ] Event stream generation (simulation)
- [ ] Three.js setup with React
- [ ] Arena and tower models
- [ ] Troop models and animations
- [ ] Timeline synchronization
- [ ] Particle effects and polish

**Weeks 21-24: Dashboard & Analytics**
- [ ] Player statistics dashboard
- [ ] Performance trends over time
- [ ] Deck archetype analytics
- [ ] Meta analysis (top decks, win rates)
- [ ] Leaderboards

**Weeks 25-28: Polish & Optimization**
- [ ] UI/UX improvements
- [ ] Performance optimization
- [ ] Mobile responsiveness
- [ ] Advanced features: replay sharing, comparisons
- [ ] Public launch

### Phase 3: Scale & Monetization (Ongoing)

- [ ] Scale infrastructure for 100k+ users
- [ ] Pro subscription tier (ad-free, advanced analytics)
- [ ] Mobile app (React Native or native)
- [ ] Live match analysis (if possible)
- [ ] Tournament analysis
- [ ] Clan analytics
- [ ] API for third-party developers
- [ ] Coaching recommendations
- [ ] Training modes and challenges

---

## Technical Challenges & Solutions

### Challenge 1: Limited Event Data from RoyaleAPI

**Problem**: RoyaleAPI may not provide detailed event streams (exact card play timing, positions, troop movements).

**Solutions**:
1. **Simulation**: Use game logic to simulate events based on final state
2. **Replay Files**: Parse official .replay files if accessible
3. **Community Data**: Crowdsource detailed match data from users
4. **Computer Vision**: Extract events from replay videos
5. **Hybrid Approach**: Combine estimation with available data

### Challenge 2: Win Probability Model Accuracy

**Problem**: Clash Royale is complex with many variables; achieving 80%+ accuracy is difficult.

**Solutions**:
1. Start with simpler model, iterate
2. Use large training dataset (1M+ matches)
3. Incorporate domain knowledge (game rules, card interactions)
4. Ensemble models (combine multiple approaches)
5. Continuous retraining with new meta data

### Challenge 3: Alternative Move Evaluation

**Problem**: Evaluating all possible alternative moves is computationally expensive (4 cards × 50 positions × timing = 200+ alternatives per move).

**Solutions**:
1. **Heuristic Pruning**: Filter obviously bad moves
2. **Fast Approximation Model**: XGBoost for quick quality estimates
3. **Top-K Search**: Only evaluate best 5-10 alternatives
4. **Pre-computation**: Cache common scenarios
5. **Async Processing**: Don't block user, compute in background

### Challenge 4: 3D Replay Without Detailed Positional Data

**Problem**: Without exact troop positions, 3D replay requires simulation.

**Solutions**:
1. **Physics-based Simulation**: Implement troop AI (pathfinding, targeting)
2. **Constraint Satisfaction**: Use final state to validate simulation
3. **Interpolation**: Smooth transitions between known events
4. **Approximation**: Accept some inaccuracy for visual representation
5. **User Feedback**: Allow users to report inaccurate replays

### Challenge 5: LLM Cost for Commentary

**Problem**: Generating commentary for every match with GPT-4 is expensive.

**Solutions**:
1. **Selective Generation**: Only generate for requested matches
2. **Cheaper Models**: Use GPT-3.5 or Claude Haiku for simple explanations
3. **Template-based**: Use templates + LLM fill-ins
4. **Batch Processing**: Generate overnight for popular players
5. **Caching**: Never regenerate same match commentary

### Challenge 6: Real-time Performance

**Problem**: Users expect analysis results quickly (< 5 seconds).

**Solutions**:
1. **Pre-computation**: Analyze popular players' matches proactively
2. **Async Processing**: Show partial results immediately, full analysis later
3. **Model Optimization**: Use TensorFlow Lite, ONNX for fast inference
4. **Caching**: Redis for frequently accessed matches
5. **Progress Indicators**: Show user that analysis is in progress

---

## Security & Privacy Considerations

### Data Privacy
- Only fetch public data from RoyaleAPI
- Anonymize player data if required by regulations
- Allow users to opt-out of public listings
- Secure API keys and credentials

### API Security
- Rate limiting to prevent abuse
- Authentication for write operations
- Input validation to prevent injection attacks
- HTTPS everywhere

### Model Security
- Protect ML models from theft (use secure serving)
- Monitor for adversarial inputs
- Version control for model updates

---

## Monitoring & Observability

### Metrics to Track
- **System**: CPU, memory, disk, network usage
- **Application**: Request latency, error rates, throughput
- **ML Models**: Inference time, accuracy metrics, prediction distribution
- **Business**: Users, matches analyzed, API calls, commentary generated

### Alerting
- High error rates
- Slow response times (> 2s for API)
- Model prediction anomalies
- Database connection issues
- RoyaleAPI downtime

### Logging
- Structured logging (JSON format)
- Centralized log aggregation (ELK)
- Log retention policy (30 days)

---

## Future Enhancements

1. **Live Match Analysis**: Analyze ongoing matches in real-time
2. **Coaching Mode**: Personalized training plans based on weaknesses
3. **Clan Analytics**: Aggregate clan statistics, compare clans
4. **Tournament Mode**: Analyze tournament brackets and performances
5. **Deck Builder**: Suggest optimal decks based on meta and player style
6. **Card Upgrade Advisor**: Recommend which cards to upgrade first
7. **Matchmaking Predictor**: Predict next opponent's deck archetype
8. **Esports Integration**: Analyze professional matches, create highlight reels
9. **Community Features**: Forums, deck sharing, replay sharing
10. **Mobile App**: Native iOS/Android apps

---

## Conclusion

This system design provides a comprehensive roadmap for building **ClashFish**, a Clash Royale game analyzer that rivals the depth and usefulness of chess.com's analysis tools. The architecture is modular, scalable, and designed to deliver actionable insights to players at all skill levels.

**Key Differentiators**:
- Deep game state analysis with win probability tracking
- Detailed move-by-move evaluation with alternatives
- AI-powered commentary that explains the "why" behind moves
- Immersive 3D replay visualization
- Strategic guidance tailored to specific matchups
- Comprehensive historical analytics

**Next Steps**:
1. Validate RoyaleAPI data availability
2. Assemble development team
3. Begin Phase 1 (MVP) implementation
4. Iterate based on user feedback
5. Scale to full feature set

This design document serves as the foundation for the development team to build ClashFish. Each section can be expanded into detailed technical specifications as implementation progresses.
