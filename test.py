def get_quotes_list():
    list = []

    with open('quotes_fixed.txt', 'r') as file:
        for line in file:
            list.append(line)

    return list

print(get_quotes_list())