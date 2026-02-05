a = "Almaty"

for i in a: #taking as i each letter in string a
    if(i == "A" or i == "a"):#if i is 'A' or 'a'
        continue             #then the loop starts again fron beginning
    print(i, end="")#printing each letter if it is not 'A' or 'a'