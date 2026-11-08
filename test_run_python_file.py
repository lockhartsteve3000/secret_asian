from functions.run_python_file import run_python_file

result = run_python_file("calculator", "main.py")
print(f"Result for main.py:\n{result}")

result = run_python_file("calculator", "main.py", ["3 + 5"])
print(f"Result for main.py with args ['3 + 5']:\n{result}")

result = run_python_file("calculator", "tests.py")
print(f"Result for tests.py:\n{result}")

result = run_python_file("calculator", "../main.py")
print(f"Result for ../main.py:\n{result}")

result = run_python_file("calculator", "nonexistent.py")
print(f"Result for 'nonexistent.py':\n{result}")

result = run_python_file("calculator", "lorem.txt")
print(f"Result for 'lorem.txt':\n{result}")