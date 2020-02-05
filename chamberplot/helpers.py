import re

def find_close_paren(s, start=0):
    stack = 0
    for i, c in enumerate(s[start:], start):
        if c == '(':
            stack += 1
        elif c == ')':
            stack -= 1
            if stack == 0:
                break

    if stack != 0:
        raise IndexError('Unbalanced parentheses')

    return i

def find_parens(s):
    outer = re.compile("\((.+)\)")
    m = outer.search(s)
    inner_str = m.group(1)

    innerre = re.compile("\('([^']+)', '([^']+)'\)")

    results = innerre.findall(inner_str)
    for x,y in results:
        print("{} <-> {}".format(x,y))