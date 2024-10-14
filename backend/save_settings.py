from dataclasses import dataclass
import pickle
from typing import TypeVar, Type

T = TypeVar('T')


def write_dataclass_to_file(obj: object, filename: str) -> None:
    """
    Write a dataclass object to a file using pickle serialization.

    :param obj: The dataclass object to write
    :param filename: The name of the file to write to
    """
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)


def read_dataclass_from_file(cls: Type[T], filename: str) -> T:
    """
    Read a dataclass object from a file using pickle deserialization.

    :param cls: The dataclass type to read into
    :param filename: The name of the file to read from
    :return: An instance of the dataclass
    """
    try:
        with open(filename, 'rb') as file:
            obj = pickle.load(file)
    except FileNotFoundError:
        print("interface not found")
        return None

    if not isinstance(obj, cls):
        raise TypeError(f"The object in the file is not an instance of {cls.__name__}")

    return obj

if __name__ == '__main__':
    # Example usage:
    @dataclass
    class Person:
        name: str
        age: int
        city: str


    # Creating a Person object
    person = Person(name="Alice", age=30, city="New York")

    # Writing to file
    write_dataclass_to_file(person, "person.pkl")

    # Reading from file
    loaded_person = read_dataclass_from_file(Person, "person.pkl")

    print(loaded_person)  # This should print: Person(name='Alice', age=30, city='New York')