import logging
from .base_agent import BaseAgent


class AnalysisAgent(BaseAgent):
    """An agent that performs analysis on provided data."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute_task(self, task, args):
        self.logger.info(f"Executing task: {task} with args: {args}")
        if task == "analyze_data":
            data = args.get("data", "")
            if not data:
                return {"content": "No data provided for analysis.", "confidence": 0.1}

            # Simple analysis: summarize and find keywords
            summary = self._summarize(data)
            trade_offs = self._identify_tradeoffs(data)

            analysis_result = f"Analysis Summary: {summary}"
            if trade_offs:
                analysis_result += f"\nKey Trade-offs Identified: {trade_offs}"

            return {"content": analysis_result, "confidence": 0.85}
        else:
            return {"content": "Unknown task for AnalysisAgent.", "confidence": 0.1}

    def _summarize(self, text):
        """A very basic summarization function."""
        sentences = text.split('.')
        # Return the first sentence as a summary
        return sentences[0].strip() + "." if sentences else ""

    def _identify_tradeoffs(self, text):
        """Identifies sentences with 'trade-off' keywords."""
        if "computational complexity" in text.lower():
            return "Higher accuracy often comes with greater computational cost."
        if "sample efficiency" in text.lower():
            return "Methods with high sample efficiency may be less stable."
        return None