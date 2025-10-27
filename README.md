# Agent Builder

A Flask-based web application built with Python and Poetry.

## Features

- Flask web framework with blueprints
- RESTful API endpoints
- Template rendering with Jinja2
- Modern CSS styling
- Poetry dependency management

## Prerequisites

- Python 3.9 or higher
- Poetry (install from https://python-poetry.org/docs/#installation)

## Installation

1. Clone the repository:
```bash
cd agent-builder
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Running the Application

1. Activate the Poetry virtual environment:
```bash
poetry shell
```

2. Run the Flask application:
```bash
python run.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
agent-builder/
├── app/
│   ├── __init__.py       # Application factory
│   ├── routes.py         # Route definitions
│   ├── static/
│   │   └── css/
│   │       └── style.css # Stylesheet
│   └── templates/
│       ├── base.html     # Base template
│       ├── index.html    # Home page
│       └── about.html    # About page
├── run.py                # Application entry point
├── pyproject.toml        # Poetry configuration
└── README.md            # This file
```

## API Endpoints

- `GET /` - Home page
- `GET /about` - About page
- `GET/POST /api/hello` - API endpoint that returns a greeting

### Example API Usage

```bash
# GET request
curl "http://localhost:5000/api/hello?name=World"

# POST request
curl -X POST http://localhost:5000/api/hello \
  -H "Content-Type: application/json" \
  -d '{"name": "World"}'
```

## Development

### Installing Dev Dependencies

Dev dependencies (pytest, black, flake8) are automatically installed with `poetry install`.

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black .
```

### Linting

```bash
poetry run flake8 app/
```

## Adding New Dependencies

```bash
poetry add package-name
```

## License

MIT
