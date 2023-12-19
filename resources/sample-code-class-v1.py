class FunClass:
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

funClass = FunClass()
funClass.add_numbers(10, 20)
funClass.multiply(10)
funClass.max_of_three(10, 30, 20)