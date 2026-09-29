# 🧠 IncidentMind

### Every incident makes the next incident easier to solve.

IncidentMind is a **memory-powered AI Incident Response Engineer** that helps engineers investigate production incidents using organizational knowledge from previous incidents.

It combines **Hindsight long-term memory** with **Groq-powered AI analysis** to recall relevant historical incidents, identify likely root causes, and suggest safe next steps for engineer review.

---

## ✨ Features

* 🧠 **Hindsight-powered memory** — retrieves up to 4 relevant historical incidents.
* 🔀 **With / Without Memory** — compare AI analysis with and without organizational memory.
* 🔎 **Historical evidence** — previous symptoms, root causes, resolutions, outcomes, and engineer feedback can inform analysis.
* 🤖 **AI incident analysis** — provides likely root cause, current evidence, historical context, recommended next steps, and confidence.
* 👨‍💻 **Human-in-the-loop** — engineers review and approve recommended remediation.
* 📚 **Continuous learning** — resolved incidents and engineer feedback are stored back into Hindsight for future use.
* 🛡️ **Safe recommendations** — the system does not claim to execute production changes.

---

## 🎯 Problem

Production incidents are often similar to problems that have already occurred.

However, useful knowledge from previous incidents can be scattered across logs, tickets, post-mortems, and individual engineer experience.

A conventional AI assistant mainly reasons from the information provided in the current incident.

**IncidentMind adds organizational memory**, allowing previous incident experience to become part of the investigation.

---

## 💡 Solution

IncidentMind maintains a memory of previous incidents and uses relevant historical context when analyzing a new incident.

The system can remember:

* Incident symptoms
* Relevant logs
* Root causes
* Resolutions
* Outcomes
* Resolution times
* Engineer feedback

This allows previous incident knowledge to remain available when similar problems occur again.

---
<img width="1536" height="1024" alt="ChatGPT Image Sep 29, 2026, 12_33_35 PM" src="https://github.com/user-attachments/assets/ad810d71-8543-445b-ac83-d85a9095eda6" />


  

### Components

| Component              | Purpose                                              |
| ---------------------- | ---------------------------------------------------- |
| **Streamlit**          | User interface for incident investigation            |
| **IncidentMind Agent** | Orchestrates memory retrieval and AI analysis        |
| **Hindsight**          | Stores and recalls organizational incident knowledge |
| **Groq**               | Provides LLM inference                               |
| **GPT-OSS-120B**       | AI reasoning model                                   |
| **Python**             | Application and agent logic                          |

---

## 🔬 Analysis Modes

IncidentMind supports two modes for evaluation:

### With Hindsight Memory

Historical incidents retrieved from Hindsight are provided to the AI as organizational evidence.

### Without Hindsight Memory

The AI analyzes only the current incident without historical incident context.

Using the same incident in both modes makes it possible to observe how organizational memory affects the analysis.

---

## 🤖 AI Response

IncidentMind produces five focused sections:

1. **Likely Root Cause**
2. **Evidence From Current Incident**
3. **Relevant Historical Incidents**
4. **Recommended Next Steps**
5. **Confidence**

Recommended actions are limited to a small number of practical investigation steps and require engineer approval.

---

## 📚 Learning

After an incident is resolved, IncidentMind can store the actual resolution information in Hindsight, including:

* Actual root cause
* Actual resolution
* Outcome
* Resolution time
* Engineer feedback

This information becomes part of the organization's incident memory and can be retrieved for future incidents.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Hindsight**
* **Groq**
* **GPT-OSS-120B**
* **Pandas**
* **python-dotenv**

---

## 📁 Project Structure

```text
incidentmind/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── agent/
│   └── agent.py
│
├── llm/
│   └── groq_client.py
│
├── memory/
│   └── hindsight_client.py
│
├── data/
│   └── incidents.json
│
├── evaluation/
│   └── test_incidents.json
│
└── utils/
    └── helpers.py
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/PAVANI-MYNAM/incidentmind.git
cd incidentmind
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file:

```env
HINDSIGHT_API_KEY=your_hindsight_api_key
GROQ_API_KEY=your_groq_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## 🔐 Security

API credentials must be stored in environment variables and **must not be committed to GitHub**.

The repository should exclude:

```text
.env
venv/
venv313/
__pycache__/
*.pyc
```

If an API key is accidentally exposed, revoke it and generate a new one.

---

## 🚀 Future Improvements

* Monitoring and alerting integrations
* Slack / Teams integration
* Jira integration
* Automated post-mortem generation
* Runbook retrieval
* Incident evaluation and benchmarking
* Production observability integrations

---

## 🧠 IncidentMind

**Memory-powered incident response for smarter, faster investigations.**

> Every incident makes the next incident easier to solve.
