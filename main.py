from input_data import A_FILE
from pizza_structures import Pizza


def main():

    pizzas = []

    with A_FILE.open() as file:
        _, two_number, three_number, four_number = map(int, file.readline().split())
        for i, line in enumerate(file):
            _, *ingredients = line.split()
            pizzas.append(Pizza(i, ingredients))

    print(two_number, three_number, four_number)
    for p in pizzas:
        print(p)


if __name__ == '__main__':
    main()
