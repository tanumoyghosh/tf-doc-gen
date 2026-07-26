from rich.console import Console
from rich.table import Table

from tf_doc_gen.models import Variable

console = Console()


def print_variables(variables: list[Variable]) -> None:
    """Print variables as a table."""

    table = Table(title="Terraform Variables", show_lines=True)

    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Default", justify="center")
    table.add_column("Description")

    for variable in variables:
        default = "-" if variable.default is None else str(variable.default)
        table.add_row(
            variable.name,
            variable.type,
            default,
            variable.description,
        )

    console.print(table)
