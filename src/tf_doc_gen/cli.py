from importlib.metadata import version as package_version
from pathlib import Path

import typer

from tf_doc_gen.fileio import is_readme_up_to_date, update_readme
from tf_doc_gen.markdown import generate_markdown
from tf_doc_gen.models import ModuleDocumentation
from tf_doc_gen.output import print_variables
from tf_doc_gen.parser import (
    extract_outputs,
    extract_providers,
    extract_requirements,
    extract_resources,
    extract_variables,
    parse_module,
)

app = typer.Typer(
    help=(
        "Generate beautiful Markdown documentation for Terraform modules.\n\n"
        "Supports Terraform requirements, providers, resources, inputs, "
        "outputs and example usage."
    )
)


@app.command()
def version() -> None:
    """Display the installed tf-doc-gen version."""
    typer.echo(package_version("tf-doc-gen"))


@app.command()
def parse(
    module_path: str = typer.Argument(
        ...,
        help="Path to the Terraform module directory.",
    ),
) -> None:
    """Parse and display the input variables defined by a Terraform module."""

    data = parse_module(module_path)

    variables = extract_variables(data)

    print_variables(variables)


@app.command()
def generate(
    module_path: str = typer.Argument(
        ...,
        help="Path to the Terraform module directory.",
    ),
    stdout: bool = typer.Option(
        False,
        "--stdout",
        help="Print the generated Markdown to standard output instead of updating README.md.",
    ),
    check: bool = typer.Option(
        False,
        "--check",
        help="Verify that README.md is up to date without modifying it.",
    ),
) -> None:
    """Generate or validate Terraform module documentation."""

    data = parse_module(module_path)

    module_path_obj = Path(module_path)

    module_doc = ModuleDocumentation(
        name=module_path_obj.name,
        requirements=extract_requirements(data),
        providers=extract_providers(data),
        resources=extract_resources(data),
        variables=extract_variables(data),
        outputs=extract_outputs(data),
    )

    markdown = generate_markdown(module_doc)

    if stdout:
        typer.echo(markdown)
        return

    if check:
        if is_readme_up_to_date(module_path_obj, markdown):
            typer.echo("README.md is up to date.")
            raise typer.Exit(code=0)

        typer.echo("README.md is out of date.")
        raise typer.Exit(code=1)

    update_readme(module_path_obj, markdown)

    typer.echo("README.md generated successfully.")


def main() -> None:
    app()
