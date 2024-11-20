from PIL import Image, ImageDraw, ImageFont

class JokeImageCreator:
    def __init__(self, font_path='Arial.ttf', max_width=900, output_size=(1080, 1080)):
        # Initialize the image settings
        self.font_path = font_path
        self.max_width = max_width
        self.output_size = output_size

    def wrap_text(self, text, font, draw):
        words = text.split()
        lines = []
        current_line = ''
        for word in words:
            # Attempt to add the next word to the current line
            test_line = f'{current_line} {word}'.strip()
            # Measure the width of the current line
            text_width = draw.textlength(test_line, font=font)
            if text_width <= self.max_width:
                current_line = test_line
            else:
                # If the line is too long, add the current line to lines and start a new line
                if current_line:
                    lines.append(current_line)
                current_line = word
        # Add the last line
        if current_line:
            lines.append(current_line)
        return lines

    def create_image(self, text, output_path, background_path):
        print(f"Creating image with text: {text}, output: {output_path}, bg_path: {background_path}")
        line_spacing_factor = 1.5  # Adjust line height to 1.5 times

        # Load the background image
        background = Image.open(background_path)
        # Resize background to the specified output size if necessary
        background = background.resize(self.output_size)

        # Prepare to draw text on the image
        draw = ImageDraw.Draw(background)

        # Load font
        font = ImageFont.truetype(self.font_path, size=80)

        # Wrap text based on the max width
        lines = self.wrap_text(text, font, draw)

        # Calculate the total height of the wrapped text block
        line_heights = []
        for line in lines:
            x0, y0, x1, y1 = draw.textbbox((0, 0), line, font=font)
            line_height = y1 - y0
            line_heights.append(line_height)

        # Calculate total text height including line spacing
        total_text_height = sum(line_heights)
        total_line_spacing = sum([line_height * (line_spacing_factor - 1) for line_height in line_heights[:-1]])
        total_text_height += total_line_spacing

        # Start Y position
        start_y = (background.height - total_text_height) // 2  # Center vertically

        # Draw each line of text
        text_color = (0, 0, 0)  # Black text
        for i, line in enumerate(lines):
            x0, y0, x1, y1 = draw.textbbox((0, 0), line, font=font)
            line_height = y1 - y0
            text_width = x1 - x0
            text_x = (background.width - text_width) // 2  # Center horizontally
            draw.text((text_x, start_y), line, fill=text_color, font=font)
            # Move down to the next line
            if i < len(lines) - 1:
                start_y += line_height * line_spacing_factor
            else:
                start_y += line_height  # Last line, no extra spacing needed

        # Save the image
        background.save(output_path)
        print(f"Image saved to {output_path}")
        return output_path

# Example usage
if __name__ == "__main__":
    # Initialize the JokeImageCreator
    joke_image_creator = JokeImageCreator(font_path='Arial.ttf', max_width=900)

    # Create an image with joke text
    joke_text = "Why don't skeletons fight each other? They don't have the guts!"
    output_file = "joke_image.jpg"
    background_image = "background.jpg"
    joke_image_creator.create_image(joke_text, output_file, background_image)
