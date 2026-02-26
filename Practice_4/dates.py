import datetime

x = datetime.datetime.now()
print(x)
print(x.strftime("%A"))#output: Friday

y = datetime.datetime(2020, 4, 21)
print(x.strftime("%a"))#output: Fri

