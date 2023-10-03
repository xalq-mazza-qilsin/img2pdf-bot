from datetime import datetime
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from loader import bot
from utils.imgtopdf import images_to_pdf, delete_specific_files
from data.config import CHANNEL_ID

router = Router()


@router.message(F.media_group_id)
async def nothing(message: types.Message):
    pass


@router.message(F.content_type == 'photo')
async def start_user(message: types.Message, state: FSMContext):
    msg = await message.answer("Rasm yuklab olinmoqda...")
    data = await state.get_data()
    images = data.get('images', [])
    photo = message.photo[-1]
    now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    image = await bot.get_file(photo.file_id)
    image_path = f"images/image_{now}.jpg"
    await bot.download_file(image.file_path, image_path)
    images.append({'path': image_path, 'width': photo.width, 'height': photo.height})
    data['images'] = images
    await state.set_data(data)
    await msg.delete()
    await message.answer("Agar rasmlar tugagan bo'lsa /stop buyrug'ini yuboring.")


@router.message(F.text == '/stop')
async def send_pdf(message: types.Message, state: FSMContext):
    data = await state.get_data()
    images = data.get('images', None)
    if images:
        msg = await message.answer("PDF jo'natilmoqda...")
        file_path = f'pdfs/{message.from_user.id}.pdf'
        images_to_pdf(images, file_path)
        bot_properties = await bot.me()
        file = await bot.send_document(chat_id=CHANNEL_ID, document=types.input_file.FSInputFile(file_path),
                                       caption=f"@{bot_properties.username} orqali tayyorlandi!"
                                               f"\n\nUser ID: {message.from_user.id}")
        await message.answer_document(file.document.file_id, caption=f"@{bot_properties.username} orqali tayyorlandi!")
        await msg.delete()
        await state.clear()

        image_paths = [image.get('path')[7:] for image in images]
        delete_specific_files("images/", image_paths)
        delete_specific_files('pdfs/', [f'{message.from_user.id}.pdf'])
    else:
        await message.answer("Siz hali rasm yubormadingiz. Iltimos kamida bir dona rasm yuboring.")
