import pygame
import math
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
PAUSE_TIME = 2

ACCELERATION = 0.1
FRICTION = 0.01 
MAX_SPEED = 5 
TURN_SPEED = 2  # Скорость поворота машинки

class Movement:
    def __init__(self, square_speed=2, car_image_path="car.png") -> None:
        self.square_speed = square_speed
        self.current_speed = 0  # Текущая скорость машинки

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Извилистая дорога с точками А и Б")

        self.segment_length = 100
        self.angle = 45

        self.turn_points = []
        self.target_index = 0

        self.car_image = pygame.image.load(car_image_path)
        self.car_image = pygame.transform.scale(self.car_image, (40, 40))

        self.font = pygame.font.SysFont("Arial", 16, bold=True)

        self.create_road()

        self.square_x, self.square_y = self.turn_points[0]
        self.current_angle = 0  # Текущий угол машинки (направление движения)
        self.target_angle = 0  # Угол к следующей точке
        self.draw_initial_state()

        time.sleep(PAUSE_TIME)
        self.main_loop()

    def create_road(self):
        x, y = 50, HEIGHT // 2
        angle = 0

        while x < WIDTH - 150:
            x2 = x + self.segment_length * math.cos(math.radians(angle))
            y2 = y + self.segment_length * math.sin(math.radians(angle))

            if 50 < y2 < HEIGHT - 50:
                self.turn_points.append((x2, y2))
                x, y = x2, y2

            angle += self.angle
            x2 = x + 75 * math.cos(math.radians(angle))
            y2 = y + 75 * math.sin(math.radians(angle))

            if 50 < y2 < HEIGHT - 50:
                self.turn_points.append((x2, y2))
                x, y = x2, y2

            angle -= self.angle * 2
            x2 = x + 75 * math.cos(math.radians(angle))
            y2 = y + 75 * math.sin(math.radians(angle))

            if 50 < y2 < HEIGHT - 50:
                self.turn_points.append((x2, y2))
                x, y = x2, y2

            angle += self.angle

        if x < WIDTH - 50:
            self.turn_points.append((WIDTH - 50, y))

    def draw_road(self):
        for i in range(len(self.turn_points) - 1):
            pygame.draw.line(self.screen, BLACK, self.turn_points[i], self.turn_points[i + 1], 3)

    def draw_square(self):
        # Плавное вращение машинки по направлению к следующей точке
        angle_diff = (self.target_angle - self.current_angle + 180) % 360 - 180  # Найти разницу углов
        if abs(angle_diff) > TURN_SPEED:
            self.current_angle += TURN_SPEED if angle_diff > 0 else -TURN_SPEED
        else:
            self.current_angle = self.target_angle  # Если разница маленькая, установить угол

        # Поворот изображения машинки в соответствии с текущим углом
        rotated_car = pygame.transform.rotate(self.car_image, -self.current_angle)
        car_rect = rotated_car.get_rect(center=(self.square_x, self.square_y))
        self.screen.blit(rotated_car, car_rect)

    def draw_markers(self):
        start_text = self.font.render("А", True, BLACK)
        self.screen.blit(start_text, (self.turn_points[0][0] - 15, self.turn_points[0][1] - 20))
        
        finish_text = self.font.render("Б", True, BLACK)
        self.screen.blit(finish_text, (self.turn_points[-1][0] + 10, self.turn_points[-1][1] - 20))

    def move_square(self):
        if self.target_index < len(self.turn_points):
            target_x, target_y = self.turn_points[self.target_index]
            
            # Рассчитываем направление на следующую точку (угол в радианах)
            direction = math.atan2(target_y - self.square_y, target_x - self.square_x)
            self.target_angle = math.degrees(direction)  # Преобразуем угол в градусы для поворота

            # Если текущая скорость меньше максимальной, увеличиваем её
            if self.current_speed < MAX_SPEED:
                self.current_speed += ACCELERATION

            # Применяем трение для снижения скорости
            self.current_speed -= FRICTION
            self.current_speed = max(self.current_speed, 0)

            # Двигаем машинку в направлении к следующей точке
            self.square_x += self.current_speed * math.cos(direction)
            self.square_y += self.current_speed * math.sin(direction)

            # Проверяем, достигла ли машинка цели (расстояние до цели)
            if math.hypot(target_x - self.square_x, target_y - self.square_y) < 5:
                self.target_index += 1

    def draw_initial_state(self):
        self.screen.fill(WHITE)
        self.draw_road()
        self.draw_square()
        self.draw_markers()
        pygame.display.flip()

    def main_loop(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(WHITE)

            self.draw_road()
            self.draw_square()
            self.draw_markers()
            self.move_square()

            pygame.display.flip()
            clock.tick(FPS)
        
        pygame.quit()
