"""
Text Analyzer Tool
A simple tool that analyzes text properties like word count, character count, etc.
"""
import re
from typing import Dict, Any


def text_analyzer_tool(text: str) -> Dict[str, Any]:
    """
    Analyzes text and returns various metrics.

    Args:
        text: The text to analyze

    Returns:
        Dictionary containing analysis results
    """
    if not text or not isinstance(text, str):
        return {
            "error": "Invalid input: text must be a non-empty string",
            "word_count": 0,
            "character_count": 0,
            "sentence_count": 0,
            "paragraph_count": 0
        }

    # Basic metrics
    word_count = len(text.split())
    character_count = len(text)
    character_count_no_spaces = len(text.replace(' ', ''))

    # Sentence count (simple approximation)
    sentence_count = len(re.findall(r'[.!?]+', text))

    # Paragraph count
    paragraph_count = len([p for p in text.split('\n\n') if p.strip()])

    # Average word length
    words = text.split()
    avg_word_length = sum(len(word)
                          for word in words) / len(words) if words else 0

    # Find longest word
    longest_word = max(words, key=len) if words else ""

    # Count unique words (case insensitive)
    unique_words = len(set(word.lower().strip('.,!?;:"()[]{}')
                       for word in words))

    analysis_result = {
        "word_count": word_count,
        "character_count": character_count,
        "character_count_no_spaces": character_count_no_spaces,
        "sentence_count": sentence_count,
        "paragraph_count": max(paragraph_count, 1),  # At least 1 paragraph
        "average_word_length": round(avg_word_length, 2),
        "longest_word": longest_word,
        "unique_word_count": unique_words,
        # Average reading speed
        "reading_time_minutes": round(word_count / 200, 1),
        "summary": f"Text contains {word_count} words, {sentence_count} sentences, and takes ~{round(word_count / 200, 1)} minutes to read."
    }

    print(
        f"📊 Text Analysis Complete: {word_count} words, {character_count} characters")

    return analysis_result


# Example usage
if __name__ == "__main__":
    sample_text = """
    This is a sample text for analysis. It contains multiple sentences!
    We can analyze various properties like word count, character count, and more.
    
    This tool is useful for content analysis and text processing workflows.
    """

    result = text_analyzer_tool(sample_text.strip())
    print("Analysis Result:")
    for key, value in result.items():
        print(f"  {key}: {value}")
