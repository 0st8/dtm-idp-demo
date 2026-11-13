# function that returns the sum of squares of a list of numbers
def sum_of_squares(numbers):
    return sum(x**2 for x in numbers)

# example usage
numbers = [1, 2, 3, 4]
print(sum_of_squares(numbers))