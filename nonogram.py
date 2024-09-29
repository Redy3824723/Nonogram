import random, os
from PIL import Image

class Cell:
    def __init__(self, x: int, y: int, number: int):
        self.x, self.y, self.number = x, y, number
        self.is_open = self.is_black = self.is_error_move = False
        self.symbol = "X"

class Nonogram():
    def __init__(self, rows: int, columns: int):
        self.rows, self.columns = rows, columns
        self.black = random.randint(round(rows * columns * 0.5), round(rows * columns * 0.75))
        self.hiden_procent = random.randint(10, 25) / 100
        self.mode, self.moves, self.life = 0, 0, 5
        self.is_game_over = False
        self.board = []
        number = 0
        for i in range(self.rows):
            temp = []
            for j in range(self.columns):
                temp.append(Cell(i, j, number))
                number += 1
            self.board.append(temp)

    def start(self, img: Image = None, size: tuple = (10, 10)):
        if img:
            img = self.generate(img, size)
            self.img_to_matrix(img)
        else:
            self.insert_random_black()
        self.hide_board()
        self.hide_lines()

    def insert_random_black(self):
        indexes = list(range(self.rows * self.columns))
        random.shuffle(indexes)
        indexes = indexes[:self.black]
        for i in range(self.rows):
            for j in range(self.columns):
                btn = self.board[i][j]
                if btn.number in indexes:
                    btn.is_black = True
                    btn.symbol = "#"

    def hide_board(self):
        indexes = list(range(self.rows * self.columns))
        random.shuffle(indexes)
        indexes = indexes[:round(len(indexes) * self.hiden_procent)]
        for i in range(self.rows):
            for j in range(self.columns):
                btn = self.board[i][j]
                if btn.number in indexes:
                    btn.is_open = True

    def count_hashes(self, leveling: bool = True):
        row_counts = []
        col_counts = [[] for _ in range(self.columns)]

        for row in self.board:
            counts = []
            current_count = 0
            for cell in row:
                if cell.is_black:
                    current_count += 1
                else:
                    if current_count > 0:
                        counts.append(current_count)
                        current_count = 0
            if current_count > 0:
                counts.append(current_count)
            row_counts.append(counts)

        for col in range(self.columns):
            current_count = 0
            for row in range(self.rows):
                if self.board[row][col].is_black:
                    current_count += 1
                else:
                    if current_count > 0:
                        col_counts[col].append(current_count)
                        current_count = 0
            if current_count > 0:
                col_counts[col].append(current_count)
        
        if leveling:
            maximum = 1
            for counts in row_counts + col_counts:
                if len(counts) > maximum:
                    maximum = len(counts)
            for counts in row_counts:
                if len(counts) < maximum:
                    counts += [" " for _ in range(maximum - len(counts))]
            for counts in col_counts:
                if len(counts) < maximum:
                    counts += [" " for _ in range(maximum - len(counts))]
        return row_counts, col_counts

    def print_board(self):
        row_counts, col_counts = self.count_hashes()
        maximum = len(row_counts[0])
        indentation = "".join(["  " for _ in range(maximum)])
        msg = indentation
        for index, _ in enumerate(col_counts[0]):
            for counts in col_counts:
                msg += f"{counts[index]} "
            if index != maximum - 1: msg += f"\n{indentation}"
        msg += "\n" + "  " * len(row_counts[0]) + "_" * (len(self.board[0]) * 2 - 1) + "\n"
        for index, row in enumerate(self.board):
            msg += " ".join([str(counts) for counts in row_counts[index]]) + "|"
            msg += " ".join([cell.symbol if self.is_game_over or cell.is_open else "." for cell in row]) + "\n"
        print(msg)

    def hide_lines(self):
        row_counts, col_counts = self.count_hashes(False)
        for index, row in enumerate(self.board):
            is_hide = 0
            for cell in row:
                if cell.is_open and cell.is_black:
                    is_hide += 1
            number = 0
            for numb in row_counts[index]:
                number += numb
            if is_hide == number:
                for cell in row:
                    cell.is_open = True

        for index in range(self.columns):
            is_hide = 0
            for row in range(self.rows):
                cell = self.board[row][index]
                if cell.is_open and cell.is_black:
                    is_hide += 1
            number = 0
            for numb in col_counts[index]:
                number += numb
            if is_hide == number:
                for row in range(self.rows):
                    self.board[row][index].is_open = True

    def generate(self, img: Image, size: tuple) -> Image:
        img = self.replace_transparent_background(img)
        return img.resize(size, Image.NEAREST).convert('1')

    def replace_transparent_background(self, img: Image) -> Image:
        new_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
        for x in range(img.width):
            for y in range(img.height):
                pixel = img.getpixel((x, y))
                if pixel == 0: new_img.putpixel((x, y), (255, 255, 255, 255))
                else: new_img.putpixel((x, y), pixel)
        return new_img.convert("RGB")

    def img_to_matrix(self, img: Image):
        self.board = []
        black = white = 0
        img = img.rotate(90)
        for x in range(img.width):
            for y in range(img.height):
                pixel = img.getpixel((x, y))
                if pixel == 0: black += 1
                else: white += 1
        if black < white: color = 0
        else: color = 255
        number = 0
        for x in range(img.width):
            temp = []
            for y in range(img.height):
                pixel = img.getpixel((x, y))
                if pixel == color:
                    cell = Cell(x, y, number)
                    cell.is_black = True
                    cell.symbol = "#"
                    temp.append(cell)
                else: temp.append(Cell(x, y, number))
                number += 1
            self.board.append(temp)

    def check_win(self):
        for row in self.board:
            for cell in row:
                if not cell.is_open:
                    return False
        return True

    def move(self, cell: Cell):
        if (not cell.is_black and not self.mode) or (cell.is_black and self.mode):
            cell.is_error_move = True
            cell.is_open = True
            self.hide_lines()
            self.life -= 1
            if not self.life:
                self.is_game_over = True
                return False
            return
        cell.is_open = True
        self.hide_lines()
        self.moves += 1
        if self.check_win():
            return True

imgs = []
for path in os.listdir(r"./images"):
    if path.endswith(".png"):
        imgs.append(f"./images/{path}")

size = (10, 10)
game = Nonogram(size[0], size[1])

"""
Для запуска игры с игровым полем по определённой картинке:
game.start(Image.open(r"./images/пироженое.png"), size)

Для запуска игры с игровым полем по случайной картинке:
game.start(Image.open(random.choice(imgs)), size)

Для запуска игры со случайным игровым полем:
game.start()
"""
game.start(Image.open(random.choice(imgs)), size)
while not game.is_game_over:
    game.print_board()
    cordinates = str(input(f"\nТекущий режим: {'Выставление крестиков' if game.mode else 'Выставление квадратов'}\nЖизни: {game.life}\nВведи координаты клетки для хода (x y) или \"mode\" для смены режима: "))
    if cordinates == "mode":
        game.mode = 0 if game.mode else 1
        continue
    cordinates = cordinates.split(" ")[:2]
    if len(cordinates) != 2: continue
    y, x = int(cordinates[0]) - 1, int(cordinates[1]) - 1
    try: cell = game.board[x][y]
    except:
        print("Клетки по таким координатам нет!")
        continue
    if cell.is_open:
        print("Эта клетка уже открыта!")
        continue
    move = game.move(cell)
    if move == True:
        game.print_board()
        print(f"Поздравляю! Вы выиграли в игру Nonogram за {game.moves} ход(-ов) и у вас осталось {game.life} жизней")
        break
    elif move == False:
        game.hiden_procent = 1
        game.print_board()
        print(f"Вы сделали не правильный ход и проиграли!")
        break