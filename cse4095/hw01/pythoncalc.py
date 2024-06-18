"""This is a simple calculator."""
import argparse

def add(x, y):
    """Addition"""
    return x + y

def subtract(x, y):
    """Subtraction-"""
    return x - y

def multiply(x, y):
    """Multiplication*"""
    return x * y

def divide(x, y):
    """Division"""
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return x / y

def main():
    """Main function for command-line calculator"""
    parser = argparse.ArgumentParser(description="Simple Command-Line Calculator")
    parser.add_argument("operation", choices=["add", "subtract", "multiply", "divide"], help="Op")
    parser.add_argument("operand1", type=float, help="First operand")
    parser.add_argument("operand2", type=float, help="Second operand")

    args = parser.parse_args()

    result = None

    if args.operation == "add":
        result = add(args.operand1, args.operand2)
    elif args.operation == "subtract":
        result = subtract(args.operand1, args.operand2)
    elif args.operation == "multiply":
        result = multiply(args.operand1, args.operand2)
    elif args.operation == "divide":
        result = divide(args.operand1, args.operand2)

    print(f"Result: {result}")

if __name__ == "__main__":
    main()
