import sys
import modi
import time

import tkinter as tk
from _tkinter import TclError
from io import StringIO
from tkinter import Tk, Canvas, Entry, Label
from tkinter import END, WORD, INSERT, NW
from tkinter.scrolledtext import ScrolledText
if sys.platform == 'darwin':
    from tkmacosx import Button
else:
    from tkinter import Button

from modi.modi import MODI
from modi.util.message_util import parse_message


class Debugger(MODI):
    """
    Implementation of GUI Debugger for PyMODI,
    run this debugger with command of:
    > python -m modi -g
    """

    def __init__(self, *args, **kwargs):
        self._buffer = StringIO()
        sys.stdout = self._buffer
        super().__init__(verbose=True, *args, **kwargs)
        debugger = DebuggerWindow(self, self._buffer)
        debugger.run()


# TODO: Apply MVC pattern here
class DebuggerWindow:
    def __init__(self, bundle: MODI, buffer: StringIO):
        self._buffer = buffer
        self.bundle = bundle
        self.__input_box = None
        self._modules = []
        self.__log = None
        self.__spec = None
        self.__curr_module = None
        self.__curr_cmd = None
        self.__tell = 0
        self.__query = None
        self.__sid, self.__did, self.__cmd, self.__data = \
            None, None, None, None

    def run(self):
        width, height = 930, 790
        window = Tk()
        window.title(f"GUI Debugger for PyMODI (v{modi.__version__})")
        window.geometry(f"{width}x{height}")
        window.resizable(False, False)
        canvas = Canvas(window, width=width, height=height)
        canvas.create_rectangle(10, 40, 410, 340, outline='black')
        canvas.pack()

        # cmd (ins) field
        Label(window, text='c:').place(x=10, y=5)
        self.__cmd = Entry(window)
        self.__cmd.place(x=25, y=5, width=40)

        # sid field
        Label(window, text='s:').place(x=70, y=5)
        self.__sid = Entry(window)
        self.__sid.place(x=85, y=5, width=40)

        # did field
        Label(window, text='d:').place(x=130, y=5)
        self.__did = Entry(window)
        self.__did.place(x=145, y=5, width=40)

        # data field
        Label(window, text='b:').place(x=190, y=5)
        self.__data = Entry(window)
        self.__data.place(x=205, y=5, width=250)
        generate_button = Button(window, text="Generate", command=self.__parse)
        generate_button.place(x=455, y=5)

        # send field
        Label(window, text='msg:').place(x=545, y=5)
        self.__input_box = Entry(window)
        self.__input_box.place(x=580, y=5, width=250)
        self.__input_box["state"] = tk.DISABLED
        send_button = Button(window, text="Send", command=self.send)
        send_button.place(x=830, y=5)

        # TODO: Remove this __query related functions
        Label(window, text="Filter by Command: ").place(x=420, y=35)
        self.__query = Entry(window)
        self.__query.place(x=545, y=33, width=35)
        Button(window, text="Filter", command=self.__change_query).place(
            x=580, y=32
        )

        # log box (where MODI json messages are shown)
        self.__log = ScrolledText(window, wrap=WORD, font=('Helvetica', 12))
        self.__log.place(x=420, y=60, width=480, height=700)

        # spec box (where module information are shown)
        self.__spec = Label(
            window,
            text=f"Running PyMODI (v{modi.__version__})",
            bg='white', anchor=NW, justify='left', font=('Helvetica', 15)
        )
        self.__spec.place(x=10, y=350, width=400, height=390)

        # generate module button in the canvas
        for module in self.bundle.modules:
            self.__create_module_button(module, window)

        # run mainloop
        while True:
            try:
                window.update()
                self.__append_log()
                if self.__curr_module:
                    self.__change_spec(self.__curr_module)
            except TclError:
                break
            time.sleep(0.1)

    def __parse(self):
        try:
            # TODO: ensure each field is in a valid form
            cmd = eval(self.__cmd.get())
            sid = eval(self.__sid.get())
            did = eval(self.__did.get())
            data = eval(self.__data.get())
            msg = parse_message(cmd, sid, did, data)
            self.__input_box["state"] = tk.NORMAL
            self.__input_box.delete(0, END)
            self.__input_box.insert(0, msg)
            self.__input_box["state"] = tk.DISABLED
        except Exception as e:
            print("An exception in Tkinter callback has been raised:", e)
            self.__input_box["state"] = tk.NORMAL
            self.__input_box.delete(0, END)
            self.__input_box.insert(0, "Invalid Arguments")
            self.__input_box["state"] = tk.DISABLED

    def __query_log(self, line: str) -> bool:
        if ('recv' not in line and 'send' not in line) or \
            (self.__curr_module and str(self.__curr_module.id) not in line
                and self.__curr_module.module_type != 'network') \
                or (self.__curr_cmd and f'"c":{self.__curr_cmd},' not in line):
            return False
        return True

    def __change_query(self):
        self.__curr_cmd = self.__query.get()
        self.__update_log()

    def __update_log(self):
        self.__log.delete('0.0', END)
        log_text = self._buffer.getvalue()
        for line in log_text.split('\n'):
            if self.__query_log(line):
                self.__log.insert(INSERT, line + '\n')

    def __append_log(self):
        log_text = self._buffer.getvalue()
        new_text = log_text[self.__tell:]
        for line in new_text.split('\n'):
            if self.__query_log(line):
                self.__log.insert(INSERT, line + '\n')
            if line and 'send' not in line and 'recv' not in line:
                sys.__stdout__.write(line + '\n')
        self.__tell += len(new_text)
        self.__log.see(INSERT)

    def send(self):
        self.bundle.send(self.__input_box.get())

    def __change_spec(self, module):
        text = '\n'.join([
            f"Module Type: {module.module_type.upper()}",
            f"ID: {module.id}",
            f"UUID: {module.uuid}",
            f"STM32 Version: {module.version}",
            f"Contains User Code: {module.has_user_code}",
            f"Connected: {module.is_connected}"
        ])
        text += "\n[Properties]\n"
        # TODO: Fix code below to properly retrieve module properties
        for prop in module._properties:
            text += (
                f"{self.get_prop_name(prop, module)}: "
                f"{module._properties[prop].value} "
                f"last updated: "
                f"{module._properties[prop].last_update_time}\n"
            )
        self.__spec.configure(text=text)

    @staticmethod
    def get_prop_name(prop, module):
        module_props = module.__class__.__dict__
        for prop_key in module_props:
            if prop == module_props[prop_key]:
                return prop_key
        return prop

    def __create_module_button(self, module, window):
        module_button = Button(
            window,
            text=f"{module.module_type}\n({module.id})"
        )

        module_type = str(module.__class__)
        if 'output' in module_type:
            color = "orange"
        elif 'input' in module_type:
            color = "purple"
        else:
            color = "yellow"
        module_button.configure(
            bg=color,
            command=lambda: self.__change_module(module)
        )
        # TODO: Update button position as the module changes its position
        module_button.place(
            x=170 + 60 * module.position[0],
            y=180 - 40 * module.position[1],
            width=60, height=40,
        )
        # module button list
        self._modules.append(module_button)

    def __change_module(self, module):
        self.__curr_module = module
        self.__update_log()
