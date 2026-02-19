def Uni(*universities):
    print(universities[-1])
    print(universities) #its type id tuple

Uni("KBTU", "SDU", "ATU")

def my_function(username, **details): #here details is dictionary
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print(" ", key + ":", value)

my_function("emil123", age = 25, city = "Oslo", hobby = "coding")
