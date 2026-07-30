# tf-doc-gen

Generate clean, customizable Markdown documentation for Terraform modules directly from HCL.

[![CI](https://github.com/tanumoyghosh/tf-doc-gen/actions/workflows/ci.yml/badge.svg)](https://github.com/tanumoyghosh/tf-doc-gen/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/tf-doc-gen.svg)](https://pypi.org/project/tf-doc-gen/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`tf-doc-gen` parses Terraform modules and generates consistent documentation for requirements, providers, resources, inputs, outputs, and example usage.

---

## Features

- Generate Markdown documentation from Terraform modules
- Extract Terraform version requirements
- Extract required providers
- Extract Terraform resources
- Document input variables
- Document outputs
- Generate example module usage
- Update existing `README.md` files without overwriting custom content
- Verify documentation using the `--check` option
- Preview generated documentation using the `--stdout` option

---

## Installation

### Install from PyPI

Install the latest published version using pip:

```bash
pip install tf-doc-gen
```

Verify the installation:
```bash
tf-doc-gen version
```

To run for a terraform module:
```bash
tf-doc-gen generate <terraform_module_path>
```

---

## Developer Setup

### Prerequisites

- Python 3.12+
- uv

Clone the repository:

```bash
git clone https://github.com/tanumoyghosh/tf-doc-gen.git
cd tf-doc-gen
```

Install dependencies:

```bash
uv sync
```

Install the Git hooks:

```bash
uv run pre-commit install
```

---

## Quick Start

Generate documentation for a Terraform module:

```bash
uv run tf-doc-gen generate examples/storage
```

Preview the generated Markdown without updating the README:

```bash
uv run tf-doc-gen generate examples/storage --stdout
```

Verify whether a README is up to date:

```bash
uv run tf-doc-gen generate examples/storage --check
```

---

## CLI

Display the available commands:

```bash
uv run tf-doc-gen --help
```

![CLI Help](https://raw.githubusercontent.com/tanumoyghosh/tf-doc-gen/master/docs/images/cli-help.png)

Parse and display Terraform input variables:

```bash
uv run tf-doc-gen parse examples/storage
```

Display the installed version:

```bash
uv run tf-doc-gen version
```

---

## Generated Documentation

The generated documentation includes:

- Example Usage
- Requirements
- Providers
- Resources
- Inputs
- Outputs

---

### Example Usage

```hcl
module "storage" {
  source              = "./modules/storage"

  resource_group_name = "<resource_group_name>"
  location            = "eastus"
  tags                = {
    <key> = "<value>"
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| Terraform | `>= 1.6.0` |

![Generated README](https://raw.githubusercontent.com/tanumoyghosh/tf-doc-gen/master/docs/images/generated-readme.png)

---

## License

This project is licensed under the MIT License. See the [MIT License](LICENSE) file for details.