import argparse
import re
import subprocess

from utils.ai_feedback_filter import AIConsumerFeedbackResponse, FeedbackType
from utils.openai_consumer import OpenAIConsumer

EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAIL = 1
DIFF_PATTERN = r"^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@.*$"


def main() -> int:
    """Gets the changes added to a git repository and sends it to the OpenAI API for processing.
    Returns:
        int: 0 if successful, 1 if failed.
    """
    exit_code = EXIT_CODE_SUCCESS
    feedback_types = [FeedbackType.REVIEW]
    ignore_fail = False

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process git diffs and send them to OpenAI API for feedback.")
    parser.add_argument("--format", action="store_true", help="Enable format feedback.")
    parser.add_argument("--security", action="store_true", help="Enable security feedback.")
    parser.add_argument("--no-fail", action="store_true", help="Gets the feedback but does not fail the hook.")
    args = parser.parse_args()

    # Determine feedback types based on arguments

    if args.format:
        feedback_types.append(FeedbackType.FORMAT)
    if args.security:
        feedback_types.append(FeedbackType.SECURITY)

    # if no fail is set, always return success
    if args.no_fail:
        ignore_fail = True
        exit_code = EXIT_CODE_SUCCESS

    try:
        consumer = OpenAIConsumer()
        # Get the changes that have been staged but not yet committed
        result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"Error running git diff: {result.stderr}")
            exit_code = EXIT_CODE_FAIL
            return exit_code
        # Get the diff output
        diff = result.stdout
        if not diff:
            print("No changes to commit.")
            return EXIT_CODE_SUCCESS
        # Get the diff separated by each file
        diff_files = diff.split("diff --git")

        for file in diff_files:
            if not file:
                continue
            file_lines = file.split("\n")
            # Get the file name
            try:
                file_name = file_lines[0].split(" ")[2].replace("b/", "", 1)
            except IndexError:
                file_name = "unknown_file"
            file_content = "\n".join(file_line for file_line in file_lines if not re.match(DIFF_PATTERN, file_line))

            # Send the diff to OpenAI API for processing
            feedback_result = AIConsumerFeedbackResponse(consumer=consumer).get_all_feedback(
                input=file_content,
                feedback_types=feedback_types,
            )
            for key, value in feedback_result.items():
                # If feedback is found, print it
                if len(value) > 0:
                    print(f"{key} Feedback for: {file_name}")
                    for line in value:
                        print(line)
                    exit_code = EXIT_CODE_FAIL

    except Exception as e:
        print(f"Unexpected error: {e}")
        exit_code = EXIT_CODE_FAIL

    return exit_code if not ignore_fail else EXIT_CODE_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
