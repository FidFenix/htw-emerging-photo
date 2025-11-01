# Contributing to HTW Emerging Photo

Thank you for your interest in contributing to the HTW Emerging Photo project!

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone <your-fork-url>
   cd htw-emerging-photo
   ```

2. **Setup Environment**
   ```bash
   make setup
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   make install
   ```

## Development Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following the project structure
   - Add tests for new functionality
   - Update documentation as needed

3. **Format and Lint**
   ```bash
   make format
   make lint
   ```

4. **Run Tests**
   ```bash
   make test
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Adding or updating tests
   - `chore:` - Maintenance tasks

6. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Standards

- **Python Style**: Follow PEP 8 (enforced by Black and Flake8)
- **Line Length**: 100 characters
- **Type Hints**: Use type hints where appropriate
- **Docstrings**: Use Google-style docstrings
- **Testing**: Maintain test coverage for new features

## Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Test both success and failure scenarios

## Documentation

- Update relevant documentation in `docs/`
- Update README.md if adding new features
- Add docstrings to all public functions/classes

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Describe your changes in the PR description
4. Link any related issues
5. Wait for review and address feedback

## Questions?

If you have questions, please refer to the documentation in the `docs/` directory or contact the development team.

Thank you for contributing! 🎉

