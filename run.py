import math
import argparse
from typing import List

from Folder import Folder, FolderDoesNotExist


def create_guidelines(depth: int, indent: int, symbol: str = "|") -> str:
    return f"{(' ' * math.ceil((indent - 1) / 2) + symbol + ' ' * math.floor((indent - 1) / 2)) * depth}"


def print_folder_structure(folder: Folder, depth: int = 0, indent: int = 4) -> None:
    print(f"{create_guidelines(depth=depth, indent=indent)} {folder}")

    if folder.children:
        for file in folder.children:
            if file.is_dir:
                print_folder_structure(file, depth=depth + 1)
                if file.children:
                    print(create_guidelines(depth=depth + 1, indent=indent))
            else:
                print(f"{create_guidelines(depth=depth + 1, indent=indent)} {file}")


def main(target_dir: str = ".", depth: int = 1, show_hidden: bool = False, exclude: List[str] = None) -> None:
    directory = Folder.from_path(target_dir)
    directory.get_children(max_depth=depth, exclude=exclude, show_hidden=show_hidden)

    print_folder_structure(directory)


def parse_bool(raw: str) -> bool:
    if raw.lower() in ['n', 'no', 'f', 'false', '0']:
        return False

    return True


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', type=str, required=False, default=".", help="The directory to explore.")
    parser.add_argument('-d', '--depth', type=int, required=False, default=1, help="How many levels to traverse.")
    parser.add_argument(
        '-sh',
        '--show_hidden',
        type=parse_bool,
        required=False,
        default=True,
        help="Show hidden files."
    )
    parser.add_argument(
        '-e',
        '--exclude',
        action='append',
        required=False,
        default=None,
        help="Folder name to exclude. Repeat flag for multiple folders.",
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    try:
        main(target_dir=args.folder, depth=args.depth, show_hidden=args.show_hidden, exclude=args.exclude)
    except FolderDoesNotExist as error:
        print(f"{error.__class__.__name__}: {str(error)}")
