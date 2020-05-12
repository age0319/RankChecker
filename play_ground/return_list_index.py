thing_list = ['ben','car','apple','ben','car','dick']

elem = "apple"

thing_index = thing_list.index(elem) if elem in thing_list else -1

# 2
print(thing_index)

elem = "nothing"

thing_index = thing_list.index(elem) if elem in thing_list else -1

# -1
print(thing_index)


elem = "car"

thing_index = thing_list.index(elem) if elem in thing_list else -1

# 1
print(thing_index)
