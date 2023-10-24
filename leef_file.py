from typing import Dict, List, Tuple
from dataclasses import dataclass


__author__ = "Nazarii Nikitchyn"


class WrongHeaderStructure(Exception):
    def __init__(
        self, message="Header structure is incorrect", header_payload=""
    ) -> None:
        self.message = message + header_payload
        super().__init__(self.message)


class LeefHeader:
    """
    Represents a LEEF header object, which contains information parsed from a LEEF-formatted log file.

    Attributes:
        __header_structure (Tuple[str]): A tuple containing the expected structure of the LEEF header.
        __content (Dict[str, str]): A dictionary containing the parsed content of the LEEF header.

    Methods:
        __init__(self, payload: str, header_structure: Tuple[str]) -> None: Initializes a new LEEF header object.
        __parse(self, payload): Parses the given LEEF header payload and returns a dictionary containing the parsed content.
        __getitem__(self, key): Returns the value associated with the given key in the LEEF header content dictionary.
    """

    def __init__(
        self, payload: str, header_structure: Tuple[str], delimeter="\t"
    ) -> None:
        self.__header_structure = header_structure
        self.__content = self.__parse(payload)
        pass

    def __parse(self, payload):
        payload = payload.strip("LEEF:")
        res = {}
        items = tuple(filter(lambda x: x, payload.split("|")))

        # Handling wrong header structure
        if len(items) != len(self.__header_structure):
            raise WrongHeaderStructure(
                header_payload=f" Not equal number of header fields: header - {items}"
            )

        if len(set(self.__header_structure)) != len(self.__header_structure):
            raise WrongHeaderStructure(
                header_payload=" All header fields must be unique"
            )

        for idx, item in enumerate(items):
            res[self.__header_structure[idx]] = item
        return res

    def __getitem__(self, key):
        return self.__content[key]


@dataclass(frozen=True)
class Record:
    header: LeefHeader
    body: Dict[str, str]


class LeefFile:
    """
    A class representing a LEEF file.

    Attributes:
    __delimeter (str): The delimiter used in the LEEF file.
    __header_structure (List[str]): The structure of the LEEF file header.
    __records (Tuple[Record]): The parsed records of the LEEF file.

    Methods:
    _parse(payload: str) -> Tuple[Record]: Parses the payload of the LEEF file and returns a tuple of Record objects.
    get_content() -> List[Record]: Returns a list of all the Record objects in the LEEF file.
    records() -> Dict: A generator that yields each Record object in the LEEF file.
    """

    def __init__(
        self, payload: str, header_structure: List[str], delimeter="\t"
    ) -> None:
        """
        Initializes a new instance of the LeefFile class.

        Args:
        payload (str): The payload of the LEEF file.
        header_structure (List[str]): The structure of the LEEF file header.
        delimeter (str): The delimiter used in the LEEF file. Defaults to "\t".
        """
        self.__delimeter = delimeter
        self.__header_structure = header_structure
        self.__records = self._parse(payload)

    def _parse(self, payload: str) -> Tuple[Record]:
        """
        Parses the payload of the LEEF file and returns a tuple of Record objects.

        Args:
        payload (str): The payload of the LEEF file.

        Returns:
        Tuple[Record]: A tuple of Record objects.
        """
        content = []
        records = payload.split("\n")
        records = list(filter(lambda x: not x.isspace() and x, records))
        for record in records:
            body = {}
            record = record.split(self.__delimeter)
            header = record.pop(0)
            header = LeefHeader(header, self.__header_structure)
            for field in record:
                name, value = field.split("=", 1)
                body[name] = value
            content.append(Record(header, body))
        return tuple(content)

    def get_content(self) -> List[Record]:
        """
        Returns a list of all the Record objects in the LEEF file.

        Returns:
        List[Record]: A list of all the Record objects in the LEEF file.
        """
        return self.__records

    def records(self) -> Dict:
        """
        A generator that yields each Record object in the LEEF file.

        Yields:
        Dict: A dictionary representing a Record object.
        """
        for record in self.__records:
            yield record


def main():
    # from pathlib import Path

    # LEEF_FILE_HEADER = ("Version", "Vendor", "Product", "ProductVersion", "rule")
    # _path_to_script_dir = Path(__file__).parent.absolute()
    # file = open(str(_path_to_script_dir) + "/test.log", "r")
    # l = LeefFile(file.read(), LEEF_FILE_HEADER)
    # file.close()

    # for i in l.records():
    # print(i)

    # a = "LEEF:1.0|Incapsula|SIEMintegration|1.0|Normal|"
    # header = LeefHeader(["Version", "Vendor", "Product", "ProductVersion", "rule"], a)
    # print(a)
    pass


if __name__ == "__main__":
    main()
