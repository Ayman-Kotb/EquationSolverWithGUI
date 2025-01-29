def divide_numbers():
    """
    Prompts the user for two numbers and divides them, handling common exceptions.
    """
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        result = num1 / num2
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
    except ValueError:
        print("Error: Please enter valid numeric values.")
    else:
        print(f"The result is: {result}")
    finally:
        print("Operation complete. Thank you for using the divider!")

if __name__ == "__main__":
    divide_numbers()
