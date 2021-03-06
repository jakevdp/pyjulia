import array
import math
import unittest

from julia import Julia, JuliaError

julia = Julia()


class JuliaTest(unittest.TestCase):

    def test_call(self):
        julia.call('1 + 1')
        julia.call('sqrt(2.0)')

    def test_eval(self):
        self.assertEqual(2, julia.eval('1 + 1'))
        self.assertEqual(math.sqrt(2.0), julia.eval('sqrt(2.0)'))
        self.assertEqual(1, julia.eval('PyObject(1)'))
        self.assertEqual(1000, julia.eval('PyObject(1000)'))
        self.assertEqual((1, 2, 3), julia.eval('PyObject((1, 2, 3))'))

    def test_call_error(self):
        try:
            julia.call('undefined_function_name()')
            self.fail('No error?')
        except JuliaError:
            pass

    def test_call_julia_function_with_python_args(self):
        self.assertEqual(['A', 'B', 'C'],
                         julia.map(julia.uppercase,
                                   array.array('c', ['a', 'b', 'c'])))
        self.assertEqual([1.0, 2.0, 3.0],
                         julia.map(julia.floor, [1.1, 2.2, 3.3]))
        self.assertEqual(1.0, julia.cos(0))

    def test_call_julia_with_python_callable(self):
        def add(a, b):
            return a + b
        self.assertEqual([1, 4, 9],
                         julia.map(lambda x: x * x, [1, 2, 3]))
        self.assertEqual([11, 11, 11],
                         julia.map(lambda x: x + 1,
                                   array.array('I', [10, 10, 10])))
        self.assertEqual(6, julia.foldr(add, 0, [1, 2, 3]))

    def test_call_python_with_julia_args(self):
        self.assertEqual(6, sum(julia.eval('(1, 2, 3)')))
        self.assertEqual([1, 4, 9], map(julia.eval('x -> x*x'), [1, 2, 3]))

    def test_import_julia_functions(self):
        import julia.sum as julia_sum
        self.assertEqual(6, julia_sum([1, 2, 3]))

    #TODO: this causes a segfault
    def test_import_julia_modules(self):
        import julia.PyCall as pycall
        self.assertEquals(6, pycall.pyeval('2 * 3'))
