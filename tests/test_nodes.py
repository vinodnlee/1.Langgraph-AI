"""
Unit tests for workflow nodes.
"""

import pytest
from src.models import GraphState
from src.nodes import (
    input_processor_node,
    data_transformer_node,
    output_generator_node
)


class TestInputProcessorNode:
    """Tests for input processor node."""

    def test_input_processor_basic(self):
        """Test basic input processing."""
        state: GraphState = {
            "input_text": "hello world",
            "processed_text": "",
            "transformed_text": "",
            "output_text": "",
            "step": "started"
        }

        result = input_processor_node(state)

        assert result["processed_text"] == "Processing: HELLO WORLD"
        assert result["step"] == "input_processed"
        assert result["input_text"] == "hello world"

    def test_input_processor_empty(self):
        """Test processing empty input."""
        state: GraphState = {
            "input_text": "",
            "processed_text": "",
            "transformed_text": "",
            "output_text": "",
            "step": "started"
        }

        result = input_processor_node(state)

        assert result["processed_text"] == "Processing: "
        assert result["step"] == "input_processed"


class TestDataTransformerNode:
    """Tests for data transformer node."""

    def test_data_transformer_fallback(self):
        """Test data transformation with fallback logic."""
        state: GraphState = {
            "input_text": "test",
            "processed_text": "Processing: TEST",
            "transformed_text": "",
            "output_text": "",
            "step": "input_processed"
        }

        result = data_transformer_node(state)

        assert "TRANSFORMED" in result["transformed_text"]
        assert result["step"] == "data_transformed"


class TestOutputGeneratorNode:
    """Tests for output generator node."""

    def test_output_generator(self):
        """Test output generation."""
        state: GraphState = {
            "input_text": "test input",
            "processed_text": "Processing: TEST INPUT",
            "transformed_text": "✨ TRANSFORMED: ENHANCED: TEST INPUT ✨",
            "output_text": "",
            "step": "data_transformed"
        }

        result = output_generator_node(state)

        assert "LANGGRAPH WORKFLOW RESULT" in result["output_text"]
        assert "test input" in result["output_text"]
        assert result["step"] == "output_generated"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
