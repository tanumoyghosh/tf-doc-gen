from tf_doc_gen.models import (
    ModuleDocumentation,
    Output,
    Provider,
    Requirement,
    Resource,
    Variable,
)


def generate_variables_markdown(variables: list[Variable]) -> str:
    """Generate a Markdown table for Terraform variables."""

    if not variables:
        return ""

    lines = [
        "## Inputs",
        "",
        "| Name | Type | Default | Description |",
        "|------|------|---------|-------------|",
    ]

    for variable in variables:
        default = "-" if variable.default is None else f"`{variable.default}`"

        lines.append(
            f"| `{variable.name}` | `{variable.type}` | {default} | {variable.description} |"
        )

    return "\n".join(lines)


def generate_outputs_markdown(outputs: list[Output]) -> str:
    """Generate a Markdown table for Terraform outputs."""

    if not outputs:
        return ""

    lines = [
        "## Outputs",
        "",
        "| Name | Description |",
        "|------|-------------|",
    ]

    for output in outputs:
        lines.append(f"| `{output.name}` | {output.description} |")

    return "\n".join(lines)


def format_example_value(value: object, indent: str = "") -> str:
    """Format a Terraform value for the example module."""

    if value is None:
        return '"<value>"'

    if isinstance(value, str):
        return f'"{value}"'

    if isinstance(value, dict):
        return f'{{\n{indent}<key> = "<value>"\n  }}'

    if isinstance(value, list):
        return '["<value>"]'

    return str(value)


def generate_example_markdown(
    module_name: str,
    variables: list[Variable],
) -> str:
    """Generate a Terraform module usage example."""

    max_name_length = max(
        [len("source"), *(len(variable.name) for variable in variables)]
    )

    lines = [
        "## Example Usage",
        "",
        "```hcl",
        f'module "{module_name}" {{',
        f'  {"source".ljust(max_name_length)} = "./modules/{module_name}"',
        "",
    ]

    for variable in variables:
        name = variable.name.ljust(max_name_length)

        if variable.default is None:
            value = f'"<{variable.name}>"'
        else:
            value = format_example_value(
                variable.default,
                indent="    ",
            )

        lines.append(f"  {name} = {value}")

    lines.extend(
        [
            "}",
            "```",
        ]
    )

    return "\n".join(lines)


def generate_requirements_markdown(
    requirements: list[Requirement],
) -> str:
    """Generate a Markdown table for Terraform requirements."""

    if not requirements:
        return ""

    lines = [
        "## Requirements",
        "",
        "| Name | Version |",
        "|------|---------|",
    ]

    for requirement in requirements:
        lines.append(f"| {requirement.name} | `{requirement.version}` |")

    return "\n".join(lines)


def generate_providers_markdown(
    providers: list[Provider],
) -> str:
    """Generate a Markdown table for Terraform providers."""

    if not providers:
        return ""

    lines = [
        "## Providers",
        "",
        "| Name | Source | Version |",
        "|------|--------|---------|",
    ]

    for provider in providers:
        lines.append(
            f"| {provider.name} | `{provider.source}` | `{provider.version}` |"
        )

    return "\n".join(lines)


def generate_resources_markdown(
    resources: list[Resource],
) -> str:
    """Generate a Markdown table for Terraform resources."""

    if not resources:
        return ""

    lines = [
        "## Resources",
        "",
        "| Type | Name |",
        "|------|------|",
    ]

    for resource in resources:
        lines.append(f"| `{resource.type}` | `{resource.name}` |")

    return "\n".join(lines)


def generate_markdown(module: ModuleDocumentation) -> str:
    """Generate complete Terraform module documentation."""

    sections: list[str] = []

    example_md = generate_example_markdown(module.name, module.variables)
    if example_md:
        sections.append(example_md)

    requirements_md = generate_requirements_markdown(module.requirements)
    if requirements_md:
        sections.append(requirements_md)

    providers_md = generate_providers_markdown(module.providers)
    if providers_md:
        sections.append(providers_md)

    resources_md = generate_resources_markdown(module.resources)
    if resources_md:
        sections.append(resources_md)

    variables_md = generate_variables_markdown(module.variables)
    if variables_md:
        sections.append(variables_md)

    outputs_md = generate_outputs_markdown(module.outputs)
    if outputs_md:
        sections.append(outputs_md)

    return "\n\n".join(sections)
