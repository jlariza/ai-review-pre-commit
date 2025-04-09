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
   git clone git@github.com:jlariza/ai-review-pre-commit.git
   cd ai-review-pre-commit
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   > **Note:** It is recommended to use a virtual environment to install the dependencies. You can create and activate a virtual environment with the following commands:
   > ```
   > python -m venv venv
   > source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   > ```

3. Set up your OpenAI API key:
   - Create `OPENAI_API_KEY` environment variable in the following format:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```


## Usage

### Local usage
When you attempt to make a commit, the pre-commit hook will automatically run. It will:
1. Retrieve the staged changes using `git diff --staged`.
2. Send the changes to OpenAI's API for review.
3. Provide feedback on the code. If no issues are found, the commit will proceed. Otherwise, the commit will be aborted, and feedback will be displayed.

To manually test the functionality, you can run the `try-repo` script:
```
pre-commit try-repo .
```

### Extenal usage
If you want to use this functionality on an external repo:
1. Ensure [pre-commit](https://pre-commit.com/) is installed
2. Ensure the `OPENAI_API_KEY` exists on your environment
3. Add the file `.pre-commit-config.yaml` on your repository's root directory, with the following configuration:

```
repos:
-   repo: https://github.com/jlariza/ai-review-pre-commit
    rev: 0.0.1
    hooks:
    -   id: ai-review
```

4. run `pre-commit install` to set up the git hook scripts
5. Commit away!

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
