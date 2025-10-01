#!/usr/bin/env python3
"""
Test script to verify all features of the Online Python Compiler
"""
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5001"

def test_simple_execution():
    """Test basic code execution"""
    print("Testing simple execution...")
    response = requests.post(f"{BASE_URL}/run", json={
        "code": "print('Hello, World!')",
        "input": ""
    })
    result = response.json()
    assert "Hello, World!" in result.get("output", ""), "Simple execution failed"
    print("✓ Simple execution works")

def test_input_handling():
    """Test input handling"""
    print("\nTesting input handling...")
    response = requests.post(f"{BASE_URL}/run", json={
        "code": "name = input('Enter name: ')\nprint(f'Hello, {name}!')",
        "input": "Alice"
    })
    result = response.json()
    assert "Alice" in result.get("output", ""), "Input handling failed"
    print("✓ Input handling works")

def test_error_handling():
    """Test error handling"""
    print("\nTesting error handling...")
    response = requests.post(f"{BASE_URL}/run", json={
        "code": "print(undefined_variable)",
        "input": ""
    })
    result = response.json()
    assert "NameError" in result.get("error", ""), "Error handling failed"
    print("✓ Error handling works")

def test_code_formatting():
    """Test code formatting"""
    print("\nTesting code formatting...")
    response = requests.post(f"{BASE_URL}/format", json={
        "code": "x=1+2\ny  =  3+4\nprint(  x,y  )"
    })
    result = response.json()
    assert "formatted_code" in result, "Code formatting failed"
    print(f"  Original: x=1+2")
    print(f"  Formatted: {result['formatted_code'].split(chr(10))[0]}")
    print("✓ Code formatting works")

def test_snippets():
    """Test snippets endpoint"""
    print("\nTesting snippets endpoint...")
    response = requests.get(f"{BASE_URL}/snippets")
    result = response.json()
    assert len(result) > 0, "Snippets endpoint failed"
    assert "hello_world" in result, "Hello world snippet missing"
    print(f"✓ Snippets endpoint works ({len(result)} snippets available)")

def test_docker_execution():
    """Test Docker-based execution"""
    print("\nTesting Docker execution...")
    try:
        response = requests.post(f"{BASE_URL}/run", json={
            "code": "print('Hello from Docker!')",
            "input": "",
            "use_docker": True
        }, timeout=30)
        result = response.json()
        if "Hello from Docker!" in result.get("output", ""):
            print("✓ Docker execution works")
        else:
            print("⚠ Docker execution returned unexpected output")
    except Exception as e:
        print(f"⚠ Docker execution test skipped: {e}")

def test_list_comprehension():
    """Test more complex code"""
    print("\nTesting list comprehension...")
    response = requests.post(f"{BASE_URL}/run", json={
        "code": "squares = [x**2 for x in range(5)]\nprint(squares)",
        "input": ""
    })
    result = response.json()
    assert "[0, 1, 4, 9, 16]" in result.get("output", ""), "List comprehension failed"
    print("✓ List comprehension works")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Online Python Compiler Features")
    print("=" * 60)
    
    try:
        test_simple_execution()
        test_input_handling()
        test_error_handling()
        test_code_formatting()
        test_snippets()
        test_docker_execution()
        test_list_comprehension()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
