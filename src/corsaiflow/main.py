#!/usr/bin/env python

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from corsaiflow.crews.data_routing_crew.data_routing_crew import DataRoutingCrew


class DataQueryState(BaseModel):
    user_query: str = ""
    selected_repository: str = ""
    tool_name: str = ""
    query_result: str = ""


class DataQueryFlow(Flow[DataQueryState]):
    """Flow for routing and executing Snowflake data queries."""

    @start()
    def receive_query(self, crewai_trigger_payload: dict = None):
        """Receive and store the user query."""
        print("Receiving user query")

        # Use trigger payload if available
        if crewai_trigger_payload:
            self.state.user_query = crewai_trigger_payload.get('user_query', '')
            print(f"User query: {self.state.user_query}")
        else:
            # Default query for testing
            self.state.user_query = "What products are available in our inventory?"

    @listen(receive_query)
    def route_and_retrieve_data(self):
        """Route the query and retrieve data from Snowflake."""
        print(f"Routing query: {self.state.user_query}")

        result = (
            DataRoutingCrew()
            .crew()
            .kickoff(inputs={"user_query": self.state.user_query})
        )

        print("Query result:", result.raw)
        self.state.query_result = result.raw

    @listen(route_and_retrieve_data)
    def format_response(self):
        """Format the final response for the user."""
        print("Formatting response")
        # The response is already formatted by the crew
        # This step can be used for additional formatting if needed
        pass


def kickoff(**kwargs):
    """
    Kickoff the data query flow.

    This function is called by 'crewai run' command.
    It accepts keyword arguments that can be passed to the flow.

    Example usage:
        crewai run
        crewai run --user_query "What products are in stock?"
    """
    data_flow = DataQueryFlow()

    # If kwargs are provided, pass them as trigger payload
    # This allows passing user_query directly: crewai run --user_query "query text"
    if kwargs:
        # Ensure user_query is in the payload if provided
        trigger_payload = kwargs.copy()
        result = data_flow.kickoff({"crewai_trigger_payload": trigger_payload})
        return result
    else:
        # No arguments provided, use default query
        result = data_flow.kickoff()
        return result


def plot():
    """Plot the data query flow."""
    data_flow = DataQueryFlow()
    data_flow.plot()


def run_with_trigger():
    """
    Run the data query flow with trigger payload.
    """
    import json
    import sys

    # Get trigger payload from command line argument
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    # Create flow and kickoff with trigger payload
    data_flow = DataQueryFlow()

    try:
        result = data_flow.kickoff({"crewai_trigger_payload": trigger_payload})
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the data query flow: {e}")


def query_snowflake_data():
    """Kickoff the data query flow."""
    data_flow = DataQueryFlow()
    data_flow.kickoff()


def query_snowflake_with_trigger():
    """
    Run the data query flow with trigger payload.
    """
    import json
    import sys

    # Get trigger payload from command line argument
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    # Create flow and kickoff with trigger payload
    data_flow = DataQueryFlow()

    try:
        result = data_flow.kickoff({"crewai_trigger_payload": trigger_payload})
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the data query flow: {e}")


if __name__ == "__main__":
    kickoff()
