from datetime import datetime

BOLD = "\033[1m"
GREY = "\033[37m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
END = "\033[0m"

FILE_TYPE_COLOUR_MAP = {
    'folder': BOLD,
    'hidden': GREY,
    'js': YELLOW,
    'jsx': YELLOW,
    'ts': CYAN,
    'tsx': CYAN,
    'scss': PURPLE,
    'py': GREEN,
    'yml': BLUE,
    'json': BLUE,
}

MAX_FILENAME_LENGTH = 24


def file_size_to_str(size: int) -> str:
    scale_unit = 'b'
    scale_size = size

    for unit in ['kb', 'mb', 'gb', 'tb']:
        if scale_size < 1024:
            break

        scale_unit = unit
        scale_size /= 1024

    return f"{round(scale_size)}{scale_unit}"


class File:
    def __init__(self, name: str, absolute_path: str, size: int, last_modified: datetime, is_hidden: bool) -> None:
        self.name = name
        self.absolute_path = absolute_path
        self.size = size
        self.last_modified = last_modified
        self.is_hidden = is_hidden
        self.is_dir = False
        self.filetype = name.split(".")[-1]

    def __str__(self) -> str:
        name = self.name

        if len(name) > MAX_FILENAME_LENGTH:
            name = name[:MAX_FILENAME_LENGTH - 3] + "..."

        return (
            f"{FILE_TYPE_COLOUR_MAP.get('hidden' if self.is_hidden else self.filetype, '')}{name}{END} "
            f"{' ' * (MAX_FILENAME_LENGTH - len(name))}"
            f"{'' if self.is_dir else file_size_to_str(self.size):>6} "
            f"    "
            f"{self.last_modified.strftime('%H:%M:%S, %d %b %Y')}"
        )
