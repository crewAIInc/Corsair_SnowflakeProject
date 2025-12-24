"""
Data Repository Discovery Tool.

This tool helps agents understand which data repositories are available
and which one should be queried for a given user question.
"""

from typing import Dict, List, Type

from pydantic import BaseModel, Field

from crewai.tools import BaseTool


class DataRepositoryToolInput(BaseModel):
    """Input schema for Data Repository Tool."""

    user_query: str = Field(
        ...,
        description="The user's query about data in Snowflake."
    )


class DataRepositoryTool(BaseTool):
    """
    Tool for discovering and selecting appropriate data repositories.

    This tool maintains a registry of available data repositories and their
    descriptions, helping agents decide which repository to query.
    """

    name: str = "data_repository_selector"
    description: str = (
        "Tool for selecting the appropriate data repository for a user query. "
        "Use this to understand which data repository (Cortex Search, Analyst, "
        "SQL database, or Agent) should be queried based on the user's question. "
        "Returns the recommended repository name and tool to use."
    )
    args_schema: Type[BaseModel] = DataRepositoryToolInput

    def __init__(
        self,
        repositories: List[Dict[str, str]] = None,
        **kwargs
    ):
        """
        Initialize Data Repository Tool.

        Args:
            repositories: List of repository configurations with keys:
                - name: Repository name
                - description: What data it contains
                - tool_name: MCP tool name to use
                - tool_type: Type of tool (search, analyst, sql, agent)
        """
        super().__init__(**kwargs)
        self.repositories = repositories or []

    def _run(self, user_query: str) -> str:
        """
        Analyze user query and recommend appropriate data repository.

        Args:
            user_query: The user's query about data

        Returns:
            Recommendation of which repository and tool to use
        """
        if not self.repositories:
            return (
                "No data repositories configured. "
                "Please configure repositories in the tool initialization."
            )

        # Simple keyword-based matching (can be enhanced with LLM)
        query_lower = user_query.lower()

        recommendations = []
        for repo in self.repositories:
            score = 0
            repo_desc = repo.get("description", "").lower()
            repo_name = repo.get("name", "").lower()

            # Check if query keywords match repository description
            if any(keyword in repo_desc for keyword in query_lower.split()):
                score += 2

            if any(keyword in repo_name for keyword in query_lower.split()):
                score += 1

            # Check for specific tool type indicators
            tool_type = repo.get("tool_type", "").lower()
            if tool_type == "search" and any(word in query_lower for word in ["search", "find", "look for"]):
                score += 2
            elif tool_type == "analyst" and any(word in query_lower for word in ["analyze", "analysis", "insight", "report"]):
                score += 2
            elif tool_type == "sql" and any(word in query_lower for word in ["query", "select", "table", "database"]):
                score += 2
            elif tool_type == "agent" and any(word in query_lower for word in ["agent", "assistant", "help"]):
                score += 2

            if score > 0:
                recommendations.append({
                    "repository": repo.get("name"),
                    "tool_name": repo.get("tool_name"),
                    "tool_type": repo.get("tool_type"),
                    "description": repo.get("description"),
                    "score": score
                })

        if not recommendations:
            return (
                f"Could not find a matching repository for query: '{user_query}'. "
                f"Available repositories: {[r['name'] for r in self.repositories]}"
            )

        # Sort by score and return top recommendation
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        top_rec = recommendations[0]

        result = {
            "recommended_repository": top_rec["repository"],
            "tool_name": top_rec["tool_name"],
            "tool_type": top_rec["tool_type"],
            "description": top_rec["description"],
            "confidence": "high" if top_rec["score"] >= 3 else "medium"
        }

        if len(recommendations) > 1:
            result["alternative_repositories"] = [
                {
                    "repository": r["repository"],
                    "tool_name": r["tool_name"],
                    "score": r["score"]
                }
                for r in recommendations[1:3]  # Top 2 alternatives
            ]

        import json
        return json.dumps(result, indent=2)

