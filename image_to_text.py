import pytesseract
from PIL import Image
import io


def convert_to_text(image_bits):

    image = Image.open(io.BytesIO(image_bits))

    # Convertir la imagen a texto con pytesseract
    text = pytesseract.image_to_string(image)

    # Imprimir el texto en la consola
    return text