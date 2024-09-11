# Flask Application Template

This repository serves as a template for creating Flask applications with a structured design, best practices, and tooling for development and deployment. It includes Docker support, linting, and configurations to help standardise projects within the team.

## Features

- **Flask Framework**: Organised structure for Flask projects, enabling scalability.
- **Docker**: Pre-configured Docker support for containerisation.
- **Pipenv**: Dependency management using Pipenv for virtual environments and package versioning.
- **Helm**: Helm charts for Kubernetes deployments.
- **Pre-commit Hooks**: Pre-configured linting and code style enforcement using `flake8`, `pylint`, and `black`.
- **Testing Setup**: Integrated with `pytest` for testing.
- **Error Handling**: Custom middleware for error handling.

## Directory Structure

```bash
.
├── Dockerfile                   # Docker image configuration
├── LICENSE                      # Project license
├── Pipfile                      # Pipenv dependencies
├── Pipfile.lock                 # Locked dependencies for Pipenv
├── README.md                    # Project documentation (this file)
├── app/                         # Application source code
│   ├── __init__.py              # Application factory
│   ├── app.py                   # Entry point for the app
│   ├── main/                    # Main application module
│   │   ├── config/              # Configuration files
│   │   │   ├── app_config.py    # Application-specific configurations
│   │   │   ├── cors_config.py   # CORS configuration
│   │   │   ├── error_handlers_config.py  # Error handler configurations
│   │   │   ├── jinja_config.py  # Jinja template configurations
│   │   │   ├── limiter_config.py  # Rate limiter configuration
│   │   │   ├── logging_config.py  # Logging configuration
│   │   │   ├── routes_config.py   # Routes configuration
│   │   │   └── sentry_config.py   # Sentry error tracking configuration
│   │   ├── middleware/          # Middleware for request/response handling
│   │   │   ├── error_handler.py  # Custom error handler middleware
│   │   ├── routes/              # Application routes
│   │   │   ├── main.py          # Main route definitions
│   │   │   └── robots.py        # Robots.txt handler route
│   │   ├── services/            # Service layer
│   │   └── validators/          # Input validation
│   ├── run.py                   # Script to run the application
│   ├── static/                  # Static files (images, JS, CSS, fonts)
│   └── templates/               # HTML templates
│       ├── components/          # Reusable HTML components
│       └── pages/               # Page templates
├── docker-compose.yaml          # Docker Compose for multi-container setups
├── docker-test.yaml             # Docker Compose for testing environment
├── helm/                        # Helm chart for Kubernetes deployment
│   └── application/             
│       ├── Chart.yaml           # Helm chart metadata
│       ├── templates/           # Kubernetes resource templates
│       ├── values-dev.yaml      # Development environment values
│       └── values-prod.yaml     # Production environment values
└── makefile                     # Makefile for automating common tasks
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone git@github.com:ministryofjustice/operations-engineering-flask-template.git
cd operations-engineering-flask-template
```

### 2. Install Dependencies with Pipenv

Ensure you have Pipenv installed:

```bash
pip install pipenv
```

Install the dependencies:

```bash
pipenv install --dev
```

Activate the virtual environment:

```bash
pipenv shell
```

### 3. Set Up Pre-commit Hooks

This project uses `pre-commit` hooks to maintain code quality. Install and set up the hooks:

```bash
pipenv run pre-commit install
```

### 4. Running the Application

Start the Flask application locally using Docker:

```bash
docker-compose up
```

The application will be available at `http://localhost:5000/`.

Alternatively, you can run the app directly using Flask:

```bash
pipenv run python app/run.py
```

### 5. Running Tests

To run the unit tests using `pytest`:

```bash
pipenv run pytest
```

## Deployment

### Docker

The repository includes a `Dockerfile` and `docker-compose.yaml` file for containerisation. Build and run the app in a Docker container:

```bash
docker build -t flask-template .
docker run -p 5000:5000 flask-template
```

### Kubernetes (Helm)

This project includes Helm charts for Kubernetes deployment. You can use the `helm/application/` directory to deploy your application with Helm. Modify `values-dev.yaml` or `values-prod.yaml` as necessary for your environment.

```bash
helm install my-app ./helm/application
```

## Linting and Code Style

- **flake8**: Enforces PEP8 style guide for Python code.
- **pylint**: Provides code analysis and checks for common errors.
- **black**: Ensures consistent code formatting (automatically run by `pre-commit`).

### Running Linters

```bash
pipenv run flake8
pipenv run pylint app
```

## Configuration

The application configuration is modularised in the `app/main/config/` directory. Each aspect of the app’s configuration (e.g., CORS, error handlers, logging) is stored in its own file. Modify the configurations to suit your application needs.

## Extending the Template

Feel free to extend the template by adding more services, blueprints, or integrating additional tools such as databases or external APIs.

---

### Contributions

If you have suggestions or improvements to this template, feel free to open a pull request or raise an issue.

### License

This project is licensed under the MIT License.
```
