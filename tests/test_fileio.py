from pathlib import Path

from tf_doc_gen.fileio import (
    BEGIN_MARKER,
    ENCODING,
    END_MARKER,
    is_readme_up_to_date,
    update_readme,
)


def test_creates_readme_when_missing(tmp_path: Path):
    content = "## Inputs"

    update_readme(tmp_path, content)

    readme = tmp_path / "README.md"

    assert readme.exists()

    text = readme.read_text()

    assert BEGIN_MARKER in text
    assert END_MARKER in text
    assert content in text


def test_appends_markers_when_readme_has_no_markers(tmp_path: Path):
    # Arrange
    readme = tmp_path / "README.md"
    readme.write_text("# My Module", encoding=ENCODING)

    content = "## Inputs"

    # Act
    update_readme(tmp_path, content)

    # Assert
    text = readme.read_text(encoding=ENCODING)

    assert text.startswith("# My Module")
    assert BEGIN_MARKER in text
    assert END_MARKER in text
    assert content in text


def test_replaces_existing_generated_section(tmp_path: Path):
    # Arrange
    readme = tmp_path / "README.md"

    readme.write_text(
        f"""# My Module

Some introduction.

{BEGIN_MARKER}

Old generated content

{END_MARKER}

## License
MIT
""",
        encoding=ENCODING,
    )

    content = "## Inputs"

    # Act
    update_readme(tmp_path, content)

    # Assert
    text = readme.read_text(encoding=ENCODING)

    assert "Old generated content" not in text
    assert content in text
    assert "# My Module" in text
    assert "Some introduction." in text
    assert "## License" in text
    assert text.count(BEGIN_MARKER) == 1
    assert text.count(END_MARKER) == 1


def test_is_readme_up_to_date_returns_true(tmp_path: Path):
    # Arrange
    content = "## Inputs"

    update_readme(tmp_path, content)

    # Act
    result = is_readme_up_to_date(tmp_path, content)

    # Assert
    assert result is True


def test_is_readme_up_to_date_returns_false_when_content_changes(tmp_path: Path):
    # Arrange
    update_readme(tmp_path, "Old content")

    # Act
    result = is_readme_up_to_date(tmp_path, "New content")

    # Assert
    assert result is False


def test_is_readme_up_to_date_returns_false_when_readme_missing(tmp_path: Path):
    # Act
    result = is_readme_up_to_date(tmp_path, "## Inputs")

    # Assert
    assert result is False


def test_is_readme_up_to_date_returns_false_without_markers(tmp_path: Path):
    # Arrange
    readme = tmp_path / "README.md"

    readme.write_text(
        "# My Module",
        encoding=ENCODING,
    )

    # Act
    result = is_readme_up_to_date(tmp_path, "## Inputs")

    # Assert
    assert result is False
