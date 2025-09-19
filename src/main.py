import os
import logging
from coordinator import Coordinator
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.memory_agent import MemoryAgent
from memory.enhanced_memory import EnhancedMemory

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """Initializes and runs the multi-agent chat system."""
    logging.info("Initializing the multi-agent system...")

    # Initialize the memory system
    memory_system = EnhancedMemory()

    # Initialize worker agents
    research_agent = ResearchAgent()
    analysis_agent = AnalysisAgent()
    memory_agent = MemoryAgent(memory_system)

    # Initialize the coordinator with all agents
    coordinator = Coordinator(research_agent, analysis_agent, memory_agent)

    logging.info("System initialized. You can now ask questions.")
    print("\nWelcome to the Multi-Agent Chat System! Type 'exit' to quit.")

    try:
        while True:
            user_query = input("\n👤 You: ")
            if user_query.lower() == 'exit':
                break

            if not user_query:
                continue

            print("🤖 System is thinking...")
            final_response = coordinator.handle_query(user_query)
            print(f"\n💡 Final Answer: {final_response}")

    except KeyboardInterrupt:
        print("\nExiting system...")
    finally:
        logging.info("Shutting down.")


if __name__ == "__main__":
    main()