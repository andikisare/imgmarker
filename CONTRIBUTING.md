# Contributing to Image Marker

Thanks for your interest in contributing! This document outlines the process for contributing to this project.

## Code of Conduct

Please be respectful and constructive in all interactions. We want this to be a welcoming project for contributors of all experience levels.

## Getting Started

1. **Set up your development environment.** Follow the instructions [here](https://imgmarker.readthedocs.io/en/latest/start/installation.html) to setup your python environment and install Image Marker.

2. **Fork the repository** and clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/imgmarker.git
   cd imgmarker
   ```

3. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Reporting Issues

Before opening a new issue, please search [existing issues](https://github.com/andikisare/imgmarker/issues) to avoid duplicates.

When reporting a bug, please include:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your OS, Python version, and imgmarker version
- Any relevant error messages or screenshots

## Suggesting Enhancements

Feature requests are welcome! Please open an issue describing:
- The problem your feature would solve
- Your proposed solution
- Any alternatives you've considered

## Making Changes

1. **Keep changes focused.** One feature or fix per pull request makes review easier and faster.
2. **Follow the existing code style.** Match the conventions already used in the file/module you're editing.
3. **Write clear commit messages.** Summarize *what* changed and *why*, not just *how*.
4. **Update documentation** if your change affects usage, configuration, or public APIs.
5. **Add or update tests** where applicable, especially for bug fixes and new features.

## Testing

Before submitting a pull request, run the test suite locally:

```bash
pip install pytest pytest-qt
cd imgmarker/imgmarker
pytest tests.py
rm -r tests/test_save/ # to be able to run tests again
```

Please make sure all tests pass and that you haven't introduced new warnings or errors.

## Submitting a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a pull request against the `main` branch of the upstream repository.
3. In your PR description, include:
   - A summary of the change
   - The motivation/context behind it
   - Any related issue numbers (e.g., `Closes #123`)
4. Be responsive to review feedback — maintainers may request changes before merging.

## Style Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style.
- Use descriptive variable and function names.
- Keep functions focused and reasonably sized.
- Add docstrings to public functions, classes, and modules.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see `LICENSE`).

## Questions?

If you have questions that aren't answered here, feel free to open an issue or start a discussion on the repository.

Thanks again for contributing!
