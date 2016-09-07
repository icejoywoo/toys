
import abc


class BasePizza(object):

    __metaclass__ = abc.ABCMeta

    default_ingredients = ['cheese']

    name = 'BasePizza'

    @classmethod
    @abc.abstractmethod
    def get_ingredients(cls):
        """ Returns the default ingredient list. """
        return cls.default_ingredients


class DietPizza(BasePizza):

    name = 'DietPizza'

    sup = super(BasePizza)

    def get_ingredients(self):
        return ['egg'] + super(DietPizza, self).get_ingredients()


class A(object):
    bar = 42

    def foo(self):
        return 'A'


class B(object):
    bar = 0

    def foo(self):
        return 'B'


class C(A, B):
    xyz = 'abc'


class D(C):
    sup = super(C)


if __name__ == '__main__':
    print(DietPizza().get_ingredients())
    print(DietPizza.mro())
    print(DietPizza().name)
    print(DietPizza().sup)
    print(D().sup)
    print(D().sup.foo())
    print(D().sup.bar)
    print(D().foo())
