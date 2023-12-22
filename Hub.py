class Hub:
    _id = -1
    _name = ""
    __id_counter__ = 0

    def __init__(self, name):
        self._id = self.__class__.__id_counter__
        self.__class__.__id_counter__ += 1
        self._name = name

    def get_name(self):
        return self._name

    def __str__(self):
        return f"Точка {self._name} с id {self._id}"

    def __repr__(self):
        return f"[{self._name}:{self._id}]"

    def __hash__(self):
        return self._id
