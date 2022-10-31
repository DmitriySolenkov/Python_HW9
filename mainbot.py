import random
from aiogram.dispatcher import FSMContext
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
button_00 = KeyboardButton('0 0')
button_01 = KeyboardButton('0 1')
button_02 = KeyboardButton('0 2')
button_10 = KeyboardButton('1 0')
button_11 = KeyboardButton('1 1')
button_12 = KeyboardButton('1 2')
button_20 = KeyboardButton('2 0')
button_21 = KeyboardButton('2 1')
button_22 = KeyboardButton('2 2')

place_kb = ReplyKeyboardMarkup()
place_kb.add(button_00, button_01, button_02, button_10,
             button_11, button_12, button_20, button_21, button_22)


storage = MemoryStorage()
bot = Bot(token='ваш токен')
dp = Dispatcher(bot, storage=storage)
players = []
count = 0
cell = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
moves = []


class UserState(StatesGroup):
    waiting_first_name = State()
    waiting_second_name = State()
    waiting_turn = State()


@dp.message_handler(commands=['tictactoe'])
async def first_name_register(message: types.Message):
    await message.answer("Сыграем!")
    await message.answer("Первый игрок, введите своё имя:")
    chat_id = message.from_user.id
    await UserState.waiting_first_name.set()


@dp.message_handler(state=UserState.waiting_first_name)
async def second_name_register(message: types.Message, state: FSMContext):
    players.append(message.text)
    await message.answer("Второй игрок, введите своё имя:")
    await UserState.waiting_second_name.set()


@dp.message_handler(state=UserState.waiting_second_name)
async def second_name_register(message: types.Message, state: FSMContext):
    global count
    global moves
    players.append(message.text)
    await message.answer(f"Привет, {players[0]} и {players[1]}")
    firstStep = random.randint(1, 2)
    match firstStep:
        case 1: count = 0
        case 2: count = 1
    await message.answer(f"{players[count]} ходит первым!")
    if count == 0:
        moves = ['X', 'O']
    else:
        moves = ['O', 'X']
    await message.answer(f"{cell[0][0]}|{cell[0][1]}|{cell[0][2]}\n_______\n{cell[1][0]}|{cell[1][1]}|{cell[1][2]}\n_______\n{cell[2][0]}|{cell[2][1]}|{cell[2][2]}")
    await message.answer(f'Ход игрока {players[count%2]}!', reply_markup=place_kb)
    await UserState.waiting_turn.set()


@dp.message_handler(state=UserState.waiting_turn)
async def turn(message: types.Message, state: FSMContext):
    global count
    global cell
    global moves
    for char in message.text:
        if char.isdigit() == True or char == " ":
            check = True
        else:
            check = False
            break
    if check == True:
        coor = list(map(int, message.text.split()))
        if len(coor) == 2:
            if 0 <= coor[0] <= 2 and 0 <= coor[1] <= 2:
                if cell[coor[0]][coor[1]] == '-':
                    cell[coor[0]][coor[1]] = moves[count % 2]
                    await message.answer(f"{cell[0][0]}|{cell[0][1]}|{cell[0][2]}\n_______\n{cell[1][0]}|{cell[1][1]}|{cell[1][2]}\n_______\n{cell[2][0]}|{cell[2][1]}|{cell[2][2]}")
                    if winCheck(cell) == True:
                        await message.answer(f'{players[count%2]} победил!')
                        await message.answer('Чтобы сыграть еще раз, введите /tictactoe')
                        await state.finish()
                    else:
                        count += 1
                        await message.answer(f'Ход игрока {players[count%2]}!', reply_markup=place_kb)
                else:
                    await message.answer("Клетка уже занята! Выберите другую!", reply_markup=place_kb)
                    await message.answer(f'Ход игрока {players[count%2]}!', reply_markup=place_kb)
            else:
                await message.answer("Слишком большие координаты, выберите клетку еще раз!", reply_markup=place_kb)
                await message.answer(f'Ход игрока {players[count%2]}!', reply_markup=place_kb)
        else:
            await message.answer("Слишком много координат, выберите клетку еще раз!", reply_markup=place_kb)
            await message.answer(f'Ход игрока {players[count%2]}!', reply_markup=place_kb)
    else:
        await message.answer("В координаты затесались буквы, выберите клетку еще раз!", reply_markup=place_kb)
        await message.answer(f'Ход игрока {players[count%2]}!', reply_markup=place_kb)


def winCheck(cell):
    if cell[0][0] == cell[0][1] == cell[0][2] != '-':
        return True
    elif cell[1][0] == cell[1][1] == cell[1][2] != '-':
        return True
    elif cell[2][0] == cell[2][1] == cell[2][2] != '-':
        return True
    elif cell[0][0] == cell[1][0] == cell[2][0] != '-':
        return True
    elif cell[0][1] == cell[1][1] == cell[2][1] != '-':
        return True
    elif cell[0][2] == cell[1][2] == cell[2][2] != '-':
        return True
    elif cell[0][0] == cell[1][1] == cell[2][2] != '-':
        return True
    elif cell[0][2] == cell[1][1] == cell[2][0] != '-':
        return True
    else:
        return False


if __name__ == '__main__':
    executor.start_polling(dp)
