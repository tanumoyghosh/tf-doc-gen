from pathlib import Path

import pytest

from tf_doc_gen.parser import (
    ENCODING,
    extract_outputs,
    extract_providers,
    extract_requirements,
    extract_resources,
    extract_variables,
    parse_file,
    parse_module,
)


def test_extract_variables():
    data = parse_file("examples/storage/variables.tf")

    variables = extract_variables(data)

    assert len(variables) == 3

    assert variables[0].name == "resource_group_name"
    assert variables[0].default is None

    assert variables[1].name == "location"
    assert variables[1].default == "eastus"

    assert variables[2].type == "map(string)"


def test_parse_module_merges_multiple_tf_files(tmp_path: Path):
    # Arrange
    (tmp_path / "variables.tf").write_text(
        """
variable "location" {
  type = string
}
""",
        encoding=ENCODING,
    )

    (tmp_path / "network.tf").write_text(
        """
variable "vnet_name" {
  type = string
}
""",
        encoding=ENCODING,
    )

    # Act
    data = parse_module(str(tmp_path))
    variables = extract_variables(data)

    # Assert
    assert len(variables) == 2
    names = {variable.name for variable in variables}
    assert names == {"location", "vnet_name"}


def test_parse_module_merges_outputs_from_multiple_tf_files(tmp_path: Path):
    # Arrange
    (tmp_path / "outputs_storage.tf").write_text(
        """
output "storage_account_id" {
  value = "storage-id"
}
""",
        encoding=ENCODING,
    )

    (tmp_path / "outputs_network.tf").write_text(
        """
output "vnet_id" {
  value = "vnet-id"
}
""",
        encoding=ENCODING,
    )

    # Act
    data = parse_module(str(tmp_path))
    outputs = extract_outputs(data)

    # Assert
    assert len(outputs) == 2
    names = {output.name for output in outputs}
    assert names == {"storage_account_id", "vnet_id"}


def test_parse_module_returns_empty_dict_for_empty_directory(tmp_path: Path):
    # Act
    data = parse_module(str(tmp_path))

    # Assert
    assert data == {}


def test_parse_module_raises_file_not_found_for_missing_directory():
    # Arrange
    missing_path = "does-not-exist"

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        parse_module(missing_path)


def test_parse_module_raises_not_a_directory(tmp_path: Path):
    # Arrange
    file = tmp_path / "main.tf"
    file.write_text("", encoding=ENCODING)

    # Act / Assert
    with pytest.raises(NotADirectoryError):
        parse_module(str(file))


def test_extract_requirements():
    # Arrange
    data = parse_file("examples/storage/versions.tf")

    # Act
    requirements = extract_requirements(data)

    # Assert
    assert len(requirements) == 1
    assert requirements[0].name == "Terraform"
    assert requirements[0].version == ">= 1.6.0"


def test_extract_providers():
    # Arrange
    data = parse_file("examples/storage/versions.tf")

    # Act
    providers = extract_providers(data)

    # Assert
    assert len(providers) == 2

    assert providers[0].name == "azurerm"
    assert providers[0].source == "hashicorp/azurerm"
    assert providers[0].version == "~> 4.0"

    assert providers[1].name == "random"
    assert providers[1].source == "hashicorp/random"
    assert providers[1].version == "~> 3.7"


def test_extract_resources():
    # Arrange
    data = parse_file("examples/storage/main.tf")

    # Act
    resources = extract_resources(data)

    # Assert
    assert len(resources) == 2

    names = {resource.name for resource in resources}
    resource_types = {resource.type for resource in resources}

    assert names == {"suffix", "priority"}
    assert resource_types == {
        "random_string",
        "random_integer",
    }
