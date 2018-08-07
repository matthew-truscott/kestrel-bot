import br_vec as vec

class Character(object):
    def __init__(self, name,
                 init_energy,
                 init_warmth,
                 init_sanity,
                 init_health):
        self.id = -1 # unset
        self.name = name
        self.energy = init_energy
        self.warmth = init_warmth
        self.sanity = init_sanity
        self.health = init_health
        self.alignment = 0
        self.position = [0, 0]
        self.active = False
        self.alive = True
        self.position = None

    def set_position(self, x, y):
        self.position = vec.vec2(x, y)

    def set_id(self, id):
        self.id = id
