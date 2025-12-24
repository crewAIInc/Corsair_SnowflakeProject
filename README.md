# CorsaiFlow Crew

Welcome to the CorsaiFlow Crew project, powered by [crewAI](https://crewai.com). This project demonstrates a multi-agent AI system that integrates with Snowflake's Model Context Protocol (MCP) to intelligently route and execute data queries across multiple data repositories.

## Features

- **Snowflake MCP Integration**: Connect to Snowflake's managed MCP server to access Cortex Search, Cortex Analyst, SQL execution, and Cortex Agents
- **Intelligent Query Routing**: Automatically determine which data repository is best suited for a user's query
- **Multi-Agent Workflow**: Two specialized agents work together to route queries and retrieve data
- **Flow-Based Architecture**: Built on CrewAI's flow system for orchestrated task execution

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Environment Setup

**Add your API keys and Snowflake configuration to the `.env` file:**

```bash
OPENAI_API_KEY=your_openai_api_key

# Snowflake MCP Configuration
SNOWFLAKE_MCP_SERVER_URL=https://your-account.snowflakecomputing.com
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_MCP_SERVER_NAME=your_mcp_server
SNOWFLAKE_ACCESS_TOKEN=your_oauth_access_token
```

See [SNOWFLAKE_MCP_SETUP.md](SNOWFLAKE_MCP_SETUP.md) for detailed setup instructions.

### Customizing

- Modify `src/corsaiflow/crews/data_routing_crew/config/agents.yaml` to customize agent behavior
- Modify `src/corsaiflow/crews/data_routing_crew/config/tasks.yaml` to customize task definitions
- Update `src/corsaiflow/crews/data_routing_crew/data_routing_crew.py` to configure data repositories
- Modify `src/corsaiflow/main.py` to add custom flows and inputs

## Running the Project

To kickstart your flow and begin execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the corsaiFlow Flow as defined in your configuration.

### Running the Data Query Flow

To run the Snowflake data query flow:

```bash
# Using Python directly
python -m corsaiflow.main query_snowflake_data

# Or with a trigger payload
python -m corsaiflow.main query_snowflake_with_trigger '{"user_query": "What products are in stock?"}'
```

The default example will route a query about product inventory and retrieve data from the appropriate Snowflake repository.

## Understanding Your Crew

### Data Routing Crew

The Data Routing Crew consists of two specialized agents:

1. **Query Router Agent**: Analyzes user queries and determines which Snowflake data repository (Cortex Search, Cortex Analyst, SQL database, or Cortex Agent) is most appropriate for answering the question.

2. **Data Retriever Agent**: Executes queries against the selected Snowflake repository using MCP tools, formats the results, and presents them to the user.

### Crew Structure

- **Agents**: Defined in `src/corsaiflow/crews/data_routing_crew/config/agents.yaml`
- **Tasks**: Defined in `src/corsaiflow/crews/data_routing_crew/config/tasks.yaml`
- **Tools**:
  - `SnowflakeMCPTool`: Wraps Snowflake MCP server interactions
  - `DataRepositoryTool`: Helps select appropriate data repositories

### Flow Architecture

The `DataQueryFlow` orchestrates the query process:
1. Receives user query
2. Routes query to appropriate repository
3. Retrieves data from Snowflake
4. Formats and returns results

## Support

For support, questions, or feedback regarding the {{crew_name}} Crew or crewAI.

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
