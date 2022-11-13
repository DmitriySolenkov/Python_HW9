import random
from fractions import Fraction
from numbers import Complex
from aiogram.dispatcher import FSMContext
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class UserState(StatesGroup):
    waiting_first_name = State()
    waiting_second_name = State()
    waiting_turn = State()
    waiting_sweets_mode = State()
    sweets_players_turn = State()
    calc_mode = State()
    calc_comp_num = State()
    calc_rat_num = State()
    calc_rat_action = State()
    calc_comp_action = State()
    calc_result = State()


button_rat_calc = KeyboardButton('Рациональные числа')
button_comp_calc = KeyboardButton('Комплексные числа')

button_action_add = KeyboardButton('+')
button_action_sub = KeyboardButton('-')
button_action_mult = KeyboardButton('*')
button_action_div = KeyboardButton('/')
button_action = KeyboardButton('Ответ')

button_play_sweets = KeyboardButton('/sweets')
button_play_tictactoe = KeyboardButton('/tictactoe')
button_calculator = KeyboardButton('/calculator')

button_00 = KeyboardButton('0 0')
button_01 = KeyboardButton('0 1')
button_02 = KeyboardButton('0 2')
button_10 = KeyboardButton('1 0')
button_11 = KeyboardButton('1 1')
button_12 = KeyboardButton('1 2')
button_20 = KeyboardButton('2 0')
button_21 = KeyboardButton('2 1')
button_22 = KeyboardButton('2 2')

buttonSweetsEasy = KeyboardButton('Легкий')
buttonSweetsHard = KeyboardButton('Сложный')

button_sweets_1 = KeyboardButton('1 конфета')
button_sweets_2 = KeyboardButton('2 конфеты')
button_sweets_3 = KeyboardButton('3 конфеты')
button_sweets_4 = KeyboardButton('4 конфеты')
button_sweets_5 = KeyboardButton('5 конфет')
button_sweets_6 = KeyboardButton('6 конфет')

result_kb = ReplyKeyboardMarkup(resize_keyboard=True)
result_kb.add(button_action)

action_kb = ReplyKeyboardMarkup(resize_keyboard=True)
action_kb.add(button_action_add, button_action_sub,
              button_action_mult, button_action_div)

game_kb = ReplyKeyboardMarkup(resize_keyboard=True)
game_kb.add(button_play_sweets, button_play_tictactoe, button_calculator)

calc_mode_kb = ReplyKeyboardMarkup(resize_keyboard=True)
calc_mode_kb.add(button_rat_calc, button_comp_calc)

place_kb = ReplyKeyboardMarkup(resize_keyboard=True)
place_kb.add(button_00, button_01, button_02, button_10,
             button_11, button_12, button_20, button_21, button_22)

sweetsMode_kb = ReplyKeyboardMarkup(resize_keyboard=True)
sweetsMode_kb.add(buttonSweetsEasy, buttonSweetsHard)

sweets_amount_kb = ReplyKeyboardMarkup(resize_keyboard=True)
sweets_amount_kb.add(button_sweets_1, button_sweets_2, button_sweets_3,
                     button_sweets_4, button_sweets_5, button_sweets_6)

storage = MemoryStorage()
bot = Bot(token='ващ токен')
dp = Dispatcher(bot, storage=storage)

first_num = 0
action = 'a'
second_num = 0


@dp.message_handler(commands=['calculator'])
async def calc_start(message: types.Message):
    await message.answer("Сейчас все посчитаем!")
    await message.answer(f'Выберите режим калькулятора:', reply_markup=calc_mode_kb)
    await UserState.calc_mode.set()


@dp.message_handler(state=UserState.calc_mode)
async def calc_mode(message: types.Message, state: FSMContext):
    if message.text == 'Рациональные числа':
        await message.answer("Работаем с рациональными числами!")
        await message.answer("Введите первую дробь через /:")
        await UserState.calc_rat_num.set()
    elif message.text == 'Комплексные числа':
        await message.answer("Работаем с комплексными числами!")
        await message.answer("Введите коэффициенты первого числа через пробел:")
        await UserState.calc_comp_num.set()
    else:
        await message.answer(f'Я вас не понимаю, выберите режим калькулятора:', reply_markup=calc_mode_kb)


@dp.message_handler(state=UserState.calc_comp_num)
async def calc_comp_num(message: types.Message, state: FSMContext):
    global first_num
    global second_num
    num = list(message.text.split(' '))
    check = True
    if len(num) != 2:
        await message.answer("Неверно введены коэффициенты, попробуйте еще раз (через пробел)")
    else:
        if num[0].isdigit() == True:
            if num[1].isdigit() == True:
                check == True
            else:
                check = False
        else:
            check = False
        if check == False:
            await message.answer("Неверно введены коэффициенты, попробуйте еще раз (через пробел)")
        else:
            print(num)
            if first_num == 0:
                first_num = complex(int(num[0]), int(num[1]))
                await message.answer(f'Выберите действие:', reply_markup=action_kb)
                await UserState.calc_comp_action.set()
            else:
                second_num = complex(int(num[0]), int(num[1]))
                await message.answer(f'Нажмите на кнопку для расчета:', reply_markup=result_kb)
                await UserState.calc_result.set()


@dp.message_handler(state=UserState.calc_comp_action)
async def calc__compaction(message: types.Message, state: FSMContext):
    global action
    if message.text == '+' or message.text == '-' or message.text == '/' or message.text == '*':
        action = message.text
        await message.answer("Введите коэффициенты второга числа через пробел:")
        await UserState.calc_comp_num.set()
    else:
        await message.answer(f'Не понимаю вас, выберите действие:', reply_markup=action_kb)


@dp.message_handler(state=UserState.calc_rat_num)
async def calc_num_rat(message: types.Message, state: FSMContext):
    global first_num
    global second_num
    num = list(message.text.split('/'))
    check = True
    if len(num) != 2:
        await message.answer("Неверно введена дробь, попробуйте еще раз (через /)")
    else:
        if num[0].isdigit() == True:
            if num[1].isdigit() == True:
                check == True
            else:
                check = False
        else:
            check = False
        if check == False:
            await message.answer("Неверно введена дробь, попробуйте еще раз (через /)")
        else:
            if int(num[0]) == 0 or int(num[1]) == 0:
                await message.answer("Не работаю с нулями, попробуйте еще раз (через /)")
            else:
                if first_num == 0:
                    first_num = Fraction(int(num[0]), int(num[1]))
                    await message.answer(f'Выберите действие:', reply_markup=action_kb)
                    await UserState.calc_rat_action.set()
                else:
                    second_num = Fraction(int(num[0]), int(num[1]))
                    await message.answer(f'Нажмите на кнопку для расчета:', reply_markup=result_kb)
                    await UserState.calc_result.set()


@dp.message_handler(state=UserState.calc_rat_action)
async def calc_action(message: types.Message, state: FSMContext):
    global action
    if message.text == '+' or message.text == '-' or message.text == '/' or message.text == '*':
        action = message.text
        await message.answer("Введите вторую дробь через /:")
        await UserState.calc_rat_num.set()
    else:
        await message.answer(f'Не понимаю вас, выберите действие:', reply_markup=action_kb)


@dp.message_handler(state=UserState.calc_result)
async def calc_result(message: types.Message, state: FSMContext):
    global first_num
    global second_num
    res = 0
    match action:
        case '+': res = first_num + second_num
        case '-': res = first_num - second_num
        case '*': res = first_num * second_num
        case '/': res = first_num / second_num
    first_num = 0
    second_num = 0
    await message.answer(f'Ответ:{res}')
    await state.finish()
    await message.answer(f"Выберите, во что хотите поиграть:", reply_markup=game_kb)


sweets_count = 0
sweetsMode = 0


@dp.message_handler(commands=['sweets'])
async def sweets_start(message: types.Message):
    await message.answer("Сыграем в конфеты!")
    await message.answer(f'Выберите сложность бота:', reply_markup=sweetsMode_kb)
    await UserState.waiting_sweets_mode.set()


@dp.message_handler(state=UserState.waiting_sweets_mode)
async def sweets_mode(message: types.Message, state: FSMContext):
    global sweetsMode
    global sweets_count
    sweets_count = 63
    if message.text == "Легкий":
        sweetsMode = 1
        await message.answer("Играем с легким ботом!")
        await message.answer(f"В кучке осталось {sweets_count} конфет!")
        await message.answer(f"Выберите, сколько конфет хотите взять!:", reply_markup=sweets_amount_kb)
        await UserState.sweets_players_turn.set()
    elif message.text == "Сложный":
        sweetsMode = 2
        await message.answer("Играем со сложным ботом!")
        await message.answer(f"В кучке осталось {sweets_count} конфет!")
        await message.answer(f"Выберите, сколько конфет хотите взять!:", reply_markup=sweets_amount_kb)
        await UserState.sweets_players_turn.set()
    else:
        await message.answer("Я вас не понимаю! Пожалуйста, выберите сложность бота!")


@dp.message_handler(state=UserState.sweets_players_turn)
async def sweets_players_turn(message: types.Message, state: FSMContext):
    global sweets_count
    mess_list = list(message.text.split())
    sweets_amount = mess_list[0]
    if sweets_amount.isdigit() == True:
        if 0 < int(sweets_amount) < 7:
            sweets_count = sweets_count - int(sweets_amount)
            if sweets_count <= 0:
                await message.answer("Вы победили!")
                await state.finish()
                await message.answer(f"Выберите, во что хотите поиграть:", reply_markup=game_kb)
            else:
                await message.answer(f"В кучке осталось {sweets_count} конфет!")
                bots_hand = bots_turn(sweets_count)
                await message.answer(f"Бот берет {bots_hand} конфет!")
                sweets_count = sweets_count - bots_hand
                if sweets_count <= 0:
                    await message.answer("Бот победил!")
                    await state.finish()
                    await message.answer(f"Выберите, во что хотите поиграть:", reply_markup=game_kb)
                else:
                    await message.answer(f"В кучке осталось {sweets_count} конфет!")
                    await message.answer(f"Выберите, сколько конфет хотите взять!:", reply_markup=sweets_amount_kb)

        else:
            await message.answer("Вы хотите взять слишком много или слишком мало конфет! Имейте совесть!")
            await message.answer(f"Выберите, сколько конфет хотите взять!:", reply_markup=sweets_amount_kb)
    else:
        await message.answer("Вы написали что-то непонятное!")
        await message.answer(f"Выберите, сколько конфет хотите взять!:", reply_markup=sweets_amount_kb)


def bots_turn(sweets_count):
    global sweetsMode
    if sweetsMode == 1:
        if sweets_count < 7:
            return random.randint(1, sweets_count+1)
        else:
            return random.randint(1, 6)
    if sweetsMode == 2:
        if sweets_count == 1:
            return sweets_count
        else:
            check = amountCheck(sweets_count)
            match check:
                case True: return 6
                case False: return takeTo6(sweets_count)


def amountCheck(amount):
    i = 0
    while i < 12:
        if amount == i*6+1:
            print('true')
            return True
        else:
            i += 1
    if i == 12:
        print('false')
        return False


def takeTo6(amount):
    if amount < 7:
        return amount
    else:
        for i in range(1, 6):
            if (amount-i) % 6 == 1:
                return i


players = []
count = 0
cell = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
moves = []


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
                        await state.finish()
                        await message.answer(f"Выберите, во что хотите поиграть:", reply_markup=game_kb)
                    elif drawCheck(cell) == True:
                        await message.answer('Ничья!')
                        await state.finish()
                        await message.answer(f"Выберите, во что хотите поиграть:", reply_markup=game_kb)
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


def drawCheck(cell):
    if winCheck(cell) == False:
        if cell[0][0] != '-' and cell[0][1] != '-' and cell[0][2] != '-' and cell[1][0] != '-' and cell[1][1] != '-' and cell[1][2] != '-' and cell[2][0] != '-' and cell[2][1] != '-' and cell[2][2] != '-':
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    executor.start_polling(dp)
