#!/usr/bin/env python3
"""
Sample Python script for testing the compiler
"""

def greet(name):
    """Simple greeting function"""
    return f"Hello, {name}!"

def calculate_sum(a, b):
    """Calculate sum of two numbers"""
    return a + b

def main():
    """Main function"""
    print("Sample Python Script")
    print("=" * 20)
    
    # Test the functions
    message = greet("World")
    print(message)
    
    result = calculate_sum(10, 20)
    print(f"Sum of 10 and 20 is: {result}")
    
    # Simple loop
    for i in range(5):
        print(f"Count: {i}")
    
    print("Script completed successfully!")

if __name__ == "__main__":
    main() 