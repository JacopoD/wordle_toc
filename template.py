#!/usr/bin/env python3

import sys
from subprocess import Popen
from subprocess import PIPE
import re
import random
import os

gbi = 0
varToStr = ["invalid"]


def printClause(cl):
    print(map(lambda x: "%s%s" % (x < 0 and eval("'-'") or eval("''"), varToStr[abs(x)]), cl))


def varName(pigeon, hole):
    return "inHole({},{})".format(pigeon, hole)


def gvi(name):
    global gbi
    global varToStr
    gbi += 1
    varToStr.append(name)
    return gbi


def gen_vars(pigeons, holes):

    varMap = {}

    # Insert here the code to add mapping from variable numbers to readable variable names.
    for p in range(pigeons):
        for h in range(holes):
            name = varName(p, h)
            varMap[name] = gvi(name)

    # A single variable with a human readable name "var_name" is added, for instance, as follows:
    varMap["var_name"] = gvi("var_name")

    # let's add another one.
    varMap["var2_name"] = gvi("var2_name")

    return varMap


def genPigConstr(pigeons, holes, vars):

    clauses = []

    # Pigeon cannot stay at two holes at the same time
    for p in range(pigeons):
        for h1 in range(holes):
            for h2 in range(h1 + 1, holes):
                clauses.append([-vars[varName(p, h1)], -vars[varName(p, h2)]])

    # Each hole contains only one pigeon
    for h in range(holes):
        for p1 in range(pigeons):
            for p2 in range(p1 + 1, pigeons):
                clauses.append([-vars[varName(p1, h)], -vars[varName(p2, h)]])

    # Each pigeon must be in some hole
    for p in range(pigeons):
        clauses.append([vars[varName(p, h)] for h in range(holes)])

    # Insert here the code to generate the clauses.  A single clause var_name | var2_name is added as follows
    clauses.append([vars["var_name"], vars["var2_name"]])

    return clauses


# A helper function to print the cnf header
def printHeader(n):
    global gbi
    return "p cnf {} {}".format(gbi, n)


# A helper function to print a set of clauses cls
def printCnf(cls):
    return "\n".join(map(lambda x: "%s 0" % " ".join(map(str, x)), cls))


# This function is invoked when the python script is run directly and not imported
if __name__ == '__main__':
    # if not (os.path.isfile(SATsolver) and os.access(SATsolver, os.X_OK)):
    # if Z3 is installed with homebrew in the PATH env no need to explicitly specify the solver
    #    print "Set the path to SAT solver correctly on line 4 of this file (%s)" % sys.argv[0]
    #    sys.exit(1)

    # This is for reading in the arguments.
    if len(sys.argv) != 3:
        print("Usage: %s <pigeons> <holes>" % sys.argv[0])
        sys.exit(1)

    pigeons = int(sys.argv[1])
    holes = int(sys.argv[2])

    vars = gen_vars(pigeons, holes)

    rules = genPigConstr(pigeons, holes, vars)

    head = printHeader(len(rules))
    rls = printCnf(rules)

    # here we create the cnf file for SATsolver
    fl = open("tmp_prob.cnf", "w")
    fl.write("\n".join([head, rls]))
    fl.close()

    # this is for running SAT solver
    ms_out = Popen(["z3 tmp_prob.cnf"], stdout=PIPE, shell=True).communicate()[0]

    # SAT solver with these arguments writes the solution to a file called "solution".  Let's check it
    # res = open("solution", "r").readlines()
    res = ms_out.decode('utf-8')
    # Print output
    print(res)
    res = res.strip().split('\n')
    
    # if it was satisfiable, we want to have the assignment printed out
    if res[0] == "s SATISFIABLE":        
        # First get the assignment, which is on the second line of the file, and split it on spaces
        # Read the solution
        asgn = map(int, res[1].split()[1:])
        # Then get the variables that are positive, and get their names.
        # This way we know that everything not printed is false.
        # The last element in asgn is the trailing zero and we can ignore it

        # Convert the solution to our names
        facts = map(lambda x: varToStr[abs(x)], filter(lambda x: x > 0, asgn))

        # Print the solution
        for f in facts:
            print(f)
