"""
Data Routing Crew for Snowflake MCP Integration.

This crew routes user queries to the appropriate Snowflake data repository
using MCP tools.
"""

import os
from typing import List, Optional

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from corsaiflow.tools import DataRepositoryTool, SnowflakeMCPTool


@CrewBase
class DataRoutingCrew:
    """Data Routing Crew for Snowflake MCP"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @property
    def mcp_server_url(self) -> str:
        """Get MCP server URL from environment."""
        return os.getenv(
            "SNOWFLAKE_MCP_SERVER_URL",
            "https://your-account.snowflakecomputing.com"
        )

    @property
    def database(self) -> str:
        """Get database name from environment."""
        return os.getenv("SNOWFLAKE_DATABASE", "your_database")

    @property
    def schema(self) -> str:
        """Get schema name from environment."""
        return os.getenv("SNOWFLAKE_SCHEMA", "your_schema")

    @property
    def server_name(self) -> str:
        """Get MCP server name from environment."""
        return os.getenv("SNOWFLAKE_MCP_SERVER_NAME", "your_mcp_server")

    @property
    def access_token(self) -> Optional[str]:
        """Get access token from environment."""
        return os.getenv("SNOWFLAKE_ACCESS_TOKEN")

    @property
    def repositories(self) -> List[dict]:
        """
        Load data repository configurations.

        This can be extended to load from a config file or database.
        """
        # Default repositories - should be configured based on your setup
        return [
            {
                "name": "Product Search",
                "description": "Search service for product information, inventory, and catalog data",
                "tool_name": "product-search",
                "tool_type": "search"
            },
            {
                "name": "Revenue Analytics",
                "description": "Semantic view for revenue analysis, sales data, and financial metrics",
                "tool_name": "revenue-semantic-view",
                "tool_type": "analyst"
            },
            {
                "name": "SQL Database",
                "description": "Direct SQL access to database tables and views",
                "tool_name": "sql_exec_tool",
                "tool_type": "sql"
            },
            {
                "name": "Cortex Agent",
                "description": "AI agent for complex data queries and analysis",
                "tool_name": "agent_1",
                "tool_type": "agent"
            }
        ]

    @agent
    def query_router(self) -> Agent:
        """Agent that routes queries to appropriate data repositories."""
        # Create data repository tool
        repo_tool = DataRepositoryTool(repositories=self.repositories)

        return Agent(
            config=self.agents_config["query_router"],  # type: ignore[index]
            tools=[repo_tool],
            verbose=True,
        )

    @agent
    def data_retriever(self) -> Agent:
        """Agent that retrieves data from Snowflake using MCP tools."""
        # Create Snowflake MCP tool
        mcp_tool = SnowflakeMCPTool(
            mcp_server_url=self.mcp_server_url,
            database=self.database,
            schema=self.schema,
            server_name=self.server_name,
            access_token=self.access_token
        )

        return Agent(
            config=self.agents_config["data_retriever"],  # type: ignore[index]
            tools=[mcp_tool],
            verbose=True,
        )

    @task
    def route_query(self) -> Task:
        """Task to analyze user query and determine appropriate data repository."""
        return Task(
            config=self.tasks_config["route_query"],  # type: ignore[index]
            agent=self.query_router(),
        )

    @task
    def retrieve_data(self) -> Task:
        """Task to retrieve data from the selected repository."""
        return Task(
            config=self.tasks_config["retrieve_data"],  # type: ignore[index]
            agent=self.data_retriever(),
            context=[self.route_query()],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Data Routing Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

