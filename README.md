# Nonogram (Русский)
### Перед запуском:
```python
pip install Pillow
```



class.Cell - класс, хранящий в себе данные о конкретной ячейки на игровом поле.

class.Nonogram - Основной класс со всеми данными об игре.
`14 строка`
`self.hiden_procent = random.randint(10, 25) / 100`
Процент открытого игрового поля при старте игры (0.1 - значит 10% игровых клеток будет уже открыто при старте игры). `random.randint(10, 25) / 100` - генератор случайного числа от 0.1 до 0.25

`15 строка`
`self.mode, self.moves, self.life = 0, 0, 5`
Первое число - стандартный режим игры (0 - выставление чёрных квадратов, 1 - выставление крестиков).
Второе число - общее количество сделанных ходов игроком за всю игру.
Третье число - количество жизней у игрока (Каждый не правильный ход -1 жизнь).


`220 строка`
## Для запуска игры с игровым полем по определённой картинке:
`game.start(Image.open(r"./images/пироженое.png"), size)`

## Для запуска игры с игровым полем по случайной картинке:
`game.start(Image.open(random.choice(imgs)), size)`

## Для запуска игры со случайным игровым полем:
`game.start()`





# Nonogram (English)
### Before launching:
``python
pip install Pillow
```



class.Cell is a class that stores data about a specific cell on the playing field.

class.Nonogram is the main class with all the data about the game.
`Line 14`
`self.hiden_procent = random.randint(10, 25) / 100`
The percentage of the open playing field at the start of the game (0.1 means 10% of the game cells will already be open at the start of the game). `random.randint(10, 25) / 100` - random number generator from 0.1 to 0.25

`Line 15`
`self.mode, self.moves, self.life = 0, 0, 5`
The first number is the standard game mode (0 - setting black squares, 1 - setting crosses).
The second number is the total number of moves made by the player during the entire game.
The third number is the number of lives the player has (Each wrong move is -1 life).


`220 line`
## To start a game with a playing field based on a certain picture:
`game.start(Image.open(r"./images/pie.png"), size)`

## To start a game with a playing field based on a random picture:
`game.start(Image.open(random.choice(imgs)), size)`

## To start the game with a random playing field:
`game.start()`
