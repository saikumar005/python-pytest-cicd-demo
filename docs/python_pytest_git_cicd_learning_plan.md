# Python Pytest + Git + CI/CD Learning Plan

## Goal

Learn how to:

1.  Write unit tests in Python using `pytest`
2.  Test FastAPI/backend code
3.  Use fixtures and mocks
4.  Run tests locally
5.  Commit and push code using Git
6.  Understand CI/CD pipelines
7.  Configure automated tests using GitHub Actions
8.  Understand how successful tests lead to deployment
9.  Apply the same approach to GenAI/RAG/Agentic AI projects

------------------------------------------------------------------------

# Phase 1 --- Python Testing Fundamentals

## 1. Understand Unit Testing

Learn:

-   What is a unit test?
-   Why unit tests are important
-   Unit test vs integration test vs end-to-end test
-   Arrange → Act → Assert
-   Happy path vs edge cases

### Practice

Create:

``` text
calculator/
├── calculator.py
└── tests/
    └── test_calculator.py
```

Implement functions such as:

``` python
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

Write tests for:

-   Normal inputs
-   Negative numbers
-   Zero
-   Decimal values
-   Invalid input
-   Exceptions

------------------------------------------------------------------------

# Phase 2 --- Learn Pytest

## 2. Basic Pytest

Install:

``` bash
pip install pytest
```

Run:

``` bash
pytest
```

Verbose:

``` bash
pytest -v
```

Specific file:

``` bash
pytest tests/test_calculator.py
```

Specific test:

``` bash
pytest tests/test_calculator.py::test_add
```

### Learn

-   Test discovery
-   Assertions
-   Test naming conventions
-   `pytest.raises`
-   Test organization

------------------------------------------------------------------------

# Phase 3 --- Fixtures and Parametrization

## 3. Fixtures

Learn how to create reusable test setup.

Example:

``` python
import pytest

@pytest.fixture
def user():
    return {
        "name": "Sai",
        "role": "engineer"
    }
```

Use fixtures for:

-   Test data
-   Database setup
-   API clients
-   Authentication
-   Temporary files
-   Common configuration

## 4. Parametrization

Learn:

``` python
@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (10, 20, 30),
        (-1, 1, 0),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Practice

Create one parametrized test with at least 5 input combinations.

------------------------------------------------------------------------

# Phase 4 --- Mocking

## 5. Learn Mocking

Understand why external dependencies should generally be mocked in unit
tests.

Examples:

-   OpenAI
-   Gemini
-   Claude
-   Databases
-   Redis
-   Vector databases
-   External REST APIs
-   AWS services

Learn:

``` python
from unittest.mock import Mock
```

and:

``` python
mock.return_value
mock.assert_called_once()
mock.assert_called_once_with(...)
```

### Practice

Create a function that calls an external LLM/API client and write a unit
test without making the real API call.

------------------------------------------------------------------------

# Phase 5 --- FastAPI Testing

## 6. Test FastAPI APIs

Learn:

``` python
from fastapi.testclient import TestClient
```

Practice testing:

-   GET endpoints
-   POST endpoints
-   Request validation
-   HTTP status codes
-   JSON responses
-   Error responses
-   Authentication/authorization behavior

Example:

``` python
def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

------------------------------------------------------------------------

# Phase 6 --- Real Project Test Structure

## 7. Create a Backend Project

Use a structure such as:

``` text
my-project/
├── app/
│   ├── main.py
│   ├── services/
│   ├── models/
│   └── utils/
│
├── tests/
│   ├── unit/
│   │   ├── test_services.py
│   │   └── test_utils.py
│   │
│   └── integration/
│       └── test_api.py
│
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

Understand the difference between:

### Unit tests

Test one piece of application logic in isolation.

### Integration tests

Test multiple components working together.

------------------------------------------------------------------------

# Phase 7 --- Git Fundamentals

## 8. Learn Git Workflow

Understand:

``` text
Working Directory
       ↓
git add
       ↓
Staging Area
       ↓
git commit
       ↓
Local Repository
       ↓
git push
       ↓
GitHub/GitLab
```

Practice:

``` bash
git init

git status

git add .

git commit -m "Add unit tests"

git branch

git checkout -b feature/add-tests

git push origin feature/add-tests
```

Learn:

-   Branches
-   Commits
-   Pull requests
-   Merge
-   Merge conflicts
-   `.gitignore`

------------------------------------------------------------------------

# Phase 8 --- CI/CD Fundamentals

## 9. Understand CI

CI = Continuous Integration.

The basic idea:

``` text
Developer
    ↓
git push
    ↓
GitHub
    ↓
CI pipeline
    ↓
Install dependencies
    ↓
Run tests
    ↓
PASS / FAIL
```

Learn why automated testing is important before merging/deploying code.

------------------------------------------------------------------------

# Phase 9 --- GitHub Actions

## 10. Create Your First CI Pipeline

Create:

``` text
.github/
└── workflows/
    └── ci.yml
```

Example:

``` yaml
name: CI

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest

      - name: Run tests
        run: pytest -v
```

Understand each step:

``` text
checkout
   ↓
setup Python
   ↓
install dependencies
   ↓
run pytest
```

------------------------------------------------------------------------

# Phase 10 --- Understand Automatic Execution

## 11. What Happens After git push?

Practice this workflow:

``` bash
git add .
git commit -m "Add tests"
git push
```

Then observe GitHub Actions.

The pipeline automatically:

1.  Starts a runner
2.  Checks out your repository
3.  Installs Python
4.  Installs dependencies
5.  Runs pytest
6.  Reports PASS/FAIL

If tests fail:

``` text
pytest
   ↓
FAIL
   ↓
CI pipeline FAIL
   ↓
Deployment blocked
```

If tests pass:

``` text
pytest
   ↓
PASS
   ↓
Build
   ↓
Deploy
```

------------------------------------------------------------------------

# Phase 11 --- Add Deployment

## 12. Understand CI/CD End-to-End

The target architecture is:

``` text
Developer
    │
    │ git push
    ▼
GitHub
    │
    ▼
CI Pipeline
    │
    ├── Checkout
    ├── Install dependencies
    ├── Lint
    ├── Unit tests
    ├── Integration tests
    └── Security checks
    │
    ▼
Build
    │
    ▼
Docker Image
    │
    ▼
Container Registry
    │
    ▼
Staging
    │
    ▼
Smoke Tests
    │
    ▼
Production
```

Learn the difference between:

-   Continuous Integration
-   Continuous Delivery
-   Continuous Deployment

------------------------------------------------------------------------

# Phase 12 --- Docker

## 13. Containerize the FastAPI Application

Create a Dockerfile.

Learn:

``` text
Dockerfile
    ↓
docker build
    ↓
Docker image
    ↓
Container
```

Practice:

``` bash
docker build -t my-api .
docker run -p 8000:8000 my-api
```

Then understand how CI/CD can automatically build the Docker image after
tests pass.

------------------------------------------------------------------------

# Phase 13 --- GenAI/RAG Testing

## 14. Apply Testing to GenAI Projects

For a RAG/Agentic AI application, separate testing into:

### Unit tests

Test:

-   Chunking logic
-   Text processing
-   Prompt construction
-   Business logic
-   Agent routing logic
-   Input validation
-   Output parsing

Mock:

-   LLM APIs
-   Vector databases
-   External APIs

### Integration tests

Test:

``` text
API
 ↓
Retriever
 ↓
Vector DB
 ↓
LLM
```

### LLM Evaluation

Use evaluation frameworks such as:

-   Ragas
-   DeepEval

Evaluate concepts such as:

-   Faithfulness
-   Answer relevancy
-   Context precision
-   Context recall
-   Hallucination

Remember:

> Pytest validates deterministic application behavior, while LLM
> evaluation validates the quality of model-generated results.

------------------------------------------------------------------------

# Phase 14 --- Build a Complete Mini Project

## 15. Final Practice Project

Build a small FastAPI RAG-style application.

### Application

``` text
POST /ask
     ↓
Validate request
     ↓
Retrieve context
     ↓
Generate answer
     ↓
Return response
```

### Tests

Create:

``` text
tests/
├── unit/
│   ├── test_retriever.py
│   ├── test_prompt.py
│   ├── test_service.py
│   └── test_agent.py
│
├── integration/
│   └── test_api.py
│
└── evaluation/
    └── test_rag_quality.py
```

### CI

Configure:

``` text
git push
    ↓
GitHub Actions
    ↓
Install dependencies
    ↓
Run unit tests
    ↓
Run integration tests
    ↓
Run quality checks
    ↓
Build Docker image
    ↓
Deploy
```

------------------------------------------------------------------------

# Final Learning Checklist

## Pytest

-   [ ] Understand unit testing
-   [ ] Write basic pytest tests
-   [ ] Assertions
-   [ ] Exception testing
-   [ ] Fixtures
-   [ ] Parametrization
-   [ ] Mocking
-   [ ] FastAPI testing
-   [ ] Unit vs integration tests

## Git

-   [ ] git init
-   [ ] git add
-   [ ] git commit
-   [ ] git branch
-   [ ] git push
-   [ ] Pull requests
-   [ ] Merge conflicts

## CI/CD

-   [ ] Understand CI
-   [ ] Understand CD
-   [ ] GitHub Actions
-   [ ] YAML workflow
-   [ ] Automated pytest execution
-   [ ] Pipeline failure blocking deployment
-   [ ] Docker build
-   [ ] Container registry
-   [ ] Staging
-   [ ] Production deployment

## GenAI

-   [ ] Mock LLM APIs
-   [ ] Test RAG components
-   [ ] Integration testing
-   [ ] Ragas
-   [ ] DeepEval
-   [ ] CI quality gates

------------------------------------------------------------------------

# The Most Important Mental Model

Memorize this flow:

``` text
WRITE CODE
    ↓
WRITE TESTS
    ↓
RUN PYTEST LOCALLY
    ↓
GIT COMMIT
    ↓
GIT PUSH
    ↓
CI PIPELINE STARTS AUTOMATICALLY
    ↓
INSTALL DEPENDENCIES
    ↓
RUN TESTS
    ↓
    ┌───────────────┐
    │ Tests pass?   │
    └───────┬───────┘
        YES│       │NO
           ↓       ↓
         BUILD    STOP
           ↓
        DEPLOY
```

## Target Outcome

By the end of this plan, you should be able to explain and demonstrate:

> "I write isolated unit tests using pytest, mock external dependencies,
> run them locally, commit the changes to Git, and push them to the
> repository. A CI/CD pipeline is triggered automatically on the push or
> pull request. It installs the dependencies, runs the test suite and
> other quality checks, and only if those checks pass does it proceed to
> build and deploy the application."
