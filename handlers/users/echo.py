import requests

from datetime import datetime
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from loader import bot
from utils.imgtopdf import images_to_pdf

router = Router()


@router.message(F.content_type == 'photo')
async def start_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    image_paths = data.get('image_paths', [])

    for photo in message.photo:
        now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        image = await bot.get_file(photo.file_id)
        image_path = f"images/image_{now}.jpg"
        await bot.download_file(image.file_path, image_path)
        image_paths.append(image_path)

    data['image_paths'] = image_paths
    await state.set_data(data)
    await message.answer("Agar rasmlar tugagan bo'lsa /stop buyrug'ini yuboring.")


@router.message(F.text == '/stop')
async def send_pdf(message: types.Message, state: FSMContext):
    data = await state.get_data()
    image_paths = data.get('image_paths', None)
    if image_paths:
        file_path = f'pdfs/{message.from_user.id}.pdf'
        images_to_pdf(image_paths, file_path)
        bot_properties = await bot.me()
        await message.answer_document(types.input_file.FSInputFile(file_path),
                                      caption=f"@{bot_properties.username} orqali tayyorlandi!")
        await state.clear()
    else:
        await message.answer("Siz hali rasm yubormadingiz. Iltimos kamida bir dona rasm yuboring.")
