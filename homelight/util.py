import sys
import os


def alert(msg: str) -> None:
	print(msg, file=sys.stderr)


def absdir(path: str) -> str:
	current_dir = os.path.dirname(__file__).replace("\\", "/")
	upper_dir = "/".join(current_dir.split("/")[:-1])
	return upper_dir + path[1:]


if __name__ == '__main__':
	print(absdir("./config"))
