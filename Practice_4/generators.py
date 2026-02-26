mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)#iterate mytuple

print(next(myit))#getting the first value
print(next(myit))#getting the second value
print(next(myit))#getting the third value



mystr = "banana"

for x in mystr: #iterating string with for loop
  print(x)



class MyNumbers:
  def __iter__(self):#must always return the iterator object itself.
    self.a = 1
    return self

  def __next__(self):#must return the next item in the sequence.
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))



#Generator
def count_up_to(n):
  count = 1
  while count <= n:
    yield count
    count += 1

for num in count_up_to(5):#printing the numbers from 1 to 5
  print(num)
