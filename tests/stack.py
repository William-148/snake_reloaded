from Collections.stack import Stack


stack = Stack()

print("**** Adding elements to stack ****")
stack.push(1)
print('Size: ' + str(stack.get_size()))
stack.push(2)
print('Size: ' + str(stack.get_size()))
stack.push(3)
print('Size: ' + str(stack.get_size()))
stack.push(4)
print('Size: ' + str(stack.get_size()))
stack.push(5)
print('Size: ' + str(stack.get_size()))
stack.push(6)
print('Size: ' + str(stack.get_size()))
stack.push(7)
print('Size: ' + str(stack.get_size()))
stack.print_values()

print("\n\n**** Pop elements to stack ****")
print(stack.pop())
print('Size: ' + str(stack.get_size()))
print(stack.pop())
print('Size: ' + str(stack.get_size()))
print(stack.pop())
print('Size: ' + str(stack.get_size()))
print(stack.pop())
print('Size: ' + str(stack.get_size()))
print(stack.pop())
print('Size: ' + str(stack.get_size()))
print(stack.pop())
print('Size: ' + str(stack.get_size()))
print(stack.pop())
print('Size: ' + str(stack.get_size()))
stack.print_values()