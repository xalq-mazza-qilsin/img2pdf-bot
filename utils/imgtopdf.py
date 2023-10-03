import os
import logging

from reportlab.lib.pagesizes import A4, mm
from reportlab.platypus import Image, SimpleDocTemplate


def images_to_pdf(images, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []

    normal_height = 685.88
    normal_width = 439.27

    for image in images:
        height = image.get('height')
        width = image.get('width')
        if width > normal_width:
            point = width / normal_width
            height /= point
        else:
            point = normal_width / width
            height *= point
        width = normal_width
        if height > normal_height:
            point = height / normal_height
            width /= point
        else:
            point = normal_height / width
            width *= point
        height = normal_height
        img = Image(image.get('path'))
        img.drawHeight = height
        img.drawWidth = width
        story.append(img)

    doc.build(story)


def delete_specific_files(folder_path, files_to_delete):
    try:
        for file_name in files_to_delete:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        logging.error(f"An error occurred when attempted to delete files: Error: {e}")
