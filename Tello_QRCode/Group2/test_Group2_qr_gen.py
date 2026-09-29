import qrcode
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate_single_qr_page(data, filename):
    """
    Generates a single QR code on its own letter-sized page and saves it as a PDF.

    Args:
        data (str): The data to encode in the QR code (e.g., "flip_forward").
        filename (str): The name for the output file (e.g., "qr_flip_forward.pdf").
    """
    # Create a new PDF file for this QR code
    c = canvas.Canvas(filename, pagesize=letter)

    # Generate a QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Calculate the position to center the image on the page
    # Letter size is 8.5 x 11 inches. 1 inch = 72 points.
    page_width_pt, page_height_pt = letter
    img_width_pt, img_height_pt = img.size

    # Scale image to fill most of the page while maintaining aspect ratio
    scale = min((page_width_pt - 100) / img_width_pt, (page_height_pt - 100) / img_height_pt)
    scaled_width = img_width_pt * scale
    scaled_height = img_height_pt * scale

    x_pos = (page_width_pt - scaled_width) / 2
    y_pos = (page_height_pt - scaled_height) / 2

    # Draw the QR code image and a text label
    c.drawInlineImage(img, x_pos, y_pos, width=scaled_width, height=scaled_height)
    c.drawCentredString(page_width_pt / 2, y_pos - 30, f"QR Code: {data}")

    c.save()
    print(f"Generated PDF: {filename}")


if __name__ == "__main__":
    commands = {
        "Door 1": "qr_door1.pdf",
        "Door 2": "qr_door2.pdf",
        "Door 3": "qr_door3.pdf",
        "Door 4": "qr_door4.pdf",
        "Door_Stop": "qr_doorstop.pdf",
    }

    for data, filename in commands.items():
        generate_single_qr_page(data, filename)