## Contributing to Dispair

If you would like to contribute to `dispair` please follow these instructions to set a local development environment up

1. Install [poetry](https://python-poetry.org/), a dependency management tool, with [pip](https://pypi.org/):
```shell
pip install -U poetry
```

2. Run this in the root directory to install the necessary packages for the project:
```shell
poetry install
```

3. Install the pre-commit configuration with:
```shell
poetry run task precommit
```

4. You're all set! You can now edit source code within the `dispair` directory

5. (Testing Bot) Run the example slash command bot with:
```shell
poetry run webhook
```

## Testing
If you want your contributions to be merged into the main repository, you must
test the source code you write.

Run tests with:
```shell
poetry run pytest ./tests --verbose
```

For larger changes like adding support for another language, please open an issue
[here](https://github.com/GDWR/dispair/issues)
