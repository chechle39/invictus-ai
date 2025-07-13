#!/usr/bin/env python3
"""
Simple Python Calculator - Test File for Migration
This file demonstrates common Python patterns for easy testing
"""

import math
import json
from datetime import datetime
from typing import List, Dict, Optional

class Calculator:
    """A simple calculator with data processing capabilities."""
    
    def __init__(self, name: str = "MyCalculator"):
        self.name = name
        self.history: List[Dict] = []
        self.created_at = datetime.now().isoformat()
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers and record the operation."""
        result = a + b
        self.history.append({
            'operation': 'add',
            'inputs': [a, b],
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        print(f"➕ {a} + {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        result = a * b
        self.history.append({
            'operation': 'multiply',
            'inputs': [a, b],
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        print(f"✖️  {a} × {b} = {result}")
        return result
    
    def power(self, base: float, exponent: float) -> float:
        """Calculate power using math library."""
        result = math.pow(base, exponent)
        self.history.append({
            'operation': 'power',
            'inputs': [base, exponent],
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        print(f"🔢 {base}^{exponent} = {result}")
        return result
    
    def process_numbers(self, numbers: List[float]) -> Optional[Dict]:
        """Process a list of numbers and return statistics."""
        if not numbers:
            return None
        
        stats = {
            'count': len(numbers),
            'sum': sum(numbers),
            'average': sum(numbers) / len(numbers),
            'min': min(numbers),
            'max': max(numbers),
            'squared': [x**2 for x in numbers]  # List comprehension
        }
        
        print(f"📊 Processed {len(numbers)} numbers:")
        print(f"   Sum: {stats['sum']}")
        print(f"   Average: {stats['average']:.2f}")
        print(f"   Range: {stats['min']} - {stats['max']}")
        
        return stats
    
    def get_summary(self) -> str:
        """Generate a summary report."""
        operations_count = len(self.history)
        
        if operations_count == 0:
            return "No operations performed yet."
        
        report = f"""
🧮 {self.name} Summary Report
{'='*40}
📅 Created: {self.created_at}
🔢 Total Operations: {operations_count}

📈 Recent Operations:"""
        
        # Show last 3 operations
        recent_ops = self.history[-3:] if len(self.history) >= 3 else self.history
        
        for i, op in enumerate(recent_ops, 1):
            inputs_str = " & ".join(map(str, op['inputs']))
            report += f"\n   {i}. {op['operation']}: {inputs_str} = {op['result']}"
        
        return report
    
    def save_to_file(self, filename: str = "calculator_history.json") -> bool:
        """Save calculation history to a JSON file."""
        data = {
            'calculator_name': self.name,
            'created_at': self.created_at,
            'total_operations': len(self.history),
            'history': self.history
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"💾 History saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return False

def test_calculator():
    """Test function to demonstrate the calculator."""
    print("🚀 Starting Calculator Test")
    print("="*30)
    
    # Create calculator instance
    calc = Calculator("TestCalc")
    
    # Perform some operations
    calc.add(10, 5)
    calc.multiply(3, 7)
    calc.power(2, 8)
    
    # Test with list processing
    numbers = [1, 2, 3, 4, 5, 10, 15, 20]
    stats = calc.process_numbers(numbers)
    
    # Print squared numbers
    if stats:
        print(f"🔢 Squared numbers: {stats['squared']}")
    
    # Generate and print summary
    summary = calc.get_summary()
    print(summary)
    
    # Save to file
    calc.save_to_file()
    
    print("\n✨ Calculator test completed!")
    return calc

# Helper functions for additional testing
def fibonacci(n: int) -> List[int]:
    """Generate fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    print(f"🔢 Fibonacci sequence ({n} terms): {fib}")
    return fib

def prime_check(number: int) -> bool:
    """Check if a number is prime."""
    if number < 2:
        return False
    
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    
    return True

def find_primes(limit: int) -> List[int]:
    """Find all prime numbers up to limit."""
    primes = [num for num in range(2, limit + 1) if prime_check(num)]
    print(f"🔍 Prime numbers up to {limit}: {primes}")
    return primes

# Main execution
if __name__ == "__main__":
    print("🎯 Python Calculator Demo")
    print("This will be converted to JavaScript!")
    print("="*50)
    
    # Run calculator test
    calculator = test_calculator()
    
    # Additional demonstrations
    print("\n🔄 Additional Demos:")
    fibonacci(8)
    find_primes(20)
    
    print("\n🎉 All tests completed successfully!")
    print("Ready for JavaScript conversion! 🚀")
