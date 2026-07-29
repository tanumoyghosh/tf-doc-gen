# tf-doc-gen

Generate clean, customizable Markdown documentation for Terraform modules directly from HCL.

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

Example:

````markdown
## Example Usage

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