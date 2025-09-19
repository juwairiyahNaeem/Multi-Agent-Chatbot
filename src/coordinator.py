import logging
import uuid
import json


class Coordinator:
    """The Coordinator agent that manages the workflow."""

    def __init__(self, research_agent, analysis_agent, memory_agent):
        self.research_agent = research_agent
        self.analysis_agent = analysis_agent
        self.memory_agent = memory_agent
        self.logger = logging.getLogger(__name__)

    def _create_plan(self, query):
        """
        Creates a simple, rule-based plan based on query keywords.
        This is a fallback mechanism if an LLM is not used or fails.
        """
        query_lower = query.lower()
        plan = []

        # Memory Check First
        if any(k in query_lower for k in ["remember", "previously", "earlier", "recall"]):
            plan.append({"agent": "memory", "task": "search_conversation", "args": {"query": query}})
            return plan

        # Research-heavy tasks
        if any(k in query_lower for k in ["find", "research", "what are", "who is"]):
            plan.append({"agent": "research", "task": "find_information", "args": {"topic": query}})

        # Analysis-heavy tasks that may follow research
        if any(k in query_lower for k in ["analyze", "compare", "summarize", "trade-offs", "efficiency"]):
            if not plan:  # If no research step was added, add one
                plan.append({"agent": "research", "task": "find_information", "args": {"topic": query}})
            plan.append({"agent": "analysis", "task": "analyze_data", "args": {"data_key": "last_output"}})

        # If no plan was created, default to a research task
        if not plan:
            plan.append({"agent": "research", "task": "find_information", "args": {"topic": query}})

        return plan

    def handle_query(self, user_query):
        """
        Handles a user query by creating a plan, executing it, and returning a final answer.
        """
        self.logger.info(f"Received query: '{user_query}'")
        task_id = str(uuid.uuid4())

        # 1. Check memory for similar, previously answered questions
        similar_knowledge = self.memory_agent.execute_task("search_knowledge", {"query": user_query})
        if similar_knowledge and similar_knowledge['confidence'] > 0.85:
            self.logger.info("Found a similar, highly relevant answer in memory. Returning cached result.")
            return f"(From memory) {similar_knowledge['content']}"

        # 2. If no similar answer, create a new plan
        plan = self._create_plan(user_query)
        self.logger.info(f"Created plan: {json.dumps(plan, indent=2)}")

        # 3. Execute the plan
        context = {}
        last_output = None

        for step in plan:
            agent_name = step["agent"]
            task = step["task"]
            args = step["args"]

            # Substitute placeholder arguments
            if "data_key" in args and args["data_key"] == "last_output":
                args["data"] = last_output
                del args["data_key"]

            self.logger.info(f"Executing step: agent='{agent_name}', task='{task}'")

            try:
                if agent_name == "research":
                    result = self.research_agent.execute_task(task, args)
                elif agent_name == "analysis":
                    result = self.analysis_agent.execute_task(task, args)
                elif agent_name == "memory":
                    result = self.memory_agent.execute_task(task, args)
                else:
                    raise ValueError(f"Unknown agent: {agent_name}")

                last_output = result['content']
                context[f"{agent_name}_{task}_result"] = result
                self.logger.info(f"Step completed with output: {result}")

            except Exception as e:
                self.logger.error(f"Error executing step {step}: {e}")
                return "I'm sorry, an error occurred while processing your request."

        # 4. Synthesize the final result (for now, just the last output)
        final_answer = last_output

        # 5. Save the new knowledge to memory
        self.logger.info("Saving new findings to memory.")
        self.memory_agent.execute_task("save_knowledge", {
            "topic": user_query,
            "content": final_answer,
            "source": "synthesis",
            "task_id": task_id
        })

        # Also save conversation history
        self.memory_agent.execute_task("save_conversation", {
            "role": "user",
            "content": user_query
        })
        self.memory_agent.execute_task("save_conversation", {
            "role": "system",
            "content": final_answer
        })

        return final_answer