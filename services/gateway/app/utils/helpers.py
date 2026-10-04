from pathlib import Path


def verify_path_exists(dir_name, parents=False):
    dir = Path(dir_name)
    dir.mkdir(parents=parents, exist_ok=True)
