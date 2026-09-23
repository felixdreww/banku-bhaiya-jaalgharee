import tkinter as tk
from datetime import datetime
import math
import time

# ============================================================
#              BANKU BHAIYA JAAL GHAREE
# ============================================================

class SpiderClock:

    def __init__(self, root):
        self.root = root
        self.root.title("BANKU BHAIYA JAAL GHAREE")
        self.root.geometry("1200x800")
        self.root.minsize(850, 650)
        self.root.configure(bg="#000000")

        # Settings
        self.fullscreen = False
        self.dark = True
        self.hour_24 = False
        self.rotation = 0

        # Stopwatch
        self.stopwatch_running = False
        self.stopwatch_start = 0
        self.stopwatch_elapsed = 0

        # Alarm
        self.alarm_enabled = False
        self.alarm_hour = 0
        self.alarm_minute = 0

        # Canvas
        self.canvas = tk.Canvas(root, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Control Bar
        self.controls = tk.Frame(root, bg="#080808", height=58)
        self.controls.place(relx=0, rely=1, relwidth=1, anchor="sw")

        self.make_buttons()

        # Keyboard shortcuts
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.bind("t", self.change_theme)
        self.root.bind("T", self.change_theme)
        self.root.bind("h", self.toggle_format)
        self.root.bind("H", self.toggle_format)
        self.root.bind("s", self.stopwatch_toggle)
        self.root.bind("S", self.stopwatch_toggle)
        self.root.bind("r", self.stopwatch_reset)
        self.root.bind("R", self.stopwatch_reset)

        self.update()

    def make_buttons(self):
        style = {
            "font": ("Arial", 10, "bold"),
            "bg": "#151515",
            "fg": "#E88920",
            "activebackground": "#321707",
            "activeforeground": "#FFB04A",
            "bd": 0,
            "padx": 13,
            "pady": 7,
            "cursor": "hand2"
        }

        tk.Button(self.controls, text="⛶ Fullscreen", command=self.toggle_fullscreen, **style).pack(side="left", padx=7, pady=9)
        tk.Button(self.controls, text="◐ Theme", command=self.change_theme, **style).pack(side="left", padx=4)
        tk.Button(self.controls, text="12H / 24H", command=self.toggle_format, **style).pack(side="left", padx=4)
        tk.Button(self.controls, text="▶ Stopwatch", command=self.stopwatch_toggle, **style).pack(side="left", padx=4)
        tk.Button(self.controls, text="↻ Reset", command=self.stopwatch_reset, **style).pack(side="left", padx=4)
        tk.Button(self.controls, text="🔔 Alarm", command=self.alarm_window, **style).pack(side="left", padx=4)

    def polar(self, cx, cy, radius, angle):
        rad = math.radians(angle)
        return (cx + radius * math.sin(rad), cy - radius * math.cos(rad))

    def glow_ring(self, radius):
        colors = ["#080300", "#100501", "#180802", "#220B03", "#2C0E03", "#351204"]
        for i, color in enumerate(colors):
            r = radius + (len(colors) - i) * 8
            self.canvas.create_oval(self.cx-r, self.cy-r, self.cx+r, self.cy+r, outline=color, width=3)

    def gear(self, x, y, radius, teeth, rotation):
        points = []
        for i in range(teeth * 2):
            angle = rotation + i * 360 / (teeth * 2)
            r = radius if i % 2 == 0 else radius * 0.78
            px, py = self.polar(x, y, r, angle)
            points.extend([px, py])

        self.canvas.create_polygon(points, fill="", outline="#351303", width=7)
        self.canvas.create_polygon(points, fill="", outline="#6F330D", width=2)
        self.canvas.create_oval(x-radius*.72, y-radius*.72, x+radius*.72, y+radius*.72, outline="#492008", width=2)
        self.canvas.create_oval(x-radius*.42, y-radius*.42, x+radius*.42, y+radius*.42, outline="#71330D", width=2)

        for i in range(8):
            angle = rotation + i * 45
            x1, y1 = self.polar(x, y, radius*.25, angle)
            x2, y2 = self.polar(x, y, radius*.66, angle)
            self.canvas.create_line(x1, y1, x2, y2, fill="#542408", width=3)

        self.canvas.create_oval(x-8, y-8, x+8, y+8, fill="#D96B10", outline="#FFAA3A", width=2)

    def web(self, x, y, radius):
        for angle in range(0, 360, 30):
            x2, y2 = self.polar(x, y, radius, angle)
            self.canvas.create_line(x, y, x2, y2, fill="#291206", width=1)

        for r in range(35, radius, 20):
            points = []
            for angle in range(0, 361, 8):
                px, py = self.polar(x, y, r, angle)
                points.extend([px, py])
            self.canvas.create_line(points, fill="#321708", width=1, smooth=True)

    def spider(self, x, y):
        for r, color in [(80, "#0D0400"), (70, "#160700"), (60, "#210A01"), (50, "#2D0D02")]:
            self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, width=4)

        glow = "#773307"
        orange = "#F58A18"
        left = [[(-14,-20), (-48,-42), (-92,-34)], [(-18,-10), (-58,-12), (-105,8)], [(-19,2), (-62,28), (-100,52)], [(-13,14), (-40,50), (-63,80)]]
        right = [[(14,-20), (48,-42), (92,-34)], [(18,-10), (58,-12), (105,8)], [(19,2), (62,28), (100,52)], [(13,14), (40,50), (63,80)]]

        for leg in left + right:
            points = []
            for px, py in leg:
                points.extend([x + px, y + py])
            self.canvas.create_line(points, fill=glow, width=8, smooth=True)
            self.canvas.create_line(points, fill=orange, width=3, smooth=True)

        self.canvas.create_oval(x-22, y-36, x+22, y+30, fill="#F48616", outline="#FFB342", width=2)
        self.canvas.create_oval(x-18, y-50, x+18, y-20, fill="#FF9720", outline="#FFC765", width=2)
        self.canvas.create_oval(x-9, y-42, x-3, y-36, fill="#100400")
        self.canvas.create_oval(x+3, y-42, x+9, y-36, fill="#100400")
        self.canvas.create_line(x, y-16, x, y+22, fill="#743007", width=2)

    def numbers(self, radius):
        for number in range(1, 13):
            angle = number * 30
            x, y = self.polar(self.cx, self.cy, radius, angle)
            self.canvas.create_text(x+2, y+2, text=str(number), fill="#1D0B03", font=("Georgia", 27, "bold"))
            self.canvas.create_text(x, y, text=str(number), fill="#71401B", font=("Georgia", 27, "bold"))

    def hands(self):
        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second

        hour_angle = hour * 30 + minute * .5
        minute_angle = minute * 6 + second * .1
        second_angle = second * 6

        hx, hy = self.polar(self.cx, self.cy, 110, hour_angle)
        self.canvas.create_line(self.cx, self.cy, hx, hy, fill="#E16E10", width=9, capstyle=tk.ROUND)

        mx, my = self.polar(self.cx, self.cy, 158, minute_angle)
        self.canvas.create_line(self.cx, self.cy, mx, my, fill="#FF9B25", width=5, capstyle=tk.ROUND)

        sx, sy = self.polar(self.cx, self.cy, 205, second_angle)
        self.canvas.create_line(self.cx, self.cy, sx, sy, fill="#FFB33E", width=2, capstyle=tk.ROUND)

        self.canvas.create_oval(self.cx-10, self.cy-10, self.cx+10, self.cy+10, fill="#FF8A17", outline="#FFD27A", width=2)

    def digital_clock(self):
        now = datetime.now()
        current = now.strftime("%H:%M:%S") if self.hour_24 else now.strftime("%I:%M:%S %p")
        date = now.strftime("%A  •  %d %B %Y")
        h = self.canvas.winfo_height()

        self.canvas.create_text(self.cx+2, h-116, text=current, fill="#261004", font=("Consolas", 34, "bold"))
        self.canvas.create_text(self.cx, h-118, text=current, fill="#B55A12", font=("Consolas", 34, "bold"))
        self.canvas.create_text(self.cx, h-76, text=date, fill="#75421B", font=("Arial", 13))

    def stopwatch_time(self):
        elapsed = (time.time() - self.stopwatch_start + self.stopwatch_elapsed) if self.stopwatch_running else self.stopwatch_elapsed
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        hundredths = int((elapsed % 1) * 100)
        return f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"

    def stopwatch_toggle(self, event=None):
        if self.stopwatch_running:
            self.stopwatch_elapsed += (time.time() - self.stopwatch_start)
            self.stopwatch_running = False
        else:
            self.stopwatch_start = time.time()
            self.stopwatch_running = True

    def stopwatch_reset(self, event=None):
        self.stopwatch_running = False
        self.stopwatch_start = 0
        self.stopwatch_elapsed = 0

    def draw_stopwatch(self):
        text = "STOPWATCH  " + self.stopwatch_time()
        self.canvas.create_text(25, 25, anchor="nw", text=text, fill="#8B4815", font=("Consolas", 12, "bold"))

    def alarm_window(self):
        win = tk.Toplevel(self.root)
        win.title("Alarm")
        win.geometry("330x250")
        win.configure(bg="#080808")
        win.resizable(False, False)

        tk.Label(win, text="🔔  SET ALARM", bg="#080808", fg="#F08A20", font=("Arial", 18, "bold")).pack(pady=20)
        frame = tk.Frame(win, bg="#080808")
        frame.pack()

        hour = tk.StringVar(value=datetime.now().strftime("%H"))
        minute = tk.StringVar(value=datetime.now().strftime("%M"))
        entry_style = {"width": 5, "bg": "#151515", "fg": "#FF9A25", "insertbackground": "white", "font": ("Consolas", 20), "justify": "center"}

        tk.Entry(frame, textvariable=hour, **entry_style).pack(side="left", padx=5)
        tk.Label(frame, text=":", bg="#080808", fg="white", font=("Arial", 20, "bold")).pack(side="left")
        tk.Entry(frame, textvariable=minute, **entry_style).pack(side="left", padx=5)

        def save_alarm():
            try:
                h = int(hour.get())
                m = int(minute.get())
                if 0 <= h <= 23 and 0 <= m <= 59:
                    self.alarm_hour = h
                    self.alarm_minute = m
                    self.alarm_enabled = True
                    win.destroy()
            except ValueError:
                pass

        tk.Button(win, text="SET ALARM", command=save_alarm, bg="#301505", fg="#FFA33A", activebackground="#512308", activeforeground="white", bd=0, padx=30, pady=10, font=("Arial", 10, "bold"), cursor="hand2").pack(pady=25)

    def check_alarm(self):
        if not self.alarm_enabled:
            return
        now = datetime.now()
        if now.hour == self.alarm_hour and now.minute == self.alarm_minute and now.second == 0:
            self.alarm_enabled = False
            self.root.bell()
            alarm = tk.Toplevel(self.root)
            alarm.title("ALARM")
            alarm.geometry("360x200")
            alarm.configure(bg="#080808")
            alarm.resizable(False, False)
            tk.Label(alarm, text="⏰", bg="#080808", fg="#FF9B25", font=("Arial", 40)).pack(pady=10)
            tk.Label(alarm, text="ALARM TIME!", bg="#080808", fg="#FF9B25", font=("Arial", 21, "bold")).pack()
            tk.Button(alarm, text="STOP", command=alarm.destroy, bg="#321506", fg="#FFAA42", bd=0, padx=35, pady=8, font=("Arial", 10, "bold")).pack(pady=15)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    def change_theme(self, event=None):
        self.dark = not self.dark
        if self.dark:
            self.canvas.configure(bg="#000000")
            self.controls.configure(bg="#080808")
        else:
            self.canvas.configure(bg="#120A05")
            self.controls.configure(bg="#1A0E07")

    def toggle_format(self, event=None):
        self.hour_24 = not self.hour_24

    def draw(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.cx = width // 2
        self.cy = height // 2 - 25

        self.glow_ring(280)
        self.canvas.create_oval(self.cx-290, self.cy-290, self.cx+290, self.cy+290, outline="#190802", width=3)
        self.canvas.create_oval(self.cx-268, self.cy-268, self.cx+268, self.cy+268, outline="#2A0F03", width=2)

        self.gear(self.cx-125, self.cy-115, 78, 18, self.rotation)
        self.gear(self.cx+125, self.cy-115, 72, 18, -self.rotation)
        self.gear(self.cx-110, self.cy+125, 52, 15, -self.rotation * 1.4)
        self.gear(self.cx+85, self.cy+130, 68, 17, self.rotation * 1.2)

        self.web(self.cx, self.cy, 215)
        self.numbers(240)
        self.hands()
        self.spider(self.cx, self.cy)
        self.digital_clock()
        self.draw_stopwatch()

        if self.alarm_enabled:
            alarm_info = f"ALARM  {self.alarm_hour:02d}:{self.alarm_minute:02d}"
            self.canvas.create_text(width - 25, 25, anchor="ne", text=alarm_info, fill="#A85212", font=("Consolas", 12, "bold"))

        # Screen par clock ka naya title
        self.canvas.create_text(self.cx, 32, text="BANKU BHAIYA JAAL GHAREE", fill="#E88920", font=("Arial", 13, "bold"))

    def update(self):
        self.rotation += 0.7
        self.check_alarm()
        self.draw()
        self.root.after(40, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    app = SpiderClock(root)
    root.mainloop()
    