import tkinter as tk

class CarDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Car Dashboard')
        self.geometry('300x200')

        self.speed_label = tk.Label(self, text='Speed')
        self.speed_label.pack()

        self.speed_entry = tk.Entry(self)
        self.speed_entry.pack()

        self.fuel_label = tk.Label(self, text='Fuel Level')
        self.fuel_label.pack()

        self.fuel_entry = tk.Entry(self)
        self.fuel_entry.pack()

        self.update_button = tk.Button(self, text='Update', command=self.update_dashboard)
        self.update_button.pack(pady=10)

    def update_dashboard(self):
        speed = self.speed_entry.get()
        fuel = self.fuel_entry.get()

        self.speed_label.config(text=f'Speed: {speed}')
        self.fuel_label.config(text=f'Fuel Level: {fuel}')

if __name__ == '__main__':
    dashboard = CarDashboard()
    dashboard.mainloop()