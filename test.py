class A(object):
    def a(self):
        b = 1

        def c():
            b = 2

        c()
        print(b)

A().a()