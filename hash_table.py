from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Initialize the hash table with the given collision type and parameters.
        
        collision_type : "Chain", "Linear", or "Double"
        params : 
            - For "Chain" or "Linear" -> (z, table_size)
            - For "Double" -> (z1, z2, c2, table_size)
        '''
        self.collision_type = collision_type
        self.size = params[-1]  # Initial table size
        self.z = params[0]
        self.table = [None] * self.size
        self.element_count = 0  # Number of elements in the table
        self.no_more_primes = False  # Track if rehashing can continue

        if self.collision_type == "Double":
            self.z2 = params[1]
            self.c2 = params[2]

    def _hash(self, key, z=None, size=None):
        # Polynomial accumulation hash function
        z = z if z else self.z
        size = size if size else self.size
        hash_value = 0
        for i, char in enumerate(key):
            hash_value += (ord(char) * (z ** i)) % size
        return hash_value % size

    def _double_hash(self, key):
        # Secondary hash function for double hashing
        h1 = self._hash(key, self.z)
        h2 = self.c2 - (self._hash(key, self.z2) % self.c2)
        return h1, h2

    def get_slot(self, key):
        # Calculate the slot index based on the collision handling type
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

    def insert(self, x):
        # Insert x based on whether it is a key (HashSet) or (key, value) (HashMap)
        key = x if isinstance(x, str) else x[0]
        slot = self.get_slot(key)
        
        if slot is not None:
            if self.collision_type == "Chain":
                if self.table[slot] is None:
                    self.table[slot] = []
                if x not in self.table[slot]:  # Prevent duplicates in chaining
                    self.table[slot].append(x)
            else:
                # For Linear or Double hashing, place the item directly in the calculated slot
                self.table[slot] = x

            self.element_count += 1

            # Trigger rehashing if load factor exceeds 0.5
            if self.get_load() >= 0.5:
                self.rehash()


    def find(self, key):
        # Return True if key is found, else False
        slot = self.get_slot(key)
        if self.collision_type == "Chain":
            if self.table[slot] is None:
                return False
            return key in [item if isinstance(item, str) else item[0] for item in self.table[slot]]
        return self.table[slot] is not None and (self.table[slot] if isinstance(self.table[slot], str) else self.table[slot][0]) == key

    def get_load(self):
        # Calculate load factor α
        return self.element_count / self.size

    

    def __str__(self):
        result = []

        for slot in self.table:
            if slot is None:
                # For an empty slot, we use the specified empty slot indicator
                result.append("<EMPTY>")
            elif isinstance(slot, list):  # Chaining case
                # Chain entries within the same slot separated by ";"
                chain_entries = []
                for item in slot:
                    if isinstance(item, tuple):  # HashMap entry (key, value)
                        chain_entries.append(f"{item[0]}, {item[1]}")
                    else:  # HashSet entry, just the key
                        chain_entries.append(str(item))
                result.append(" ; ".join(chain_entries))
            else:  # Probing case (Linear or Double hashing)
                # Single entry in each slot
                if isinstance(slot, tuple):  # HashMap entry
                    result.append(f"{slot[0]}, {slot[1]}")
                else:  # HashSet entry
                    result.append(str(slot))

        # Join each slot with "|" to create the final table representation
        return " | ".join(result)



    
    def rehash(self):
        try:
            new_size = get_next_size()
            if new_size is None:
                # No more primes available for resizing
                self.no_more_primes = True
                return

            # Retrieve and store current items in order
            old_items = self.items()
            
            # Update table size and reset
            self.size = new_size
            self.table = [None] * new_size
            self.element_count = 0  # Reset element count

            # Reinsert each item into the new table to preserve original sequence
            for item in old_items:
                if isinstance(item, tuple):
                    self.insert(item)  # For HashMap (key, value) pairs
                else:
                    self.insert(item)  # For HashSet items
        except IndexError:
            # Handle the case gracefully without errors when primes are exhausted
            self.no_more_primes = True


    


class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)

    def insert(self, x):
        if not self.find(x):
            super().insert(x)

    def find(self, key):
        # Check if the key is in the HashSet
        return super().find(key)
    
    def items(self):
        # Collect all items in the hash table and return them as a list
        entries = []
        for slot in self.table:
            if slot is not None:
                if isinstance(slot, list):  # For chaining, where each slot is a list of items
                    entries.extend(slot)
                else:  # For linear probing or double hashing, where each slot is a single item
                    entries.append(slot)
        return entries
    
    def give(self):
        # This version of give will iterate through each slot to maintain order as much as possible
        ordered_items = []
        for slot in self.table:
            if slot is not None:
                if isinstance(slot, list):  # Chaining case
                    ordered_items.extend(slot)  # Preserves order within each slot
                else:
                    ordered_items.append(slot)
        return ordered_items

class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)

    def insert(self, x):
        # Insert (key, value) pair if key is not already present
        key, value = x
        if not self.find(key):
            super().insert((key, value))

    def find(self, key):
        # Return the value if key is found, else None
        slot = self.get_slot(key)
        if slot is None:
            return None
        if self.collision_type == "Chain":
            for item in self.table[slot] or []:
                if isinstance(item, tuple) and item[0] == key:
                    return item[1]
        elif self.table[slot] is not None:
            return self.table[slot][1]
        return None

    def items(self):
        # Returns all (key, value) pairs as a list of tuples
        entries = []
        for slot in self.table:
            if slot:
                if isinstance(slot, list):  # For chaining
                    entries.extend([(key, value) for key, value in slot])
                else:  # For linear probing or double hashing
                    entries.append(slot)
        return entries
