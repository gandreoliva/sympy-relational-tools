from __future__ import division, print_function
from sympy import *

_inverse_relations = { Ge: Le, Le: Ge, Gt: Lt, Lt: Gt }

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
    >>> from sympy_relational_tools import *
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
    >>> from sympy_relational_tools import *
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
    >>> from sympy_relational_tools import *
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
    >>> from sympy_relational_tools import *
    >>> x,y,th = symbols(r'x,y,theta',real=True)

    >>> eq1 = Eq(sin(th), y)
    >>> eq2 = Eq(cos(th), x)
    >>> div_equations(eq1,eq2)
    Eq(sin(theta)/cos(theta), y/x)
    ```
    """
    return Eq( equation1.lhs/equation2.lhs, equation1.rhs/equation2.rhs )


def invert_ineq(ineq):
    r"""
    Changes the direction of an inequality

    Parameters
    ==========
    ineq : Relational

    Returns
    =======
    Relational, direction inverted

    Example
    =======
    ```
    >>> from sympy import *
    >>> from sympy_relational_tools import *
    >>> x = symbols('x',real=True)

    >>> ineq = Ge(x,3)
    >>> invert_ineq(ineq)
    -x <= -3
    ```
    """
    return _inverse_relations[ineq.func]( -ineq.lhs, -ineq.rhs, evaluate=False)


def _both_sides_add_ineq(relation,argument):
    r"""
    Adds `argument` to each side of `relation`, according to the property
    $ x>y \implies x + c > y + c $, where $c \in \mathbb R$.
    """
    return relation.func( relation.lhs+argument, relation.rhs+argument, evaluate=False )

def _both_sides_mul_ineq(relation,argument,interval,variable):
    r"""
    Multiplies `argument` to each side of `relation`.

    If `interval` is not present, global assumptions are used (properties is_positive, is_negative).

    If `interval` is not present, the function returns the resulting inequality.

    Rules are made according to: $x \le y \implies xc \le yc$ if $c>0$ and $xc \ge yc$ if $c<0$.

    If `interval` is present, `variable` must be too, and `solveset` is used to determine
    the intervals where the inequality must or not change sign (solveset supports only univariable
    inequalities).

    If `interval` is present, the function returns a dictionary with intervals and solutions.
    """
    if interval is None:
        if argument.is_positive == True:
            return relation.func( relation.lhs*argument, relation.rhs*argument, evaluate=False )
        elif argument.is_negative == True:
            return _inverse_relations[relation.func]( relation.lhs*argument, relation.rhs*argument, evaluate=False )
        elif argument == 0:
            return relation.func(0,0)
        else:
            raise ValueError("Couldn't determine sign of the argument")
    else:
        if variable is None:
            raise TypeError("If `interval` is given, a variable must be specified. Only univariable inequalities are supported")
        # Determine where in the given interval the argument is positive, negative and zero:
        positive_interval = solveset(argument>0,variable,domain=interval)
        negative_interval = solveset(argument<0,variable,domain=interval)
        zeros = solveset(argument,variable,domain=interval)
        # The resulting inequalities depend on the interval of the argument
        ans_if_positive = relation.func( relation.lhs*argument, relation.rhs*argument, evaluate=False )
        ans_if_negative = _inverse_relations[relation.func]( relation.lhs*argument, relation.rhs*argument, evaluate=False )
        ans_if_zero = relation.func(0,0)
        return {positive_interval: ans_if_positive, negative_interval: ans_if_negative, zeros: ans_if_zero }

def _both_sides_pow_ineq(relation,argument,interval,variable):
    r"""
    Applies a power to both sides of an inequality. The only implemented power is -1 (reciprocal of both sides).
    If `interval` is not present, global assumptions are used (properties is_positive, is_negative).

    If `interval` is not present, the function returns the resulting inequality.

    The rules implemented are:
    $ x > y \implies 1/x < 1/y$ if $x>0,y>0$ or $x<0,y<0$, and $1/x>1/y$ if $x>0,y<0$ or $x<0,y>0$

    If `interval` is present, `variable` must be too, and `solveset` is used to determine
    the intervals where the inequality must or not change sign (solveset supports only univariable
    inequalities).

    If `interval` is present, the function returns a dictionary with intervals and solutions.

    `solveset` can be useful in order to determine an adequate interval where the original inequality holds.

    Example
    =======
    ```python
    >>> from sympy_relational_tools import *
    >>> x = symbols('x',real=True)
    >>> ie1 = Ge(x,x**2,evaluate=False); ie1
    x >= x**2
    >>> both_sides(ie1,Pow,-1,Interval(-oo,oo),x)
    {Interval.open(0, oo): 1/x <= x**(-2), Interval.open(-oo, 0): 1/x >= x**(-2)}
    ```
    """
    if argument == -1:
        if interval is None:
            # Method 1: global assumptions
            if variable is None:
                raise TypeError("If `interval` is given, a variable must be specified. Only univariable inequalities are supported")
            if (relation.lhs.is_positive == True) and (relation.rhs.is_positive == True):
                return relation.func( 1/relation.lhs, 1/relation.rhs, evaluate=False )
            elif (relation.lhs.is_positive == True) and (relation.rhs.is_negative == True):
                return relation.func( 1/relation.lhs, 1/relation.rhs, evaluate=False )
            elif (relation.lhs.is_negative == True) and (relation.rhs.is_positive == True):
                return relation.func( 1/relation.lhs, 1/relation.rhs, evaluate=False )
            elif (relation.lhs.is_negative == True) and (relation.rhs.is_negative == True):
                return _inverse_relations[relation.func]( 1/relation.lhs, 1/relation.rhs, evaluate=False )
            elif (relation.lhs == 0):
                raise ZeroDivisionError("Can't take reciprocals with one side zero")
            elif (relation.rhs == 0):
                raise ZeroDivisionError("Can't take reciprocals with one side zero")
            else:
                raise ValueError("Couldn't determine sign of the expressions")
        else:
            # Method 2: solveset
            # Determine where are both sides positive or negative
            lhs_positive_interval = solveset(relation.lhs>0,variable,domain=interval)
            rhs_positive_interval = solveset(relation.rhs>0,variable,domain=interval)
            lhs_negative_interval = solveset(relation.lhs<0,variable,domain=interval)
            rhs_negative_interval = solveset(relation.rhs<0,variable,domain=interval)

            if (relation.lhs == 0):
                raise ZeroDivisionError("Can't take reciprocals with one side zero")
            elif (relation.rhs == 0):
                raise ZeroDivisionError("Can't take reciprocals with one side zero")

            # For both sides positive or negative, the relation is inversed
            pp_interval = lhs_positive_interval.intersect(rhs_positive_interval)
            nn_interval = lhs_negative_interval.intersect(rhs_negative_interval)
            eqsigns = _inverse_relations[relation.func]( 1/relation.lhs, 1/relation.rhs, evaluate=False )
            # For both sides of different signs, the relation is not inversed
            pn_interval = lhs_positive_interval.intersect(rhs_negative_interval)
            np_interval = lhs_negative_interval.intersect(rhs_positive_interval)
            difsigns = relation.func( 1/relation.lhs, 1/relation.rhs, evaluate=False )

            result = {}
            if nn_interval != EmptySet():
                result[nn_interval] = eqsigns
            if pp_interval != EmptySet():
                result[pp_interval] = eqsigns
            if pn_interval != EmptySet():
                result[pn_interval] = difsigns
            if np_interval != EmptySet():
                result[np_interval] = difsigns

            return result

    else:
        raise NotImplementedError("Only reciprocals (Pow,-1) are implemented")







def both_sides(relation,function,argument=None,interval=None,variable=None):
    r"""
    Applies a `function` with an `argument` to a `relation` and returns the resulting
    Relational.

    Parameters
    ==========
    relation: Relational
    function: sympy function to be applied
        currently implemented: Add,Mul,Pow,factor,simplify,collect,expand,together,apart
    argument: Sympy expression (optional)
    interval: Interval() (optional)
        interval in which the relation holds (intended to be used with inequalities)
    variable: Sympy expression (optional)
        if `interval` is specified, variable must also be specified. (Intended to be
        used with inequalities; only univariable inequalities are implemented)

    Warnings
    ========
    * Specifying an `interval` causes the fucntion to use `solveset`, which is slow.
    * Differentiation and integration are not implemented for equalities.
    * Unequalities are not supported.

    Rules implemented
    =================
    * Equality: any function applied to both sides preserves equality.
    * Addition to inequalities: $ x>y \implies x + c > y + c $, where $c \in \mathbb R$.
    * Multiplication to inequalities: $x \le y \implies xc \le yc$ if $c>0$ and $xc \ge yc$ if $c<0$.
    * Reciprocal of an inequality: $ x > y \implies 1/x < 1/y$ if $x>0,y>0$
      or $x<0,y<0$, and $1/x>1/y$ if $x>0,y<0$ or $x<0,y>0$
    * Subtraction and division of a quantity are achieved with addition of the inverse
      and multiplication of the reciprocal.


    Examples
    ========
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
    ```
    """
    if relation.func == Eq:
        return Eq( function(relation.lhs,argument), function(relation.rhs,argument) )
    else:
        if function == Add:
            return _both_sides_add_ineq(relation,argument)
        elif function == Mul:
            return _both_sides_mul_ineq(relation,argument,interval,variable)
        elif function == Pow:
            return _both_sides_pow_ineq(relation,argument,interval,variable)
        elif function in [factor,simplify,collect,expand,together,apart]:
            return relation.func( function(relation.lhs), function(relation.rhs), evaluate=False )
        else:
            raise NotImplementedError("Function not yet implemented")
