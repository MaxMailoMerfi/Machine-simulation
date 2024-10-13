import matplotlib.pyplot as plt

class GraphSpeed():
    def __init__(self) -> None:
        pass
    
    def draw_graph(self, speed_list):
        plt.plot(speed_list, label='Speed over Time')
        plt.title('График изменения скорости')
        plt.xlabel('Время (в кадрах)')
        plt.ylabel('Скорость')
        plt.legend()
        plt.grid(True)
        plt.show()
