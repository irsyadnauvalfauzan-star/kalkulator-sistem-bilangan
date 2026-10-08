
from kivy.config import Config
Config.set("graphics", "width", "390")
Config.set("graphics", "height", "844")
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line


# =========================
# WARNA
# =========================
BG = (0.95, 0.96, 0.97, 1)
CARD = (1, 1, 1, 1)
TEXT = (0.08, 0.11, 0.15, 1)
MUTED = (0.40, 0.45, 0.49, 1)
BLUE = (0.09, 0.47, 1, 1)
BLUE_DARK = (0.04, 0.35, 0.78, 1)
BORDER = (0.84, 0.87, 0.90, 1)
DISABLED = (0.90, 0.92, 0.94, 1)


class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = dp(10)
        self.spacing = dp(5)
        with self.canvas.before:
            Color(*CARD)
            self.rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(12)]
            )
            Color(*BORDER)
            self.line = Line(
                rounded_rectangle=(
                    self.x, self.y, self.width, self.height, dp(12)
                ),
                width=0.7,
            )
        self.bind(pos=self._update, size=self._update)

    def _update(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.line.rounded_rectangle = (
            self.x, self.y, self.width, self.height, dp(12)
        )


class AppButton(Button):
    def __init__(self, **kwargs):
        bg = kwargs.pop("bg", CARD)
        fg = kwargs.pop("fg", TEXT)
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = bg
        self.color = fg
        self.font_size = sp(15)
        self.bold = True


class MobileCalculator(App):
    def build(self):
        Window.clearcolor = BG
        Window.size = (390, 844)

        self.current_page = "PROGRAMMER"
        self.root_box = BoxLayout(
            orientation="vertical",
            padding=[dp(10), dp(8), dp(10), dp(8)],
            spacing=dp(7),
        )

        self.build_header()
        self.content = BoxLayout()
        self.root_box.add_widget(self.content)

        self.show_programmer()
        return self.root_box

    def txt(self, text, size=13, color=TEXT, bold=False, halign="left"):
        label = Label(
            text=text,
            font_size=sp(size),
            color=color,
            bold=bold,
            halign=halign,
            valign="middle",
        )
        label.bind(size=lambda obj, val: setattr(obj, "text_size", (obj.width, None)))
        return label

    # =========================
    # HEADER / TAB HP
    # =========================
    def build_header(self):
        title_row = BoxLayout(size_hint_y=None, height=dp(38))
        title_row.add_widget(self.txt("Kalkulator Sistem Bilangan", 18, TEXT, True))
        self.root_box.add_widget(title_row)

        tabs = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(4))

        self.btn_programmer = AppButton(
            text="PROGRAMMER", bg=BLUE, fg=(1, 1, 1, 1)
        )
        self.btn_kabataku = AppButton(text="KABATAKU BINER")

        self.btn_programmer.bind(on_release=lambda *_: self.show_programmer())
        self.btn_kabataku.bind(on_release=lambda *_: self.show_kabataku())

        tabs.add_widget(self.btn_programmer)
        tabs.add_widget(self.btn_kabataku)
        self.root_box.add_widget(tabs)

    def set_tab(self, page):
        self.current_page = page
        self.btn_programmer.background_color = (
            BLUE if page == "PROGRAMMER" else CARD
        )
        self.btn_programmer.color = (
            (1, 1, 1, 1) if page == "PROGRAMMER" else TEXT
        )
        self.btn_kabataku.background_color = (
            BLUE if page == "KABATAKU" else CARD
        )
        self.btn_kabataku.color = (
            (1, 1, 1, 1) if page == "KABATAKU" else TEXT
        )

    # =========================
    # PROGRAMMER
    # =========================
    def show_programmer(self):
        self.set_tab("PROGRAMMER")
        self.content.clear_widgets()

        root = BoxLayout(orientation="vertical", spacing=dp(6))

        self.p_base = getattr(self, "p_base", 10)
        self.p_value = getattr(self, "p_value", "0")
        self.p_first = getattr(self, "p_first", None)
        self.p_operator = getattr(self, "p_operator", None)
        self.p_waiting = getattr(self, "p_waiting", False)
        self.p_fresh = getattr(self, "p_fresh", True)

        # Display
        display = Card(size_hint_y=None, height=dp(67))
        self.p_display = self.txt(self.p_value, 31, TEXT, True, "right")
        display.add_widget(self.p_display)
        root.add_widget(display)

        # Base
        base = GridLayout(cols=4, spacing=dp(4), size_hint_y=None, height=dp(40))
        self.p_base_buttons = {}
        for number, name in [(10, "DEC"), (16, "HEX"), (8, "OCT"), (2, "BIN")]:
            b = AppButton(text=name)
            b.bind(on_release=lambda _, x=number: self.p_change_base(x))
            base.add_widget(b)
            self.p_base_buttons[number] = b
        root.add_widget(base)

        # Conversion
        conversion = Card(
            orientation="vertical", size_hint_y=None, height=dp(102)
        )
        conversion.add_widget(self.txt("KONVERSI", 10, MUTED, True))
        self.p_rows = {}
        for name in ["HEX", "DEC", "OCT", "BIN"]:
            row = BoxLayout(size_hint_y=None, height=dp(19))
            row.add_widget(self.txt(name, 9, MUTED, True))
            value = self.txt("0", 10, TEXT)
            row.add_widget(value)
            self.p_rows[name] = value
            conversion.add_widget(row)
        root.add_widget(conversion)

        # Keypad
        scroll = ScrollView(do_scroll_x=False, bar_width=0)
        keypad = GridLayout(
            cols=5,
            spacing=dp(4),
            padding=[0, dp(2)],
            size_hint_y=None,
            row_default_height=dp(46),
            row_force_default=True,
        )
        keypad.bind(minimum_height=keypad.setter("height"))

        rows = [
            ["A", "B", "C", "D", "E"],
            ["F", "<<", ">>", "CE", "⌫"],
            ["7", "8", "9", "AND", "OR"],
            ["4", "5", "6", "XOR", "NOT"],
            ["1", "2", "3", "+", "−"],
            ["0", "", "", "×", "÷"],
            ["", "", "", "=", ""],
        ]

        self.p_hex_buttons = {}
        self.p_num_buttons = {}

        for row in rows:
            for value in row:
                if value == "":
                    keypad.add_widget(Widget())
                    continue

                b = AppButton(text=value)

                if value in "ABCDEF":
                    b.bind(on_release=lambda _, d=value: self.p_input(d))
                    self.p_hex_buttons[value] = b
                elif value.isdigit():
                    b.bind(on_release=lambda _, d=value: self.p_input(d))
                    self.p_num_buttons[value] = b
                else:
                    b.bind(on_release=lambda _, v=value: self.p_action(v))

                keypad.add_widget(b)

        scroll.add_widget(keypad)
        root.add_widget(scroll)

        self.content.add_widget(root)
        self.p_update()

    @staticmethod
    def to_base(n, base):
        if n < 0:
            return "-" + MobileCalculator.to_base(-n, base)
        if base == 2:
            return format(n, "b")
        if base == 8:
            return format(n, "o")
        if base == 10:
            return str(n)
        if base == 16:
            return format(n, "X")
        return str(n)

    @staticmethod
    def from_base(value, base):
        return int(value, base)

    def p_change_base(self, base):
        try:
            number = self.from_base(self.p_value, self.p_base)
        except ValueError:
            number = 0

        self.p_base = base
        self.p_value = self.to_base(number, base)
        self.p_fresh = False
        self.p_waiting = False
        self.p_update()

    def p_input(self, value):
        allowed = {
            2: "01",
            8: "01234567",
            10: "0123456789",
            16: "0123456789ABCDEF",
        }

        if value not in allowed[self.p_base]:
            return

        if self.p_waiting:
            self.p_value = value
            self.p_waiting = False
            self.p_fresh = False
        elif self.p_fresh:
            self.p_value = value
            self.p_fresh = False
        else:
            self.p_value += value

        self.p_update()

    def p_clear(self):
        self.p_value = "0"
        self.p_first = None
        self.p_operator = None
        self.p_waiting = False
        self.p_fresh = True
        self.p_update()

    def p_backspace(self):
        if len(self.p_value) > 1:
            self.p_value = self.p_value[:-1]
        else:
            self.p_value = "0"
            self.p_fresh = True
        self.p_update()

    def p_operator_set(self, op):
        try:
            self.p_first = self.from_base(self.p_value, self.p_base)
        except ValueError:
            return
        self.p_operator = op
        self.p_waiting = True

    def p_calculate(self):
        if self.p_first is None or self.p_operator is None:
            return

        try:
            second = self.from_base(self.p_value, self.p_base)
            op = self.p_operator

            if op == "+":
                result = self.p_first + second
            elif op == "-":
                result = self.p_first - second
            elif op == "×":
                result = self.p_first * second
            elif op == "÷":
                if second == 0:
                    raise ZeroDivisionError
                result = self.p_first // second
            elif op == "AND":
                result = self.p_first & second
            elif op == "OR":
                result = self.p_first | second
            elif op == "XOR":
                result = self.p_first ^ second
            elif op == "<<":
                result = self.p_first << second
            elif op == ">>":
                result = self.p_first >> second
            else:
                return

            self.p_value = self.to_base(result, self.p_base)
            self.p_first = None
            self.p_operator = None
            self.p_waiting = True
            self.p_fresh = False
            self.p_update()

        except ZeroDivisionError:
            self.p_value = "Error"
            self.p_first = None
            self.p_operator = None
            self.p_update()

    def p_not(self):
        try:
            n = self.from_base(self.p_value, self.p_base)
            self.p_value = self.to_base(~n, self.p_base)
            self.p_update()
        except ValueError:
            pass

    def p_action(self, value):
        if value == "CE":
            self.p_clear()
        elif value == "⌫":
            self.p_backspace()
        elif value == "=":
            self.p_calculate()
        elif value == "NOT":
            self.p_not()
        else:
            self.p_operator_set("-" if value == "−" else value)

    def p_update(self):
        self.p_display.text = self.p_value

        try:
            n = self.from_base(self.p_value, self.p_base)
            self.p_rows["HEX"].text = self.to_base(n, 16)
            self.p_rows["DEC"].text = self.to_base(n, 10)
            self.p_rows["OCT"].text = self.to_base(n, 8)

            binary = self.to_base(n, 2)
            if not binary.startswith("-"):
                binary = binary.zfill(max(4, ((len(binary) + 3) // 4) * 4))
                binary = " ".join(
                    binary[i:i + 4] for i in range(0, len(binary), 4)
                )
            self.p_rows["BIN"].text = binary
        except ValueError:
            pass

        allowed = {
            2: "01",
            8: "01234567",
            10: "0123456789",
            16: "0123456789ABCDEF",
        }[self.p_base]

        for d, b in self.p_hex_buttons.items():
            b.disabled = d not in allowed
            b.background_color = DISABLED if b.disabled else CARD

        for d, b in self.p_num_buttons.items():
            b.disabled = d not in allowed
            b.background_color = DISABLED if b.disabled else CARD

        for base, b in self.p_base_buttons.items():
            b.background_color = BLUE if base == self.p_base else CARD
            b.color = (1, 1, 1, 1) if base == self.p_base else TEXT

    # =========================
    # KABATAKU
    # =========================
    def show_kabataku(self):
        self.set_tab("KABATAKU")
        self.content.clear_widgets()

        root = BoxLayout(orientation="vertical", spacing=dp(6))

        title = Card(orientation="vertical", size_hint_y=None, height=dp(62))
        title.add_widget(self.txt("KABATAKU BINER", 21, TEXT, True))
        title.add_widget(self.txt("Hitung biner + simpan/pinjam", 10, MUTED))
        root.add_widget(title)

        input_card = Card(
            orientation="vertical", size_hint_y=None, height=dp(177)
        )

        self.b_entry_a = TextInput(
            multiline=False,
            font_size=sp(20),
            halign="right",
            padding=[dp(8), dp(10)],
            size_hint_y=None,
            height=dp(45),
        )
        self.b_entry_b = TextInput(
            multiline=False,
            font_size=sp(20),
            halign="right",
            padding=[dp(8), dp(10)],
            size_hint_y=None,
            height=dp(45),
        )

        top = BoxLayout(size_hint_y=None, height=dp(92), spacing=dp(6))

        col1 = BoxLayout(orientation="vertical")
        col1.add_widget(self.txt("BILANGAN 1", 9, MUTED, True))
        col1.add_widget(self.b_entry_a)

        col2 = BoxLayout(orientation="vertical")
        col2.add_widget(self.txt("BILANGAN 2", 9, MUTED, True))
        col2.add_widget(self.b_entry_b)

        top.add_widget(col1)
        top.add_widget(col2)
        input_card.add_widget(top)

        self.b_op = "+"
        ops = GridLayout(cols=4, spacing=dp(4), size_hint_y=None, height=dp(36))
        self.b_op_buttons = {}

        for op in ["+", "−", "×", "÷"]:
            b = AppButton(text=op)
            b.bind(on_release=lambda _, x=op: self.b_set_op(x))
            ops.add_widget(b)
            self.b_op_buttons[op] = b

        input_card.add_widget(ops)

        root.add_widget(input_card)

        actions = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(5))
        hitung = AppButton(text="HITUNG", bg=BLUE, fg=(1, 1, 1, 1))
        bersihkan = AppButton(text="BERSIHKAN")
        hitung.bind(on_release=lambda *_: self.b_calculate())
        bersihkan.bind(on_release=lambda *_: self.b_clear())
        actions.add_widget(hitung)
        actions.add_widget(bersihkan)
        root.add_widget(actions)

        result = Card(
            orientation="vertical", size_hint_y=None, height=dp(105)
        )
        result.add_widget(self.txt("HASIL", 9, MUTED, True))
        self.b_result_label = self.txt(
            "Masukkan dua bilangan biner", 22, TEXT, True, "right"
        )
        result.add_widget(self.b_result_label)
        self.b_check_label = self.txt("", 9, MUTED, False, "right")
        result.add_widget(self.b_check_label)
        root.add_widget(result)

        steps = Card(orientation="vertical")
        steps.add_widget(self.txt("LANGKAH PERHITUNGAN", 10, TEXT, True))

        self.b_steps = TextInput(
            readonly=True,
            multiline=True,
            font_size=sp(11),
            background_color=CARD,
            foreground_color=TEXT,
            padding=[dp(5), dp(5)],
        )
        steps.add_widget(self.b_steps)
        root.add_widget(steps)

        self.b_set_op("+")
        self.content.add_widget(root)

    def b_set_op(self, op):
        self.b_op = op
        for key, b in self.b_op_buttons.items():
            b.background_color = BLUE if key == op else CARD
            b.color = (1, 1, 1, 1) if key == op else TEXT

    def b_get_inputs(self):
        a = self.b_entry_a.text.replace(" ", "").replace("_", "")
        b = self.b_entry_b.text.replace(" ", "").replace("_", "")

        if not a or not b:
            raise ValueError("Kedua bilangan harus diisi.")

        if any(ch not in "01" for ch in a + b):
            raise ValueError("Hanya boleh menggunakan 0 dan 1.")

        return a, b

    @staticmethod
    def binary_add(a, b):
        width = max(len(a), len(b))
        a = a.zfill(width)
        b = b.zfill(width)

        carry = 0
        result = ""
        carry_row = ["0"] * width
        steps = []

        for i in range(width - 1, -1, -1):
            x = int(a[i])
            y = int(b[i])
            total = x + y + carry
            bit = total % 2
            new_carry = total // 2

            carry_row[i] = str(carry)
            result = str(bit) + result

            steps.append(
                f"Kolom {width - i}: {x} + {y} + {carry} = {total} "
                f"→ tulis {bit}, simpan {new_carry}"
            )

            carry = new_carry

        if carry:
            result = "1" + result
            carry_display = "1" + "".join(carry_row)
        else:
            carry_display = "".join(carry_row)

        return result, carry_display, steps

    @staticmethod
    def binary_subtract(a, b):
        if int(a, 2) < int(b, 2):
            raise ValueError(
                "Untuk pengurangan ini, Bilangan 1 harus lebih besar "
                "atau sama dengan Bilangan 2."
            )

        width = max(len(a), len(b))
        a = a.zfill(width)
        b = b.zfill(width)

        borrow = 0
        result = ""
        borrow_row = ["0"] * width
        steps = []

        for i in range(width - 1, -1, -1):
            x = int(a[i]) - borrow
            y = int(b[i])

            if x < y:
                borrow_row[i] = "1"
                steps.append(
                    f"Kolom {width - i}: tidak cukup → pinjam 1 dari kiri."
                )
                x += 2
                new_borrow = 1
            else:
                new_borrow = 0

            bit = x - y
            result = str(bit) + result
            borrow = new_borrow

            steps.append(
                f"Kolom {width - i}: {x} - {y} = {bit}"
            )

        return result.lstrip("0") or "0", "".join(borrow_row), steps

    def b_calculate(self):
        try:
            a, b = self.b_get_inputs()

            if self.b_op == "+":
                result, carry, steps = self.binary_add(a, b)
                width = max(len(a), len(b))
                aa = a.zfill(width)
                bb = b.zfill(width)

                details = (
                    "PENJUMLAHAN BINER\n\n"
                    f"CARRY : {carry}\n\n"
                    f"  {aa}\n"
                    f"+ {bb}\n"
                    f"  {'-' * width}\n"
                    f"  {result}\n\n"
                    "LANGKAH DARI KANAN KE KIRI:\n"
                    + "\n".join(
                        f"{i}. {s}" for i, s in enumerate(steps, 1)
                    )
                )

            elif self.b_op == "−":
                result, borrow, steps = self.binary_subtract(a, b)
                width = max(len(a), len(b))
                aa = a.zfill(width)
                bb = b.zfill(width)

                details = (
                    "PENGURANGAN BINER\n\n"
                    f"BORROW : {borrow}\n\n"
                    f"  {aa}\n"
                    f"- {bb}\n"
                    f"  {'-' * width}\n"
                    f"  {result.zfill(width)}\n\n"
                    "LANGKAH DARI KANAN KE KIRI:\n"
                    + "\n".join(
                        f"{i}. {s}" for i, s in enumerate(steps, 1)
                    )
                )

            elif self.b_op == "×":
                result = format(int(a, 2) * int(b, 2), "b")
                steps = []

                for i, bit in enumerate(reversed(b)):
                    partial = (
                        a + ("0" * i)
                        if bit == "1"
                        else "0" * (len(a) + i)
                    )
                    steps.append(
                        f"Baris {i + 1}: bit {bit} → {partial}"
                    )

                details = (
                    "PERKALIAN BINER\n\n"
                    f"{a}\n× {b}\n"
                    f"{'-' * max(len(a), len(b))}\n"
                    f"{result}\n\n"
                    "LANGKAH:\n"
                    + "\n".join(
                        f"{i}. {s}" for i, s in enumerate(steps, 1)
                    )
                )

            else:
                divisor = int(b, 2)
                if divisor == 0:
                    raise ZeroDivisionError

                quotient, remainder = divmod(int(a, 2), divisor)
                result = format(quotient, "b")
                rem = format(remainder, "b")

                details = (
                    "PEMBAGIAN BINER\n\n"
                    f"{a} ÷ {b}\n\n"
                    f"Hasil bagi : {result}\n"
                    f"Sisa       : {rem}"
                )

            self.b_result_label.text = result
            self.b_check_label.text = (
                f"Desimal: {int(a, 2)} {self.b_op} {int(b, 2)} = "
                f"{int(result, 2)}"
            )
            self.b_steps.text = details

        except ZeroDivisionError:
            self.b_result_label.text = "Error"
            self.b_check_label.text = "Bilangan kedua tidak boleh 0."

        except ValueError as exc:
            self.b_result_label.text = "Input salah"
            self.b_check_label.text = str(exc)

    def b_clear(self):
        self.b_entry_a.text = ""
        self.b_entry_b.text = ""
        self.b_result_label.text = "Masukkan dua bilangan biner"
        self.b_check_label.text = ""
        self.b_steps.text = ""
        self.b_set_op("+")


if __name__ == "__main__":
    MobileCalculator().run()
