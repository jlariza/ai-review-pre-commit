# AI review pre commit

This project implements a custom pre-commit hook for [pre-commit](https://pre-commit.com/) framework that checks the content of files staged for commit. The hook uses OpenAI's API to review the code and provide feedback before the commit is finalized.

## Project Structure

```
ai-review-pre-commit
├── .env
├── .gitignore
├── .pre-commit-hooks.yaml
├── main.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── tests
│   └── test_utils.py
└── utils
    ├── __init__.py
    └── openai_consumer.py
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-review-pre-commit
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the root directory (if not already present).
   - Add your OpenAI API key in the following format:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```


## Usage

When you attempt to make a commit, the pre-commit hook will automatically run. It will:
1. Retrieve the staged changes using `git diff --staged`.
2. Send the changes to OpenAI's API for review.
3. Provide feedback on the code. If no issues are found, the commit will proceed. Otherwise, the commit will be aborted, and feedback will be displayed.

To manually test the functionality, you can run the `main.py` script:
```
python main.py
```

## Testing

To run the tests for the utility functions, navigate to the `tests` directory and execute:
```
pytest tests/test_utils.py
```

This will ensure that the utility functions behave as expected and meet the defined criteria.

## Disclaimer

**This project is a work in progress and should not be used in production.** The functionality and reliability of the code are still under development, and there may be bugs or incomplete features.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.
