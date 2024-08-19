from typing import Set
from .directory_structure import DirectoryStructure


class DirectoryPrinter:
    """
    ディレクトリの構造を表示するクラス。
    DirectoryStructureクラスを使用してディレクトリを解析し、結果を表示します。
    """

    def __init__(self, directory: str, ignore_folders: Set[str] = None):
        """
        クラスの初期化メソッド。

        Args:
            directory (str): 表示するディレクトリのパス。
            ignore_folders (Set[str], optional): 無視するフォルダのセット。デフォルトはNone。
        """
        self.structure = DirectoryStructure(directory, ignore_folders)

    def print_structure(self) -> None:
        """
        ディレクトリの構造を表示します。
        各ディレクトリとファイルの階層を反映して、インデントを調整します。
        """
        for path in sorted(self.structure.directory.rglob("*")):
            if any(ignored in path.parts for ignored in self.structure.ignore_folders):
                continue

            level = len(path.relative_to(self.structure.directory).parts) - 1
            indent = " " * 4 * level

            if path.is_dir():
                print(f"{indent}{path.name}/")
            elif path.suffix == ".py":
                print(f"{indent}{path.name}")
                definitions = self.structure.parse_file_structure(path)
                for definition in definitions:
                    print(f"{indent}    {definition}")
