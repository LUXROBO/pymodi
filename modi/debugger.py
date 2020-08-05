import threading as th
from tkinter import Tk, Canvas, Button, Entry, Label, NW, WORD, END, INSERT
from tkinter.scrolledtext import ScrolledText
from _tkinter import TclError
from modi.modi import MODI
import sys
from io import StringIO


class Debugger(MODI):
    def __init__(self, *args, **kwargs):
        self._buffer = StringIO()
        sys.stdout = self._buffer
        super().__init__(verbose=True, *args, **kwargs)

    def start(self):
        _DebuggerWindow(self, self._buffer).start()


class _DebuggerWindow(th.Thread):
    def __init__(self, bundle: MODI, buffer: StringIO):
        super().__init__(daemon=True)
        self._buffer = buffer
        self.bundle = bundle
        self.__input_box = None
        self._modules = []
        self.__log = None
        self.__spec = None
        self.__curr_module = None
        self.__tell = 0

    def run(self) -> None:
        width, height = 900, 550
        window = Tk()
        window.title("PyMODI Debugger")
        window.geometry(f"{width}x{height}")
        window.resizable(False, False)
        canvas = Canvas(window, width=width, height=height)
        canvas.create_rectangle(10, 60, 400, 340, outline='black')
        canvas.pack()

        self.__input_box = Entry(window)
        self.__input_box.place(x=10, y=25, width=340)

        send_button = Button(window, text="Send", command=self.send)
        send_button.place(x=360, y=20)

        self.__log = ScrolledText(window, wrap=WORD, font=('Helvetica', 12))
        self.__log.place(x=420, y=10, width=470, height=330)
        self.__log.insert(INSERT, "ASdasdasdas")
        self.__log.delete('0.0', END)

        self.__spec = Label(window, text="Your MODI", bg='white', anchor=NW,
                            justify='left', font=('Helvetica', 10))
        self.__spec.place(x=10, y=350, width=300, height=200)

        for module in self.bundle._modules:
            self.__create_module_button(module, window)

        while True:
            try:
                window.update()
                self.__update_log()
                if self.__curr_module:
                    self.__change_spec(self.__curr_module)
            except TclError:
                break

    def __update_log(self):
        log_text = self._buffer.getvalue()
        new_text = log_text[self.__tell:]
        for line in new_text.split('\n'):
            if 'recv' in line or 'send' in line:
                self.__log.insert(INSERT, line + '\n')
            elif line:
                sys.__stdout__.write(line + '\n')
        self.__tell += len(new_text)

    def send(self):
        self.bundle.send(self.__input_box.get())

    def __change_spec(self, module):
        text = '\n'.join([f"Module Type: {module.module_type}",
                          f"Id: {module.id}",
                          f"UUID: {module.uuid}",
                          f"Version: {module.version}",
                          f"User Code: {module.has_user_code}",
                          f"Connected: {module.is_connected}"])
        text += '\n[Properties]\n'
        for prop in module._properties:
            text += f"{prop.name}: {module._properties[prop].value}\n"
        self.__spec.configure(text=text)

    def __create_module_button(self, module, window):
        module_button = Button(window,
                               text=f"{module.module_type}\n({module.id})")
        module_type = str(module.__class__)
        if 'output' in module_type:
            color = '#fb973f'
        elif 'input' in module_type:
            color = '#9672f9'
        else:
            color = '#f3c029'
        module_button.configure(bg=color,
                                command=lambda: self.__change_module(module))
        module_button.place(x=170 + 60 * module.position[0],
                            y=180 - 40 * module.position[1],
                            width=60, height=40)
        self._modules.append(module_button)

    def __change_module(self, module):
        self.__curr_module = module
