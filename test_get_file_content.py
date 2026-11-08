from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

result = get_file_content("calculator", "pkg/calculator.py")
print(f"Result for '../' file:\n{result}")

result = get_file_content("calculator", "main.py")
print(f"Result for 'main.py' file:\n{result}")

result = get_file_content("calculator", "/bin/cat")
print(f"Result for '/bin/cat' file:\n{result}")

result = get_file_content("calculator", "pkg/does_not_exist.py")
print(f"Result for 'pkg/does_not_exist.py' file:\n{result}")