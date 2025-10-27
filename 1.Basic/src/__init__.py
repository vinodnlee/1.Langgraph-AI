"""
LangGraph Sample Project Package
A production-ready LangGraph workflow application with 3 sample nodes.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

from src.workflows.basic_workflow import create_langgraph_workflow, run_workflow
from src.workflows.advanced_workflow import create_advanced_workflow

__all__ = [
    "create_langgraph_workflow",
    "run_workflow",
    "create_advanced_workflow",
]
