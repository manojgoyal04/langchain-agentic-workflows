# LangChain Agentic Workflows

A LangChain-based search agent that uses OpenAI's GPT-4o model and Tavily search to perform intelligent web searches and provide formatted results.

## Features

- 🤖 **Intelligent Search Agent**: Powered by OpenAI's GPT-4o model
- 🔍 **Web Search Integration**: Uses Tavily search for advanced web searching
- 🎨 **Beautiful Terminal Output**: Rich formatting with tables, panels, and progress indicators
- 📊 **Step-by-Step Execution**: Visual display of agent execution steps
- 🔧 **Tool Call Tracking**: See exactly what tools the agent uses and when

## Requirements

- Python >= 3.14
- OpenAI API Key
- Tavily API Key (get one for free at [https://tavily.com/](https://tavily.com/))

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd langchain-agentic-workflows
```

2. Install dependencies using `uv` (or your preferred package manager):
```bash
uv sync
```

Or if using pip:
```bash
pip install -r requirements.txt
```

## Setup

1. Create a `.env` file in the project root:
```bash
touch .env
```

2. Add your API keys to the `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Usage

Run the main script:
```bash
python main.py
```

The agent will execute a search query (currently configured to search for Digital Marketing Director job postings in Bangalore on LinkedIn) and display the results in a beautifully formatted terminal output.

### Current Query

The default query searches for:
> "search for 3 job postings for an Digital Marketing Director in the bangalore on linkedin and list their details?"

You can modify the query in `main.py` at line 177 to search for different information.

## Project Structure

```
langchain-agentic-workflows/
├── main.py              # Main application code
├── pyproject.toml       # Project dependencies and configuration
├── README.md           # This file
└── .env                # Environment variables (create this)
```

## Dependencies

- `langchain` - Core LangChain framework
- `langchain-openai` - OpenAI integration
- `langchain-tavily` - Tavily search tool integration
- `python-dotenv` - Environment variable management
- `rich` - Beautiful terminal formatting
- `black` - Code formatting
- `isort` - Import sorting

## How It Works

1. **Agent Creation**: The `create_search_agent()` function initializes:
   - OpenAI's GPT-4o model (temperature=0 for deterministic results)
   - Tavily search tool with advanced search depth
   - A LangChain agent that combines both

2. **Query Execution**: The agent processes the query and:
   - Determines if a search is needed
   - Calls the Tavily search tool when appropriate
   - Processes search results
   - Generates a final response

3. **Output Formatting**: The `format_agent_output()` function displays:
   - The original query in a styled panel
   - A step-by-step table showing all agent actions
   - Tool calls and their results
   - The final formatted result in a markdown panel

## Example Output

The application provides:
- 🔍 **Search Query Panel**: Shows the query being processed
- 📊 **Agent Execution Steps Table**: Lists all steps including:
  - Human messages
  - AI agent responses
  - Tool calls (🔧)
  - Tool results
- ✨ **Final Result Panel**: Displays the formatted answer in markdown

## License

This project is part of a LangChain course.

