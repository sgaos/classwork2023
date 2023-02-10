import math


def is_adult(age):
    if age >= 18:
        return True
    else:
        return False


def area_of_ellipse(x: list):
    """ calculate the area of an ellipse based on various inputs

        The function receives a list of numbers in one of three formats.
            * A single number represents the radius of a circle
            * Two numbers represents the two axes of an ellipse
            * Four numbers representing the bounding box of an ellipse
                with axes aligned with the x and y axes. (x1, y1, x2, y2)
        It then calculates the area of the ellipse based on the type
        of input.

        Args:
            x (list): a list of varying length depending on the method
                        of describing the ellipse

        Returns:
            float: the area of the ellipse, or
            None: if the input to the function does not meet one of
                    the expected formats.
    """

    data = x.split(",")
    if len(data) = 1:
        area = math.pi * data[0]**2
    elif len(data) = 2:
        area = math.pi * data[0] * data[1]
    elif len(data) = 4:
        a = (data[2] - data[0]) / 2
        b = (data[3] - data[1]) / 2
        area = math.pi * a * b
    else:
        area = None
    return area
