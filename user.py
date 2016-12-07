
class User:
    def __init__(self, name, uuid):
        self._name = name
        self._info = {}
        self._uuid = uuid

    # def __setattr__(self, key, value):
    #     if key == "age":
    #         self.info["age"] = value
    #     else:
    #         setattr(self, key, value)

    def __str__(self):
        return 'name: {}\nuuid: {}\n'.format(self._name, self._uuid) + '\n'\
            .join(str(key) + ": " + str(value) for key, value in self._info.items())

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def age(self):
        return self._info["age"] if "age" in self._info else None

    @age.setter
    def age(self, age):
        self._info["age"] = age

    @property
    def music(self):
        return self._info["music"] if "music" in self._info else None

    @music.setter
    def music(self, music):
        if isinstance(music, type([])):
            self._info["music"] = music
        elif isinstance(music, type("")):
            try:
                self._info["music"].append(music)
            except (KeyError, AttributeError):
                self._info["music"] = []
                self._info["music"].append(music)

    @property
    def gender(self):
        return self._info["gender"] if "gender" in self._info else None

    @gender.setter
    def gender(self, gender):
        self._info["gender"] = gender

    @property
    def employed(self):
        return self._info["employed"] if "employed" in self._info else None

    @employed.setter
    def employed(self, is_employed):
        self._info["employed"] = is_employed

    @property
    def uuid(self):
        return self._uuid
