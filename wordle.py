import z3
from feedback2 import wordleScore

WL = 5

CHARS_2 = "abcdefghijklmnopqrstuvwxyz"
CHARS = {letter:idx for idx, letter in enumerate(CHARS_2)}


DICT_PATH = "/usr/share/dict/words"


TARGET = "query"

def main():
    solver = z3.Solver()
    char_vars = char_variables()

    solver = add_max_len_constraint(solver, char_vars)

    words = get_filtered_dict()

    solver = add_only_words_in_dict_constraint(solver, char_vars, words)

    W = [None,None,None,None,None]

    # result = solver.check()

    # print(result)

    attempts = 5

    while attempts >= 0:

        result = solver.check()

        result_string = model_to_string(char_vars, solver.model())
        print(result_string)

        score = wordleScore(TARGET, result_string)

        if sum(score) == 10:
            print("Done")
            return

        for i in range(5):
            if score[i] == 2:
                W[i] = result_string[i]
                add_char_in_fixed_pos_constraint(solver, char_vars, result_string[i], i)

        for i in range(5):
            if score[i] == 1:
                solver = add_must_contain_constraint(solver, char_vars, result_string[i])
                solver = add_banned_char_in_pos_constraint(solver, char_vars, result_string[i], i)

        for i in range(5):
            if score[i] == 0:
                if (result_string[i] not in W):
                    solver = add_banned_char_constraint(solver, char_vars, result_string[i])
                else:
                    solver = add_only_one_time_constraint(solver, char_vars, result_string[i])

        attempts -= 1
    print("Failed, too many attempts")
    pass

def char_variables():
    cvs = []
    for i in range(WL):
        cvs.append(z3.Int("char_" + str(i)))
    return cvs

# Every char can be a number from 0 to 25 i.e. from a to z (both included)
def add_max_len_constraint(solver, char_vars):
    for c_v in char_vars:
        # solver.add(c_v >= 0, c_v <= 25)
        solver.add(z3.And(c_v >= 0, c_v <= 25))

    return solver


# Converts the model which holds the solution in numbers from 0 to 25 to a word
def model_to_string(char_vars, model):
    s = ""
    for c_v in char_vars:
        s += CHARS_2[model[c_v].as_long()]
    return s


def get_filtered_dict():
    words = set()
    with open(DICT_PATH, 'r') as d:
        for l in d.readlines():
            l = l.strip()
            l = l.lower()
            if l.isalpha() and len(l) == WL:
                words.add(l)
    return words

def add_only_words_in_dict_constraint(solver, char_vars, dict: set):
    all_w_constaints = []
    for w in dict:
        w_constraint = []
        for i in range(WL):
            w_constraint.append(char_vars[i] == CHARS[w[i]])
        all_w_constaints.append(z3.And(w_constraint))
    
    solver.add(z3.Or(all_w_constaints))
    return solver

def add_banned_char_constraint(solver, char_vars, char):
    for c_v in char_vars:
        solver.add(c_v != CHARS[char])
        # solver.add(z3.Not(z3.eq(c_v, char)))
    return solver

def add_must_contain_constraint(solver, char_vars, char):
    constraint = []
    for c_v in char_vars:
        constraint.append(c_v == CHARS[char])

    solver.add(z3.Or(constraint))
    return solver
    
def add_banned_char_in_pos_constraint(solver, char_vars, char, pos):
    solver.add(char_vars[pos] != CHARS[char])
    return solver


def add_char_in_fixed_pos_constraint(solver, char_vars, char, pos):
    solver.add(char_vars[pos] == CHARS[char])
    return solver


def add_only_one_time_constraint(solver, char_vars, char):
    one_time = []
    
    for c_v in char_vars:
        rule = []
        rule.append(c_v == CHARS[char])
        for other_c_v in char_vars:
            if other_c_v == c_v:
                continue
            rule.append(other_c_v != CHARS[char])
        one_time.append(z3.And(rule))

    solver.add(z3.Or(one_time))
    return solver


if __name__ == "__main__":
    main()