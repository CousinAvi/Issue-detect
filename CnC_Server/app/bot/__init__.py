from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = "5173732024:AAFY-kMYgBySve6ILTpsY2LEnwtbeuPoKtQ"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['get_chat_id'])
async def send_welcome(message: types.Message):

    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.]\nChat id is: "+ str(message.chat.id))
