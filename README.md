# Proposal-sentinel
Research &amp; Grant Proposal Red-Flag and Strength Analyzer — Lightweight Python tool.
🛰 Proposal Sentinel

Red-flag & strength analyzer for research and grant proposals

🔍 What is this?

Proposal Sentinel is a lightweight AI-powered tool that scans research or grant proposals and highlights:
	•	🚨 Red flags (weak verbs, vague claims, missing structure)
	•	✅ Strengths (clear problem statement, actionable language)
	•	📊 Overall balance score

It’s designed for academics, grant writers, and even students — but kept light, fast, and pure Python.
No installs, no external libraries, just plug and play.

Why this project?

I wanted to explore a niche problem: why do so many proposals fail before peer review?
Turns out, the writing itself hides a lot of signals. Proposal Sentinel is my attempt at a tool that doesn’t just say “good/bad,” but helps people see how their words land.

Most AI projects are generic sentiment analyzers or text classifiers. This one? It’s specific, targeted, and professional — something you don’t see often on GitHub.

⸻

🛠 Features
	•	CLI-based proposal analyzer (python -m proposal_sentinel analyze your_file.txt)
	•	Text-based report + JSON structured output
	•	Example input and output included in /examples
	•	Unit tests with unittest
	•	Pure Python, runs anywhere

🚀 Quick Start

Clone the repo:
git clone https://github.com/Devwithumar/proposal-sentinel.git
cd proposal-sentinel

Analyze a sample proposal:
python -m proposal_sentinel analyze examples/sample_proposal.txt

Output example (sample_report.txt):
Strengths:
- Clear objective stated
- Problem context described

Red Flags:
- Lacks specific methodology
- Too many vague phrases ("might", "could")

Balance Score: 63/100

📂 Project Structure

proposal-sentinel/
│── proposal_sentinel/       # Core analyzer code
│── examples/                # Sample proposals + reports
│── tests/                   # Unit tests
│── README.md
│── LICENSE
│── run.sh                   # Quick start script


⸻

🧪 Tests
Run unit tests with:
python -m unittest discover tests

🗺 Roadmap
	•	Add scoring weights for funding body preferences
	•	Expand analyzer with domain-specific rules (STEM, humanities, NGOs)
	•	Web dashboard frontend (Flask + simple UI)

  👤 Author

Built with curiosity by Devwithumar
If you like this project, ⭐ it — more niche but impactful AI tools coming every week.



