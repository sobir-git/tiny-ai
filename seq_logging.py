class Log(list):
    """ A list of strings with some good printing functionality """

    def __init__(self, text="", level=0):
        self.text = text
        self.level = level

    def __str__(self):
        return "{} {}".format('-' * self.level, self.text)


class LogTree:
    def __init__(self):
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print(self, level=0, **kwargs):
        for child in self.children:
            if isinstance(child, str):
                text = "{}| {}".format('----' * level, child)
                print(text, **kwargs)
            else:
                child.print(level + 1, **kwargs)

    def string(self, level=0):
        result = []
        for child in self.children:
            if isinstance(child, str):
                text = "{}{}| {}".format(
                    '    ' * max(level - 1, 0), '----' * (level > 0), child)
                result.append(text)
            else:
                result.extend(child.string(level=level + 1))

        return result


if __name__ == "__main__":
    lt = LogTree(["1, -2, 3, -4"])
    lt1 = LogTree(["1, 3  \t\tby alternation"])
    lt2 = LogTree(["-2, -4  \t\tby alternation"])
    lt3 = LogTree(["2, 4  \t\tby abs values"])
    lt4 = LogTree(["-1, -1  \t\tby abs values"])
    lt2.add_child(lt3)
    lt2.add_child(lt4)
    lt.add_child(lt1)
    lt.add_child(lt2)
    lt.print()
