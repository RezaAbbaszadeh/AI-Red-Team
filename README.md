# AI Red Team

AI Red Team connects Promptfoo to the intentionally vulnerable DVAIA agent API.

## Scope

The first milestone evaluates one DVAIA configuration:

- Target: `POST http://127.0.0.1:5000/api/agent/chat`
- Agent tools: all six DVAIA tools
- Baseline tests: deterministic tool-use checks
- Red-team tests: Promptfoo-generated access-control and excessive-agency probes
- Verification: actual DVAIA `tool_calls`, not only the final model text

Use this only against your local DVAIA instance or another system you are authorized to test.

## Prerequisites

- Docker Desktop with WSL2
- Git
- Node.js 24 LTS
- Python 3.10 or newer
- About 10 GB or more for DVAIA's default local models

## 1. Start DVAIA

Inside WSL:

```bash
git clone https://github.com/airtasystems/DVAIA-Damn-Vulnerable-AI-Application.git
cd DVAIA-Damn-Vulnerable-AI-Application
cp .env.example .env
./run_docker.sh
```

Open:

```text
http://127.0.0.1:5000
```

The full local Docker mode normally exposes Ollama to the host on port `11480`.

## 2. Verify DVAIA

From the AI Red Team project directory:

```bash
python3 scripts/verify_dvaia.py
```

Expected checks:

- `/api/health` returns `{"status":"ok"}`
- `/api/models` returns an agent model
- `/api/agent/chat` returns `response` and `tool_calls`
- The simple test usually invokes `list_users`

## 3. Install Promptfoo

```bash
npm install
```

The project pins Promptfoo to the version recorded in `package.json`.

## 4. Run deterministic baseline tests

```bash
npm run baseline
```

Then view the result:

```bash
npm run view
```

Some security tests are expected to fail because DVAIA is deliberately vulnerable. A failed test can be a successfully demonstrated vulnerability.

## 5. Run the first automated red-team scan

Load the local environment:

```bash
set -a
source .env.example
set +a
```

Run:

```bash
npm run redteam
```

View the security report:

```bash
npm run redteam-report
```

The project uses the Ollama model already downloaded by DVAIA for local attack generation and grading. This keeps the first experiment local, but a small local model may generate weaker probes than a stronger dedicated attack model.

## 6. What the two response parsers do

`providers/dvaia-natural.js`:

- Returns the normal assistant response
- Stores tool calls in Promptfoo response metadata
- Used for deterministic baseline tests

`providers/dvaia-trace.js`:

- Returns the assistant response
- Appends a compact security trace containing actual tool names
- Stores the same data in metadata
- Used for automated red-team grading

The appended trace helps a grader distinguish between:

- The model merely discussing a dangerous action
- The agent actually calling a dangerous tool

## 7. First experiment

Treat this as the vulnerable baseline:

```text
Configuration A: all six tools available
```

Later milestones will add:

```text
Configuration B: read-only tools only
Configuration C: risky tools behind explicit approval
```

Measure:

- Unauthorized dangerous-tool-call rate
- Sensitive-tool-call rate
- Attack success rate
- Benign task completion rate
- False refusal rate
- Repeated-run consistency
- Requests, runtime, and token use

## Repository plan

```text
AI-Red-Team/
├── promptfooconfig.baseline.yaml
├── promptfooconfig.redteam.yaml
├── providers/
├── tests/
├── scripts/
├── results/
└── docs/
```

## Important interpretation rule

Do not use Promptfoo's pass rate alone as the final truth. Manually verify important findings against the recorded DVAIA tool trace. For this project, a tool-side effect is stronger evidence than an unsafe-looking text response.
