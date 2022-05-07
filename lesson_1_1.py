from abc import ABC, abstractmethod
import json


class SerializationInterface(ABC):

    @abstractmethod
    def serialization(self, *args):
        pass

    @abstractmethod
    def deserialization(self, *args):
        pass


class Serialization(SerializationInterface):

    def serialization(self, *args):
        return json.dumps(args, indent=1)

    def deserialization(self, *args):
        return json.loads(*args)


json_file = """{
  "car": "Mercedes",
  "color": "Black",
  "year": 2022,
  "class": ["A", "S", "C"]
}"""


data = json.loads(json_file)
car = Serialization()
car.serialization(data)
car.deserialization(json_file)
