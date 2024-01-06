from PIL import Image, ImageDraw

def draw_custom_lines(image_path, lines):
    """
    Draw lines with custom settings on an image.

    :param image_path: Path to the image.
    :param lines: List of tuples, each containing (start_x, start_y, end_x, end_y, line_type, width)
                  where line_type is "solid" or "dotted" and width is the line thickness.
    """
    # Open the image
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)

        # Function to draw a dotted line
        def draw_dotted_line(start, end, width):
            line_length = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
            dots = int(line_length / 12)
            for i in range(dots):
                segment_start = (start[0] + (end[0] - start[0]) * i / dots, start[1] + (end[1] - start[1]) * i / dots)
                segment_end = (start[0] + (end[0] - start[0]) * (i + 0.5) / dots, start[1] + (end[1] - start[1]) * (i + 0.5) / dots)
                draw.line([segment_start, segment_end], fill="orange", width=width)


        # Iterate over the lines and draw each one
        for start_x, start_y, end_x, end_y, line_type, width in lines:
            start, end = (start_x, start_y), (end_x, end_y)
            if line_type == "solid":
                draw.line([start, end], fill="orange", width=width)
                # draw.line([(start_x, start_y), (end_x, end_y)], fill="orange", width=width)
            elif line_type == "dotted":
                draw_dotted_line(start, end, width)

        # Save or display the modified image
        img.save("advanced_wine-lined.png")
        img.show()

# Example usage
lines = [
    (222, 2, 222, 100, "solid", 8),  # Dotted line from (start-tupple) to (end-tupple) with thickness 8
    (1270, 100, 1270, 202, "solid", 8),
    (450, 202, 450, 305, "solid", 8), 
    (1000, 305, 1000, 390, "solid", 8),
    (300, 390, 300, 482, "solid", 8),
    (400, 482, 400, 575, "solid", 8), 
    (500, 575, 500, 665, "solid", 8),
    (600, 665, 600, 850, "solid", 8),
]
draw_custom_lines("advanced_wine.png", lines)
