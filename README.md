# New Game Plus

A game recommendation system that suggests video games based on titles you've previously played. Built with Python and Prolog for logic-based recommendations.

## Features

- Personalized game recommendations based on your gaming history
- Prolog-powered recommendation logic
- Multiple recommendation strategies (genre, platform, rating similarity)
- Real game data from IGDB (Internet Game Database)
- Fast queries with SWI-Prolog backend

## Prerequisites

Before installation, ensure you have:

1. **Python 3.12 or higher**
   - Check: `python3.12 --version`
   - Download: https://www.python.org/downloads/

2. **SWI-Prolog** (MUST be installed BEFORE creating Python virtual environment)
   - macOS: `brew install swi-prolog`
   - Ubuntu/Debian: `sudo apt-get install swi-prolog`
   - Windows: https://www.swi-prolog.org/download/stable
   - Verify: `swipl --version`

3. **IGDB API Account** (free)
   - Required for fetching game data
   - Setup instructions below

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/osyounis/new_game_plus.git
cd new_game_plus
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up IGDB API Credentials

1. Go to https://api-docs.igdb.com/#account-creation
2. Sign up for a Twitch account (if needed)
3. Visit https://dev.twitch.tv/console/apps
4. Click "Register Your Application"
5. Fill in:
   - **Name**: "New Game Plus Recommender"
   - **OAuth Redirect URLs**: http://localhost
   - **Category**: Application Integration
6. Click "Manage" → Copy your **Client ID**
7. Click "New Secret" → Copy your **Client Secret**

8. Create `.env` file in project root:
```bash
cp .env.example .env
```

9. Edit `.env` and add your credentials:
```
IGDB_CLIENT_ID=paste_your_client_id_here
IGDB_CLIENT_SECRET=paste_your_client_secret_here
```

### 5. Fetch Game Data and Generate Knowledge Base

```bash
# Fetch 50 games from IGDB
python src/igdb_client.py

# Convert to Prolog facts
python src/generate_facts.py
```

## Usage

### Interactive Mode

```bash
python src/main.py
```

You'll be prompted to enter a game title.

### Direct Query

```bash
python src/main.py --game "Dark Souls"
```

### Limit Results

```bash
python src/main.py --game "The Witcher 3" --limit 10
```

### Example Output

```
============================================================
Recommendations based on: Dark Souls
============================================================

Similar Games (Genre + Rating):
  1. Bloodborne
  2. Elden Ring
  3. Dark Souls II
  4. Demon's Souls
  5. Sekiro: Shadows Die Twice

Same Genre:
  1. Bloodborne
  2. The Witcher 3: Wild Hunt
  3. Dragon's Dogma
  ...
```

## Project Structure

```
new_game_plus/
├── src/                    # Python source code
│   ├── main.py            # Main CLI application
│   ├── igdb_client.py     # IGDB API client
│   ├── generate_facts.py  # JSON → Prolog converter
│   └── prolog_bridge.py   # Python-Prolog interface (pyswip)
├── prolog/                 # Prolog knowledge base
│   ├── knowledge_base.pl  # Game facts (auto-generated)
│   └── rules.pl           # Recommendation rules
├── data/                   # Game data
│   └── games.json         # IGDB game data (50 games)
├── .env                    # API credentials (NOT in git)
├── .env.example           # Template for .env
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## How It Works

The recommendation system uses a hybrid Python-Prolog architecture:

1. **Data Collection** (`igdb_client.py`)
   - Fetches game data from IGDB API
   - Stores raw JSON in `data/games.json`

2. **Fact Generation** (`generate_facts.py`)
   - Converts JSON to Prolog facts
   - Creates `prolog/knowledge_base.pl`
   - Format: `game(Title, Genre, Platform, Rating)`

3. **Recommendation Rules** (`prolog/rules.pl`)
   - Defines logic for matching games
   - Strategies: genre, platform, rating similarity

4. **Query Engine** (`prolog_bridge.py`)
   - Bridges Python and Prolog via pyswip
   - Sends queries to Prolog
   - Returns results to Python

5. **User Interface** (`main.py`)
   - CLI for user interaction
   - Displays formatted recommendations

**Data Flow:**
```
IGDB API → igdb_client.py → data/games.json
                                    ↓
                             generate_facts.py
                                    ↓
                      prolog/knowledge_base.pl ← rules.pl
                                    ↓
           User → main.py → prolog_bridge.py → Prolog
                                    ↓
                            Recommendations
```

## Testing

Test each component individually:

```bash
# Test IGDB API connection
python src/igdb_client.py

# Test Prolog fact generation
python src/generate_facts.py

# Test Prolog bridge directly
python src/prolog_bridge.py

# Test full system
python src/main.py --game "The Witcher 3: Wild Hunt"
```

## License

GNU General Public License v3.0 - See LICENSE file for details

## Acknowledgments

- [IGDB API](https://api-docs.igdb.com/) for game data
- [SWI-Prolog](https://www.swi-prolog.org/) for the logic programming engine
- [pyswip](https://github.com/yuce/pyswip) for Python-Prolog integration