def add_numbers(num1, num2):
    sum = num1 + num2
    print("Sum: ",sum)

def multiply(numbers):
    total = 1
    for x in numbers:
        total *= x
    return total

def max_of_three(a, b, c):
  if a >= b and a >= c:
    return a
  elif b >= a and b >= c:
    return b
  else:
    return c

def reverse_string(string):
  reversed_string = ""
  for i in range(len(string) - 1, -1, -1):
    reversed_string += string[i]
  return reversed_string

  def factorial(n):
  if n == 0:
    return 1
  else:
    return n * factorial(n - 1)

def is_in_range(number, lower_bound, upper_bound):
  return lower_bound <= number <= upper_bound


def count_upper_lower_case(string):
  upper_case_count = 0
  lower_case_count = 0
  for letter in string:
    if letter.isupper():
      upper_case_count += 1
    elif letter.islower():
      lower_case_count += 1
  return upper_case_count, lower_case_count