from utils.args import get_args
from utils.logging import setup_logging

args = get_args()

setup_logging(args)

from server import Server


def main():
    server = Server(args)
    server.start()


if __name__ == '__main__':
	main()

