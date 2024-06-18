from tkinter import *
import random

# === Settings
PREFER_GAME_FIELD_WIDTH = 1200
PREFER_GAME_FIELD_HEIGHT = 600
START_SPEED = [250, 230, 210, 190, 170]
STEPS_FOR_ONE_SQUARE = 8
THINGS_SIZE = 30    # need to be equals to BRICK_SPACE + BRICK_WIDTH
EYE_SIZE = THINGS_SIZE / 5
TONGUE_SIZE = THINGS_SIZE / 5
ONE_STEP = THINGS_SIZE / STEPS_FOR_ONE_SQUARE
START_BODY_PARTS = 5

# === Colors
BACKGROUND_COLOR = "#181513"
BORDER_COLOR = "#c10020"
WALL_COLOR = "#3366FF"
FOOD_COLOR = "#f3da0b"
POISON_COLOR = ["#ff2400",
                "#EA2302",
                "#D52103",
                "#C02005",
                "#AB1F07",
                "#961D09",
                "#811C0A",
                "#6C1A0C",
                "#57190E",
                "#421810"]
SNAKE_COLOR = "#00db6a"
SNAKE_HEAD_COLOR = "#00a550"
SNAKE_CRASH_COLOR = "#D229A9"
SNAKE_EYE_COLOR = "#F5F5F5"
SNAKE_PUPIL_COLOR = "#B32428"
SNAKE_TONGUE_COLOR = "#ff2400"

# === Briks settings
BRICK_SPACE = 3
BRICK_WIDTH = 27
BRICK_HEIGHT = 12
BRICK_COLOR = "#8A2800"
BRICK_EDGE_COLOR = "#C76D4C"

NUM_OF_SQUARES_X = PREFER_GAME_FIELD_WIDTH // THINGS_SIZE
GAME_FIELD_WIDTH = NUM_OF_SQUARES_X * THINGS_SIZE
NUM_OF_SQUARES_Y = PREFER_GAME_FIELD_HEIGHT // THINGS_SIZE
GAME_FIELD_HEIGHT = NUM_OF_SQUARES_Y * THINGS_SIZE
TLGC = 3 * BRICK_SPACE + 2 * BRICK_HEIGHT - 2   #TOP_LEFT_GAME_CANVAS
GAME_NUM_OF_SQUARES_X = NUM_OF_SQUARES_X - 2
GAME_NUM_OF_SQUARES_Y = NUM_OF_SQUARES_Y - 2

class Game:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.game_speed = START_SPEED[0]
        self.game_status = 'inactive' # inactive/active/pause
        self.title_text_object = 0

        self.canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_FIELD_HEIGHT, width=GAME_FIELD_WIDTH)
        self.canvas.pack()

        self.label = Label(window, text=f'Очки: {self.score} - Уровень {self.level}' , font=('consolas', 30))
        self.label.pack()

        self.draw_outside_wall()

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.poison = Poison(self.canvas)

        self.canvas.bind('<Left>', lambda event: self.snake.change_direction('left'))
        self.canvas.bind('<a>', lambda event: self.snake.change_direction('left'))
        self.canvas.bind('<Down>', lambda event: self.snake.change_direction('down'))
        self.canvas.bind('<s>', lambda event: self.snake.change_direction('down'))
        self.canvas.bind('<Up>', lambda event: self.snake.change_direction('up'))
        self.canvas.bind('<w>', lambda event: self.snake.change_direction('up'))
        self.canvas.bind('<Right>', lambda event: self.snake.change_direction('right'))
        self.canvas.bind('<d>', lambda event: self.snake.change_direction('right'))
        self.canvas.bind('<space>', lambda event: self.pause())
        self.canvas.focus_set()
        self.canvas.update() 

        self.prepare_game()

    def prepare_game(self):
        self.score = 0
        self.level = 1

        self.start()

    def start(self):
        self.game_status = 'pause' # inactive/active/pause
        self.game_speed = START_SPEED[self.level - 1]

        self.snake.reset()
        self.food.reset(self.snake)
        self.poison.reset(self.snake, self.food)
        self.poison.hide()
        print(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2)
        self.title_text_object = self.canvas.create_text(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, \
                                                             font=('consolas',40), text=f'Уровень {self.level} - готов? (пробел)', fill='red', tag='title_text')
        self.step()

    def step(self):
        self.snake.update_squares_directions()
        if not self.snake.check_collisions():
            if self.game_status == 'active':
                self.snake.move_squares()

                if self.snake.check_eat(self.food):
                    self.food.reset(self.snake)
                    # if random.randint(0, 9) == 0:
                    if True:
                        self.poison.reset(self.snake, self.food)
                        window.after(int(1.5 * (START_SPEED[0] / STEPS_FOR_ONE_SQUARE)), self.poison.start_blinking)
                    else:
                        self.poison.hide()
                    self.snake.grow_up(1)
                if self.snake.check_eat(self.poison):
                    self.game_over('Отравился')
                window.after(int(self.game_speed / STEPS_FOR_ONE_SQUARE), self.step)
        else:
            self.game_over('Врезался')

    def pause(self):
        if self.game_status == 'pause':
            self.game_status = 'active'
            self.canvas.delete('title_text')
            self.step()
        elif self.game_status == 'active':
            self.game_status = 'pause'
            self.canvas.delete('title_text')
            self.title_text_object = self.canvas.create_text(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, \
                                                             font=('consolas',40), text='Пауза', fill='red', tag='title_text')
        elif self.game_status == 'inactive':
            self.game_status = 'active'
            self.canvas.delete('title_text')
            self.prepare_game()

    def game_over(self, reason):
        self.game_status = 'inactive'
        self.canvas.delete('title_text')
        self.title_text_object = self.canvas.create_text(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, \
                                                         font=('consolas',40), text=reason + ' - конец игры', fill='red', tag='title_text')
        self.canvas.itemconfigure(self.snake.body_parts[0],fill=SNAKE_CRASH_COLOR)

    def score_up(self):
        pass

    def level_up(self):
        pass

    def label_update(self):
        pass




    def draw_outside_wall(self):
        # top
        for j in range(0, BRICK_SPACE + BRICK_HEIGHT + 1, BRICK_SPACE + BRICK_HEIGHT):
            for i in range(NUM_OF_SQUARES_X):
                x = j + BRICK_SPACE + i * (BRICK_SPACE + BRICK_WIDTH)
                y = j + BRICK_SPACE

                if i != NUM_OF_SQUARES_X - 1 or j < 1:
                    self.canvas.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_HEIGHT, fill=BRICK_COLOR, width=0, tag='outside_wall')
                    self.canvas.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_SPACE, fill=BRICK_EDGE_COLOR, width=0, tag='outside_wall')

        # left
        for j in range(0, BRICK_SPACE + BRICK_HEIGHT + 1, BRICK_SPACE + BRICK_HEIGHT):
            for i in range(NUM_OF_SQUARES_Y - 1):
                x = j + BRICK_SPACE
                y = j + 2 * BRICK_SPACE + BRICK_HEIGHT + i * (BRICK_SPACE + BRICK_WIDTH)

                if i != NUM_OF_SQUARES_Y - 2 or j < 1:
                    self.canvas.create_rectangle(x, y, x + BRICK_HEIGHT, y + BRICK_WIDTH, fill=BRICK_COLOR, width=0, tag='outside_wall')
                    self.canvas.create_rectangle(x, y, x + BRICK_SPACE, y + BRICK_WIDTH, fill=BRICK_EDGE_COLOR, width=0, tag='outside_wall')

        # bottom
        for j in range(0, BRICK_SPACE + BRICK_HEIGHT + 1, BRICK_SPACE + BRICK_HEIGHT):
            for i in range(NUM_OF_SQUARES_X):
                x = j + BRICK_SPACE + i * (BRICK_SPACE + BRICK_WIDTH)
                y = - j + 2 * BRICK_SPACE + BRICK_HEIGHT + (NUM_OF_SQUARES_Y - 1) * (BRICK_SPACE + BRICK_WIDTH)

                if i != NUM_OF_SQUARES_X - 1 or j < 1:
                    self.canvas.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_HEIGHT, fill=BRICK_COLOR, width=0, tag='outside_wall')
                    self.canvas.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_SPACE, fill=BRICK_EDGE_COLOR, width=0, tag='outside_wall')

        # right
        for j in range(0, BRICK_SPACE + BRICK_HEIGHT + 1, BRICK_SPACE + BRICK_HEIGHT):
            for i in range(NUM_OF_SQUARES_Y - 1):
                x = - j + NUM_OF_SQUARES_X * (BRICK_SPACE + BRICK_WIDTH) - BRICK_HEIGHT
                y = j + 2 * BRICK_SPACE + BRICK_HEIGHT + i * (BRICK_SPACE + BRICK_WIDTH)

                if i != NUM_OF_SQUARES_Y - 2 or j < 1:
                    self.canvas.create_rectangle(x, y, x + BRICK_HEIGHT, y + BRICK_WIDTH, fill=BRICK_COLOR, width=0, tag='outside_wall')
                    self.canvas.create_rectangle(x, y, x + BRICK_SPACE, y + BRICK_WIDTH, fill=BRICK_EDGE_COLOR, width=0, tag='outside_wall')

        # holes
        for i in range(GAME_NUM_OF_SQUARES_X):
            for j in range(GAME_NUM_OF_SQUARES_Y):
                # self.canvas.create_rectangle(TLGC + i * THINGS_SIZE, TLGC + j * THINGS_SIZE, \
                #                       TLGC + (i + 1) * THINGS_SIZE, TLGC + (j + 1) * THINGS_SIZE, fill=SNAKE_COLOR)
                if j == 0 and i == int(GAME_NUM_OF_SQUARES_X / 3):
                    self.canvas.create_rectangle(TLGC + i * THINGS_SIZE, TLGC + (j - 1) * THINGS_SIZE, \
                                            TLGC + (i + 1) * THINGS_SIZE, TLGC + j * THINGS_SIZE, \
                                            fill=BACKGROUND_COLOR, width=0, tag='outside_wall')
                if j == GAME_NUM_OF_SQUARES_Y - 1 and i == int(GAME_NUM_OF_SQUARES_X / 3 * 2):
                    self.canvas.create_rectangle(TLGC + i * THINGS_SIZE, TLGC + (j + 1) * THINGS_SIZE, \
                                            TLGC + (i + 1) * THINGS_SIZE, TLGC + (j + 2) * THINGS_SIZE, \
                                            fill=BACKGROUND_COLOR, width=0, tag='outside_wall')
                if i == 0 and j == int(GAME_NUM_OF_SQUARES_Y / 3 * 2):
                    self.canvas.create_rectangle(TLGC + (i - 1) * THINGS_SIZE, TLGC + j * THINGS_SIZE, \
                                            TLGC + i * THINGS_SIZE, TLGC + (j + 1) * THINGS_SIZE, \
                                            fill=BACKGROUND_COLOR, width=0, tag='outside_wall')
                if i == GAME_NUM_OF_SQUARES_X - 1 and j == int(GAME_NUM_OF_SQUARES_Y / 3):
                    self.canvas.create_rectangle(TLGC + (i + 1) * THINGS_SIZE, TLGC + j * THINGS_SIZE, \
                                            TLGC + (i + 2) * THINGS_SIZE, TLGC + (j + 1) * THINGS_SIZE, \
                                            fill=BACKGROUND_COLOR, width=0, tag='outside_wall')


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_parts = []
        self.waiting_parts = []
        self.body_parts_coords = []
        self.waiting_parts_coords = []
        self.body_parts_directions = []
        self.head_parts = []

    def reset(self):
        self.canvas.delete('snake')
        self.canvas.delete('head_parts')

        self.direction = 'down'
        self.body_parts.clear()
        self.waiting_parts.clear()
        self.body_parts_coords.clear()
        self.waiting_parts_coords.clear()
        self.body_parts_directions.clear()
        self.head_parts.clear()

        for i in range(START_BODY_PARTS - 1, -1, -1):
            self.body_parts_directions.append(self.direction)
            self.body_parts_coords.append([0, i * THINGS_SIZE])
            self.body_parts.append([0])

        for i, coords in enumerate(self.body_parts_coords):
            x, y = coords
            if i == 0:
                self.body_parts[i] = self.canvas.create_rectangle(TLGC + x, TLGC + y, TLGC + x + THINGS_SIZE, TLGC + y + THINGS_SIZE, \
                                                            fill=SNAKE_HEAD_COLOR, tag="snake")
            else:
                self.body_parts[i] = self.canvas.create_rectangle(TLGC + x, TLGC + y, TLGC + x + THINGS_SIZE, TLGC + y + THINGS_SIZE, \
                                                            fill=SNAKE_COLOR, tag="snake")


        self.canvas.tag_lower(self.body_parts[-1])

        for i in range(0, 5):
            self.head_parts.append([0])

        self.redraw_head_parts()

    def change_direction(self, new_direction):
        current_direction = self.body_parts_directions[0]

        #if self.game_status == 'active':
        if new_direction == 'left':
            if current_direction != 'right':
                self.direction = new_direction
        elif new_direction == 'right':
            if current_direction != 'left':
                self.direction = new_direction
        elif new_direction == 'up':
            if current_direction != 'down':
                self.direction = new_direction
        elif new_direction == 'down':
            if current_direction != 'up':
                self.direction = new_direction
        # else:
        #     self.direction = current_direction


    def update_squares_directions(self):
        for i, coords in reversed(list(enumerate(self.body_parts_coords))):
            x, y = coords
            if x % THINGS_SIZE == 0 and y % THINGS_SIZE == 0:
                if i == 0:
                    self.body_parts_directions[i] = self.direction
                else:
                    self.body_parts_directions[i] = self.body_parts_directions[i - 1]

    def check_collisions(self):
        x, y = self.body_parts_coords[0]

        current_direction = self.body_parts_directions[0]
        dx = 0
        dy = 0
        check_self_collision_x = 0
        check_self_collision_y = 0
        if current_direction == 'left':
            dx = - ONE_STEP
            check_self_collision_x = - THINGS_SIZE
        elif current_direction == 'down':
            dy = ONE_STEP
            check_self_collision_y = THINGS_SIZE
        elif current_direction == 'right':
            dx = ONE_STEP
            check_self_collision_x = THINGS_SIZE
        elif current_direction == 'up':
            dy = - ONE_STEP
            check_self_collision_y = - THINGS_SIZE
        check_self_collision_x += x
        check_self_collision_y += y
        x += dx
        y += dy

        if x < 0 and y != int(GAME_NUM_OF_SQUARES_Y / 3 * 2) * THINGS_SIZE:
            return True
        elif x > (GAME_NUM_OF_SQUARES_X - 1) * THINGS_SIZE and y != int(GAME_NUM_OF_SQUARES_Y / 3) * THINGS_SIZE:
            return True
        elif y < 0 and x != int(GAME_NUM_OF_SQUARES_X / 3) * THINGS_SIZE:
            return True
        elif y > (GAME_NUM_OF_SQUARES_Y - 1) * THINGS_SIZE and x != int(GAME_NUM_OF_SQUARES_X / 3 * 2) * THINGS_SIZE:
            return True

        for part_coords in self.body_parts_coords[1:-1]:
            if check_self_collision_x == part_coords[0] and check_self_collision_y == part_coords[1]:
                return True

        return False

    def check_eat(self, object_to_check):
        object_x, object_y = object_to_check.coords
        if self.body_parts_coords[0][0] == object_x and self.body_parts_coords[0][1] == object_y:
            return True
        return False

    def move_squares(self):
        for i, part in enumerate(self.body_parts):
            current_direction = self.body_parts_directions[i]
            dx = 0
            dy = 0
            throughPortal = True
            if current_direction == 'left':
                dx = - ONE_STEP
            elif current_direction == 'down':
                dy = ONE_STEP
            elif current_direction == 'right':
                dx = ONE_STEP
            elif current_direction == 'up':
                dy = - ONE_STEP

            self.body_parts_coords[i][0] += dx
            new_x = self.body_parts_coords[i][0]
            self.body_parts_coords[i][1] += dy
            new_y = self.body_parts_coords[i][1]

            if new_x <= -THINGS_SIZE and new_y == int(GAME_NUM_OF_SQUARES_Y / 3 * 2) * THINGS_SIZE:
                self.canvas.delete(part)
                self.body_parts_coords[i][0] = new_x = (GAME_NUM_OF_SQUARES_X) * THINGS_SIZE
                self.body_parts_coords[i][1] = new_y = int(GAME_NUM_OF_SQUARES_Y / 3) * THINGS_SIZE
            elif new_x >= (GAME_NUM_OF_SQUARES_X) * THINGS_SIZE and new_y == int(GAME_NUM_OF_SQUARES_Y / 3) * THINGS_SIZE:
                self.canvas.delete(part)
                self.body_parts_coords[i][0] = new_x = -THINGS_SIZE
                self.body_parts_coords[i][1] = new_y = int(GAME_NUM_OF_SQUARES_Y / 3 * 2) * THINGS_SIZE
            elif new_y <= -THINGS_SIZE and new_x == int(GAME_NUM_OF_SQUARES_X / 3) * THINGS_SIZE:
                self.canvas.delete(part)
                self.body_parts_coords[i][0] = new_x = int(GAME_NUM_OF_SQUARES_X / 3 * 2) * THINGS_SIZE
                self.body_parts_coords[i][1] = new_y = (GAME_NUM_OF_SQUARES_Y) * THINGS_SIZE
            elif new_y >= (GAME_NUM_OF_SQUARES_Y) * THINGS_SIZE and new_x == int(GAME_NUM_OF_SQUARES_X / 3 * 2) * THINGS_SIZE:
                self.canvas.delete(part)
                self.body_parts_coords[i][0] = new_x = int(GAME_NUM_OF_SQUARES_X / 3) * THINGS_SIZE
                self.body_parts_coords[i][1] = new_y = -THINGS_SIZE
            else:
                throughPortal = False

            if throughPortal:
                self.body_parts[i] = self.canvas.create_rectangle(TLGC + new_x, TLGC + new_y, TLGC + new_x + THINGS_SIZE, TLGC + new_y + THINGS_SIZE, \
                                                        fill=SNAKE_COLOR, tag="snake")
            else:
                self.canvas.move(part, dx, dy)

        self.redraw_head_parts()

        x, y = self.body_parts_coords[0]
        if x % THINGS_SIZE == 0 and y % THINGS_SIZE == 0:
            if len(self.waiting_parts) > 0:
                self.body_parts_directions.append(self.body_parts_directions[-1])
                self.body_parts.append(self.waiting_parts.pop(0))
                self.body_parts_coords.append(self.waiting_parts_coords.pop(0))

    def redraw_head_parts(self):
        current_direction = self.body_parts_directions[0]
        x1, y1, x2, y2 = self.canvas.coords(self.body_parts[0])
        x = int((x1 + x2) / 2)
        y = int((y1 + y2) / 2)
        delta_eye_1 = delta_eye_2_x = delta_eye_2_y = THINGS_SIZE / 4
        color = SNAKE_EYE_COLOR
        width = 0
        size = 0

        if current_direction == 'left':
            x_tongue = x - THINGS_SIZE / 2
            y_tongue = y
            delta_eye_1 *= -1
            delta_eye_2_x *= -1
        elif current_direction == 'down':
            x_tongue = x
            y_tongue = y + THINGS_SIZE / 2
            delta_eye_2_x *= -1
        elif current_direction == 'right':
            x_tongue = x + THINGS_SIZE / 2
            y_tongue = y
            delta_eye_2_y *= -1
        elif current_direction == 'up':
            x_tongue = x
            y_tongue = y - THINGS_SIZE / 2
            delta_eye_1 *= -1
            delta_eye_2_y *= -1

        for i, part in enumerate(self.head_parts):
            self.canvas.delete(part)

            if i == 0:
                if current_direction == 'left':
                    self.head_parts[i] = self.canvas.create_line(x_tongue, y_tongue, x_tongue - TONGUE_SIZE, y_tongue - TONGUE_SIZE / 3, \
                                            x_tongue - 2 * TONGUE_SIZE, y_tongue + TONGUE_SIZE / 3, \
                                            x_tongue - 3 * TONGUE_SIZE, y_tongue, width=3, tag='head_parts', fill=SNAKE_TONGUE_COLOR)
                elif current_direction == 'down':
                    self.head_parts[i] = self.canvas.create_line(x_tongue, y_tongue, x_tongue - TONGUE_SIZE / 3, y_tongue + TONGUE_SIZE, \
                                            x_tongue + TONGUE_SIZE / 3, y_tongue + 2 * TONGUE_SIZE, \
                                            x_tongue, y_tongue + 3 * TONGUE_SIZE, width=3, tag='head_parts', fill=SNAKE_TONGUE_COLOR)
                elif current_direction == 'right':
                    self.head_parts[i] = self.canvas.create_line(x_tongue, y_tongue, x_tongue + TONGUE_SIZE, y_tongue + TONGUE_SIZE / 3, \
                                            x_tongue + 2 * TONGUE_SIZE, y_tongue - TONGUE_SIZE / 3, \
                                            x_tongue + 3 * TONGUE_SIZE, y_tongue, width=3, tag='head_parts', fill=SNAKE_TONGUE_COLOR)
                elif current_direction == 'up':
                    self.head_parts[i] = self.canvas.create_line(x_tongue, y_tongue, x_tongue + TONGUE_SIZE / 3, y_tongue - TONGUE_SIZE, \
                                            x_tongue - TONGUE_SIZE / 3, y_tongue - 2 * TONGUE_SIZE, \
                                            x_tongue, y_tongue - 3 * TONGUE_SIZE, width=3, tag='head_parts', fill=SNAKE_TONGUE_COLOR)

            if i in [1, 2]:
                dx = dy = delta_eye_1
            elif i in [3, 4]:
                dx = delta_eye_2_x
                dy = delta_eye_2_y

            if i in [1, 3]:
                color = SNAKE_EYE_COLOR
                width = 1
                size = EYE_SIZE / 2
            elif i in [2, 4]:
                color = SNAKE_PUPIL_COLOR
                width = 1
                size = EYE_SIZE / 4

            if i > 0:
                self.head_parts[i] = self.canvas.create_oval(x + dx - size, y + dy - size, \
                                                            x + dx + size, y + dy + size, \
                                                            width = width, tag='head_parts', fill = color)

    def grow_up(self, num_of_squares):
            for i in range(num_of_squares):
                x, y = self.body_parts_coords[-1]
                self.waiting_parts_coords.append([x, y])
                new_body_part = self.canvas.create_rectangle(TLGC + x, TLGC + y, TLGC + x + THINGS_SIZE, TLGC + y + THINGS_SIZE, \
                                                            fill=SNAKE_COLOR, tag="snake")
                self.canvas.tag_lower(new_body_part)
                self.waiting_parts.append(new_body_part)

class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.coords = []

    def reset(self, snake):
        while True:
            x = random.randint(0, GAME_NUM_OF_SQUARES_X - 1) * THINGS_SIZE
            y = random.randint(0, GAME_NUM_OF_SQUARES_Y - 1) * THINGS_SIZE
            if not self.check_overlap(snake, x, y):
                break

        self.canvas.delete('food')
        self.coords = [x, y]
        self.body = self.canvas.create_oval(TLGC + x, TLGC + y, TLGC + x + THINGS_SIZE, TLGC + y + THINGS_SIZE, \
                                                 fill=FOOD_COLOR, width = 0, tag="food")
        self.canvas.tag_lower(self.body)

    def check_overlap(self, snake, check_x, check_y):
        for snake_part_coords in snake.body_parts_coords:
            snake_part_x, snake_part_y = snake_part_coords
            if check_x == snake_part_x and check_y == snake_part_y:
                return True
        return False

class Poison:
    def __init__(self, canvas):
        self.canvas = canvas
        self.num_color = 0
        self.colors_array = []
        self.blinking_status = False

    def reset(self, snake, food):
        while True:
            x = random.randint(0, GAME_NUM_OF_SQUARES_X - 1) * THINGS_SIZE
            y = random.randint(0, GAME_NUM_OF_SQUARES_Y - 1) * THINGS_SIZE
            if not self.check_overlap(snake, food, x, y):
                break

        self.hide()
        self.coords = [x, y]
        self.body = self.canvas.create_oval(TLGC + x, TLGC + y, TLGC + x + THINGS_SIZE, TLGC + y + THINGS_SIZE, \
                                                 fill=POISON_COLOR[0], width = 0, tag="poison")
        self.canvas.tag_lower(self.body)

    def check_overlap(self, snake, food, check_x, check_y):
        for snake_part_coords in snake.body_parts_coords:
            snake_part_x, snake_part_y = snake_part_coords
            if check_x == snake_part_x and check_y == snake_part_y:
                return True

        food_part_x, food_part_y = food.coords
        if check_x == food_part_x and check_y == food_part_y:
            return True

        return False

    def hide(self):
        self.blinking_status = False
        self.colors_array.clear()
        self.num_color = 0
        self.canvas.delete('poison')
        self.coords = [- THINGS_SIZE, - THINGS_SIZE]

    def start_blinking(self):
        self.blinking_status = True
        self.blinking()

    def blinking(self):
        if self.blinking_status == True:
            if len(self.colors_array) < 1:
                self.colors_array = POISON_COLOR + list(reversed(POISON_COLOR[1:-1]))
            self.canvas.itemconfigure(self.body,fill=self.colors_array.pop())
            window.after(int(START_SPEED[0] / STEPS_FOR_ONE_SQUARE), self.blinking)

# ================================================

window = Tk()
window.title("Змейка дикого Макса 2")
window.resizable(False,False)

game = Game()

window.mainloop()
