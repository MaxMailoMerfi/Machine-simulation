import pygame
import math
import time
import random
from speed_graph import GraphSpeed

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
PAUSE_TIME = 2

ACCELERATION = 0.5
FRICTION = 0.05
MAX_SPEED = 10 
TURN_SPEED = 2

class Movement:
    def __init__(self, square_speed=2, car_image_path="car.png") -> None:
        self.square_speed = square_speed
        self.current_speed = 0
        self.speed_log = []

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Извилистая дорога с точками А и Б")

        self.turn_points = []
        self.target_index = 0

        self.car_image = pygame.image.load(car_image_path)
        self.car_image = pygame.transform.scale(self.car_image, (40, 40))

        self.font = pygame.font.SysFont("Arial", 16, bold=True)

        self.create_road()

        self.square_x, self.square_y = self.turn_points[0]
        self.current_angle = 0
        self.target_angle = 0
        self.draw_initial_state()

        time.sleep(PAUSE_TIME)
        self.main_loop()

    def create_road(self):
        x, y = 50, HEIGHT // 2
        angle = 0

        while x < WIDTH - 150:
            angle += random.randint(-45, 45) 
            segment_length = random.randint(50, 120) 

            x2 = x + segment_length * math.cos(math.radians(angle))
            y2 = y + segment_length * math.sin(math.radians(angle))

            # Проверка, чтобы точки дороги оставались в пределах экрана
            if 50 < y2 < HEIGHT - 50 and 50 < x2 < WIDTH - 50:
                self.turn_points.append((x2, y2))
                x, y = x2, y2

        if x < WIDTH - 50:
            self.turn_points.append((WIDTH - 50, y))

    def draw_road(self):
        for i in range(len(self.turn_points) - 1):
            pygame.draw.line(self.screen, BLACK, self.turn_points[i], self.turn_points[i + 1], 3)

    def draw_square(self):
        angle_diff = (self.target_angle - self.current_angle + 180) % 360 - 180  
        if abs(angle_diff) > TURN_SPEED:
            self.current_angle += TURN_SPEED if angle_diff > 0 else -TURN_SPEED
        else:
            self.current_angle = self.target_angle  

        rotated_car = pygame.transform.rotate(self.car_image, -self.current_angle)
        car_rect = rotated_car.get_rect(center=(self.square_x, self.square_y))
        self.screen.blit(rotated_car, car_rect)

    def draw_speed(self):
        speed_text = self.font.render(f"Speed: {self.current_speed:.2f}", True, BLACK)
        self.screen.blit(speed_text, (10, 10))  

    def draw_markers(self):
        start_text = self.font.render("А", True, BLACK)
        self.screen.blit(start_text, (self.turn_points[0][0] - 15, self.turn_points[0][1] - 20))
        
        finish_text = self.font.render("Б", True, BLACK)
        self.screen.blit(finish_text, (self.turn_points[-1][0] + 10, self.turn_points[-1][1] - 20))

    def move_square(self):
        if self.target_index < len(self.turn_points):
            target_x, target_y = self.turn_points[self.target_index]
        
            direction = math.atan2(target_y - self.square_y, target_x - self.square_x)
            self.target_angle = math.degrees(direction)  

            angle_diff = abs(self.target_angle - self.current_angle) % 360
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
            
            turn_slowdown_factor = (angle_diff / 180) * 0.8  

            if angle_diff > 10:
                self.current_speed *= (1 - turn_slowdown_factor)

            if self.current_speed < MAX_SPEED:
                self.current_speed += ACCELERATION

            if self.current_speed > 0:
                self.current_speed -= FRICTION
                self.current_speed = max(self.current_speed, 0)

            self.speed_log.append(self.current_speed)

            self.square_x = max(0, min(WIDTH, self.square_x + self.current_speed * math.cos(direction)))
            self.square_y = max(0, min(HEIGHT, self.square_y + self.current_speed * math.sin(direction)))

            if math.hypot(target_x - self.square_x, target_y - self.square_y) < 5:
                self.target_index += 1

    def draw_initial_state(self):
        self.screen.fill(WHITE)
        self.draw_road()
        self.draw_square()
        self.draw_markers()
        self.draw_speed()
        pygame.display.flip()

    def get_speed_log(self):
        return self.speed_log

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
            self.draw_speed()

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

        graph = GraphSpeed()
        graph.draw_graph(self.get_speed_log())