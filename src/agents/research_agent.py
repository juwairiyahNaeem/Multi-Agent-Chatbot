import logging
from .base_agent import BaseAgent

class ResearchAgent(BaseAgent):
    """An agent that performs 'research' from a mock knowledge base."""

    def __init__(self):
        self.knowledge_base = {
            "neural networks": "The main types of neural networks are Feedforward, Recurrent (RNNs), and Convolutional (CNNs).",
            "transformer architectures": "Transformers, introduced in 'Attention Is All You Need', rely on self-attention mechanisms, avoiding recurrence. Key components are multi-head attention and positional encodings. Their computational complexity is O(n^2 * d).",
            "reinforcement learning papers": "Recent RL papers focus on sample efficiency and safety. Key methodologies include model-based RL, offline RL, and hierarchical RL. Common challenges are sparse rewards and sim-to-real transfer.",
            "machine learning optimization": "Common optimization techniques include Gradient Descent, Stochastic Gradient Descent (SGD), Adam (Adaptive Moment Estimation), and RMSprop. Adam is often most effective as a default due to its adaptive learning rate.",
            "gradient descent": "An optimization algorithm used to minimize a function by iteratively moving in the direction of steepest descent.",
            "adam optimizer": "An adaptive learning rate optimization algorithm that's been designed specifically for training deep neural networks."
        }
        self.logger = logging.getLogger(__name__)

    def execute_task(self, task, args):
        self.logger.info(f"Executing task: {task} with args: {args}")
        if task == "find_information":
            topic = args.get("topic", "").lower()
            # Simple keyword matching
            for key, value in self.knowledge_base.items():
                if all(word in topic for word in key.split()):
                    return {"content": value, "confidence": 0.9}
            return {"content": "Information not found.", "confidence": 0.2}
        else:
            return {"content": "Unknown task for ResearchAgent.", "confidence": 0.1}