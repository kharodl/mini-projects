import re


def find(*filesnames):
    """
    Finds names in common between who files assuming names are wrapped
    with quotation marks such as an HTML file (adjust regex as needed)
    :param filesnames: (strings) list of filenames to search for names
    :return: (set) names in common
    """
    files = set()
    for f_name in filesnames:
        with open(f_name, 'r') as f:
            files.add(f.read())
    matches = set()

    for text in files:
        found = set(re.findall(r'\"([A-Z]\S*\s[A-Z]\S*)\"', text))
        matches = matches & found if matches else found

    return matches


if __name__ == '__main__':
    names = find("100w.txt", "151.txt")
    print(names)
