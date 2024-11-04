from collections import UserDict

class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, r):
        self.data[r.name.value] = r

    def find(self, name):
        try:
            return self.data[name]
        except KeyError:
            print(f"No record with name '{name}'")

    def delete(self, name):
        try:
            self.data.pop(name)
        except KeyError:
            print(f"No record with name '{name}'")

    def __str__(self):
        return "\n".join(map(str, self.data.values()))
