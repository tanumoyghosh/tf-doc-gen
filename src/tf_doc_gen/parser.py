from pathlib import Path
from typing import Any, cast

import hcl2

from tf_doc_gen.models import Output, Provider, Requirement, Resource, Variable

ENCODING = "utf-8"


def parse_file(file_path: str) -> dict[str, Any]:
    """Parse a Terraform file and return its contents."""

    with Path(file_path).open("r", encoding=ENCODING) as file:
        return cast(dict[str, Any], hcl2.load(file))


def clean(value: Any) -> Any:
    """Normalize values returned by python-hcl2."""

    if isinstance(value, str):
        return value.strip('"').removeprefix("${").removesuffix("}")

    return value


def extract_variables(data: dict[str, Any]) -> list[Variable]:
    """Extract Terraform variables from parsed HCL."""

    variables: list[Variable] = []

    for variable in data.get("variable", []):
        for name, attributes in variable.items():
            variables.append(
                Variable(
                    name=clean(name),
                    description=clean(attributes.get("description", "")),
                    type=clean(attributes.get("type")),
                    default=clean(attributes.get("default")),
                )
            )

    return variables


def extract_outputs(data: dict[str, Any]) -> list[Output]:
    """Extract Terraform outputs from parsed HCL."""

    outputs: list[Output] = []

    for output in data.get("output", []):
        for name, attributes in output.items():
            outputs.append(
                Output(
                    name=clean(name),
                    description=clean(attributes.get("description", "")),
                    value=clean(attributes.get("value")),
                )
            )

    return outputs


def extract_requirements(data: dict[str, Any]) -> list[Requirement]:
    """Extract Terraform version requirements."""

    requirements: list[Requirement] = []

    for terraform in data.get("terraform", []):
        required_version = terraform.get("required_version")

        if required_version:
            requirements.append(
                Requirement(
                    name="Terraform",
                    version=clean(required_version),
                )
            )

    return requirements


def extract_providers(data: dict[str, Any]) -> list[Provider]:
    """Extract Terraform required providers."""

    providers: list[Provider] = []

    for terraform in data.get("terraform", []):
        required_providers = terraform.get("required_providers", [])

        for provider_group in required_providers:
            for name, attributes in provider_group.items():
                if not isinstance(attributes, dict):
                    continue

                providers.append(
                    Provider(
                        name=clean(name),
                        source=clean(attributes.get("source", "")),
                        version=clean(attributes.get("version", "")),
                    )
                )

    return providers


def extract_resources(data: dict[str, Any]) -> list[Resource]:
    """Extract Terraform resources."""

    resources: list[Resource] = []

    for resource in data.get("resource", []):
        for resource_type, instances in resource.items():
            for resource_name in instances:
                resources.append(
                    Resource(
                        type=clean(resource_type),
                        name=clean(resource_name),
                    )
                )

    return resources


def parse_module(module_path: str) -> dict[str, Any]:
    """Parse all Terraform files in a module."""

    module = Path(module_path)

    if not module.exists():
        raise FileNotFoundError(f"Module not found: {module}")

    if not module.is_dir():
        raise NotADirectoryError(f"Expected a directory: {module}")

    merged: dict[str, Any] = {}

    for tf_file in sorted(module.glob("*.tf")):
        parsed = parse_file(str(tf_file))

        for key, value in parsed.items():
            if isinstance(value, list):
                merged.setdefault(key, []).extend(value)
            else:
                merged[key] = value

    return merged
