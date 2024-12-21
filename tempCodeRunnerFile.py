    sk = lib.search_keyword(word)
    if sort_output:
        sk.sort()
        
    if sk == sorted(word_to_books[word]):
        print("SEARCH KEYWORD CORRECT!")
    else:
        print("SEARCH KEYWORD FAILED!")
    print("\n\n")