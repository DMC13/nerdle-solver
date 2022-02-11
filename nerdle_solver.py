import sympy
from itertools import permutations, combinations_with_replacement as comb_w_repl


def valid_strings_cleaning(valid_strings):
    cleaned = ''
    valid = '1234567890+-*/='
    for char in valid_strings:
        if char not in valid:
            raise SyntaxError('the input strings contain invalid character')
        if char not in cleaned:
            cleaned += char if char != '=' else ''
    return cleaned


def ask_equal_sign_position():
    ans = input('is the = sign at the #-2 position? (y/n) ')
    if ans.lower() == 'y':
        return -2
    else:
        ans = input('is the = sign at the #-3 position? (y/n) ')
        return -3 if ans.lower() == 'y' else -4


class AnEquation(object):

    def __init__(self, valid_strings, equal_sign_position, equation_length=8):
        if len(valid_strings) + 1 > equation_length:
            raise IndexError('too many letters provided')
        self.val_str = valid_strings
        self.equ_pos = equal_sign_position
        self.equ_len = equation_length

    def find_all_combinations(self):
        all_combinations = list()
        combinations = list(comb_w_repl(self.val_str, self.equ_len-1))
        val_str_set = set([c for c in self.val_str])
        for c in combinations:
            all_combinations.append(c) if val_str_set.issubset(c) else ''
        self.all_combinations = all_combinations

    def check_permutations(self, permut):
        operators = '+-*/'
        cp_permut = permut.copy()
        for p in permut:
            skip = False
            # no operators in first lhs position
            if p[0] in operators:
                cp_permut.remove(p)
                continue
            for pos in range(1, self.equ_len+self.equ_pos-1):
                # no consecutive operators
                if p[pos] in operators and p[pos+1] in operators:
                    cp_permut.remove(p)
                    skip = True
                    break
                # no 0 after /
                if p[pos] == '/' and p[pos+1] == '0':
                    cp_permut.remove(p)
                    skip = True
                    break
            if not skip:
                # no 0 in first rhs position if len(rhs)>1
                if self.equ_pos < -2 and p[self.equ_len+self.equ_pos] == 0:
                    cp_permut.remove(p)
                    continue
                # no operators on rhs
                for pos in range(self.equ_len+self.equ_pos, self.equ_len-1):
                    if p[pos] in operators:
                        cp_permut.remove(p)
                        break
        return cp_permut

    def find_all_possibilities(self):
        all_possibilities = list()
        for comb in self.all_combinations:
            permut = self.check_permutations(list(permutations(comb)))
            all_possibilities.extend(permut)
        self.all_possibilities = all_possibilities

    def form_calculation(self, strings):
        lhs, rhs = '', ''
        for pos in range(0, self.equ_len + self.equ_pos):
            lhs += strings[pos]
        for pos in range(self.equ_len + self.equ_pos, self.equ_len-1):
            rhs += strings[pos]
        return lhs, rhs

    def calculate(self):
        solvable = False
        print('\n\nresult:\n')
        for p in self.all_possibilities:
            lhs, rhs = self.form_calculation(p)
            try:
                if float(sympy.sympify(lhs)) == float(rhs):
                    if len(rhs) > 1 and rhs[0] == '0':
                        continue
                    print(f'-> {lhs}={rhs}')
                    solvable = True
            except:
                continue
        if not solvable:
            print('oops... seems your input is not solvable :(')
        else:
            print('\ndone!')

    def solve(self):
        self.find_all_combinations()
        self.find_all_possibilities()
        self.calculate()


if __name__ == '__main__':
    print('nerdlegame solver by DMC13\n')
    print('first, please try the below equations by your self:')
    print('-> 0 + 1 2 / 3 = 4')
    print('-> 9 * 8 - 7 = 6 5')

    valid_strings = input('\ntell me the valid letters: (e.g. 13578+*): ')
    valid_strings = valid_strings_cleaning(valid_strings)

    equal_sign_position = ask_equal_sign_position()

    # equation_length = int(input('how many columns in your nerdlegame? (6/8): '))

    Q = AnEquation(valid_strings, equal_sign_position)
    Q.solve()
