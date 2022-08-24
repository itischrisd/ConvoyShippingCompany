# read animals.txt
# and write animals_new.txt

animals = open("animals.txt", 'r')
animals_new = open('animals_new.txt', 'w', encoding='utf-8')



for line in animals.readlines():
    animal = line.rstrip('\n')
    animals_new.write(animal + " ")

animals.close()
animals_new.close()