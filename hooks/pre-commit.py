import subprocess

from dotenv import load_dotenv

from src.openai_consumer import OpenAIConsumer

load_dotenv()

PASS = 0
FAIL = 1


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
            # # get file name
            # file_name = file.split(" ")[2].split("/")[1]
            # # get file content
            # file_content = file.split("@@")[1].split(" ")[2]
            # # get the diff content
            # diff_content = file.split("@@")[1].split(" ")[3]

            # Send the diff to OpenAI API for processing
            response = consumer.generate_text(
                instructions="Please review this code and provide feedback. Return OK if there is no feedback.",
                input=file,
                model="gpt-4o",
            )
            # Parse the response
            response = response.split("\n")
            # Check if the response contains feedback
            feedback = [line for line in response if line]
            # If feedback is found, print it
            if feedback:
                print("Feedback:")
                for line in feedback:
                    print(line)
                exit_code = FAIL

        else:
            print("No feedback found.")
            exit_code = PASS

    except Exception:
        exit_code |= FAIL

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
