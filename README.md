# Flask Application Template

This repository serves as a template for quickly setting up Flask applications with the best practices and linting standards followed by our team.

## Features

- **Flask**: A minimal and extensible web framework for Python.
- **Modular Structure**: Organised in a scalable way with `app`, `static`, and `templates` directories.
- **Linting**: Pre-configured with `flake8`, `pylint`, and `pre-commit` hooks.
- **Pre-commit Hooks**: Ensures code quality by running checks automatically before each commit.
- **Testing Setup**: Uses `pytest` for unit testing.
- **Pipenv**: Dependency management using Pipenv for virtual environments and package versioning.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd flask_template
```

### 2. Install Dependencies with Pipenv

Make sure you have Pipenv installed. If not, install it using:

```bash
pip install pipenv
```

Install the dependencies specified in `Pipfile`:

```bash
pipenv install --dev
```

Activate the virtual environment:

```bash
pipenv shell
```

### 3. Setup Pre-commit Hooks

This project uses `pre-commit` to ensure code quality before committing. Install and set up the hooks by running:

```bash
pipenv run pre-commit install
```

### 4. Run the Application

```bash
pipenv run flask run
```

The application will be running at `http://127.0.0.1:5000/`.

### 5. Running Tests

To run the unit tests using `pytest`:

```bash
pipenv run pytest
```

## Linting and Code Style

- **flake8**: Configured to enforce line length and ignore certain stylistic errors.
- **pylint**: Provides code analysis and checks for common errors.

### To run linters manually:

```bash
pipenv run flake8
pipenv run pylint app
```

## Extending the Template

Feel free to modify or extend the template to suit your project needs. This includes adding new blueprints, integrating databases, or setting up custom middleware.

---

### Contributions

If you have suggestions or improvements to this template, feel free to open a pull request or raise an issue.

### License

This project is licensed under the MIT License.
```
