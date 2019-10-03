# ----------------------------------------------------------------------
# Name:     Affine Cipher Frequency Analysis
#
# Date:     Spring 2019
# ----------------------------------------------------------------------
import string


def main():
    short_enc = affine_encrypt('affine cipher test', 5, 8)
    long_enc = affine_encrypt('the quick brown fox jumped over the lazy dog', 11, 17)
    affine = 'The affine cipher is a type of monoalphabetic substitution cipher, ' \
             'wherein each letter in an alphabet is mapped to its numeric equivalent, ' \
             'encrypted using a simple mathematical function, and converted back to a letter.'
    miracles = 'The Miracles are particularly valuable as a historical source. ' \
               'As the eminent scholar of the medieval Balkans, Dimitri Obolensky, ' \
               'writes, "in no other contemporary work will he find so much precise ' \
               'and first-hand information on the military organization and topography ' \
               'of Thessaloniki during one of the most dramatic centuries of its ' \
               'history; on the methods of warfare and the techniques of siege-craft ' \
               'used in the Balkan wars of the time; and on the strategy and tactics ' \
               'of the northern barbarians who, thrusting southward in successive waves ' \
               'down river valleys and across mountain passes, sought in the sixth and ' \
               'seventh centuries to gain a foothold on the warm Aegean coastland and ' \
               'to seize its commanding metropolis which always eluded their grasp. And ' \
               'there can be few documents stemming from the Christian world of the Middle ' \
               'Ages in which the belief held by the citizens of a beleaguered city that ' \
               'they stand under the supernatural protection of a heavenly patron is so ' \
               'vividly and poignantly expressed."'
    affine_enc = affine_encrypt(affine, 3, 7)
    miracles_enc = affine_encrypt(miracles, 7, 12)

    print("Encrypted text")
    print(short_enc)
    print(long_enc)
    print(affine_enc)
    print(miracles_enc)
    print()

    print("Frequency analysis over all letters")
    print(freq_analysis(short_enc))
    print(freq_analysis(long_enc))
    print(freq_analysis(affine_enc))
    print(freq_analysis(miracles_enc))
    print()

    print("Frequency analysis top two only")
    print(freq_analysis_top_two(short_enc))
    print(freq_analysis_top_two(long_enc))
    print(freq_analysis_top_two(affine_enc))
    print(freq_analysis_top_two(miracles_enc))


def affine_encrypt(input_string, a, b):
    output_string = []
    for x in input_string.upper():
        if x in string.ascii_uppercase:
            index = (a * string.ascii_uppercase.index(x) + b) % 26
            output_string.append(string.ascii_uppercase[index])
        else:
            output_string.append(x)
    output_string = ''.join(output_string)
    return output_string


def affine_decrypt(input_string, a, b):
    a_inv = 0
    for x in range(1, 26):
        if (a * x % 26) == 1:
            a_inv = x
            break
        a_inv = x
    output_string = []
    for x in input_string.upper():
        if x in string.ascii_uppercase:
            index = (a_inv * (string.ascii_uppercase.index(x) - b)) % 26
            output_string.append(string.ascii_uppercase[index])
        else:
            output_string.append(x)
    output_string = ''.join(output_string)
    return output_string


def freq_analysis_top_two(input_string):
    a, b = 0, 0
    max_range = 0
    while a % 2 == 0:
        a, b = find_ab(input_string, max_range)
        max_range += 1
    return affine_decrypt(input_string, a, b)


def find_ab(input_string, max_range=0):
    letter_count = count_letter_freq(input_string)
    letters_e_t = sorted(letter_count, key=letter_count.get, reverse=True)[max_range:(max_range+2)]
    e_freq = string.ascii_uppercase.index(letters_e_t[0])
    t_freq = string.ascii_uppercase.index(letters_e_t[1])
    a = 19 * (e_freq - t_freq) % 26
    b = 19 * (4 * t_freq - (19 * e_freq)) % 26
    return a, b


def freq_analysis(input_string):
    letter_count = count_letter_freq(input_string)
    pairs = freq_pair(letter_count)

    output_string = []
    for x in input_string.upper():
        if x in string.ascii_letters:
            output_string.append(pairs[x])
        else:
            output_string.append(x)

    return ''.join(output_string)


def count_letter_freq(input_string):
    letter_count = {}
    for x in input_string.upper():
        if x in string.ascii_uppercase:
            if x in letter_count:
                letter_count[x] += 1
            else:
                letter_count[x] = 1
    return letter_count


def freq_pair(letter_count):
    letter_freq = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    most_frequent = []
    for x in sorted(letter_count, key=letter_count.get, reverse=True):
        if x in string.ascii_uppercase:
            most_frequent.append(x)
    freq_result = {}
    for input_char, output_char in zip(most_frequent, letter_freq):
        freq_result[input_char] = output_char
    return freq_result


if __name__ == "__main__":
    main()
