import chromadb
import uuid
import datetime


class EnhancedMemory:
    """Manages structured memory with vector search capabilities."""

    def __init__(self, path="./chroma_db"):
        # Use an in-memory implementation for simplicity, can be changed to HttpClient
        self.client = chromadb.Client()

        # Knowledge Base Collection (Vector Store)
        self.kb_collection = self.client.get_or_create_collection(
            name="knowledge_base"
        )

        # Other memories are kept as simple in-memory lists for this example
        self.conversation_memory = []
        self.agent_state_memory = {}  # {task_id: [states]}

    def add_knowledge(self, content, topic, source, task_id):
        """Adds a piece of knowledge to the vector store."""
        doc_id = str(uuid.uuid4())
        self.kb_collection.add(
            documents=[content],
            metadatas=[{
                "topic": topic,
                "source": source,
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "task_id": task_id
            }],
            ids=[doc_id]
        )

    def search_knowledge(self, query, n_results=1):
        """Searches the knowledge base using vector similarity."""
        if self.kb_collection.count() == 0:
            return None
        results = self.kb_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def add_conversation_turn(self, role, content):
        """Adds a turn to the conversation history."""
        turn = {
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        self.conversation_memory.append(turn)

    def get_conversation_history(self):
        """Retrieves the full conversation history."""
        return self.conversation_memory

    def update_agent_state(self, task_id, agent_name, status, details):
        """Tracks the state of an agent for a given task."""
        if task_id not in self.agent_state_memory:
            self.agent_state_memory[task_id] = []

        state = {
            "agent": agent_name,
            "status": status,  # e.g., 'completed', 'failed'
            "details": details,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        self.agent_state_memory[task_id].append(state)