import ast
from pathlib import Path
from typing import List, Set


class DirectoryStructure:
    """
    ディレクトリの構造を解析するクラス。
    指定されたディレクトリ内のPythonファイルをリストアップし、
    それぞれのファイルから関数、クラス、メソッドを抽出します。
    """

    def __init__(self, directory: str, ignore_folders: Set[str] = None):
        """
        クラスの初期化メソッド。

        Args:
            directory (str): 解析するディレクトリのパス。
            ignore_folders (Set[str], optional): 無視するフォルダのセット。デフォルトはNone。
        """
        self.directory = Path(directory)
        self.ignore_folders = ignore_folders if ignore_folders else set()

    def list_py_files(self) -> List[Path]:
        """
        指定されたディレクトリ内のすべてのPythonファイルを再帰的にリストアップします。
        無視するフォルダ内のファイルはリストアップしません。

        Returns:
            List[Path]: Pythonファイルのパスのリスト。
        """
        py_files = []
        for path in self.directory.rglob("*.py"):
            if not any(ignored in path.parts for ignored in self.ignore_folders):
                py_files.append(path)
        return py_files

    def extract_definitions(self, node: ast.AST, indent_level: int = 1) -> List[str]:
        """
        ASTノードから関数、クラス、およびメソッドの定義を抽出します。

        Args:
            node (ast.AST): ASTノード。
            indent_level (int): インデントのレベル。

        Returns:
            List[str]: 関数、クラス、およびメソッドのリスト。
        """
        indent = " " * 4 * indent_level
        definitions = []

        if isinstance(node, ast.FunctionDef):
            definitions.append(f"{indent}Function: {node.name}()")

        elif isinstance(node, ast.ClassDef):
            definitions.append(f"{indent}Class: {node.name}")
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    definitions.append(f"{indent}    Method: {child.name}()")

        return definitions

    def parse_file_structure(self, py_file: Path) -> List[str]:
        """
        指定されたPythonファイルの構造を解析し、関数、クラス、およびメソッドを抽出します。

        Args:
            py_file (Path): Pythonファイルのパス。

        Returns:
            List[str]: ファイル内の関数、クラス、およびメソッドのリスト。
        """
        with open(py_file, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read(), filename=py_file)

        definitions = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                definitions.extend(self.extract_definitions(node))

        return definitions
