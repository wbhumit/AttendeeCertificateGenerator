import io
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont

# Initialize the Flask app
app = Flask(__name__)

# --- Configuration ---
TEMPLATE_IMAGE_PATH = "certificate_template.png"
FONT_PATH = "font.ttf"
FONT_SIZE = 60  # Adjust this size to fit your template
TEXT_COLOR = "black"  # Adjust the color (e.g., "#000000")
# Adjust this (x, y) coordinate to position the name on your template
# (0, 0) is the top-left corner.
# You will need to experiment to find the perfect spot.
NAME_POSITION = (300, 450)
# ---------------------


@app.route('/')
def home():
    """Renders the homepage with the name input form."""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_certificate():
    """Generates and downloads the certificate."""
    try:
        # Get the name from the form
        name = request.form['name']

        # Open the template image
        with Image.open(TEMPLATE_IMAGE_PATH) as img:
            draw = ImageDraw.Draw(img)

            # Load the font
            try:
                font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
            except IOError:
                return "Error: Font file not found. Make sure 'font.ttf' is in the correct directory.", 500

            # --- Optional: Center the text ---
            # If you want to center the text, uncomment the lines below
            # and adjust the Y_POSITION variable.
            
            # text_width = draw.textlength(name, font=font)
            # img_width, img_height = img.size
            # x = (img_width - text_width) / 2
            # y = img_height * 0.5 # (50% down from the top)
            # NAME_POSITION = (x, y)
            # ---------------------------------

            # Draw the name on the image
            draw.text(NAME_POSITION, name, font=font, fill=TEXT_COLOR)

            # Save the image to an in-memory buffer
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0) # Rewind the buffer to the beginning

            # Sanitize the name for the filename
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-')).rstrip()
            download_name = f"Workshop_Certificate_{safe_name}.png"

            # Send the image as a file download
            return send_file(
                buffer,
                mimetype='image/png',
                as_download=True,
                download_name=download_name
            )

    except FileNotFoundError:
        return "Error: Certificate template image not found. Make sure 'certificate_template.png' is in the correct directory.", 500
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    # This is only for local testing.
    # Render.com will use Gunicorn to run the app.
    app.run(debug=True)