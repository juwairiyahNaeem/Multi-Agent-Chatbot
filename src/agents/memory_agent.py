import logging
from .base_agent import BaseAgent


class MemoryAgent(BaseAgent):
    """An agent to manage the system's memory."""

    def __init__(self, memory_system):
        self.memory = memory_system
        self.logger = logging.getLogger(__name__)

    def execute_task(self, task, args):
        self.logger.info(f"Executing task: {task} with args: {args}")
        try:
            if task == "save_knowledge":
                self.memory.add_knowledge(
                    content=args["content"],
                    topic=args["topic"],
                    source=args["source"],
                    task_id=args["task_id"]
                )
                return {"content": "Knowledge saved.", "confidence": 1.0}

            elif task == "save_conversation":
                self.memory.add_conversation_turn(
                    role=args["role"],
                    content=args["content"]
                )
                return {"content": "Conversation turn saved.", "confidence": 1.0}

            elif task == "search_knowledge":
                results = self.memory.search_knowledge(args["query"])
                if results and results['distances'][0][0] < 0.5:  # Example threshold
                    return {
                        "content": results['documents'][0][0],
                        "confidence": 1.0 - results['distances'][0][0]
                    }
                return {"content": None, "confidence": 0.0}

            elif task == "search_conversation":
                # A simple implementation to get the last relevant chat
                history = self.memory.get_conversation_history()
                query_words = set(args["query"].lower().split())
                for turn in reversed(history):
                    if query_words.intersection(set(turn['content'].lower().split())):
                        return {"content": f"We previously discussed: '{turn['content']}'", "confidence": 0.8}
                return {"content": "I don't recall that discussion.", "confidence": 0.3}

            else:
                return {"content": f"Unknown task for MemoryAgent: {task}", "confidence": 0.1}

        except Exception as e:
            self.logger.error(f"Error in MemoryAgent task '{task}': {e}")
            return {"content": f"Failed to execute memory task '{task}'.", "confidence": 0.0}