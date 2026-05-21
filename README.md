# AI Bootcamp — Homework 2

A Python learning project for experimenting with AI agents, external API integrations, and LangGraph-powered workflows.

---

## Overview

This project contains bootcamp exercises focused on building AI-powered workflows. The current implementation features a **Weather & Country Information Assistant** — an AI agent that combines two tools to answer questions about whether conditions and country details for any given location.

The agent uses **LangGraph** and **OpenAI GPT-4.1-mini** to intelligently decide when and how to invoke each tool, then synthesizes the results into a coherent, user-friendly response.

---

## Features

- 🌤️ **Weather Lookup** — Fetches real-time weather data (temperature, humidity, description, and feels-like) for any city via OpenWeatherMap, and recommends appropriate clothing based on the current temperature.
- 🌍 **Country Information** — Retrieves key country details (capital city, currency, and population) from the REST Countries API.
- 🤖 **AI Agent Orchestration** — Uses a LangGraph agent to coordinate both tools and return a comprehensive, unified answer.
- 📡 **Streaming Output** — Streams agent responses in real-time, showing tool calls, results, and token usage as they are generated.

---

## Project Structure

```
homework-2/
├── main.py            # Agent definition, tool functions, and execution logic
├── pyproject.toml     # Project metadata and dependencies
├── uv.lock            # Locked dependency versions
├── .env.homework-2    # Environment variables (API keys — not committed to version control)
└── README.md          # Project documentation
```

---

## Prerequisites

- **Python:** Version 3.12 or higher
- **Package Manager:** [`uv`](https://github.com/astral-sh/uv) (recommended)

---

## Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

using `uv`:

```bash
uv sync
```

### 4. Configure Environment Variables

Create a `.env.homework-2` file in the project root and populate it with your API keys:

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# OpenWeatherMap
OPENWEATHER_API_KEY=your_openweathermap_api_key

# LangSmith (optional — for tracing)
LANGCHAIN_API_KEY=
LANGCHAIN_TRACING_V2=
LANGCHAIN_PROJECT=

# Ollama (optional)
OLLAMA_BASE_URL=http://localhost:11434

# Environment
ENVIRONMENT=development
```

> ⚠️ **Never commit your `.env` file or API keys to version control.**

### 5. Run the Application

```bash
python main.py
```

---

## Tools

### `check_weather(location: str)`

Calls the [OpenWeatherMap API](https://openweathermap.org/api) to retrieve current weather conditions for a given city. Returns temperature, humidity, a weather description, and a clothing recommendation based on the following thresholds:

| Temperature Range | Condition     | Recommendation                        |
|-------------------|---------------|---------------------------------------|
| Below 0°C         | Freezing      | Wear very thick clothing              |
| 0°C – 12°C        | Cold / Chilly | Wear a coat                           |
| 12°C – 27°C       | Warm          | Light clothing; ideal for activities  |
| 27°C – 35°C       | Hot           | Very light clothing; stay hydrated    |
| Above 35°C        | Dangerous     | Stay indoors; keep cooling system on  |

### `get_country_information(name: str)`

Calls the [REST Countries API](https://restcountries.com/) to retrieve structured information about a country by name. Returns the common name, capital city, currency, and population.

---

## Dependencies

| Package             | Purpose                                      |
|---------------------|----------------------------------------------|
| `langchain`         | Core LLM framework                           |
| `langchain-openai`  | OpenAI model integration                     |
| `langgraph`         | Agent orchestration and graph-based workflows|
| `openai`            | OpenAI API client                            |
| `requests`          | HTTP calls to external APIs                  |
| `python-dotenv`     | Loading environment variables from `.env`    |

---

## Example Usage

**User prompt:**
> *"What is the weather in Tennessee, USA and provide information about country USA? Also, add information about the country like capital, currency and population."*

**Agent behaviour:**
1. Calls `check_weather("Tennessee, US")` → returns real-time weather + clothing advice
2. Calls `get_country_information("USA")` → returns capital, currency, and population
3. Synthesizes both results into a single, coherent response

---

## License

This project is for educational purposes as part of an AI Bootcamp curriculum.
