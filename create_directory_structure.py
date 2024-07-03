import os


def create_directory_structure(base_path):
    structure = {
        "app": {
            "__init__.py": "",
            "main.py": "",
            "api": {"__init__.py": "", "endpoints": {"__init__.py": ""}},
        },
        "tests": {"__init__.py": "", "test_main.py": ""},
        ".gitignore": "",
        "requirements.txt": "",
        "README.md": "",
        ".pre-commit-config.yaml": "",
    }

    def create_structure(current_path, structure):
        for name, content in structure.items():
            path = os.path.join(current_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                with open(path, "w") as f:
                    f.write(content)

    create_structure(base_path, structure)


# Usage
create_directory_structure("side-project")
