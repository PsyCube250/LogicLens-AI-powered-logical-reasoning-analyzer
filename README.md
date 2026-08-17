# LogicLens

AI-powered logical reasoning analyzer for detecting fallacies, cognitive biases, and counterexamples in natural language claims.

Break down a statement and see its logic — analyzing propositional structure, checking counterexamples, logical fallacies, and cognitive biases.

## Features

- **Claim structure analysis**: Identifies the type, subject, conclusion, and logical direction of a statement
- **Counterexample detection**: Automatically searches for counterexamples and determines whether they hold and violate the original conclusion
- **Logical fallacy detection**: Detects common fallacies (e.g. hasty generalization, slippery slope)
- **Cognitive bias detection**: Detects common cognitive biases
- **Web interface**: Visual analysis UI built with React + Vite
- **CLI tool**: Interactive terminal-based analysis

## Tech Stack

- **Backend**: Python, FastAPI, DeepSeek API
- **Frontend**: React, Vite

## Project Structure

logic_agent/
├── agent/ # Core agent logic
├── tools/ # Analysis tools (fallacy, bias, counterexample, classifier)
├── data/ # Logical fallacy dataset
├── web/ # Frontend (React + Vite)
├── api.py # FastAPI backend entry point
├── main.py # CLI entry point
├── requirements.txt # Python dependencies
└── start.sh / start.ps1 # One-click startup scripts
## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/PsyCube250/LogicLens-AI-powered-logical-reasoning-analyzer.git
cd LogicLens-AI-powered-logical-reasoning-analyzer
```

### 2. Configure environment variables

Create a `.env` file in the project root:

DEEPSEEK_API_KEY=your_key_here

> You can get a key from the [DeepSeek Open Platform](https://platform.deepseek.com).

### 3. Install dependencies

Backend:
```bash
pip install -r requirements.txt
```

Frontend:
```bash
cd web
npm install
```

### 4. Run the app

**Option 1: One-click startup script**

Windows (PowerShell):
```powershell
.\start.ps1
```

macOS / Linux:
```bash
./start.sh
```

**Option 2: Start manually**

Backend (new terminal, project root):
```bash
uvicorn api:app --reload --port 8000
```

Frontend (new terminal, inside `web`):
```bash
npm run dev
```

Once running, open `http://127.0.0.1:5173` to use the web interface.

### 5. CLI usage (optional)

```bash
python main.py
```

## API

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET  | `/api/health` | Health check |
| POST | `/api/analyze` | Submit a statement and get its logical analysis |

## License

[MIT](./LICENSE)

