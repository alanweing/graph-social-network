
class UserGenerator:

    users_list = [
        {"name": "Ronald", "age": "47", "gender": "male", "employed": True, "musics":
            ["Green Day - Still Breathing", "Twenty One Pilots - Cancer"]
         },
        {"name": "Alexander", "age": "43", "gender": "male", "employed": False, "musics":
            ["Calvin Harris - My Way", "Alok - Hear me Now", "Make U Sweat - Nightlife is Magic"]
         },
        {"name": "Kylee", "age": "53", "gender": "female", "employed": True, "musics":
            ["Alesso - Take My Breath Away"]
         },
        {"name": "Gary", "age": "74", "gender": "male", "employed": False, "musics":
            ["Johann Sebastian", "Lise de la Salle", "Wolfgang Amade", "Robert Schumann"]
         },
        {"name": "Christina", "age": "61", "gender": "female", "employed": False, "musics":
            ["Franz Schubert", "Sergei Prokofiev"]
         },
        {"name": "Joyce", "age": "72", "gender": "female", "employed": False, "musics":
            ["The xx - VCR", "The xx - Islands", "Chet Faker - Release Your Problems", "Chet Faker - Talk is Cheap"]
         }
    ]

    @staticmethod
    def generate(number_of_users, uuids):
        uuids = [uuid for uuid in uuids]
        generated_users = []
        for user in UserGenerator.users_list:
            user_ = User(user["name"], uuids.pop(0))
            user_.age = user["age"]
            user_.employed = user["employed"]
            user_.gender = user["gender"]
            user_.music = user["musics"]
            generated_users.append(user_)
        return generated_users[0:number_of_users]


class User:
    def __init__(self, name, uuid):
        self._name = name
        self._info = {}
        self._uuid = uuid

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
