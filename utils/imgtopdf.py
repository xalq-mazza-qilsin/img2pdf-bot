from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image


def images_to_pdf(image_paths, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []

    for image_path in image_paths:
        img = Image(image_path)
        img.drawHeight = 500  # Set the height of the image in the PDF
        img.drawWidth = 500   # Set the width of the image in the PDF
        story.append(img)

    doc.build(story)
