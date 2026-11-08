from functions.write_file import write_file

result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(f"Result for lorem.txt:\n{result}")

result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(f"Result for 'pkg' directory:\n{result}")

result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(f"Result for '/tmp' directory:\n{result}")

