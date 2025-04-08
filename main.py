import re
import subprocess

from dotenv import load_dotenv

from utils.openai_consumer import OpenAIConsumer

load_dotenv()

PASS = 0
FAIL = 1
DIFF_PATTERN = r"^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@.*$"


def main() -> int:
    """Gets the changes added to a git repository and sends it to the OpenAI API for processing.
    Returns:
        int: 0 if successful, 1 if failed.
    """

    exit_code = PASS

    try:
        consumer = OpenAIConsumer()
        # Get the changes that have been staged but not yet committed
        result = subprocess.run(
            ["git", "diff", "--staged"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            print(f"Error running git diff: {result.stderr}")
            exit_code = FAIL
            return exit_code
        # Get the diff output
        diff = result.stdout
        if not diff:
            print("No changes to commit.")
            return PASS
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
            file_content = "\n".join(
                file_line
                for file_line in file_lines
                if not re.match(DIFF_PATTERN, file_line)
            )

            # Send the diff to OpenAI API for processing
            response = consumer.generate_text(
                instructions="Please review this code and provide feedback. Return OK if there is no feedback.",
                input=file_content,
                model="gpt-4o-mini",
            )
            # Parse the response
            response = response.split("\n")
            # Check if the response contains feedback
            feedback = [line for line in response if line and line != "OK"]
            # If the feedback is empty, continue to the next file
            if not feedback:
                print(f"No feedback for: {file_name}")
                continue
            # If feedback is found, print it
            if feedback:
                print(f"Feedback for: {file_name}")
                for line in feedback:
                    print(line)
                exit_code = FAIL

        else:
            print("No feedback found.")
            exit_code = PASS

    except Exception as e:
        print(f"Unexpected error: {e}")
        exit_code |= FAIL

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
