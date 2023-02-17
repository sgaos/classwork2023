def calc_square_root(n):

    try:
        from my_math_calculator import sqrt
    except ModuleNotFoundError:
        from math import sqrt

    answer = sqrt(n)
    return answer


def main():
    x = 4
    try:
        answer = calc_square_root(x)
    except TypeError:
        new_x = int(x)
        answer = calc_square_root(new_x)
    except ValueError:
        print("You must send a positive number")
        answer = ""
    # The bare except clause is commented out to pass PEP-8
    # except:
    #     print("All errors")
    print(answer)


if __name__ == "__main__":
    main()
