# Contributing to neutron-diffusion-dd

Thank you for your interest in contributing to neutron-diffusion-dd! We welcome contributions from the community and appreciate your efforts to improve this project.

## How To Contribute

We're excited to work with you! Here are the ways you can contribute:

1. **Report Bugs**: If you find a bug, please open an issue with detailed information about the problem.
2. **Suggest Features**: Have ideas for improvements? Open an issue to discuss your feature request.
3. **Fix Issues**: Browse existing issues and submit pull requests to fix bugs or implement features.
4. **Improve Documentation**: Help us improve our documentation by fixing typos, adding examples, or clarifying explanations.
5. **Review Code**: Help review pull requests from other contributors.

### Before You Start

- Make sure you have a [GitHub account](https://github.com/signup/free).
- Read our [Code of Conduct](CODE_OF_CONDUCT.md) (if applicable).
- Familiarize yourself with the project structure and existing codebase.
- Check for existing issues or pull requests related to your contribution idea.

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/carlosr301101/neutron-diffusion-dd.git`
3. Install [UV](https://docs.astral.sh/uv)
4. Install dependencies: `uv sync`
5. Make your changes
6. Test your changes thoroughly
7. Submit a pull request

## How to Acknowledge

We value all contributions to this project. Contributors will be acknowledged in the following ways:

- Pull requests will be reviewed promptly and constructively
- Significant contributions may be highlighted in release notes
- Your GitHub profile will be linked as a contributor in the project history

We appreciate all types of contributions, including:
- Code contributions
- Documentation improvements
- Bug reports
- Feature suggestions
- Community support and discussions

## How to Fork and Contribute

### Fork the Repository

1. Navigate to the main page of the repository
2. Click the "Fork" button in the upper right corner
3. Choose your GitHub account as the destination for the fork

### Clone Your Fork

```bash
git clone https://github.com/carlosr301101/neutron-diffusion-dd.git
cd neutron-diffusion-dd
```

### Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names like:
- `feature/add-new-feature`
- `bugfix/fix-login-issue`
- `docs/update-readme`

### Make Your Changes

- Write clear, well-documented code
- Follow the project's coding standards
- Add tests if applicable
- Update documentation as needed

### Format Your Code

This project uses Ruff for code formatting and linting. Before submitting your changes, make sure to format your code:

```bash
uvx ruff format .
```

To lint your code and check for issues:
```bash
uvx ruff check .
```

To automatically fix issues:
```bash
uvx ruff check --fix .
```

### Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add new feature to improve user experience"
```

Use conventional commit messages:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring without feature changes
- `test`: Adding or modifying tests
- `chore`: Other changes

### Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### Submit a Pull Request

1. Navigate to the original repository
2. Click on "Pull Requests"
3. Click "New Pull Request"
4. Select your fork and branch
5. Fill out the pull request template
6. Submit for review


Ruff helps maintain consistent code style and catches common issues. Please ensure your code passes all checks before submitting a pull request.

## Additional Guidelines

- Be respectful and constructive in all interactions
- Provide detailed information in issue reports
- Keep pull requests focused on a single feature or fix
- Write tests for new functionality
- Update documentation for changes that affect users
- Follow the existing code style and conventions

## Questions?

If you have questions about contributing, feel free to open an issue with the "question" label or contact the maintainers.

Thank you again for your interest in contributing!
