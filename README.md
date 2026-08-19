# LogicLens

LogicLens is an AI-powered logical reasoning analyzer that breaks down
natural-language claims, examines their propositional structure, identifies
logical fallacies and cognitive biases, and generates potential
counterexamples.

## Features

- **Claim structure analysis**: Identifies the claim type, subject,
  conclusion, and logical direction.
- **Counterexample detection**: Generates potential counterexamples
  and evaluates whether they challenge the original conclusion.
- **Logical fallacy detection**: Detects common logical fallacies,
  such as hasty generalization and slippery slope.
- **Cognitive bias detection**: Identifies cognitive biases that may
  influence the statement.
- **Web interface**: Provides a visual analysis interface built with
  React and Vite.
- **CLI tool**: Supports interactive analysis from the terminal.

## Tech Stack

### Backend

- Python
- FastAPI
- Uvicorn
- DeepSeek API

### Frontend

- React
- Vite

### Data

- JSON-based logical fallacy dataset

## Project Structure

```text
.
├── agent/
│   ├── __init__.py
│   └── router.py
├── tools/
│   ├── base.py
│   ├── bias.py
│   ├── claim_classifier.py
│   ├── counterexample.py
│   ├── fallacy.py
│   └── registry.py
├── data/
│   └── logical_fallacy_dataset_200.json
├── web/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── api.py
├── llm.py
├── main.py
├── planner.py
├── state.py
├── requirements.txt
├── start.sh
└── readme.md
```

## Getting Started

Follow the steps below to run LogicLens locally.

### Prerequisites

Make sure the following software is installed:

- Python 3.10 or later
- Node.js 18 or later
- npm
- Git
- A valid DeepSeek API key

You can obtain a DeepSeek API key from the
[DeepSeek Open Platform](https://platform.deepseek.com/).

### 1. Clone the Repository

```bash
git clone https://github.com/PsyCube250/LogicLens-AI-powered-logical-reasoning-analyzer.git
cd LogicLens-AI-powered-logical-reasoning-analyzer
```

### 2. Create a Python Virtual Environment

Using a virtual environment is recommended to keep the project's Python
dependencies isolated from your system installation.

#### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
```

After activation, your terminal prompt should display `(.venv)`.

### 3. Configure Environment Variables

Copy the example environment file.

#### macOS or Linux

```bash
cp .env.example .env
```

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace the placeholder with your DeepSeek API key:

```dotenv
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

Do not commit your `.env` file or expose your API key publicly.
Make sure `.env` is included in `.gitignore`.

### 4. Install Backend Dependencies

Make sure the virtual environment is activated, then run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Install Frontend Dependencies

From the project root, run:

```bash
cd web
npm install
cd ..
```

### 6. Start the Application

You can start LogicLens using the startup script or run the backend and
frontend manually.

#### Option A: Use the Startup Script

On macOS or Linux:

```bash
chmod +x start.sh
./start.sh
```

#### Option B: Start the Backend and Frontend Manually

Open two terminal windows.

In the first terminal, activate the virtual environment and start the
FastAPI backend from the project root.

On macOS or Linux:

```bash
source .venv/bin/activate
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

In the second terminal, start the React frontend:

```bash
cd web
npm run dev
```

### 7. Open the Web Interface

After both services have started, open the following address in your browser:

```text
http://127.0.0.1:5173
```

The backend API runs at:

```text
http://127.0.0.1:8000
```

If FastAPI's interactive documentation is enabled, it is available at:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation may be available at:

```text
http://127.0.0.1:8000/redoc
```

### 8. Verify the Backend

Check the backend health endpoint:

```bash
curl http://127.0.0.1:8000/api/health
```

A successful response indicates that the backend is running.

You can also open the endpoint directly in a browser:

```text
http://127.0.0.1:8000/api/health
```

### 9. Run the CLI

LogicLens also provides an optional command-line interface.

Make sure the virtual environment is activated, then run the following
command from the project root:

```bash
python main.py
```

Follow the prompts in the terminal to submit a statement for analysis.

### 10. Stop the Application

Press `Ctrl+C` in each terminal running the backend or frontend.

To leave the Python virtual environment, run:

```bash
deactivate
```

## Troubleshooting

### `DEEPSEEK_API_KEY` Is Missing

Make sure the `.env` file is located in the project root and contains:

```dotenv
DEEPSEEK_API_KEY=your_actual_api_key
```

Restart the backend after changing the `.env` file.

### `uvicorn` Command Not Found

Activate the virtual environment and reinstall the backend dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, start Uvicorn through Python:

```bash
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

### Port 8000 Is Already in Use

Start the backend on a different port:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8001
```

If you change the backend port, update the frontend API configuration so
that it sends requests to the new address.

### Port 5173 Is Already in Use

Vite may automatically select another available port. Check the URL printed
in the terminal after running:

```bash
npm run dev
```

### Frontend Cannot Connect to the Backend

Confirm that:

1. The FastAPI backend is running.
2. The frontend is using the correct backend URL.
3. The backend port matches the URL configured in the frontend.
4. CORS allows requests from the frontend development server.
5. The health endpoint can be opened successfully.

### PowerShell Blocks Virtual Environment Activation

If PowerShell prevents the activation script from running, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

This changes the execution policy only for the current PowerShell session.

### Node.js Dependencies Fail to Install

Check the installed versions:

```bash
node --version
npm --version
```

Then try reinstalling the frontend dependencies:

```bash
cd web
npm install
```


## API

| Method | Endpoint         | Description                                     |
| ------ | ---------------- | ----------------------------------------------- |
| GET    | `/api/health`  | Health check                                    |
| POST   | `/api/analyze` | Submit a statement and get its logical analysis |

## License

[MIT](./LICENSE)
