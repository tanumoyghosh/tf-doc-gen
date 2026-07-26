# tf-doc-gen

Generate clean, customizable Markdown documentation for Terraform modules directly from HCL.

## Features

- Generate Terraform module documentation in Markdown
- Extract Terraform requirements
- Extract Terraform providers
- Extract Terraform resources
- Extract Terraform input variables
- Extract Terraform outputs
- Generate ready-to-use Terraform module examples
- Update existing `README.md` files without overwriting custom content
- Verify documentation is up to date using `--check`
- Print generated documentation using `--stdout`
- Built with Python, Typer, and python-hcl2

## Installation

### Prerequisites

- Python 3.12+
- uv

Clone the repository:

```bash
git clone https://github.com/<your-username>/tf-doc-gen.git
cd tf-doc-gen
```

Install dependencies:

```bash
uv sync
```

Install Git hooks:

```bash
uv run pre-commit install
```

---

## Usage

Display CLI help:

```bash
uv run tf-doc-gen --help
```

Generate documentation:

```bash
uv run tf-doc-gen generate examples/storage
```

Preview the generated documentation:

```bash
uv run tf-doc-gen generate examples/storage --stdout
```

Verify that a README is up to date:

```bash
uv run tf-doc-gen generate examples/storage --check
```

Display Terraform variables:

```bash
uv run tf-doc-gen parse examples/storage
```

Display the installed version:

```bash
uv run tf-doc-gen version
```

---

## Generated Documentation

`tf-doc-gen` generates documentation containing:

- Example Usage
- Requirements
- Providers
- Resources
- Inputs
- Outputs

---

## Project Structure

```text
.
├── examples/
├── src/
├── tests/
├── .github/
└── pyproject.toml
```

---

## Quality Checks

Run the following commands before committing changes:

```bash
# Verify formatting
uv run ruff format --check .

# Lint the code
uv run ruff check .

# Static type checking
uv run mypy src

# Run the test suite
uv run pytest
```

---

## Tech Stack

- Python 3.12
- Typer
- python-hcl2
- Ruff
- Mypy
- Pytest
- Pre-commit
- GitHub Actions

---

## Roadmap

Planned enhancements include:

- Terraform data source documentation
- Nested module support
- Custom Markdown templates
- PyPI package publishing

---

## License

This project is licensed under the MIT License.