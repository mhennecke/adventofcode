import re


def inc_c(s: list[str], i: int = 0) -> list[str]:
    allowed = 'abcdefghjkmnpqrstuvwxyz'
    c = s[-(i + 1)]
    c_i = allowed.find(c)
    if c_i == -1:
        # looked for a char not in allow list: i, k or l
        c_i_new = allowed.find(chr(ord(c) + 1))
    else:
        c_i_new = c_i + 1

    if c_i_new >= len(allowed):
        if i > len(s):
            return None
        else:
            # overflow
            inc_c(s, i + 1)

    s[-(i + 1)] = allowed[c_i_new % len(allowed)]
    return s


def is_compliant(s: str) -> bool:
    allowed = 'abcdefghjkmnpqrstuvwxyz'
    # no forbidden characters
    if re.search(r'^[^iol]*$', s):
        nr_pairs = 0

        consec_chr = []
        for i in range(len(s)):
            if not consec_chr:
                consec_chr.append((s[i], 1))
            else:
                last_c, last_occ = consec_chr[-1]
                if last_c == s[i]:
                    consec_chr[-1] = (last_c, last_occ + 1)
                else:
                    consec_chr.append((s[i], 1))

        nr_pairs = sum(map(lambda c: c[1] == 2, consec_chr))

        # check for increasing straight
        is_straight = False

        nr_straight = 0
        nr_straight_consec = 1
        for i in range(len(s) - 1):
            s_allowed_i = allowed.find(s[i])
            s_allowed_ip1 = allowed.find(s[i + 1])
            if s_allowed_ip1 == s_allowed_i + 1 and s_allowed_i >= 0 and s_allowed_ip1 >= 0:
                nr_straight_consec += 1
            else:
                nr_straight_consec = 1

            if nr_straight_consec == 3:
                nr_straight += 1

        return nr_pairs >= 2 and nr_straight > 0
    else:
        return False


def new_password(pwd: str) -> str:
    # Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
    # Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
    # Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.

    assert len(pwd) == 8

    new_pwd = list(pwd)

    while True:
        new_pwd = inc_c(new_pwd)
        new_pwd_s = ''.join(new_pwd)
        if new_pwd is None:
            print("unable to find new compliant password")
            return None
        if is_compliant(new_pwd_s):
            return new_pwd_s
        else:
            pass
            # print(f'{new_pwd_s} is not compliant')


assert not is_compliant('hxbxxzyy')
assert not is_compliant('abcdahhh')
assert not is_compliant('abcdhhhh')
assert not is_compliant('abcdefhh')
assert not is_compliant('ghjaaadd')
assert is_compliant('abcdffaa')
assert is_compliant('abcdffaa')
assert is_compliant('ghjaabcc')

#assert new_password('ghizzzzy') == 'ghjaabcc'
#
#assert new_password('abcdefgh') == 'abcdffaa'
#assert new_password('ghijklmn') == 'ghjaabcc'

print(f'old: hxbxwxba, new: {new_password("hxbxwxba")}')
print(f'old: hxbxxyzz, new: {new_password("hxbxxyzz")}')
