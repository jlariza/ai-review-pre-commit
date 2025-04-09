import pytest

from utils.ai_feedback_filter import AIConsumerFeedbackResponse, FeedbackType
from utils.protocols import AIConsumerProtocol


class MockAIConsumer(AIConsumerProtocol):
    def generate_text(self, instructions: str, input: str, model: str) -> str:
        if AIConsumerFeedbackResponse.TYPES_OF_FEEDBACK[FeedbackType.REVIEW] in instructions:
            return "Feedback 1\nFeedback 2\nOK"
        elif AIConsumerFeedbackResponse.TYPES_OF_FEEDBACK[FeedbackType.SECURITY] in instructions:
            return "Security Feedback 1\nOK"
        elif AIConsumerFeedbackResponse.TYPES_OF_FEEDBACK[FeedbackType.FORMAT] in instructions:
            return "Format Feedback 1\nFormat Feedback 2\nOK"
        return "OK"


@pytest.fixture
def ai_consumer_feedback_response():
    mock_consumer = MockAIConsumer()
    return AIConsumerFeedbackResponse(consumer=mock_consumer)


def test_get_review_feedback(ai_consumer_feedback_response):
    """
    Test the `get_review_feedback` method of the `ai_consumer_feedback_response` object.

    This test verifies that the `get_review_feedback` method returns the expected feedback
    when provided with a sample input. The expected feedback is a list containing
    "Feedback 1" and "Feedback 2".

    Args:
        ai_consumer_feedback_response: An instance of the class that implements the
                                       `get_review_feedback` method.

    Assertions:
        - Ensures that the returned feedback matches the expected list of feedback strings.
    """
    feedback = ai_consumer_feedback_response.get_review_feedback("sample input")
    assert feedback == ["Feedback 1", "Feedback 2"]


def test_get_security_feedback(ai_consumer_feedback_response):
    """
    Test the `get_security_feedback` method of the `ai_consumer_feedback_response` object.

    This test verifies that the `get_security_feedback` method returns the expected
    security feedback when provided with a sample input.

    Args:
        ai_consumer_feedback_response: A fixture or mock object representing the
            `ai_consumer_feedback_response` instance.

    Assertions:
        Ensures that the returned feedback matches the expected list
        containing "Security Feedback 1".
    """
    feedback = ai_consumer_feedback_response.get_security_feedback("sample input")
    assert feedback == ["Security Feedback 1"]


def test_get_format_feedback(ai_consumer_feedback_response):
    """
    Test the `get_format_feedback` method of the `ai_consumer_feedback_response` object.

    This test verifies that the `get_format_feedback` method correctly processes the input
    and returns the expected list of formatted feedback strings.

    Args:
        ai_consumer_feedback_response: An instance of the class containing the
                                       `get_format_feedback` method.

    Steps:
        1. Call the `get_format_feedback` method with a sample input string.
        2. Assert that the returned feedback matches the expected list of strings.

    Expected Result:
        The method should return a list containing the strings
        ["Format Feedback 1", "Format Feedback 2"].
    """
    feedback = ai_consumer_feedback_response.get_format_feedback("sample input")
    assert feedback == ["Format Feedback 1", "Format Feedback 2"]


def test_get_all_feedback(ai_consumer_feedback_response):
    """
    Test the `get_all_feedback` method of the `ai_consumer_feedback_response` object.

    This test verifies that the `get_all_feedback` method correctly retrieves feedback
    for the specified input and feedback types. It ensures that the returned feedback
    matches the expected structure and content.

    Assertions:
    - The returned feedback dictionary contains the expected keys (`review`, `security`, `format`).
    - The values for each key match the expected feedback content.
    """
    feedback = ai_consumer_feedback_response.get_all_feedback(
        "sample input", feedback_types=[FeedbackType.REVIEW, FeedbackType.SECURITY]
    )
    assert feedback == {
        "review": ["Feedback 1", "Feedback 2"],
        "security": ["Security Feedback 1"],
        "format": [],
    }


def test_generate_instructions_invalid_feedback_type(ai_consumer_feedback_response):
    """
    Test that the `_generate_instructions` method raises a `ValueError`
    when provided with an invalid feedback type.

    This test ensures that the method correctly validates the input
    and raises an appropriate exception with the expected error message.

    Args:
        ai_consumer_feedback_response: Fixture providing an instance of
                                       the AIConsumerFeedbackResponse class.

    Raises:
        ValueError: Expected to be raised when an invalid feedback type
                    is passed to the `_generate_instructions` method.
    """
    with pytest.raises(ValueError, match="Invalid feedback type"):
        ai_consumer_feedback_response._generate_instructions("INVALID_TYPE")
