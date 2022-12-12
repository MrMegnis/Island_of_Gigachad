def f(x, y):
    return x ** 2 + y ** 2
def f1(x, y):
    return 2 * x


def f2(x, y):
    return 2 * y



a = 0.4
e = 0.5
x_0 = 2
y_0 = -1
# x_0 *= 10
# y_0 *= 10
x = x_0 - a * f1(x_0, y_0)
y = y_0 - a * f2(x_0, y_0)
# x = x_0
# y = y_0

# while (x - x_0) ** 2 + (y - y_0) ** 2 > e ** 2:
for i in range(6):
    x_0, x = x, x_0 - a * f1(x_0, y_0)
    y_0, y = y, y_0 - a * f2(x_0, y_0)
    print(x, y, x_0, y_0, (x - x_0) ** 2 + (y - y_0) ** 2, f(x, y))
    # print(x / 10, y / 10, x_0 / 10, y_0 / 10, (x - x_0) ** 2 + (y - y_0) ** 2, f(x, y))
