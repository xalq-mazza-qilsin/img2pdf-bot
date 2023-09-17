import io
from aiogram import Router, types, F
from loader import bot
from utils.imgtopdf import images_to_pdf

router = Router()


@router.message(F.photo)
async def start_user(message: types.Message):
    image_file_id = message.photo[-1].file_id
    image = await bot.get_file(image_file_id)
    image_path = image.file_path
    await bot.download_file(image_path, "image.jpg")
    images_to_pdf(["image.jpg"], "result.pdf")
