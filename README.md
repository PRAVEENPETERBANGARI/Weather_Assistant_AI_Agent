# Weather_Assistant_AI_Agent

# 🌦️ Weather Alert Assistant

An AI-powered weather monitoring and notification system built using the OpenAI Agents SDK. The assistant analyzes real-time weather conditions, identifies abnormal or severe weather events, and automatically sends personalized email alerts to users.

## 🚀 Features

* 🌍 Detects weather conditions for any city or location
* 🤖 Multi-agent workflow powered by OpenAI Agents SDK
* 📍 Extracts and validates locations from natural language queries
* 🌦️ Retrieves current weather and forecast data using external APIs
* ⚠️ Identifies severe weather conditions such as heavy rain, storms, extreme temperatures, and high winds
* ✉️ Automatically composes and sends email notifications
* 🔎 End-to-end tracing and observability with OpenAI tracing
* 🖥️ Interactive user interface built with Gradio
* 🧩 Modular and extensible architecture for adding new agents and tools

## 🏗️ Architecture

```text
User Query
    │
    ▼
Location Extraction Agent
    │
    ▼
Weather Agent ──► Weather APIs
    │
    ▼
Alert Evaluation Logic
    │
    ▼
Email Agent ──► Email Service
    │
    ▼
User Notification
```

## 🛠️ Tech Stack

* Python 3.11+
* OpenAI Agents SDK
* Gradio
* OpenAI Models
* Open-Meteo API
* AsyncIO
* SMTP / Email API
* Python Dotenv

## 📂 Project Structure

## 📂 Project Structure

```text
weather_alert_flow/
├── notebooks/
│   ├── .gradio/
│   ├── weather_agent_with_email_alert
│   ├── weather_agent_with_gradio_chat
│   └── weather_alert_agent
│
├── src/
│   ├── __init__.py
│   ├── Agents.py
│   ├── Email_Tool.py
│   ├── Instructions.py
│   ├── Models.py
│   └── Weather_Tools.py
│
├── .env
├── README.md
└── requirements.txt
```

### Directory Overview

| Path                   | Description                                                                 |
| ---------------------- | --------------------------------------------------------------------------- |
| `notebooks/`           | Databricks notebooks for agent development, testing, and Gradio integration |
| `notebooks/.gradio/`   | Gradio configuration and temporary UI files                                 |
| `src/Agents.py`        | Defines weather and email agents along with workflow orchestration          |
| `src/Email_Tool.py`    | Email utility functions and SMTP integration                                |
| `src/Instructions.py`  | System prompts and agent instructions                                       |
| `src/Models.py`        | Pydantic models and structured output schemas                               |
| `src/Weather_Tools.py` | Weather API integrations and helper functions                               |
| `.env`                 | Environment variables and API credentials                                   |
| `requirements.txt`     | Python dependencies                                                         |
| `README.md`            | Project documentation                                                       |

### Import Example

Ensure the `src` directory is added to the Python path before importing modules in Databricks notebooks:

```python
import sys

sys.path.append("../src")

from Agents import weather_agent
from Weather_Tools import get_weather
from Email_Tool import send_email
```


## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/weather-alert-assistant.git
cd weather-alert-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini

SENDGRIP_API_KEY=your_sendgrid_key
```

## ▶️ Run the Application

```bash
python app.py
```

Open the Gradio URL displayed in the terminal.

## 💬 Example Queries

* "What's the weather in Bengaluru today?"
* "Notify me if heavy rain is expected in Mumbai."
* "Send today's weather report for Munnar to [john@example.com](mailto:john@example.com)."
* "Alert me when temperatures exceed 40°C in Delhi."

## 📊 Tracing & Observability

Every workflow execution generates a unique trace ID for debugging and monitoring.

```python
with trace(
    workflow_name="weather_alert_workflow",
    trace_id=trace_id
):
    result = await Runner.run(agent, user_input)
```

## 🔮 Future Enhancements

* SMS and WhatsApp notifications
* Daily scheduled weather reports
* Multi-location monitoring
* Weather trend analytics dashboard
* Calendar integration
* Slack and Microsoft Teams notifications

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.
