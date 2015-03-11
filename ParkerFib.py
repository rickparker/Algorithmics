def fib(target):
    if target == 0 or target == 1:
        print "fib(%d) is %d" % (target, target)
        return
    first_val = 0
    second_val = 1
    temp = first_val + second_val
    for x in range (1, target):
        temp = first_val + second_val
        first_val = second_val
        second_val = temp
    print "fib(%d) is %d" % (target, temp)

fib(0)
fib(1)
fib(2)
fib(3)
fib(4)
fib(5)
fib(6)
fib(7)
fib(8)
fib(9)
fib(10)

fib(200)
