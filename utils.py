import base64
import mimetypes
import pathlib
from typing import Tuple

def encode_image_to_base64(image_path: str) -> Tuple[str, str]:
    """
    Encode the image at the given path to Base64 format and return the MIME type and Base64-encoded image data.

    Args:
        image_path (str): The path to the image file.

    Returns:
        Tuple[str, str]: A tuple containing the MIME type and the Base64-encoded image data.

    Exceptions:
        FileNotFoundError: Raised if the file at the specified path does not exist.
        IOError: Raised if the file cannot be read or if the file format is invalid.
    """
    try:
        # Get the MIME type of the file
        mime = mimetypes.guess_type(image_path)[0] or "application/octet-stream"
        
        # Read the file and encode it to Base64
        data = pathlib.Path(image_path).read_bytes()
        b64 = base64.b64encode(data).decode()
        
        return mime, b64
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{image_path}' not found. Please check the path.")
    except IOError as e:
        raise IOError(f"Unable to read the file '{image_path}': {str(e)}")