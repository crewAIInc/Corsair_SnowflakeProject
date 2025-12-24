# Snowflake MCP Setup Guide

This guide explains how to configure and use the Snowflake MCP integration with CrewAI.

## Prerequisites

1. A Snowflake account with access to create MCP servers
2. An MCP server object created in Snowflake (see [Snowflake MCP Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp))
3. OAuth authentication configured (or Programmatic Access Token)

## Environment Variables

Set the following environment variables before running the crew:

```bash
export SNOWFLAKE_MCP_SERVER_URL="https://your-account.snowflakecomputing.com"
export SNOWFLAKE_DATABASE="your_database"
export SNOWFLAKE_SCHEMA="your_schema"
export SNOWFLAKE_MCP_SERVER_NAME="your_mcp_server"
export SNOWFLAKE_ACCESS_TOKEN="your_oauth_access_token"
```

## Creating an MCP Server in Snowflake

1. Navigate to your desired database and schema in Snowflake
2. Create the MCP server using SQL:

```sql
CREATE MCP SERVER my_mcp_server
FROM SPECIFICATION $$
  tools:
    - name: "product-search"
      type: "CORTEX_SEARCH_SERVICE_QUERY"
      identifier: "database1.schema1.Cortex_Search_Service1"
      description: "cortex search service for all products"
      title: "Product Search"
    - name: "revenue-semantic-view"
      type: "CORTEX_ANALYST_MESSAGE"
      identifier: "database1.schema1.Semantic_View_1"
      description: "Semantic view for all revenue tables"
      title: "Semantic view for revenue"
    - name: "sql_exec_tool"
      type: "SYSTEM_EXECUTE_SQL"
      description: "A tool to execute SQL queries against the connected Snowflake database."
      title: "SQL Execution Tool"
    - name: "agent_1"
      type: "CORTEX_AGENT_RUN"
      identifier: "db.schema.agent"
      description: "agent that gives the ability to..."
      title: "Agent V2"
$$
```

## OAuth Authentication Setup

1. Create a security integration:

```sql
CREATE SECURITY INTEGRATION my_oauth_integration
  TYPE = OAUTH
  OAUTH_CLIENT = CUSTOM
  ENABLED = TRUE
  OAUTH_CLIENT_TYPE = 'CONFIDENTIAL'
  OAUTH_REDIRECT_URI = '<redirect_URI>'
```

2. Retrieve client ID and secrets:

```sql
SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('MY_OAUTH_INTEGRATION');
```

3. Use the OAuth flow to obtain an access token, or use a Programmatic Access Token (PAT).

## Configuring Data Repositories

The data repositories are configured in `data_routing_crew.py`. Update the `_load_repositories()` method to match your MCP server configuration:

```python
def _load_repositories(self) -> List[dict]:
    return [
        {
            "name": "Product Search",
            "description": "Search service for product information",
            "tool_name": "product-search",  # Must match MCP tool name
            "tool_type": "search"
        },
        {
            "name": "Revenue Analytics",
            "description": "Semantic view for revenue analysis",
            "tool_name": "revenue-semantic-view",  # Must match MCP tool name
            "tool_type": "analyst"
        },
        # Add more repositories as needed
    ]
```

## Usage

### Using the Flow

```python
from corsaiflow.main import DataQueryFlow

# Create and run the flow
flow = DataQueryFlow()
result = flow.kickoff({
    "crewai_trigger_payload": {
        "user_query": "What products are available in our inventory?"
    }
})
```

### Using the Crew Directly

```python
from corsaiflow.crews.data_routing_crew.data_routing_crew import DataRoutingCrew

crew = DataRoutingCrew()
result = crew.crew().kickoff(
    inputs={"user_query": "Show me revenue trends for Q4"}
)
```

## Tool Types

The integration supports the following MCP tool types:

1. **CORTEX_SEARCH_SERVICE_QUERY**: Unstructured search on data
   - Arguments: `{"query": "search text", "limit": 10, "columns": [...]}`

2. **CORTEX_ANALYST_MESSAGE**: Generate insights from semantic views
   - Arguments: `{"message": "your question"}`

3. **SYSTEM_EXECUTE_SQL**: Execute SQL queries
   - Arguments: `{"query": "SELECT ..."}`

4. **CORTEX_AGENT_RUN**: Interact with Cortex Agents
   - Arguments: `{"message": "your message"}`

5. **GENERIC**: Custom UDFs and stored procedures
   - Arguments: Varies based on function signature

## Troubleshooting

### Authentication Issues

- Ensure your access token is valid and not expired
- Check that the OAuth integration is properly configured
- Verify the token has the necessary permissions

### Tool Not Found

- Verify the tool name in your repository configuration matches the MCP server tool name
- Check that you have USAGE permission on the MCP server
- Ensure you have the required permissions for the specific tool type

### Connection Issues

- Verify the MCP server URL is correct
- Check that the database, schema, and server name are correct
- Ensure network connectivity to Snowflake

## Security Recommendations

1. Use OAuth authentication instead of hardcoded tokens
2. Store credentials in environment variables or secure secret management
3. Follow the least-privilege principle for MCP server and tool permissions
4. Verify third-party MCP servers before use
5. Use hyphens (`-`) instead of underscores (`_`) in hostnames

