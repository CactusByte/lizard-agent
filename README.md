![image](https://github.com/user-attachments/assets/eee6c02d-83d3-4b4d-892a-f2fabf7d7d5d)


# Lizard Agent 🦎

An AI-powered agent that can interact with Pump.fun to create and manage tokens, with built-in captcha solving capabilities.

## Features

- 🤖 AI-powered agent using GPT-4
- 🔍 Web search capabilities via Tavily
- 🪙 Token creation on Pump.fun
- 🤖 Automated captcha solving using CapSolver
- 💬 Interactive chat interface

## Prerequisites

- Python 3.9 - 3.11 (3.13 not recommended)
- OpenAI API key
- Tavily API key
- CapSolver API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lizardbackend.git
cd lizardbackend
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix/MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
CAPSOLVER_API_KEY=your_capsolver_api_key
```

## Usage

1. Start the agent:
```bash
python agent_chat.py
```

2. Interact with the agent using natural language. Example commands:
```
Create token with name TEST, ticker TEST, description "This is a test token"
```

## Token Creation Format

When creating a token, use the following format:
```
Create token with name NAME, ticker TICKER, description DESCRIPTION
```

Example:
```
Create token with name Yongi, ticker YNG, description "Best coin ever"
```

## Features in Detail

### AI Agent
- Uses GPT-4 for natural language understanding
- Can handle complex queries and instructions
- Integrates with web search for real-time information

### Token Creation
- Automated token creation on Pump.fun
- Handles captcha solving automatically
- Supports custom token names, tickers, and descriptions

### Captcha Solving
- Uses CapSolver for automated captcha solving
- Supports hCaptcha challenges
- Handles token creation verification

## Error Handling

The agent includes comprehensive error handling for:
- API failures
- Invalid input formats
- Network issues
- Captcha solving failures

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4
- Tavily for search capabilities
- CapSolver for captcha solving
- Pump.fun for the token creation platform 
