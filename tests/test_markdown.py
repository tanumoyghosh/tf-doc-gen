from tf_doc_gen.markdown import (
    generate_example_markdown,
    generate_markdown,
    generate_providers_markdown,
    generate_requirements_markdown,
    generate_resources_markdown,
)
from tf_doc_gen.models import (
    ModuleDocumentation,
    Output,
    Provider,
    Requirement,
    Resource,
    Variable,
)


def test_generate_markdown_without_outputs():
    variables = [
        Variable(
            name="location",
            description="Azure region",
            type="string",
            default="eastus",
        )
    ]

    module = ModuleDocumentation(
        name="storage",
        variables=variables,
    )
    markdown = generate_markdown(module)

    assert 'module "storage"' in markdown
    assert "## Inputs" in markdown
    assert "## Outputs" not in markdown


def test_generate_markdown_without_variables():
    # Arrange
    module = ModuleDocumentation(
        name="storage",
        outputs=[
            Output(
                name="storage_account_id",
                description="Storage Account ID",
                value="azurerm_storage_account.this.id",
            )
        ],
    )

    # Act
    markdown = generate_markdown(module)

    # Assert
    assert 'module "storage"' in markdown
    assert "## Inputs" not in markdown
    assert "## Outputs" in markdown


def test_generate_markdown_with_variables_and_outputs():
    # Arrange
    module = ModuleDocumentation(
        name="storage",
        variables=[
            Variable(
                name="location",
                description="Azure region",
                type="string",
                default="eastus",
            )
        ],
        outputs=[
            Output(
                name="storage_account_id",
                description="Storage Account ID",
                value="azurerm_storage_account.this.id",
            )
        ],
    )

    # Act
    markdown = generate_markdown(module)

    # Assert
    assert 'module "storage"' in markdown
    assert '"./modules/storage"' in markdown
    assert "## Inputs" in markdown
    assert "## Outputs" in markdown
    assert "location" in markdown
    assert "storage_account_id" in markdown


def test_generate_requirements_markdown():
    requirements = [
        Requirement(
            name="Terraform",
            version=">= 1.6.0",
        )
    ]

    markdown = generate_requirements_markdown(requirements)

    assert "## Requirements" in markdown
    assert "Terraform" in markdown
    assert ">= 1.6.0" in markdown


def test_generate_providers_markdown():
    providers = [
        Provider(
            name="azurerm",
            source="hashicorp/azurerm",
            version="~> 4.0",
        )
    ]

    markdown = generate_providers_markdown(providers)

    assert "## Providers" in markdown
    assert "azurerm" in markdown
    assert "hashicorp/azurerm" in markdown
    assert "~> 4.0" in markdown


def test_generate_resources_markdown():
    resources = [
        Resource(
            type="random_string",
            name="suffix",
        ),
        Resource(
            type="random_integer",
            name="priority",
        ),
    ]

    markdown = generate_resources_markdown(resources)

    assert "## Resources" in markdown
    assert "random_string" in markdown
    assert "suffix" in markdown
    assert "random_integer" in markdown
    assert "priority" in markdown


def test_generate_markdown_with_all_sections():
    module = ModuleDocumentation(
        name="storage",
        requirements=[
            Requirement(
                name="Terraform",
                version=">= 1.6.0",
            )
        ],
        providers=[
            Provider(
                name="azurerm",
                source="hashicorp/azurerm",
                version="~> 4.0",
            )
        ],
        resources=[
            Resource(
                type="random_string",
                name="suffix",
            )
        ],
        variables=[
            Variable(
                name="location",
                description="Azure region",
                type="string",
                default="eastus",
            )
        ],
    )

    markdown = generate_markdown(module)

    assert 'module "storage"' in markdown
    assert '"./modules/storage"' in markdown
    assert "## Requirements" in markdown
    assert "## Providers" in markdown
    assert "## Resources" in markdown
    assert "## Inputs" in markdown


def test_generate_example_markdown():
    variables = [
        Variable(
            name="resource_group_name",
            description="Resource Group Name",
            type="string",
            default=None,
        ),
        Variable(
            name="location",
            description="Azure region",
            type="string",
            default="eastus",
        ),
    ]

    markdown = generate_example_markdown(
        "storage",
        variables,
    )

    assert 'module "storage"' in markdown
    assert '"./modules/storage"' in markdown
    assert "resource_group_name" in markdown
    assert '"<resource_group_name>"' in markdown
    assert "location" in markdown
    assert '"eastus"' in markdown
