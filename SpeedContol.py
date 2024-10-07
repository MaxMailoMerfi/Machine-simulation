import tkinter as tk
from draw import Movement  

class SpeedControlWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Настройки скорости")

        self.label = tk.Label(self.root, text="Скорость движения машинки:")
        self.label.pack()

        self.speed_var = tk.DoubleVar()
        self.speed_var.set(2)

        self.speed_scale = tk.Scale(
            self.root, from_=0.1, to=10.0, resolution=0.1, orient='horizontal', variable=self.speed_var
        )
        self.speed_scale.pack()

        self.button = tk.Button(self.root, text="Запуск", command=self.start_animation)
        self.button.pack()

    def start_animation(self):
        speed = self.speed_var.get()
        self.root.destroy()
        start = Movement(square_speed=speed, car_image_path="car.png")

    def run(self):
        self.root.mainloop()