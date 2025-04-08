# python-precommit-project

This project implements a custom pre-commit hook for Git that checks the content of files staged for commit. The hook executes a TODO function defined in the utility module, which determines whether the commit should proceed based on the content of the files.

## Project Structure

```
python-precommit-project
├── hooks
│   └── pre-commit.py
├── src
│   ├── main.py
│   └── utils.py
├── tests
│   └── test_utils.py
├── .git
│   └── hooks
│       └── pre-commit (symlink to ../hooks/pre-commit.py)
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-precommit-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure that the pre-commit hook is set up correctly. The `.git/hooks/pre-commit` file should be a symlink to `hooks/pre-commit.py`.

## Usage

When you attempt to make a commit, the pre-commit hook will automatically run. It will read the content of the files you are trying to commit and execute the TODO function from `src/utils.py`. If the function returns a failure status, the commit will be aborted, and you will see an error message.

## Testing

To run the tests for the utility functions, navigate to the `tests` directory and execute:
```
pytest test_utils.py
```

This will ensure that the TODO function behaves as expected and meets the defined criteria.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.