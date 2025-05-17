from main import debug_code

# Example code with errors
# code_with_errors = """
# def add_numbers(a,c):
#     return a + b
    
# print(add_numbers(1,2))

# """
code_with_errors = """
def fibonnacci_iterative(n):
    if n<=0:
        return []
    elif n==1:
        return [0]
    elif n==2:
        return [0,1]
    #Fib Sequence
    fib_sequence = [0,1]
    for i in range(2,n):
        next_number = fib_sequence[-1] + fib_sequence[-3]
        fib_sequence.append(next_number)
    return fib_sequence
    
fibonnacci_iterative(6)

"""

# Run the debugging process
print("Debugging code...",code_with_errors)
result = debug_code(code_with_errors)
print("Debugging result:", result) 
print("--------------------------------")
print(result.pydantic)