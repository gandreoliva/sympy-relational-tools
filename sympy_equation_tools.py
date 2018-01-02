from __future__ import division, print_function
from sympy import *
r"""
Minimal version of sympy_relational_tools with only the functions for equations.
Works with sympy >= 0.7.4.1

"""

def add_equations(equation1,equation2):
    r"""
    Adds each side of two equations and returns the resulting equation.

    Parameters
    ==========
    equation1 : Equality
    equation2 : Equality

    Examples
    ========
    ```python
    >>> from sympy import *
    >>> from sympy_equation_tools import *
    >>> x,y = symbols('x,y',real=True)

    >>> eq1 = Eq(x+10, 4*y-2)
    >>> eq2 = Eq(sin(x)+5*x, -y**2)
    >>> add_equations(eq1,eq2)
    Eq(-4*x - sin(x) + 10, y**2 + 4*y - 2)
    ```
    """
    return Eq( equation1.lhs + equation2.lhs, equation1.rhs+equation2.rhs )

def sub_equations(equation1,equation2):
    r"""
    Subtracts each side of two equations and returns the resulting equation.

    Parameters
    ==========
    equation1 : Equality | minuend
    equation2 : Equality | subtrahend

    Example
    =======
    ```python
    >>> from sympy import *
    >>> from sympy_equational_tools import *
    >>> x,y = symbols('x,y',real=True)

    >>> eq1 = Eq(x+5, y-3)
    >>> eq2 = Eq(x, 10*y)
    >>> sub_equations(eq1,eq2)
    Eq(5, -9*y - 3)
    ```
    """
    return Eq( equation1.lhs - equation2.lhs, equation1.rhs-equation2.rhs )

def mul_equations(equation1,equation2):
    r"""
    Multiplies each side of two equations and returns the resulting equation.

    Parameters
    ==========
    equation1 : Equality
    equation2 : Equality

    Example
    =======
    ```python
    >>> from sympy import *
    >>> from sympy_equation_tools import *
    >>> x,y = symbols('x,y',real=True)

    >>> eq1 = Eq(x+5, x**2)
    >>> eq2 = Eq(y+10*x, 6)
    >>> mul_equations(eq1,eq2)
    Eq((x + 5)*(10*x + y), 6*x**2)
    ```
    """
    return Eq( equation1.lhs * equation2.lhs, equation1.rhs*equation2.rhs )

def div_equations(equation1,equation2):
    r"""
    Divides each side of two equations and returns the resulting equation.

    Parameters
    ==========
    equation1 : Equality | dividend
    equation2 : Equality | divisor

    Example
    =======
    ```python
    >>> from sympy import *
    >>> from sympy_equation_tools import *
    >>> x,y,th = symbols(r'x,y,theta',real=True)

    >>> eq1 = Eq(sin(th), y)
    >>> eq2 = Eq(cos(th), x)
    >>> div_equations(eq1,eq2)
    Eq(sin(theta)/cos(theta), y/x)
    ```
    """
    return Eq( equation1.lhs/equation2.lhs, equation1.rhs/equation2.rhs )






def both_sides(equation,function,argument=None):
    r"""
    Applies a `function` with an `argument` to a `equation` and returns the resulting one.

    Subtraction and division of a quantity are achieved with addition of the inverse
    and multiplication of the reciprocal.

    Parameters
    ==========
    relation: Equation
    function: sympy function to be applied
        currently implemented: Add,Mul,Pow,factor,simplify,collect,expand,together,apart
    argument: Sympy expression (optional)

    Warnings
    ========
    * Differentiation and integration are not implemented for equalities.


    Examples
    ========
    ```python
    >>> from sympy_equation_tools import *
    >>> x,y = symbols('x,y',real=True)
    >>> a = symbols('a',positive=True)
    >>> equation = Eq(5*x+x**2, x+5)
    >>> both_sides(equation,Add,-5*x)
    Eq(x**2, -4*x + 5)

    >>> equation1 = Eq(sin(x),x+1)
    >>> equation2 = both_sides(equation1,Pow,-2)
    >>> equation2
    Eq(sin(x)**(-2), 1/(x + 1)**2)

    >>> both_sides(equation2,expand)
    Eq(sin(x)**(-2), 1/(x**2 + 2*x + 1))
    ```
    """
    return Eq( function(equation.lhs,argument), function(equation.rhs,argument) )
