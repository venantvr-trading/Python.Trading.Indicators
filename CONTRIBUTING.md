# Contributing to Python Trading Indicators

Thank you for your interest in contributing to Python Trading Indicators! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Python.Trading.Indicators.git
   cd Python.Trading.Indicators
   ```

2. **Set up development environment**:
   ```bash
   make setup-dev
   ```
   This will install all development dependencies including testing, linting, and formatting tools.

3. **Verify your setup**:
   ```bash
   make test
   ```

## Development Workflow

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **pytest** for testing

Run all quality checks:

```bash
make check
```

Format your code:

```bash
make format
```

### Testing

All contributions must include appropriate tests.

- Write unit tests for individual indicators
- Write integration tests for indicator combinations
- Include edge cases and error conditions

Run tests:

```bash
make test
```

### Adding New Indicators

When adding a new technical indicator:

1. **Inherit from the base `Indicator` class**:
   ```python
   from venantvr.indicators.indicator import Indicator
   
   class MyIndicator(Indicator):
       def __init__(self, param1: float = 10.0, enabled: bool = True):
           super().__init__(enabled)
           self.__param1 = param1
       
       def compute_indicator(self, candles: DataFrame):
           # Your calculation logic here
           pass
       
       def evaluate_buy_condition(self) -> bool:
           # Your buy condition logic
           return False
       
       def evaluate_sell_condition(self) -> bool:
           # Your sell condition logic  
           return False
   ```

2. **Follow naming conventions**:
    - Use descriptive class names ending in `Indicator`
    - Use private attributes with double underscore prefix
    - Use type hints for all parameters

3. **Add comprehensive tests**:
    - Create `tests/test_my_indicator.py`
    - Test initialization, calculation, and conditions
    - Test edge cases and error handling

4. **Update documentation**:
    - Add your indicator to the README.md
    - Include usage examples
    - Document all parameters

### Commit Guidelines

We follow conventional commits:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions/changes
- `refactor:` for code refactoring
- `style:` for formatting changes
- `ci:` for CI/CD changes

Example:

```
feat: add MACD indicator with signal line crossover detection

- Implement MACD calculation with configurable periods
- Add buy/sell signals based on MACD line and signal line crossover
- Include comprehensive tests and documentation
- Support volume confirmation for signals
```

### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-new-indicator
   ```

2. **Make your changes** following the guidelines above

3. **Run quality checks**:
   ```bash
   make check
   ```

4. **Commit your changes** with descriptive messages

5. **Push to your fork** and create a pull request

6. **Fill out the PR template** with:
    - Description of changes
    - Testing performed
    - Documentation updates
    - Breaking changes (if any)

### Code Review

All contributions go through code review. Reviewers will check for:

- Code quality and style
- Test completeness
- Documentation completeness
- Performance implications
- Security considerations

## Types of Contributions

### Bug Reports

When filing bug reports, please include:

- Python version and OS
- Library version
- Minimal code example to reproduce
- Expected vs actual behavior
- Full error traceback

### Feature Requests

For new features, please:

- Check if it's already requested in issues
- Provide detailed use case description
- Consider implementation complexity
- Discuss API design implications

### Documentation

Documentation improvements are always welcome:

- Fix typos and grammar
- Add examples and tutorials
- Improve API documentation
- Translate to other languages

## Financial Disclaimer

This library is for educational and research purposes only. Contributors should:

- Not provide financial advice
- Include appropriate disclaimers
- Focus on technical implementation
- Avoid making performance claims

## Questions?

- Open an issue for bugs and feature requests
- Start a discussion for questions about contributing
- Check existing issues before creating new ones

Thank you for contributing to Python Trading Indicators!