import hash_table as ht

class DigitalLibrary:
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass


class MuskLibrary(DigitalLibrary):
    def __init__(self, book_titles, texts):
        # Initialize titles and create sorted, unique word lists for each book
        self.books = {title: self._merge_sort(self._get_unique_words(text)) for title, text in zip(book_titles, texts)}
        self.book_titles = book_titles

    def distinct_words(self, book_title):
        # Return the list of distinct words in sorted order
        return self.books.get(book_title, [])

    def count_distinct_words(self, book_title):
        # Return the number of distinct words
        return len(self.distinct_words(book_title))

    def search_keyword(self, keyword):
        # Return a list of book titles containing the exact keyword
        matching_titles = [title for title, words in self.books.items() if keyword in words]
        return self._merge_sort(matching_titles)

    def print_books(self):
        # Sort book titles using merge_sort and print each title with its distinct words in lexicographical order
        sorted_titles = self._merge_sort(list(self.books.keys()))
        for title in sorted_titles:
            words = self.books[title]
            print(f"{title}: {' | '.join(words)}")

    def _get_unique_words(self, text):
        """
        Returns a list of unique words from a sorted list of words.
        """
        sorted_words = self._merge_sort(text)
        unique_words = []
        previous_word = None
        for word in sorted_words:
            if word != previous_word:
                unique_words.append(word)
            previous_word = word
        return unique_words

    @staticmethod
    def _merge_sort(arr):
        """
        Sorts the input array using the merge sort algorithm.
        """
        # Base case: A list of zero or one elements is already sorted
        if len(arr) <= 1:
            return arr

        # Recursive case: Split the list into halves
        mid = len(arr) // 2
        left_half = MuskLibrary._merge_sort(arr[:mid])
        right_half = MuskLibrary._merge_sort(arr[mid:])

        # Merge the sorted halves
        return MuskLibrary._merge(left_half, right_half)

    @staticmethod
    def _merge(left, right):
        """
        Merges two sorted arrays into a single sorted array.
        """
        sorted_arr = []
        i = j = 0

        # Compare elements in left and right arrays and merge them in sorted order
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                sorted_arr.append(left[i])
                i += 1
            else:
                sorted_arr.append(right[j])
                j += 1

        # Append any remaining elements from left and right arrays
        sorted_arr.extend(left[i:])
        sorted_arr.extend(right[j:])

        return sorted_arr



class JGBLibrary:
    def __init__(self, name, params):
        '''
        name : "Jobs", "Gates" or "Bezos"
        params : Parameters for the Hash Table
        '''
        # Set the collision handling type based on library name
        if name == "Jobs":
            collision_type = "Chain"
        elif name == "Gates":
            collision_type = "Linear"
        elif name == "Bezos":
            collision_type = "Double"
        else:
            raise ValueError("Invalid library name for collision handling")

        # Initialize the main hash table to store each book's title and its word set
        self.books = ht.HashMap(collision_type, params)
        self.collision_type = collision_type
        self.params = params

    def add_book(self, book_title, text):
        """Add a book with its title and words using a separate HashSet for each book."""
        # Create a new HashSet for the book's words
        word_set = ht.HashSet(self.collision_type, self.params)
        
        # Insert each word from the text into the book's HashSet
        for word in text:
            word_set.insert(word)
        
        # Insert the book's title and its HashSet into the main books HashMap
        self.books.insert((book_title, word_set))

    def distinct_words(self, book_title):
        word_set = self.books.find(book_title)
        return word_set.give() if word_set else []


    def count_distinct_words(self, book_title):
        word_set = self.books.find(book_title)
        return len(word_set.give()) if word_set else 0


    def search_keyword(self, keyword):
        found_books = []
        for book_title, word_set in self.books.items():
            if word_set.find(keyword):
                found_books.append(book_title)
        return found_books


    def print_books(self):
        for item in self.books.items():
            # Handle both non-chaining and chaining cases
            if isinstance(item, tuple):
                book_title, word_set = item
            else:
                book_title, word_set = item[0], item[1]

            words = word_set.give() if word_set else []
            print(f"{book_title}: {' | '.join(words) if words else '<EMPTY>'}")