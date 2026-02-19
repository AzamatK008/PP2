a = lambda n: n*n #lambda functions can have only oen expression

print(a(5))

def f_(n):
    return lambda a: a*n #it's just like a function in another function

fx = f_(2)

print(fx(324))