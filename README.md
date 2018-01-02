# Sympy Relational tools

Small module for working with `Relational`s, designed to work with Sympy>= 1.1.1

## Installation
Simply put the module in your working directory or add it to your `$PYTHONPATH`.

## Functions implemented
* `add_equations(equation1,equation2)`: add each side of two equations
* `sub_equations(equation1,equation2)`: subtracts each side of two equations
* `mul_equations(equation1,equation2)`: multiplies two equations
* `div_equations(equation1,equation2)`: divides two equations
* `both_sides(relation,function,argument=None,interval=None,variable=None)`:
   applies a function to both sides of a relation.

## Rules implemented for both_sides
* Equality: any function applied to both sides preserves equality.
* Addition to inequalities: $ x>y \implies x + c > y + c $, where $c \in \mathbb R$.
* Multiplication to inequalities: $x \le y \implies xc \le yc$ if $c>0$ and $xc \ge yc$ if $c<0$.
* Reciprocal of an inequality: $ x > y \implies 1/x < 1/y$ if $x>0,y>0$
 or $x<0,y<0$, and $1/x>1/y$ if $x>0,y<0$ or $x<0,y>0$
* Subtraction and division of a quantity are achieved with addition of the inverse
 and multiplication of the reciprocal.


## Examples
```python
>>> from sympy_relational_tools import *
>>> x,y = symbols('x,y',real=True)
>>> a = symbols('a',positive=True)
>>> equation = Eq(5*x+x**2, x+5)
>>> both_sides(equation,Add,-5*x)
Eq(x**2, -4*x + 5)

>>> equation1 = Eq(sin(x),x+1)
>>> equation2 = both_sides(equation1,Pow,-2)
>>> equation1
Eq(sin(x), x + 1)
>>> both_sides(equation2,expand)
Eq(sin(x)**(-2), 1/(x**2 + 2*x + 1))

>>> inequality = Ge(x+1,0,evaluate=False)
>>> both_sides(inequality,Mul,a)
a*(x + 1) >= 0

>>> inequality = Ge(x+1,x**2,evaluate=False)
>>> both_sides(inequality,Pow,-1,Interval(-1,1),x)
{Union(Interval.open(-1, 0), Interval.Lopen(0, 1)): 1/(x + 1) <= x**(-2)}

>>> eq1 = Eq(x+10, 4*y-2)
>>> eq2 = Eq(sin(x)+5*x, -y**2)
>>> add_equations(eq1,eq2)
Eq(-4*x - sin(x) + 10, y**2 + 4*y - 2)

>>> eq1 = Eq(sin(th), y)
>>> eq2 = Eq(cos(th), x)
>>> div_equations(eq1,eq2)
Eq(sin(theta)/cos(theta), y/x)
```

## Further documentation
Print each function's docstring for further documentation.
`print(both_sides.__doc__)``
