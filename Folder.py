import os
from os import listdir, path
from typing import List, Union, Optional
from datetime import datetime

from File import File


class FolderDoesNotExist(Exception):
    pass


class Folder(File):
    def __init__(
            self,
            name: str,
            absolute_path: str,
            size: int,
            last_modified: datetime,
            is_hidden: bool,
            children: Optional[List[Union['Folder', File]]] = None
    ) -> None:
        File.__init__(self, name, absolute_path, size, last_modified, is_hidden)
        self.children = children
        self.is_dir = True
        self.filetype = 'folder'

    @staticmethod
    def from_path(target_dir: str) -> 'Folder':
        folder_absolute_path = str(path.abspath(target_dir))
        folder_name = folder_absolute_path.split('/')[-1]

        if not path.isdir(folder_absolute_path):
            raise FolderDoesNotExist(f"'{folder_absolute_path}' is not a valid directory.")

        folder_stats = os.stat(folder_absolute_path)

        return Folder(
            name=folder_name,
            absolute_path=folder_absolute_path,
            size=folder_stats.st_size,
            last_modified=datetime.fromtimestamp(folder_stats.st_mtime),
            is_hidden=folder_name[0] == ".",
        )

    def get_children(
            self,
            max_depth: int = 0,
            current_depth: int = 0,
            exclude: List[str] = None,
            show_hidden: bool = False,
    ) -> None:
        children: List[Union[Folder, File]] = []
        exclude = exclude or []

        for item in listdir(self.absolute_path):
            if item in exclude:
                continue

            item_hidden = item[0] == "."

            if item_hidden and not show_hidden:
                continue

            item_absolute_path = path.join(self.absolute_path, item)
            item_stats = os.stat(item_absolute_path)
            class_variables = {
                "name": item,
                "absolute_path": item_absolute_path,
                "size": item_stats.st_size,
                "last_modified": datetime.fromtimestamp(item_stats.st_mtime),
                "is_hidden": item_hidden,
            }

            if path.isdir(item_absolute_path):
                folder = Folder(**class_variables)

                if current_depth < max_depth:
                    folder.get_children(max_depth=max_depth, current_depth=1, show_hidden=show_hidden)

                children.append(folder)
            else:
                children.append(File(**class_variables))

        self.children = sorted(children, key=lambda x: (not x.is_dir, x.name))