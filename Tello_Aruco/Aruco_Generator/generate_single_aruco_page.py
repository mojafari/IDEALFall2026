import cv2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image


def generate_single_aruco_page(dictionary_name, marker_id, filename):
    """
    Generates a single ArUco marker on its own letter-sized page and saves it as a PDF.

    Args:
        dictionary_name (str): The name of the ArUco dictionary.
        marker_id (int): The ID of the marker to generate.
        filename (str): The name for the output file (e.g., "aruco_marker_0.pdf").
    """
    try:
        aruco_dict = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, dictionary_name))
    except AttributeError:
        print(f"Error: Dictionary '{dictionary_name}' not found.")
        return

    # Create a new PDF file for this marker
    c = canvas.Canvas(filename, pagesize=letter)

    # Generate the ArUco marker image
    marker_size_px = 800  # Generate a large image for high-quality printing
    marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size_px, borderBits=1)

    # Convert to PIL Image for PDF drawing
    pil_img = Image.fromarray(marker_img)

    # Calculate position to center the image on the page
    page_width_pt, page_height_pt = letter

    # Calculate scale factor for the marker (e.g., make it 6 inches wide)
    marker_size_in = 6
    marker_size_pt = marker_size_in * 72

    x_pos = (page_width_pt - marker_size_pt) / 2
    y_pos = (page_height_pt - marker_size_pt) / 2

    # Draw the image and label on the PDF
    c.drawInlineImage(pil_img, x_pos, y_pos, width=marker_size_pt, height=marker_size_pt)
    c.drawCentredString(page_width_pt / 2, y_pos - 30, f"ArUco ID: {marker_id}")

    c.save()
    print(f"Generated PDF: {filename}")


if __name__ == "__main__":
    dictionary_name = "DICT_4X4_50"
    ids = [0, 1, 2, 3, 4]  # The IDs from your Tello code

    for marker_id in ids:
        filename = f"aruco_marker_{marker_id}.pdf"
        generate_single_aruco_page(dictionary_name, marker_id, filename)