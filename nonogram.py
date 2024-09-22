import random

# Класс ячейки
class Cell:
    def __init__(self, x: int, y: int, number: int):
        self.x, self.y, self.number = x, y, number
        self.is_open = self.is_black = False
        self.count_bomb = 0
        self.symbol = "X"

# Основой класс игры
class Nonogram():
    def __init__(self, rows: int, columns: int):
        self.rows, self.columns = rows, columns

        # Формирование случайного количества чёрных клеток на доске
        self.black = random.randint(round(rows * columns * 0.5), round(rows * columns * 0.75))

        # Генерация пустой доски
        self.board = []
        number = 0
        for i in range(self.rows):
            temp = []
            for j in range(self.columns):
                temp.append(Cell(i, j, number))
                number += 1
            self.board.append(temp)

    # Подставление чёрных клеток на случайные места
    def insert_black(self):
        indexes = list(range(self.rows * self.columns))
        random.shuffle(indexes)
        indexes = indexes[:self.black]
        for i in range(self.rows):
            for j in range(self.columns):
                btn = self.board[i][j]
                if btn.number in indexes:
                    btn.is_black = True
                    btn.symbol = "#"

    # Подсчёт чёрных клеток по горизонтале и вертикале
    def count_hashes(self):
        num_rows = len(self.board)
        num_cols = len(self.board[0]) if num_rows > 0 else 0
        row_counts = []
        col_counts = [[] for _ in range(num_cols)]

        # Подсчет по строкам
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

        # Подсчет по столбцам
        for col in range(num_cols):
            current_count = 0
            for row in range(num_rows):
                if self.board[row][col].is_black:
                    current_count += 1
                else:
                    if current_count > 0:
                        col_counts[col].append(current_count)
                        current_count = 0
            if current_count > 0:
                col_counts[col].append(current_count)
        
        # Выравнивание всех списков
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

    # Вывод доски в консоль
    def print_board(self):
        row_counts, col_counts = self.count_hashes()
        maximum = len(row_counts[0])
        indentation = "".join(["  " for _ in range(maximum)])
        msg = indentation
        for index, _ in enumerate(col_counts[0]):
            for counts in col_counts:
                msg += f"{counts[index]} "
            if index != maximum - 1: msg += f"\n{indentation}"
        msg += "\n"
        for index, row in enumerate(self.board):
            for counts in row_counts[index]:
                msg += f"{counts} "
            msg += " ".join([cell.symbol for cell in row]) + "\n"
        print(msg)

# Инициализация игры
game = Nonogram(5, 5)
game.insert_black()
game.print_board()
