# Create AI Agent

## 🧠 Overview

The **Create AI Agent** project provides a user-friendly interface to create AI agents using different voice providers. It supports:

- **Retell**: A platform offering LLM-based voice agents.
- **VAPI**: A service enabling voice interactions via APIs.

Users can select a provider and voice to generate a personalized AI agent.

## 🚀 Features

- **Dynamic Voice Selection**: Choose from a variety of voices based on the selected provider.
- **Provider-Specific Configuration**: Supports unique configurations for Retell and VAPI.
- **Responsive Design**: Optimized for both desktop and mobile devices.

## 🛠️ Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- A virtual environment manager (e.g., `venv` or `virtualenv`)

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/create-ai-agent.git
   cd create-ai-agent/server

2. Create and activate Virtual Environment:

   ```bash
   python -m venv venv
   source venv/Scripts/activate

3. Set up environment variables:

   ```bash
   RETELL_API_KEY=your_retell_api_key
   VAPI_API_KEY=your_vapi_api_key
   llm_id=your_llm_id

4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload


  





