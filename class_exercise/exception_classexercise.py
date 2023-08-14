def add_two_numbers(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Only integers are allowed")
    if a < 0 or b < 0:
        raise ValueError("Nagative number are not allowed")
    c = a + b
    return c

def main():
    a = [1, 1.1, 2, 3, 5, 6, -1]
    b = [0, 1 ,2.1, 4, -1, -2, -4]
    for i in range(len(a)):
        try:
            summ = add_two_numbers(a[i], b[i])
            print("The sum of {} and {} is {}".format(a[i],b[i],summ))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()


