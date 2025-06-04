import asyncio
import logging
import os
import sys
import database
import random
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import admin
import constants
import buttons

IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)



dp = Dispatcher(storage=MemoryStorage())

class EditBot(StatesGroup):
    waiting_for_admin = State()
    
    waiting_for_props_select = State()
    waiting_for_props = State()
    waiting_for_props_edit_or_delete = State()
    
    waiting_for_new_props = State()
    waiting_for_photo = State()

class BotState(StatesGroup):
    waiting_response = State()
    admin = State()
    replenish = State()
    replenish_id = State()
    replenish_sum = State()
    replenish_check = State()
    withdraw = State()
    withdraw_props = State()
    withdraw_id = State()
    withdraw_sum = State()
    withdraw_code = State()
    

   

@dp.message(CommandStart())
async def command_start_handler(message: Message, state) -> None:
    # status = await message.bot.get_chat_member(constants.channel, message.chat.id)
    # if status.status != "left" and message.chat.id != constants.replenish_chat_id and message.chat.id != constants.withdraw_chat_id and message.chat.id != constants.channel:
      await state.clear()
      await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!\n\n📲 Пополнение/Вывод: 0%\n⏳ Моментальные пополнения\n\nСлужба поддержки: @" + constants.bot_admin, reply_markup=buttons.main_kb(message.from_user.username))
    # else:
      await message.answer("Что-бы продолжить подпишитесь на канал", reply_markup=buttons.subscribe_kb())
        
@dp.message(F.text == "Отменить")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state != BotState.waiting_response:
     await command_start_handler(message, state)
    else:
     await message.answer("Пожалуйста дождитесь финального ответа системы!")


@dp.message(F.text == "📃 Инструкция")
async def ins_handler(message: Message):
   await message.answer("Недоступно", reply_markup=buttons.main_kb(message.from_user.username))


# 
@dp.message(F.text == "⬆ Пополнить")
async def replenish_handler(message: Message, state: FSMContext):
    status = await message.bot.get_chat_member(constants.channel, message.chat.id)
    if status.status == "kicked":
        await message.answer("Вы были заблокировны")
    else:
     if status.status != "left" and message.chat.id != constants.replenish_chat_id and message.chat.id != constants.withdraw_chat_id and message.chat.id != constants.channel:    
      await state.set_state(BotState.replenish)
      await message.answer("⬆", reply_markup=buttons.main_cancel_kb())      
      await message.answer("Выберите способ пополнения:", reply_markup=buttons.main_inline_replenish_kb())
     else:
      await message.answer("Что-бы продолжить подпишитесь на канал", reply_markup=buttons.subscribe_kb())
     
@dp.message(F.text == "⬇ Вывести") 
async def withdraw_handler(message: Message, state: FSMContext):
    status = await message.bot.get_chat_member(constants.channel, message.chat.id)
    if status.status == "kicked":
        await message.answer("Вы были заблокировны")
    else:
     if status.status != "left" and message.chat.id != constants.replenish_chat_id and message.chat.id != constants.withdraw_chat_id and message.chat.id != constants.channel:
      await state.set_state(BotState.withdraw)
      await message.answer("⬇", reply_markup=buttons.main_cancel_kb())
      await message.answer("❗ВАЖНО!!! ВЫВОД СРЕДСТВ ОСУЩЕСТВЛЯЕТСЯ ТОЛЬКО НА ТЕ РЕКВИЗИТЫ С КОТОРЫХ БЫЛ СОВЕРШЕН ПЛАТЁЖ❗")
      await message.answer("Выберите способ вывода:", reply_markup=buttons.main_inline_withdraw_kb())
     else:
      await message.answer("Что-бы продолжить подпишитесь на канал", reply_markup=buttons.subscribe_kb())
# 




# 
@dp.message(F.text == "⚙️ Настройки")
async def admin_handler(message: Message, state: FSMContext):
    if message.chat.id != constants.replenish_chat_id and message.chat.id != constants.withdraw_chat_id and message.chat.id != constants.channel:
      await admin.admin_handler(message, state) 
    
@dp.message(BotState.admin)
async def admin_options_handler(message: Message, state: FSMContext):
    await admin.admin_ops(message, state) 
    
@dp.message(EditBot.waiting_for_admin)
async def bot_admin_handler(message: Message, state: FSMContext):
    await admin.handle_admin(message, state)

@dp.message(EditBot.waiting_for_props_select)
async def bot_props_slect_handler(message: Message, state: FSMContext):
    await admin.handle_props_select(message, state)

@dp.message(EditBot.waiting_for_props)
async def bot_props_handler(message: Message, state: FSMContext):
    await admin.handle_props(message, state)
    
@dp.message(EditBot.waiting_for_props_edit_or_delete)
async def bot_props_handler(message: Message, state: FSMContext):
    await admin.handle_props_edit_or_delete(message, state)

@dp.message(EditBot.waiting_for_photo, F.photo)
async def bot_qr_handler(message: Message, state: FSMContext):
    await admin.handle_photo(message, state)

@dp.message(EditBot.waiting_for_new_props)
async def bot_new_props_handler(message: Message, state: FSMContext):
    await admin.handle_new_props(message, state)
# 


# 
@dp.callback_query(BotState.withdraw)
async def withdraw_query_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data == "withdraw1" or callback.data == "withdraw2" or callback.data == "withdraw3":
        await state.set_state(BotState.withdraw_props)
        await callback.message.edit_reply_markup(None)
        
        if(callback.data == "withdraw1"):
            await state.update_data(withdraw="МБАНК")
            await callback.message.edit_text("Метод вывода: " + "МБАНК")
            await callback.message.answer("Введите номер кошелка")
        if(callback.data == "withdraw2"):
            await state.update_data(withdraw="О Деньги!")
            await callback.message.edit_text("Метод вывода: " + "О Деньги!")
            await callback.message.answer("Введите номер кошелка")
        if(callback.data == "withdraw3"):
            await state.update_data(withdraw="По номеру карты")
            await callback.message.edit_text("Метод вывода: " + "По номеру карты")
            await callback.message.answer("Введите номер кошелка")

@dp.message(BotState.withdraw_props)
async def withdraw_props_handler(message: Message, state: FSMContext) -> None:
      if message.text.isdigit():
        length = len(message.text)
        if length > 8:
            await state.update_data(withdraw_props=message.text)
            await state.set_state(BotState.withdraw_id)
            
            xid = database.get_user_data(message.chat.id)
            if xid:
             await message.answer("Введите ID(Номер счёта) 1X!", reply_markup=buttons.main_id_kb(xid))
            else:
             await message.answer("🚩 Вывод доступен только тем пользователям, которые\nосуществляли пополнение через нашего бота", reply_markup=buttons.main_kb(message.from_user.username))
             state.clear()
        else:
            await message.answer("Слишком короткий номер")
      else:
            await message.answer("Укажите правильный номер (только цифры).")

@dp.message(BotState.withdraw_id)
async def withdraw_id_handler(message: Message, state: FSMContext) -> None:
      if message.text.isdigit():
            id_length = len(message.text)
            if id_length > 6:
                await state.update_data(user_xbet_id=message.text)
                await state.set_state(BotState.withdraw_sum)
                
                await message.answer("Укажите сумму вывода KGS.\nМинимальная: 150", reply_markup=buttons.main_cancel_kb())
            else:
                await message.answer("Слишком короткий код")
      else:
            await message.answer("Укажите правильный ID (только цифры).")

@dp.message(BotState.withdraw_sum)
async def withdraw_sum_handler(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        user_sum = int(message.text)
        if user_sum > 149:
            await state.update_data(user_sum=message.text)
            await state.set_state(BotState.withdraw_code)
            
            await message.answer(f"Адрес вывода: Mobcash")
            await message.answer("Введите код от 1X", reply_markup=buttons.main_cancel_kb())
        else:
            await message.answer("Мимиальная сумма вывода 150 KGS")
            

@dp.message(BotState.withdraw_code)
async def withdraw_code_handler(message: Message, state: FSMContext) -> None:
    length = len(message.text)
    if(length > 3):
        await state.update_data(code=message.text)
        await state.update_data(user_id=message.chat.id)
        
        
        data = await state.get_data()
        method = data.get("withdraw")
        props = data.get("withdraw_props")
        xid = data.get("user_xbet_id")
        amount = data.get("user_sum")
        code = message.text
        username = message.from_user.username
        
        
        
        await(message.answer("🕘 Ваша заявка в расмотрении...", reply_markup=None))
        
        # await message.bot.send_message(constants.chat, f"{html.bold('ЗАПРОС НА ВЫВОД')}\n\nПользователь: @{username}\nМетод: {method}\nРеквизит: {html.code(props)}\n1X ID: {html.code(xid)}\nКод: {html.code(code)}\nСумма: {amount}")
        # await message.bot.send_message(constants.chat, str(message.chat.id))
        if message.from_user.username != 'None':
         await message.bot.send_message(constants.withdraw_chat_id, f"{html.bold('ЗАПРОС НА ВЫВОД')}\n\nПользователь: @{username}\nМетод: {method}\nРеквизит: {html.code(props)}\n1X ID: {html.code(xid)}\nКод: {html.code(code)}\nСумма: {amount}")
        else:
         await message.bot.send_message(constants.withdraw_chat_id, f"{html.bold('ЗАПРОС НА ВЫВОД')}\n\nПользователь: @{message.from_user.first_name}\nМетод: {method}\nРеквизит: {html.code(props)}\n1X ID: {html.code(xid)}\nКод: {html.code(code)}\nСумма: {amount}")
        await message.bot.send_message(constants.withdraw_chat_id, str(message.chat.id), reply_markup=buttons.main_inline_admin_withdraw_kb())
        await state.set_state(BotState.waiting_response)
# 



# 
@dp.callback_query(BotState.replenish)
async def replenish_query_handler(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data == "replenish1" or callback.data == "replenish2":
        await state.set_state(BotState.replenish_id)
        await callback.message.edit_reply_markup(None)
        
        if(callback.data == "replenish1"):
            await state.update_data(replenish="По номеру телефона")
        if(callback.data == "replenish2"):
            await state.update_data(replenish="qr")    
        
        xid = database.get_user_data(callback.message.chat.id)
        if xid:
         await callback.message.answer("Введите ID(Номер счёта) 1X!", reply_markup=buttons.main_id_kb(xid))
        else:
         await callback.message.answer("Введите ID(Номер счёта) 1X!", reply_markup=buttons.main_cancel_kb())
            

@dp.message(BotState.replenish_id)
async def id_handler(message: Message, state: FSMContext) -> None:
        if message.text.isdigit():
            id_length = len(message.text)
            if id_length > 6:
                await state.update_data(user_xbet_id=message.text)
                await state.set_state(BotState.replenish_sum)
                await message.answer("Укажите сумму пополнения KGS.\nМинимальная: 100\nМаксимальная: 100 000", reply_markup=buttons.main_cancel_kb())
            else:
                await message.answer("Слишком короткий ID")
        else:
            await message.answer("Укажите правильный ID (только цифры).")
            
@dp.message(BotState.replenish_sum)
async def sum_handler (message: Message, state: FSMContext) -> None: 
    try: 
     if message.text.isdigit():
        user_sum = int(message.text)
        if user_sum > 99 and user_sum < 100000:
            
            await state.set_state(BotState.replenish_check)       
            await state.update_data(amount=message.text)
            await message.answer("📤")
            
            d = await state.get_data() 
            qr = d.get("replenish")  
            
            if qr == 'qr':
             await message.answer(f"Сумма к оплате: {html.code(message.text)}" + "\n\nРекзвизиты: " + html.code("QR Код") + "\nНажмите чтобы скопировать ☝\n\nОтправьте УКАЗАННУЮ СУММУ\nна счёт и ОТПРАВЬТЕ ЧЕК")
             path = os.path.join(IMG_DIR, "qr.jpg")
             if os.path.exists(path):
              photo = FSInputFile(path)
              data = database.get_bot_data()
              qr_link = data["qr"]
              
              
              await message.answer_photo(photo, reply_markup=buttons.payment_kb(qr_link))
            else:
             data = database.get_bot_data()
             props = data["props"]
             new_props = data["new_props"]
             all_props = [props] +  new_props
             random_props = random.choice(all_props) if all_props else None
             await message.answer(f"Сумма к оплате: {html.code(message.text)}" + "\n\nРекзвизиты: " + html.code(random_props) + "\nНажмите чтобы скопировать ☝\n\nОтправьте УКАЗАННУЮ СУММУ\nна счёт и ОТПРАВЬТЕ ЧЕК")
            asyncio.create_task(timer(message, state))
        else:
            await message.answer("\nМинимальная: 100\nМаксимальная: 100 000")   
     else:
        await message.answer("Введите сумму пополнения!")  
    except TypeError:
        await message.answer("Не отправляйте файлы и т.п") 
            
async def timer(message: Message, state: FSMContext, duration: int = 300):
    timer_message = await message.answer("⏳ Ожидаем оплату... Осталось 5:00")
    last_text = "⏳ Ожидаем оплату... Осталось 5:00"

    for remaining in range(duration, 0, -1):
        minutes = remaining // 60
        seconds = remaining % 60
        new_text = f"⏳ Ожидаем оплату... Осталось {minutes}:{seconds:02d}"

        if remaining % 5 == 0 or remaining <= 10:
            if new_text != last_text:
                try:
                    await timer_message.edit_text(new_text)
                    last_text = new_text
                except Exception as e:
                    if "message is not modified" not in str(e):
                        logging.warning(f"Ошибка редактирования таймера: {e}")
                    break

        await asyncio.sleep(1)

        current_state = await state.get_state()
        if current_state is None or current_state != BotState.replenish_check.state:
            logging.info("Таймер был отменён")
            await timer_message.delete()
            await message.bot.delete_message(chat_id=message.chat.id, message_id=timer_message.message_id - 1)
            break

    current_state = await state.get_state()
    if current_state == BotState.replenish_check.state:
        await message.answer(
            "⏰ Время на оплату вышло. Если вы не отправили чек — операция отменена.",
            reply_markup=buttons.main_kb(message.from_user.username)
        )
        await state.clear()
        
@dp.message(BotState.replenish_check, F.photo)
async def check_handler(message: Message, state: FSMContext):
    await state.update_data(user_id=message.chat.id)
    
    
    data = await state.get_data()
    xid = data.get("user_xbet_id")
    method = data.get("replenish")
    database.update_user(message.chat.id, message.from_user.username, xid)
    
    await(message.answer("🕘 Ваша заявка в расмотрении...", reply_markup=None))
    
    
    # await message.bot.forward_message(constants.chat, message.chat.id, message.message_id)
    # await message.bot.send_message(constants.chat, f"Пользователь: @{message.from_user.username}\n1X ID: {html.code(xid)}\nМетод: {method}")
    # await message.bot.send_message(constants.chat, str(message.chat.id)) 
     
    await message.bot.forward_message(constants.replenish_chat_id, message.chat.id, message.message_id)
    if message.from_user.username != 'None':
     await message.bot.send_message(constants.replenish_chat_id, f"Пользователь: @{message.from_user.username}\n1X ID: {html.code(xid)}\nМетод: {method}")
    else:
     await message.bot.send_message(constants.replenish_chat_id, f"Пользователь: {message.from_user.first_name}\n1X ID: {html.code(xid)}\nМетод: {method}")    
    await message.bot.send_message(constants.replenish_chat_id, str(message.chat.id), reply_markup=buttons.main_inline_admin_replenish_kb())
    await state.set_state(BotState.waiting_response)

@dp.callback_query(lambda c: c.data == "subscribe")
async def query_handler(callback: CallbackQuery) -> None:
    status = await callback.message.bot.get_chat_member(constants.channel, callback.message.chat.id)
    
    if status.status != "left":
        await callback.message.answer(f"Привет, {html.bold(callback.message.from_user.full_name)}!\n\n📲 Пополнение/Вывод: 0%\n⏳ Моментальные пополнения\n\nСлужба поддержки: @" + constants.bot_admin, reply_markup=buttons.main_kb(callback.message.from_user.username))
    else:
        await callback.bot.answer_callback_query(callback_query_id=callback.id, text='Вы не подписались!')

@dp.callback_query(lambda c: c.data == "accept")
async def query_handler(callback: CallbackQuery) -> None:
       username = database.get_username(callback.message.text)       
       await callback.message.bot.send_message(callback.message.text, "✅ Ваш счет пополнен!", reply_markup=buttons.main_kb(username))
       await callback.message.edit_reply_markup(None)
       await callback.message.edit_text("Одобрен")
       
@dp.callback_query(lambda c: c.data == "cancel")
async def query_handler(callback: CallbackQuery) -> None:       
       username = database.get_username(callback.message.text)
       await callback.message.bot.send_message(callback.message.text, "❌ Ваша заявка была отклонена. Проверьте 1X ID или ЧЕК который вы отправили.\n\nСлужба поддержки: @" + constants.bot_admin, reply_markup=buttons.main_kb(username))
       await callback.message.edit_reply_markup(None)
       await callback.message.edit_text("Отклонён")
       
@dp.callback_query(lambda c: c.data == "waccept")
async def query_handler(callback: CallbackQuery) -> None:    
       username = database.get_username(callback.message.text)
       await callback.message.bot.send_message(callback.message.text, "✅ Вывод прошёл успешно", reply_markup=buttons.main_kb(username))
       await callback.message.edit_reply_markup(None)
       await callback.message.edit_text("Одобрен")
       
@dp.callback_query(lambda c: c.data == "wcancel")
async def query_handler(callback: CallbackQuery) -> None:    
       username = database.get_username(callback.message.text)
       await callback.message.bot.send_message(callback.message.text, "❌ Ваша заявка была отклонена. Проверьте 1X ID или НОМЕР который вы отправили.\n\nСлужба поддержки: @" + constants.bot_admin, reply_markup=buttons.main_kb(username))
       await callback.message.edit_reply_markup(None)
       await callback.message.edit_text("Отклонён")
       
@dp.callback_query(lambda c: c.data == "block_user")
async def query_handler(callback: CallbackQuery) -> None:
    await callback.message.bot.ban_chat_member(callback.message.text, callback.message.from_user.id)
    await callback.message.edit_reply_markup(buttons.unblock_kb())

@dp.callback_query(lambda c: c.data == "unblock_user")
async def query_handler(callback: CallbackQuery) -> None:
    await callback.message.bot.unban_chat_member(callback.message.text, callback.message.from_user.id)
    await callback.message.edit_reply_markup(buttons.block_kb())    
# 
            
            
            
            
            
            
            
            
async def main() -> None:
    load_dotenv('.env')
    
    TOKEN = os.getenv("TOKEN")
    
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main(), debug=True)
    