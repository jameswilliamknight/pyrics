import logging


class Logger:

    __is_verbose = False

    def __init__(self, args):
        self.__is_verbose = args.verbose
        if self.__is_verbose:
            logging.basicConfig(level=logging.INFO)

    def verbose(self, *print_args):
        if self.__is_verbose:
            print(*print_args)

    @staticmethod
    def info(*print_args):
        print(*print_args)
