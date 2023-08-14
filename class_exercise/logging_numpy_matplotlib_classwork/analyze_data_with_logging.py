def analyze_signal(filename):
    in_file = open(filename, 'r')
    number_of_positives = 0
    total_number = 0
    while True:
        new_data = in_file.read(1)
        total_number += 1
        if new_data == "+":
            number_of_positives += 1
        elif new_data == "\n":
            break
    percent_positive = round(number_of_positives / total_number * 100, 1)
    return percent_positive


if __name__ == '__main__':
    answer = analyze_signal("signal.txt")
    print("Percent positive = {}".format(answer))

