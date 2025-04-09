from unittest.mock import MagicMock, patch

import pytest
from openai import OpenAIError

from utils.openai_consumer import OpenAIConsumer

# utils/test_openai_consumer.py


@pytest.fixture
def mock_openai_client():
    with patch("utils.openai_consumer.OpenAI") as MockOpenAI:
        mock_client = MockOpenAI.return_value
        yield mock_client


def test_generate_text_success(mock_openai_client):
    """
    Test that `generate_text` returns the expected output when the API call is successful.
    """
    # Arrange
    mock_openai_client.responses.create.return_value = MagicMock(
        output_text="Generated text"
    )
    consumer = OpenAIConsumer()

    # Act
    result = consumer.generate_text(
        instructions="Write a poem", input="Roses are red", model="gpt-4o-mini"
    )

    # Assert
    assert result == "Generated text"
    mock_openai_client.responses.create.assert_called_once_with(
        model="gpt-4o-mini", instructions="Write a poem", input="Roses are red"
    )


def test_generate_text_error(mock_openai_client):
    """
    Test that `generate_text` raises a RuntimeError when the API call fails.
    """
    # Arrange
    mock_openai_client.responses.create.side_effect = OpenAIError("API error")
    consumer = OpenAIConsumer()

    # Act & Assert
    with pytest.raises(RuntimeError, match="Error generating text: API error"):
        consumer.generate_text(
            instructions="Write a story", input="Once upon a time", model="gpt-4o-mini"
        )
    mock_openai_client.responses.create.assert_called_once_with(
        model="gpt-4o-mini", instructions="Write a story", input="Once upon a time"
    )
