## Python Development

First install poetry:
```
sudo apt install python3 pipx
pipx install poetry
```

Then navigate to the poetry project directory (where the pyproject.toml file is located) and run `poetry install`

if you need to add a new dependency run `poetry add <dep name>`
to reformat python code run `poetry run black .`
to manage python imports code run `poetry run isort .`
to lint python code run `poetry run flake8 .`
for debugging and static typing of python code run `poetry run mypy .`
to run python tests run `poetry run pytest ./tests/__init__.py`

to show a tree of the current packages and their dependencies run `poetry show --tree`


## C++ Development

For all C++ development (primarily on srsRAN code) we will be using clangd to format code as we write.

Install the C++ VSCode extension, and it will automatically detect and use the .clang-tidy file
If you are using another editor install and run a clangd LSP server like so:
```
sudo apt install clangd
cd <repo folder>
clangd --clang-tidy .
```
Then the clangd process will format code passed through stdout

## Repo Management

what repos should we have? Should everything be committed to one or should we split based on responsiblites.
