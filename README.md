# Partner App QA Automation Framework

Enterprise-grade, production-ready QA automation framework supporting web, mobile, API, and database testing.

## Features

- 🎭 **Page Object Model** - Scalable page organization
- 📱 **Multi-Platform** - Web, Mobile (iOS/Android), API, Database
- 🤖 **BDD Support** - Pytest-BDD and Behave integration
- 🔄 **Parallel Execution** - pytest-xdist support
- 📊 **Advanced Reporting** - Allure, HTML, Slack integration
- 📹 **Visual Evidence** - Screenshots, videos, logs
- 🔌 **CI/CD Ready** - Jenkins, GitHub Actions, GitLab CI
- 🏗️ **Enterprise Architecture** - SOLID, DRY, Clean Architecture

## Quick Start

### Prerequisites
- Python 3.13+
- Git
- Docker (optional)

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/partner-app-qa.git
cd partner_app_qa

# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## Project Structure

```
partner_app_qa/
├── config/                 # Configuration management
├── core/                   # Core automation modules
├── pages/                  # Web page objects
├── mobile_pages/          # Mobile page objects
├── api/                   # API automation layer
├── database/              # Database validation layer
├── features/              # BDD feature files
├── step_definitions/      # Step implementations
├── fixtures/              # Pytest fixtures
├── tests/                 # Test suites
├── reports/               # Test reports
├── docker/                # Docker configurations
└── kubernetes/            # K8s configurations
```

## Core Modules

### Driver Management
- **DriverManager** - Playwright driver factory
- **AppiumManager** - Appium mobile driver management
- **Logger** - Centralized logging with correlation IDs
- **WaitUtils** - Explicit wait strategies
- **ScreenshotManager** - Automated screenshot capture
- **RetryHandler** - Retry mechanism with exponential backoff

### Page Object Model
Every page contains:
- `locators.py` - Selector definitions
- `page.py` - Low-level interactions
- `actions.py` - Business workflows
- `assertions.py` - Validation methods

### Components
Reusable UI components:
- Navigation bar
- OTP component
- Toast notifications
- Date picker
- File upload

## BDD Framework

### Supported Tags
- `@smoke` - Smoke tests
- `@sanity` - Sanity tests
- `@regression` - Regression tests
- `@critical` - Critical path tests
- `@mobile` - Mobile tests
- `@android` - Android specific
- `@ios` - iOS specific
- `@api` - API tests
- `@db` - Database tests
- `@e2e` - End-to-end tests

## API Automation

Support for:
- REST APIs
- GraphQL
- JWT, OAuth2
- Contract validation
- Schema validation
- Negative testing

## Database Validation

Support for:
- PostgreSQL
- MySQL
- Oracle
- MongoDB
- Redis

## Reporting

### Allure Reports
```bash
pytest tests/ --alluredir=reports/allure
allure serve reports/allure
```

### HTML Reports
Built-in HTML reporting integration

## Parallel Execution

```bash
# Run with xdist (4 workers)
pytest tests/ -n 4

# Run specific markers in parallel
pytest tests/ -m smoke -n 4
```

## CI/CD Integration

### GitHub Actions
```bash
git push origin feature-branch
# Automatically triggers tests
```

### Docker Execution
```bash
docker-compose up
```

## Configuration

Environment-based configuration:
- `config/environments/dev.yaml`
- `config/environments/staging.yaml`
- `config/environments/prod.yaml`

## Logging

Centralized logging with:
- Correlation IDs
- Request IDs
- Scenario IDs
- Device IDs
- Structured logging

## Contributing

1. Follow PEP8 standards
2. Write tests for new features
3. Use type hints
4. Follow SOLID principles
5. Create meaningful commit messages

## License

MIT

## Support

For issues and questions, please contact qa@partnerapp.com
