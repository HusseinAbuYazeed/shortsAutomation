from pathlib import Path


def read_file(path: Path) -> str:
    """Read a text file and return its content."""

    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def write_file(path: Path, content: str) -> None:
    """Write text content to a file."""

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

def wait_for_file(path: Path, message: str):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

        print(message)
        input("Press Enter when you're done...")

    return path