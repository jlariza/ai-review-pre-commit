from unittest.mock import MagicMock, patch

import pytest

from hooks.main import EXIT_CODE_FAIL, EXIT_CODE_SUCCESS, main

# filepath: /Users/jose.ariza/projects/python-precommit-project/hooks/test_main.py


@pytest.fixture
def mock_subprocess_run():
    with patch("hooks.main.subprocess.run") as mock_run:
        yield mock_run


@pytest.fixture
def mock_feedback_response():
    with patch("hooks.main.AIConsumerFeedbackResponse") as mock_response:
        yield mock_response


@pytest.fixture
def mock_openai_client():
    with patch("utils.openai_consumer.OpenAI") as MockOpenAI:
        mock_client = MockOpenAI.return_value
        yield mock_client


def test_main_no_changes(mock_subprocess_run, mock_openai_client):
    """
    Test main function when no changes are staged for commit.
    """
    # Arrange
    mock_openai_client.responses.create.return_value = MagicMock(output_text="Generated text")
    mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="")

    # Act
    result = main()

    # Assert
    assert result == EXIT_CODE_SUCCESS
    mock_subprocess_run.assert_called_once_with(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True,
    )


def test_main_successful_feedback(mock_subprocess_run, mock_feedback_response, mock_openai_client):
    """
    Test main function when feedback processing is successful with no issues.
    """
    # Arrange
    mock_openai_client.responses.create.return_value = MagicMock(output_text="Generated text")
    mock_subprocess_run.return_value = MagicMock(
        returncode=0,
        stdout="diff --git a/file1.py b/file1.py\n@@ -1 +1 @@\nprint('Hello')",
    )
    mock_feedback_response.return_value.get_all_feedback.return_value = {"FORMAT": []}

    # Act
    result = main()

    # Assert
    assert result == EXIT_CODE_SUCCESS
    mock_subprocess_run.assert_called_once()
    mock_feedback_response.return_value.get_all_feedback.assert_called_once()


def test_main_feedback_with_issues(mock_subprocess_run, mock_feedback_response, mock_openai_client):
    """
    Test main function when feedback processing finds issues.
    """
    # Arrange
    mock_openai_client.responses.create.return_value = MagicMock(output_text="Generated text")
    mock_subprocess_run.return_value = MagicMock(
        returncode=0,
        stdout="diff --git a/file1.py b/file1.py\n@@ -1 +1 @@\nprint('Hello')",
    )
    mock_feedback_response.return_value.get_all_feedback.return_value = {"FORMAT": ["Issue 1", "Issue 2"]}

    # Act
    result = main()

    # Assert
    assert result == EXIT_CODE_FAIL
    mock_subprocess_run.assert_called_once()
    mock_feedback_response.return_value.get_all_feedback.assert_called_once()


def test_main_git_diff_error(mock_subprocess_run, mock_openai_client):
    """
    Test main function when git diff command fails.
    """
    # Arrange
    mock_openai_client.responses.create.return_value = MagicMock(output_text="Generated text")
    mock_subprocess_run.return_value = MagicMock(returncode=1, stderr="Git error")

    # Act
    result = main()

    # Assert
    assert result == EXIT_CODE_FAIL
    mock_subprocess_run.assert_called_once()


def test_main_unexpected_exception(mock_subprocess_run, mock_openai_client):
    """
    Test main function when an unexpected exception occurs.
    """
    # Arrange
    mock_openai_client.responses.create.return_value = MagicMock(output_text="Generated text")
    mock_subprocess_run.side_effect = Exception("Unexpected error")

    # Act
    result = main()

    # Assert
    assert result == EXIT_CODE_FAIL
    mock_subprocess_run.assert_called_once()
