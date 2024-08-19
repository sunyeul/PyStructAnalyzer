import ast
from pathlib import Path
from typing import List, Set, Optional
from .explainer import SourceCodeExplainer


class DirectoryStructure:
    """
    ディレクトリの構造を解析するクラス。
    指定されたディレクトリ内のPythonファイルをリストアップし、
    それぞれのファイルから関数、クラス、メソッドを抽出します。
    """

    def __init__(self, directory: str, ignore_folders: Optional[Set[str]] = None):
        """
        クラスの初期化メソッド。

        Args:
            directory (str): 解析するディレクトリのパス。
            ignore_folders (Set[str], optional): 無視するフォルダのセット。デフォルトはNone。
        """
        self.directory = Path(directory)
        self.ignore_folders = ignore_folders if ignore_folders else set()
        self.exlainer = SourceCodeExplainer()

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

    def extract_definitions(
        self, node: ast.AST, source_code: str, indent_level: int = 1
    ) -> List[str]:
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
            func_code: str = ast.get_source_segment(source_code, node)
            explanation = self.exlainer.explain(func_code)
            definitions.append(f"{indent}Function: {node.name}() - {explanation}")

        elif isinstance(node, ast.ClassDef):
            class_code: str = ast.get_source_segment(source_code, node)
            explanation = self.exlainer.explain(class_code)
            definitions.append(f"{indent}Class: {node.name} - {explanation}")
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    method_code: str = ast.get_source_segment(source_code, child)
                    explanation = self.exlainer.explain(method_code)
                    definitions.append(
                        f"{indent}    Method: {child.name}() - {explanation}"
                    )

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
            source_code = file.read()
            tree = ast.parse(source_code, filename=py_file)

        definitions = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                definitions.extend(self.extract_definitions(node, source_code))

        return definitions
