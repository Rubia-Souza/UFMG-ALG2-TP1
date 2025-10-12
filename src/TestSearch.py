from Search import search_in_reversed_index

if __name__ == "__main__":
    print(search_in_reversed_index("Computer AND (science OR engineering)"))
    print(search_in_reversed_index("Data AND (analysis OR visualization)"))
    print(search_in_reversed_index("Quantum AND computing"))
    print(search_in_reversed_index("nonexistentword AND anothernonexistentword"))