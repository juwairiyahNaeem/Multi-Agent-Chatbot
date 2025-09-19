#  Multi-Agent Chatbot (MAC)

This project is a multi-agent system designed to answer user questions through a coordinated effort between specialized AI agents. A central Coordinator agent manages a team of workers—a Research Agent, an Analysis Agent, and a Memory Agent—to provide comprehensive answers and persist knowledge over time.
This system is built using Python, with Docker for containerization and ChromaDB as its vector-based memory layer.

## 🏛️ System Architecture

The chatbot operates on a simple but effective hierarchical agent structure:

### Coordinator Agent (The Manager): 

This is the brain of the operation. It receives user queries, analyzes them, and creates a step-by-step plan. It then delegates tasks to the appropriate worker agents and synthesizes their findings into a final answer.

### Research Agent (The Researcher): 

This agent is responsible for information retrieval. It simulates searching a knowledge base (like a mock web search) to find raw data relevant to a user's query.

### Analysis Agent (The Analyst): 

This agent takes the data found by the Research Agent and performs reasoning, summarization, and comparison to extract meaningful insights.

### Memory Agent (The Librarian): 

This agent manages the system's long-term memory. It uses the ChromaDB vector store to save important findings, allowing the system to recall information from previous conversations and avoid redundant work.

A typical workflow looks like this:
User Query -> Coordinator -> Research Agent -> Analysis Agent -> Coordinator -> Memory Agent -> Final Answer to User

## 🚀 Getting Started

Follow these instructions to get the chatbot up and running on your local machine.
Prerequisites

You will need the following software installed on your computer:
Git: To clone the repository. (Download Git)
Docker & Docker Compose: To build and run the application container. (Download Docker Desktop)
Installation & Running

### 1. Clone the Repository

Open your terminal and clone your GitHub repository to your local machine.
git clone [https://github.com/juwairiyahNaeem/Multi-Agent-Chatbot.git](https://github.com/juwairiyahNaeem/Multi-Agent-Chatbot.git)


### 2. Navigate to the Project Directory

cd Multi-Agent-Chatbot


### 3. Build and Run the Container

Use Docker Compose to build the image and start the application. This single command handles everything.
docker-compose up --build


The first time you run this, it will download the necessary Python base image and install the required libraries. Subsequent runs will be much faster.

### 4. Chat with the Bot!

Your terminal is now connected to the running application. You will see a welcome message, and you can start typing your questions at the 👤 You: prompt.

### 5. Stop the Application

To stop the chatbot, simply press Ctrl + C in the terminal.
💬 Example Questions to Ask
The chatbot's knowledge is based on the pre-loaded data in the ResearchAgent. You can ask the following questions to test its different capabilities:

### 1. Simple Query

This tests the ResearchAgent's ability to retrieve a direct fact.
What are the main types of neural networks?


### 2. Complex Query

This tests the collaboration between the ResearchAgent and the AnalysisAgent.
Research transformer architectures and analyze their computational efficiency.


### 3. Multi-Step Query

This tests the system's ability to handle a query that requires both research and analysis to identify key points.
Find recent papers on reinforcement learning and identify common challenges.


### 4. Memory Test

Ask this question after you have already asked about neural networks. It tests the MemoryAgent's ability to recall past conversations.
What did we discuss about neural networks earlier?


### 5. Collaborative Query

This tests the entire workflow, from research to analysis and summarization.
Compare gradient descent and the adam optimizer.
