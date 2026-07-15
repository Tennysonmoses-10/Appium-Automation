"""
QUICK START GUIDE - Partner App QA Automation Framework
"""

# ============================================================================
# INSTALLATION
# ============================================================================

## Option 1: Local Development Setup

# 1. Clone repository
git clone https://github.com/your-org/partner-app-qa.git
cd partner_app_qa

# 2. Create Python virtual environment
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -e ".[dev]"

# 4. Install Playwright browsers
playwright install

# 5. Copy environment file
cp .env.example .env

# 6. Run smoke tests
pytest tests/ -m smoke -v

## Option 2: Docker Setup

# 1. Build and run with docker-compose
docker-compose -f docker/docker-compose.yml up

# 2. Tests start automatically
# 3. View Allure report at http://localhost:4040

# ============================================================================
# RUNNING TESTS
# ============================================================================

## Basic Execution

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/e2e/test_login.py -v

# Run specific test
pytest tests/e2e/test_login.py::TestLoginUI::test_login_page_loaded -v

## By Markers

# Smoke tests
pytest tests/ -m smoke -v

# Regression tests
pytest tests/ -m regression -v

# API tests
pytest tests/ -m api -v

# Mobile tests
pytest tests/ -m mobile -v

# Multiple markers
pytest tests/ -m "smoke or critical" -v

## With Reporting

# Run with Allure reporting
pytest tests/ -v --alluredir=reports/allure

# Generate and serve Allure report
allure serve reports/allure

# Run with HTML reporting
pytest tests/ -v --html=reports/report.html --self-contained-html

## Parallel Execution

# Run with 4 workers
pytest tests/ -v -n 4

# Run with auto worker detection
pytest tests/ -v -n auto

# Parallel by test class
pytest tests/ -v -n 4 --dist loadscope

## Debug Mode

# Verbose output with debug logs
pytest tests/ -vv -s --log-cli-level=DEBUG

# Stop on first failure
pytest tests/ -x

# Show slowest tests
pytest tests/ -v --durations=10

# ============================================================================
# BDDTESTING
# ============================================================================

## Run BDD scenarios
pytest features/ -v --alluredir=reports/allure

## Run specific feature
pytest features/login.feature -v

## Run specific tag
pytest features/ -v -k "smoke"

## Generate report
pytest features/ -v --alluredir=reports/allure
allure serve reports/allure

# ============================================================================
# CODE QUALITY
# ============================================================================

# Format code with Black
black .

# Sort imports
isort .

# Lint with Pylint
pylint core/ pages/ api/ database/

# Type check with MyPy
mypy core/ pages/ api/ database/

# Run all checks
black --check .
isort --check-only .
pylint core/
mypy core/

# ============================================================================
# CREATING NEW TESTS
# ============================================================================

## 1. Create Page Object

# Create folder structure
mkdir -p pages/dashboard

# Create locators.py
cat > pages/dashboard/locators.py << 'EOF'
class DashboardLocators:
    TITLE = "//h1[contains(text(), 'Dashboard')]"
    USER_NAME = "//span[@class='user-name']"
    LOGOUT_BUTTON = "//button[contains(text(), 'Logout')]"
EOF

# Create page.py with interactions
# Create actions.py with workflows
# Create assertions.py with validations

## 2. Create Fixtures

# Add to fixtures/conftest.py
@pytest.fixture
async def dashboard_fixtures(browser_driver):
    page = browser_driver.get_page()
    dashboard = DashboardPage(page)
    actions = DashboardActions(dashboard)
    assertions = DashboardAssertions(dashboard)
    yield dashboard, actions, assertions

## 3. Write Tests

# Create test file
cat > tests/e2e/test_dashboard.py << 'EOF'
import pytest

@pytest.mark.smoke
async def test_dashboard_loads(dashboard_fixtures):
    dashboard, actions, assertions = dashboard_fixtures
    assert await assertions.verify_page_loaded()
    assert await assertions.verify_user_name_displayed()
EOF

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================

## Development (localhost)
ENVIRONMENT=dev
API_BASE_URL=http://localhost:8080
PLAYWRIGHT_HEADLESS=false

## Staging
ENVIRONMENT=staging
API_BASE_URL=https://api-staging.partnerapp.com
PLAYWRIGHT_HEADLESS=true

## Production
ENVIRONMENT=prod
API_BASE_URL=https://api.partnerapp.com
PLAYWRIGHT_HEADLESS=true

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

## Issue: Playwright browsers not installed
Solution:
  playwright install

## Issue: Port already in use
Solution:
  # Change port in docker-compose.yml or environment
  lsof -i :4723  # Find process
  kill -9 <PID>

## Issue: Database connection failed
Solution:
  # Verify database is running
  docker ps
  # Check connection string in .env
  # Verify database service is ready

## Issue: Tests timing out
Solution:
  # Increase timeout
  export TEST_TIMEOUT=600
  # Or update in .env
  # Check if application is responding

## Issue: Flaky tests
Solution:
  # Review wait strategies
  # Increase implicit waits if needed
  # Check for race conditions in test
  # Use @retry decorator

# ============================================================================
# GIT WORKFLOW
# ============================================================================

# 1. Create feature branch
git checkout -b feature/new-test-suite

# 2. Make changes and commit
git add .
git commit -m "feat: add dashboard tests"

# 3. Push to remote
git push origin feature/new-test-suite

# 4. Create pull request
# GitHub Actions automatically runs tests

# 5. Review and merge
git checkout main
git pull origin main
git merge feature/new-test-suite

# ============================================================================
# USEFUL COMMANDS
# ============================================================================

# List all test markers
pytest --markers

# Generate coverage report
pytest tests/ --cov=core,pages,api,database --cov-report=html
# Open htmlcov/index.html

# Profile test execution
pytest tests/ --profile

# Show collected tests without running
pytest tests/ --collect-only

# Generate JUnit XML for CI/CD
pytest tests/ --junitxml=test-results.xml

# Watch mode for development
pytest-watch tests/ --runner "python -m pytest"

# ============================================================================
# EXAMPLES
# ============================================================================

## Example: Run smoke tests with HTML report
pytest tests/ -m smoke -v --html=reports/report.html --self-contained-html

## Example: Run tests in parallel with coverage
pytest tests/ -v -n auto --cov=core,pages --cov-report=html

## Example: Run tests with specific environment
ENVIRONMENT=staging pytest tests/ -v -m regression

## Example: Run BDD with Allure report
pytest features/ -v --alluredir=reports/allure -m "smoke"

# ============================================================================
# LEARNING RESOURCES
# ============================================================================

Documentation: README.md
Architecture: ARCHITECTURE.md
API Reference: docs/api-reference.md
Examples: examples/

Pytest: https://docs.pytest.org/
Playwright: https://playwright.dev/python/
Appium: http://appium.io/
BDD: https://pytest-bdd.readthedocs.io/

# ============================================================================
# SUPPORT
# ============================================================================

Issues: GitHub Issues
Questions: qa@partnerapp.com
Documentation: docs/
Slack: #qa-automation
