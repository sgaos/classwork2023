def sqrt(n):

    # We are using n itself as
    # initial approximation This
    # can definitely be improved

    if type(n) is str:
        raise TypeError("Cannot send a string.")
    if n < 0:
        raise ValueError("You cannot send a negative number"
                         " to this function.")

    x = n
    y = 1

    # e decides the accuracy level
    e = 0.000001
    while (x - y > e):
        x = (x + y)/2
        y = n / x

    return x
