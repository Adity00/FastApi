import random
import string

# letters = ["A","B","C","D","E","F","G","H","I"]
# numbers = ["0","1","2","3","4","5","6","7","8","9"]
res = ''
# c = ["N","C"]

chars = string.digits+string.ascii_letters
for i in range(4):
    res+=random.choice(chars)    

print(dir(string))

print(string.ascii_letters)
print(res)