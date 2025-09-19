from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def execute_task(self, task, args):
        """Executes a given task with provided arguments."""
        pass