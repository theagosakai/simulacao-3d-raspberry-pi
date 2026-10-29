from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle, PushMatrix, PopMatrix, Rotate
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget


class RaspberryBoard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_code = "pi5"
        self.angle = -8
        self.touch_down = None
        self.powered = True
        self.blinking = True
        self.blink_phase = False
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        Clock.schedule_interval(self.update_led, .65)

    def set_model(self, model_code):
        self.model_code = model_code
        self.angle = -8
        self.update_canvas()

    def update_led(self, _dt):
        if self.blinking and self.powered:
            self.blink_phase = not self.blink_phase
            self.update_canvas()

    def toggle_power(self):
        self.powered = not self.powered
        self.update_canvas()
        return self.powered

    def toggle_led(self):
        self.blinking = not self.blinking
        self.update_canvas()
        return self.blinking

    def reset_view(self):
        self.angle = -8
        self.update_canvas()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_down = touch.x
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.touch_down is not None and self.collide_point(*touch.pos):
            self.angle += (touch.x - self.touch_down) * 0.35
            self.touch_down = touch.x
            self.update_canvas()
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self.touch_down = None
        return super().on_touch_up(touch)

    def chip(self, x, y, w, h, label="", radius=4):
        Color(.12, .14, .15)
        RoundedRectangle(pos=(x, y), size=(w, h), radius=[radius])
        Color(.75, .78, .77)
        if label:
            Label(text=label, pos=(x, y + h * .32), size=(w, h * .36),
                  font_size=min(11, w * .07), halign="center", valign="middle")

    def update_canvas(self, *_args):
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            Rotate(origin=(self.center_x, self.center_y), angle=self.angle, axis=(0, 0, 1))

            w, h = self.width, self.height
            scale = min(w / 520, h / 350)
            models = {
                "pi5": ("Raspberry Pi 5", "BCM2712", "LPDDR4X", 520, 350),
                "pi4": ("Raspberry Pi 4 Model B", "BCM2711", "LPDDR4", 520, 350),
                "pi3": ("Raspberry Pi 3 Model B+", "BCM2837B0", "LPDDR2", 520, 350),
                "pizero": ("Raspberry Pi Zero 2 W", "RP3A0-AU", "LPDDR2", 340, 310),
            }
            _name, soc, ram, bw_units, bh_units = models[self.model_code]
            bw, bh = bw_units * scale, bh_units * scale
            bx, by = self.center_x - bw / 2, self.center_y - bh / 2

            # Sombra e PCB
            Color(0, .12, .09)
            RoundedRectangle(pos=(bx - 6 * scale, by - 8 * scale), size=(bw + 12 * scale, bh + 12 * scale), radius=[8])
            Color(.075, .55, .31)
            RoundedRectangle(pos=(bx, by), size=(bw, bh), radius=[8])

            # Trilhas decorativas
            Color(.14, .68, .42)
            for i in range(1, 12):
                Line(points=[bx + i * 42 * scale, by + 5 * scale,
                             bx + i * 42 * scale, by + bh - 5 * scale], width=.4)

            # SoC, memoria, portas e GPIO
            soc_x = bx + (112 if self.model_code == "pizero" else 188) * scale
            soc_y = by + (112 if self.model_code == "pizero" else 105) * scale
            soc_size = 104 * scale if self.model_code == "pizero" else 118 * scale
            self.chip(soc_x, soc_y, soc_size, soc_size, soc)
            ram_x = bx + (126 if self.model_code == "pizero" else 202) * scale
            ram_y = by + (64 if self.model_code == "pizero" else 47) * scale
            self.chip(ram_x, ram_y, 82 * scale, 48 * scale, ram)
            self.chip(bx + 55 * scale, by + 58 * scale, 48 * scale, 38 * scale, "PMIC")
            self.chip(bx + 410 * scale, by + 72 * scale, 54 * scale, 54 * scale, "Wi-Fi", radius=27)
            self.chip(bx + 362 * scale, by + 205 * scale, 116 * scale, 48 * scale)

            Color(.78, .62, .12)
            for row in range(2):
                for col in range(20):
                    Ellipse(pos=(bx + (366 + col * 5.3) * scale,
                                 by + (212 + row * 12) * scale),
                            size=(4 * scale, 4 * scale))

            Color(.09, .10, .10)
            RoundedRectangle(pos=(bx + 454 * scale, by + 35 * scale), size=(66 * scale, 86 * scale), radius=[5])
            RoundedRectangle(pos=(bx + 458 * scale, by + 145 * scale), size=(62 * scale, 62 * scale), radius=[5])
            RoundedRectangle(pos=(bx + 458 * scale, by + 218 * scale), size=(62 * scale, 62 * scale), radius=[5])
            Color(.68, .71, .70)
            RoundedRectangle(pos=(bx + 445 * scale, by - 12 * scale), size=(54 * scale, 38 * scale), radius=[8])

            Color(.12, .14, .13)
            RoundedRectangle(pos=(bx + 72 * scale, by + 128 * scale), size=(68 * scale, 116 * scale), radius=[3])
            Color(.08, .09, .09)
            RoundedRectangle(pos=(bx + 78 * scale, by + 140 * scale), size=(54 * scale, 88 * scale), radius=[3])

            # LEDs
            green = (.35, 1, .42, 1) if self.powered else (.12, .22, .14, 1)
            red = (.9, .18, .18, 1) if self.powered and (not self.blinking or self.blink_phase) else (.16, .08, .08, 1)
            Color(*green)
            Ellipse(pos=(bx + 18 * scale, by + 302 * scale), size=(7 * scale, 7 * scale))
            Color(*red)
            Ellipse(pos=(bx + 32 * scale, by + 302 * scale), size=(7 * scale, 7 * scale))

            # Furos de montagem
            Color(.55, .62, .58)
            for px, py in ((18, 18), (480, 18), (18, 310), (480, 310)):
                Ellipse(pos=(bx + px * scale, by + py * scale), size=(22 * scale, 22 * scale))
            Color(.03, .03, .03)
            for px, py in ((23, 23), (485, 23), (23, 315), (485, 315)):
                Ellipse(pos=(bx + px * scale, by + py * scale), size=(12 * scale, 12 * scale))
            PopMatrix()


class RaspberryApp(App):
    title = "Simulacao Raspberry Pi"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=12, spacing=8)
        title = Label(text="[b]Raspberry Pi 5[/b]", markup=True, size_hint=(1, .08), font_size="22sp")
        root.add_widget(title)

        model_bar = Spinner(
            text="Raspberry Pi 5",
            values=("Raspberry Pi 5", "Raspberry Pi 4 Model B",
                    "Raspberry Pi 3 Model B+", "Raspberry Pi Zero 2 W"),
            size_hint=(1, .08),
        )
        root.add_widget(model_bar)

        board = RaspberryBoard(size_hint=(1, .64))
        root.add_widget(board)

        model_codes = {
            "Raspberry Pi 5": "pi5",
            "Raspberry Pi 4 Model B": "pi4",
            "Raspberry Pi 3 Model B+": "pi3",
            "Raspberry Pi Zero 2 W": "pizero",
        }

        def on_model(_spinner, text):
            board.set_model(model_codes[text])
            title.text = f"[b]{text}[/b]"

        model_bar.bind(text=on_model)

        buttons = BoxLayout(size_hint=(1, .18), spacing=8)
        power = Button(text="DESLIGAR", background_color=(.68, .82, .24, 1))
        led = Button(text="LED PISCANDO", background_color=(.12, .3, .24, 1))
        reset = Button(text="RESETAR", background_color=(.14, .18, .24, 1))

        def on_power(_button):
            powered = board.toggle_power()
            _button.text = "LIGAR" if not powered else "DESLIGAR"

        def on_led(_button):
            blinking = board.toggle_led()
            _button.text = "LED PISCANDO" if blinking else "LED PARADO"

        power.bind(on_release=on_power)
        led.bind(on_release=on_led)
        reset.bind(on_release=lambda _button: board.reset_view())
        buttons.add_widget(power)
        buttons.add_widget(led)
        buttons.add_widget(reset)
        root.add_widget(buttons)
        return root


if __name__ == "__main__":
    RaspberryApp().run()
