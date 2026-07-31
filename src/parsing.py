import sys


class Parser:
    def __init__(self) -> None:
        pass

    @classmethod
    def parse(cls):
        try:

            filename = sys.argv[1]

            splitted_filename = filename.split(".")

            if len(splitted_filename) != 2 or len(splitted_filename[0]) < 1:
                raise ValueError("the configuration file name are incorrect")

            if splitted_filename[1] != "json":
                raise ValueError("the configuration file must be a json file")

        except Exception as e:
            print("Error:", e)
            sys.exit()
