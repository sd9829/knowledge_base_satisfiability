# Author

    Name: Soumya Dayal
    Username: sd9829

# Overview

This Python script determines if a Knowledge Base (KB) is satisfiable using the resolution-based method. It takes a CNF (Conjunctive Normal Form) file as input and checks for satisfiability. If the KB is satisfiable, it prints "yes"; otherwise, it prints "no."

# Input

The script reads a CNF file that contains information about predicates, variables, constants, functions, and clauses.

    Predicates: List of predicates.
    Variables: List of variables.
    Constants: List of constants.
    Functions: List of functions.
    Clauses: List of clauses in CNF.

# Example

Suppose you have a CNF file (f1.cnf) with the following content:

cnf

p 3 1 2
v 2 a b
c 2 x y
f 1 f
x(a)
x(b)
!x(f(x))

The script will determine if the KB is satisfiable and print either "yes" or "no" accordingly.

# Function Descriptions
pl_resolution(kb)

    Returns True if it finds an empty clause (indicating unsatisfiability), else returns False if a subset of the KB is found.

pl_resolve(ci, cj)

    Returns clauses after resolving two input clauses ci and cj.

unification(ci, cj)

    Unifies two clauses ci and cj and returns the unified clauses.
Ensure that the CNF file is formatted correctly and follows the specified structure for proper execution of the script.
