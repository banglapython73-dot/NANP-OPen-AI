# This file will contain the architecture for our Specialist Agent Swarm.
import os
from duckduckgo_search import DDGS
import wikipedia

# Using mocked tools to bypass environmental network restrictions and test agent logic.
class Toolbelt:
    """
    A collection of mocked tools that return pre-defined data.
    This allows us to test the agent swarm's logic without network dependencies.
    """
    def __init__(self):
        pass

    def search_web(self, query: str, max_results: int = 5):
        """Returns a mocked web search result."""
        print(f"MOCKED TOOL: Simulating web search for '{query}'...")
        if "openai" in query.lower():
            return [
                {"title": "OpenAI - Wikipedia", "body": "OpenAI is an American artificial intelligence (AI) research laboratory consisting of the non-profit OpenAI, Inc. ... Its founders are Sam Altman, Elon Musk, Greg Brockman, Ilya Sutskever, Wojciech Zaremba, and John Schulman."},
                {"title": "About OpenAI", "body": "OpenAI was founded in 2015 by a group of technology leaders who were concerned about the potential risks of artificial intelligence."},
            ]
        return [{"title": "Mock Search Result", "body": "This is a simulated search result for your query."}]

    def search_wikipedia(self, query: str, sentences: int = 3):
        """Returns a mocked Wikipedia summary."""
        print(f"MOCKED TOOL: Simulating Wikipedia search for '{query}'...")
        if "openai" in query.lower():
            return "OpenAI is an artificial intelligence research organization. It was founded in December 2015 by Sam Altman, Greg Brockman, Elon Musk, Ilya Sutskever, Wojciech Zaremba, and John Schulman. Their mission is to ensure that artificial general intelligence benefits all of humanity."
        return f"This is a mocked Wikipedia summary for the query: '{query}'."

class Agent:
    """
    Base class for all specialist agents.
    """
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.toolbelt = Toolbelt()

    def run(self, task: str) -> str:
        """The main execution method for an agent."""
        raise NotImplementedError("Each agent must implement the 'run' method.")

class FactFinderAgent(Agent):
    """
    This agent specializes in finding facts quickly from reliable sources.
    """
    def __init__(self):
        super().__init__(
            name="FactFinder",
            role="To find, verify, and consolidate facts from web search and Wikipedia."
        )

    def run(self, task: str) -> str:
        print(f"AGENT '{self.name}': Starting task - {task}")

        # --- Step 1: Search the web ---
        web_results = self.toolbelt.search_web(task)

        # --- Step 2: Search Wikipedia ---
        wiki_summary = self.toolbelt.search_wikipedia(task)

        # --- Step 3: Consolidate findings ---
        # For now, we'll just combine the results into a simple report.
        # In the future, an AI model would summarize this.

        report = f"--- FactFinder Report for '{task}' ---\n\n"
        report += "== Wikipedia Summary ==\n"
        report += f"{wiki_summary}\n\n"
        report += "== Web Search Results ==\n"

        if web_results:
            for i, result in enumerate(web_results, 1):
                report += f"{i}. {result.get('title', 'No Title')}\n"
                report += f"   - {result.get('body', 'No snippet')}\n"
        else:
            report += "No web results found.\n"

        print(f"AGENT '{self.name}': Task completed.")
        return report

# Import the powerful model's generation function directly to prevent circular imports
from .powerful_model import generate_powerful_response

# --- Controller ---
def run_agent_swarm(prompt: str):
    """
    Controller that runs the agent swarm and then uses a powerful AI to synthesize the results.
    """
    # Step 1: Run the FactFinder agent to gather raw data
    fact_finder = FactFinderAgent()
    raw_report = fact_finder.run(prompt)

    print("AGENT SWARM: Raw report gathered. Now synthesizing with powerful model...")

    # Step 2: Create a new prompt for the powerful AI to summarize the raw report
    synthesis_prompt = (
        f"Based on the following research report, please provide a clear and concise answer to the user's original question: '{prompt}'.\n\n"
        f"--- Research Report ---\n"
        f"{raw_report}\n"
        f"--- End of Report ---\n\n"
        f"Please synthesize the information into a final answer."
    )

    # Step 3: Call the powerful AI to generate the final, polished answer
    final_answer = generate_powerful_response(synthesis_prompt)

    return final_answer
