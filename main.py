from directory_structure.directory_printer import DirectoryPrinter


def main():
    # 実行するディレクトリを指定します。
    directory = "src"
    ignore_folders = {"__pycache__"}

    printer = DirectoryPrinter(directory=directory, ignore_folders=ignore_folders)
    printer.print_structure()


if __name__ == "__main__":
    main()
