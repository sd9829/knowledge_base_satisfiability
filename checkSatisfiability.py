"""
@author: Soumya Dayal
@Username: sd9829
the program determines if the KB is satisfiable and print either,
"yes" (it is satisfiable; it cannot find any new clauses) or "no"
(it is not satisfiable; it finds the empty clause).
"""
import sys

# global variables
predicates = []
variables = []
constants = []
functions = []
clauses = []

if len(sys.argv) < 1:
    print("Usage: python3 lab2.py testcases/functions/f1.cnf")
else:
    filename = sys.argv[1]
    f = open(filename, 'r')
    lines = f.readlines()
    predicates = lines[0].split()[1:]
    variables = lines[1].split()[1:]
    constants = lines[2].split()[1:]
    functions = lines[3].split()[1:]
    for i in range(5, len(lines)):
        clauses.append(lines[i].strip())
    f.close()


def pl_resolution(kb):
    """
    returns true if it finds an empty clause, else returns false if subset of kb found
    """
    new = []
    pairs = []
    while True:
        for i in range(len(kb)):
            for j in range(i + 1, len(kb)):
                pairs.append((kb[i], kb[j]))
        for (ci, cj) in pairs:
            resolve = pl_resolve(ci, cj)
            if [] in resolve:
                return True
            for cl in resolve:
                if cl not in new:
                    new.append(cl)
        if set(new).issubset(set(kb)):
            return False
        for clause in new:
            if clause not in kb:
                kb.append(clause)


def pl_resolve(ci, cj):
    """
    returns clauses after resolving ci and cj clauses
    """
    resolve = []
    split_ci = ci.split(" ")
    split_cj = cj.split(" ")
    for i in split_ci:
        for j in split_cj:
            unify_i, unify_j = unification(i, j)
            if unify_i == ("!" + unify_j) or ("!" + unify_i) == unify_j:
                ci_split = ci.split(" ")
                cj_split = cj.split(" ")
                ci_split.remove(i)
                cj_split.remove(j)
                resolve = post_resolution(ci_split, cj_split)
    return resolve


def unification(ci, cj):
    """
    Unifies clauses
    """
    ci_brackets = count_brackets(ci)
    cj_brackets = count_brackets(cj)
    if "," in ci and "," in cj:
        if ci_brackets == 4 or cj_brackets == 4:
            ci, cj = parse_data(ci, cj)
        ci_var_split, cj_var_split = parse_variable(ci, cj)
        temp = []

        for i in range(len(ci_var_split)):
            if ci_var_split[i] in variables:
                ci = ci.replace(ci_var_split[i], cj_var_split[i])
                temp.append(cj_var_split[i])
        for i in temp:
            cj_var_split.remove(i)

        for i in range(len(cj_var_split)):
            if cj_var_split[i] in variables:
                cj = cj.replace(cj_var_split[i], ci_var_split[i])
    else:
        var_ci = get_variable(ci)
        var_cj = get_variable(cj)
        if ci_brackets == 2 and cj_brackets == 2:
            if var_ci in variables:
                ci = ci.replace(var_ci, var_cj)
            elif var_cj in variables:
                cj = cj.replace(var_cj, var_ci)
        else:
            if ci_brackets == 4 and cj_brackets == 4:
                ci, cj = four_brackets(var_ci, var_cj)
            elif ci_brackets == 4:
                ci, cj = diff_brackets(var_ci, ci, cj)
            else:
                cj, ci = diff_brackets(var_cj, cj, ci)
    return ci, cj


def count_brackets(clause):
    """
    Counts no of brackets in the given clause
    """
    count = 0
    for b in clause:
        if b == "(" or b == ")":
            count += 1
    return count


def get_variable(c):
    """
    Used to get the variable between the brackets
    """
    start = c.find('(')
    end = c.rfind(')')
    return c[start + 1: end]


def parse_variable(ci, cj):
    '''
    returns the variables as a list after parsing
    '''
    var_ci = get_variable(ci)
    var_cj = get_variable(cj)
    return var_ci.split(","), var_cj.split(",")


def four_brackets(ci, cj):
    """
    Used when both the clauses have 4 brackets
    """
    ci_before_bracke = ci.split("(")[0]
    if ci_before_bracke in functions:
        var_ci = get_variable(ci)
        var_cj = get_variable(cj)
        if var_ci in variables:
            ci = ci.replace(var_ci, var_cj)
        elif var_cj in variables:
            cj = cj.replace(var_cj, var_ci)
    return ci, cj


def diff_brackets(c, c1, c2):
    """
    Used when both clauses have different number of brackets
    """
    before_bracket = c.split("(")[0]
    if before_bracket in functions:
        var_c2 = get_variable(c2)
        if var_c2 in variables:
            c2 = c2.replace(var_c2, c)
    return c1, c2


def parse_data(ci, cj):
    """
    Used to parse data
    """
    ci_var_split, cj_var_split = parse_variable(ci, cj)

    ci_brackets = count_brackets(ci)
    cj_brackets = count_brackets(cj)

    if ci_brackets == 4 and cj_brackets == 4:
        for i in range(len(ci_var_split)):
            if "(" in ci_var_split[i]:
                ci_split_with_bracket = ci_var_split[i]
                cj_split_with_bracket = cj_var_split[i]
                ci, cj = four_brackets(ci_split_with_bracket, cj_split_with_bracket)
                return ci, cj

    elif ci_brackets == 4:
        for i in range(len(cj_var_split)):
            if cj_var_split[i] in variables:
                cj = cj.replace(cj_var_split[i], ci_var_split[i])
        return ci, cj

    elif cj_brackets == 4:
        for i in range(len(ci_var_split)):
            if ci_var_split[i] in variables:
                ci = ci.replace(ci_var_split[i], cj_var_split[i])
        return ci, cj
    return ci, cj


def post_resolution(ci, cj):
    """
    Returns the clauses after resolution
    """
    clause_string = []
    new_ci = ""
    new_cj = ""
    space = ""
    if len(ci) > 1:
        space = " "

    for c in ci:
        if len(new_ci):
            new_ci += space + c
        else:
            new_ci += c
    space = ""
    if len(cj) > 1:
        space = " "

    for c in cj:
        if len(new_cj):
            new_cj += space + c
        else:
            new_cj += c

    if not len(new_ci) and not len(new_cj):
        clause_string.append([])

    if not len(new_cj) or not len(new_ci):
        clause_string.append(new_ci + new_cj)
    else:
        clause_string.append(new_ci + " " + new_cj)
    return clause_string


def main():
    if pl_resolution(clauses):
        print("no")
    else:
        print("yes")


if __name__ == "__main__":
    main()
