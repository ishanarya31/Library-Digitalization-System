from hash_table import HashSet, HashMap
from prime_generator import get_next_size



class DynamicHashSet:
    def __init__(self, collision_type, params):
        self.collision_type = collision_type
        self.size = params[-1]
        self.z = params[0]
        self.table = [None] * self.size
        self.element_count = 0

        if self.collision_type == "Double":
            self.z2 = params[1]
            self.c2 = params[2]

    def _hash(self, key):
        hash_value = 0
        for i, char in enumerate(key):
            hash_value += (ord(char) * (self.z ** i)) % self.size
        return hash_value % self.size

    def _double_hash(self, key):
        h1 = self._hash(key)
        h2 = self.c2 - (self._hash(key, self.z2) % self.c2)
        return h1, h2

    def get_slot(self, key):
        if self.collision_type == "Chain":
            return self._hash(key)
        elif self.collision_type == "Linear":
            slot = self._hash(key)
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot] == key:
                    return slot
                slot = (slot + 1) % self.size
                if slot == original_slot:
                    return None
            return slot
        elif self.collision_type == "Double":
            h1, h2 = self._double_hash(key)
            slot = h1
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot] == key:
                    return slot
                slot = (slot + h2) % self.size
                if slot == original_slot:
                    return None
            return slot

    def insert(self, x):
        slot = self.get_slot(x)
        if slot is not None:
            if self.collision_type == "Chain":
                if self.table[slot] is None:
                    self.table[slot] = []
                if x not in self.table[slot]:
                    self.table[slot].append(x)
            else:
                self.table[slot] = x
            self.element_count += 1

            if self.get_load() >= 0.5:
                self.rehash()

    def rehash(self):
        old_table = self.table
        self.size = get_next_size()
        self.table = [None] * self.size
        self.element_count = 0

        for slot in old_table:
            if slot:
                if isinstance(slot, list):
                    for item in slot:
                        self.insert(item)
                else:
                    self.insert(slot)

    def get_load(self):
        return self.element_count / self.size

    def __str__(self):
        output = []
        for slot in self.table:
            if slot is None:
                output.append("<EMPTY>")
            elif isinstance(slot, list):
                output.append(" | ".join(str(item) for item in slot))
            else:
                output.append(str(slot))
        return " ; ".join(output)



class DynamicHashMap:
    def __init__(self, collision_type, params):
        self.collision_type = collision_type
        self.size = params[-1]
        self.z = params[0]
        self.table = [None] * self.size
        self.element_count = 0

        if self.collision_type == "Double":
            self.z2 = params[1]
            self.c2 = params[2]

    def _hash(self, key):
        hash_value = 0
        for i, char in enumerate(key):
            hash_value += (ord(char) * (self.z ** i)) % self.size
        return hash_value % self.size

    def _double_hash(self, key):
        h1 = self._hash(key)
        h2 = self.c2 - (self._hash(key, self.z2) % self.c2)
        return h1, h2

    def get_slot(self, key):
        if self.collision_type == "Chain":
            return self._hash(key)
        elif self.collision_type == "Linear":
            slot = self._hash(key)
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot][0] == key:
                    return slot
                slot = (slot + 1) % self.size
                if slot == original_slot:
                    return None
            return slot
        elif self.collision_type == "Double":
            h1, h2 = self._double_hash(key)
            slot = h1
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot][0] == key:
                    return slot
                slot = (slot + h2) % self.size
                if slot == original_slot:
                    return None
            return slot

    def insert(self, key, value):
        slot = self.get_slot(key)
        if slot is not None:
            if self.collision_type == "Chain":
                if self.table[slot] is None:
                    self.table[slot] = []
                self.table[slot].append((key, value))
            else:
                self.table[slot] = (key, value)
            self.element_count += 1

            if self.get_load() >= 0.5:
                self.rehash()

    def rehash(self):
        old_table = self.table
        self.size = get_next_size()
        self.table = [None] * self.size
        self.element_count = 0

        for slot in old_table:
            if slot:
                if isinstance(slot, list):
                    for key, value in slot:
                        self.insert(key, value)
                else:
                    self.insert(slot[0], slot[1])

    def get_load(self):
        return self.element_count / self.size

    def __str__(self):
        output = []
        for slot in self.table:
            if slot is None:
                output.append("<EMPTY>")
            elif isinstance(slot, list):
                output.append(" ; ".join(f"{key}: {value}" for key, value in slot))
            else:
                output.append(f"{slot[0]}: {slot[1]}")
        return " ; ".join(output)
