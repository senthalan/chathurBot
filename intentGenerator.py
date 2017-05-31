columns = {"memory": "number", "price": "number", "model": "string", "company": "string", "onlineStore": "string"}


def generate_intent():
    strings = []
    numbers = []
    for column in columns.keys():
        if columns[column] == "number":
            numbers.append(column)
        elif columns[column] == "string":
            strings.append(column)
        else:
            print "something else " + column + " : " + columns[column]

    for string in strings:
        print string + "_equal"
        print string + "_less"
        print string + "_greater"
        print string + "_between"

        print
        for number in numbers:
            print string + "_max_" + number
            print string + "_min_" + number

        print "-----------------------------"
    print "///////////////////////////////"
    for number in numbers:
        print "min_" + number + "_equal"
        print "max_" + number + "_equal"
        print "min_" + number + "_less"
        print "max_" + number + "_less"
        print "min_" + number + "_greater"
        print "max_" + number + "_greater"
        print "min_" + number + "_between"
        print "max_" + number + "_between"


if __name__ == "__main__":
    generate_intent()