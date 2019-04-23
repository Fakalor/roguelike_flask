class Item:
    ''' nadklasa przedmiotow '''
    def __init__(self):
        self._typeItem = ''
        self._addStrenght = 0
        self._addDexterity = 0
        self._addStamina = 0

    @property
    def addStrenght(self):
        return self._addStrenght
    @addStrenght.setter
    def addStrenght(self, value):
        self._addStrenght = int(value)

    @property
    def addDexterity(self):
        return self._addDexterity
    @addDexterity.setter
    def addDexterity(self, value):
        self._addDexterity = int(value)

    @property
    def addStamina(self):
        return self._addStamina
    @addStamina.setter
    def addStamina(self, value):
        self._addStamina = int(value)