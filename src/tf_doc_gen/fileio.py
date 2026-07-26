from pathlib import Path

BEGIN_MARKER = "<!-- BEGIN_TF_DOCS -->"
END_MARKER = "<!-- END_TF_DOCS -->"
ENCODING = "utf-8"


def write_readme(module_path: Path, content: str) -> None:
    """Write generated documentation to README.md."""

    readme = module_path / "README.md"
    readme.write_text(content, encoding=ENCODING)


def update_readme(module_path: Path, content: str) -> None:
    """Update the generated section in README.md."""

    readme = module_path / "README.md"

    if not readme.exists():
        readme.write_text(
            f"{BEGIN_MARKER}\n\n{content}\n\n{END_MARKER}\n",
            encoding=ENCODING,
        )
        return

    existing = readme.read_text(encoding=ENCODING)

    start = existing.find(BEGIN_MARKER)
    end = existing.find(END_MARKER)

    if start == -1 or end == -1:
        updated = (
            existing.rstrip()
            + "\n\n"
            + BEGIN_MARKER
            + "\n\n"
            + content
            + "\n\n"
            + END_MARKER
            + "\n"
        )

        readme.write_text(updated, encoding=ENCODING)

        return

    updated = (
        existing[: start + len(BEGIN_MARKER)]
        + "\n\n"
        + content
        + "\n\n"
        + existing[end:]
    )

    readme.write_text(updated, encoding=ENCODING)


def is_readme_up_to_date(module_path: Path, content: str) -> bool:
    """Return True if the generated README content is already up to date."""

    readme = module_path / "README.md"

    if not readme.exists():
        return False

    existing = readme.read_text(encoding=ENCODING)

    start = existing.find(BEGIN_MARKER)
    end = existing.find(END_MARKER)

    if start == -1 or end == -1:
        return False

    end += len(END_MARKER)

    generated = BEGIN_MARKER + "\n\n" + content + "\n\n" + END_MARKER

    existing_generated = existing[start:end].strip()

    return existing_generated == generated.strip()
