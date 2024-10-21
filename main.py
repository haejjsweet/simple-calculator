from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


def create_button(text, size_hint, pos_hint, func):
    button_parameters = {
        'text': text,
        'size_hint': size_hint,
        'pos_hint': pos_hint
    }
    button = Button(**button_parameters)
    button.bind(on_press=func)
    return button


class Calculator(App):
    def __init__(self):
        App.__init__(self)
        self.input = TextInput()
        self.cur_num = ''
        self.count_unclosed_braces = 0

    def build_nums(self, screen, button_size):
        start_x = 0
        start_y = button_size[1]
        button_num = 1
        for row in range(3):
            for column in range(3):
                screen.add_widget(create_button(str(button_num), button_size,
                                                {'x': start_x + button_size[0] * column,
                                                 'y': start_y + button_size[1] * row}, self.click_num))
                button_num += 1

        screen.add_widget(create_button('0', (0.25, 0.14), {'x': 0.25, 'y': 0}, self.click_num))

    def build(self):
        screen = Screen()
        self.input.pos_hint = {'x': 0, 'y': 0.7}
        self.input.size_hint = (1, 0.3)
        screen.add_widget(self.input)
        # заполнитm
        button_size = (0.25, 0.14)
        self.build_nums(screen, button_size)
        # операции
        screen.add_widget(create_button('+', button_size, {'x': 0.75, 'y': 0.14}, self.click_op))
        screen.add_widget(create_button('-', button_size, {'x': 0.75, 'y': 0.28}, self.click_op))
        screen.add_widget(create_button('*', button_size, {'x': 0.75, 'y': 0.42}, self.click_op))
        screen.add_widget(create_button('/', button_size, {'x': 0.75, 'y': 0.56}, self.click_op))
        # добавки
        screen.add_widget(create_button('(', button_size, {'x': 0.5, 'y': 0.56}, self.click_brace_open))
        screen.add_widget(create_button('.', button_size, {'x': 0.5, 'y': 0}, self.click_dot))
        screen.add_widget(create_button(')', button_size, {'x': 0, 'y': 0}, self.click_brace_close))
        # удаление
        screen.add_widget(create_button('del', button_size, {'x': 0.25, 'y': 0.56}, self.click_del))
        screen.add_widget(create_button('C', button_size, {'x': 0, 'y': 0.56}, self.click_c))

        screen.add_widget(create_button('=', button_size, {'x': 0.75, 'y': 0}, self.click_solve))
        return screen

    def click(self, *args):
        button: Button = args[0]
        print(button.text)

    def click_num(self, *args):
        button: Button = args[0]
        # если нет решения то отчистить
        if self.input.text == 'нет решения':
            self.input.text = ''
            self.cur_num = ''
        # если ничего не написано или 1 эл не равен 0
        if len(self.cur_num) == 0 or (self.cur_num[0] != "0" or '.' in self.cur_num):
            if self.input.text == '' or self.input.text[-1] != ')':
                self.input.text += button.text
                self.cur_num += button.text

    def click_op(self, *args):
        button: Button = args[0]
        # ставим знак только если что то написано И перед знаком стоит цифра
        if len(self.input.text) != 0 and self.input.text[-1].isdigit():
            self.input.text += button.text
            self.cur_num = ''

    def click_solve(self, *args):
        button: Button = args[0]
        try:
            if self.input.text[-1] in '*/+-%':
                return
            result = round(eval(self.input.text), 15)
        except ZeroDivisionError:
            result = 'нет решения'
        except SyntaxError:
            return
        self.input.text = str(result)
        if result == 'нет решения':
            self.cur_num = ''
        else:
            self.cur_num = str(result)
        self.count_unclosed_braces = 0

    def click_brace_open(self, *args):
        button: Button = args[0]
        if self.input.text == '' or self.input.text[-1] in '*/+-%':
            self.input.text += '('
            self.count_unclosed_braces += 1
            self.cur_num = ''

    def click_brace_close(self, *args):
        button: Button = args[0]
        if self.input.text != '' and (self.input.text[-1].isdigit() or self.input.text[-1] == ')') and self.count_unclosed_braces >= 1:
            self.input.text += ')'
            self.count_unclosed_braces -= 1
            self.cur_num = ''

    def click_c(self, *args):
        button: Button = args[0]
        self.input.text = ''
        self.cur_num = ''
        self.count_unclosed_braces = 0

    def click_del(self, *args):
        if self.input.text != '' and self.input.text[-1] == ')':
            self.count_unclosed_braces += 1
        elif self.input.text != '' and self.input.text[-1] == '(':
            self.count_unclosed_braces -= 1
        button: Button = args[0]
        result = self.input.text[:-1]
        self.input.text = result
        self.cur_num = self.cur_num[:-1]

    def click_dot(self, *args):
        if self.cur_num != '' and '.' not in self.cur_num:
            self.input.text += '.'
            self.cur_num += '.'


bimbim = Calculator()

bimbim.run()
