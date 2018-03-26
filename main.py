import search

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App


class Zamina(BoxLayout):
    def take_str(self, text):
        try:
            seq = text.split(',')
            seq = list(int(i)
                       for i in filter(lambda x: x and not x.isspace(), seq))
        except ValueError:
            self.rtinput.text = "!! Please follow the style 1, 2, 3, 4"
            return False

        search.report = False
        if len(seq) < 2:
            return False

        result = search.findNext(seq)
        next_number = result.value
        solution = result.log_tree.string()
        self.rtinput.text = '\n'.join(solution)
        if next_number is None:
            next_number = ":("


class SequencesApp(App):
    def build(self):
        return Zamina()


if __name__ == "__main__":
    SequencesApp().run()
