class Character(object):
    def __init__(self, name,
                 init_energy,
                 init_warmth,
                 init_sanity,
                 init_health):
        self.id
        self.name = name
        self.energy = init_energy
        self.warmth = init_warmth
        self.sanity = init_sanity
        self.health = init_health
        self.alignment = 0
        self.position = [0, 0]
        self.active = False
        self.alive = True

    def set_position(self, rowpos, colpos):
        self.position = [rowpos, colpos]
