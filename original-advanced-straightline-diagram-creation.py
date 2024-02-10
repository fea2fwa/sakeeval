from PIL import Image, ImageDraw

saketype = 45  # 15:大吟醸 45:吟醸 52:特別純米 60:純米 76:普通
saketype_line = "solid"

rice = 50  # 18:山田錦 50:美山錦 80:五百万石
rice_line ="dotted"

fstarter = 70  # 30:速醸酛 70:山廃 78:生酛
fstarter_line = "solid"

yeast = 53  # 12:1801 23:15(01) 38:9 50:7 53:6 
yeast_line = "solid"

ForR = 100  # 0:Fruit 100:Rice

amino = 82  # 26:1 66:2 82:3
amino_line = "solid"

acid = 67  # 13:4 15:3 26:2 67:1 
acid_line = "dotted"

svm = 51  # 15:-10 51:0 86:10
svm_line = "solid"

DorS = 30  # 0:Dry 100:Sweet

# ラインの一番左のピクセル
av_line_start_left = 222
# ラインの一番右のピクセル
av_line_end_right = 1270
# ラインの一番左から一番右までの長さ
av_line_length = av_line_end_right - av_line_start_left
# パーセンテージを掛けて長さを計算するための定数
av_line_add = av_line_length/100


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
        img.save("advanced-lined.png")
        img.show()

# 描くラインをリストで提供
lines = [
    (av_line_start_left+saketype*av_line_add, 2, av_line_start_left+saketype*av_line_add, 100, saketype_line, 8),  # Dotted line from (start-tupple) to (end-tupple) with thickness 8
    (av_line_start_left+rice*av_line_add, 100, av_line_start_left+rice*av_line_add, 202, rice_line, 8),
    (av_line_start_left+fstarter*av_line_add, 202, av_line_start_left+fstarter*av_line_add, 305, fstarter_line, 8), 
    (av_line_start_left+yeast*av_line_add, 305, av_line_start_left+yeast*av_line_add, 398, yeast_line, 8),
    (av_line_start_left+ForR*av_line_add, 398, av_line_start_left+ForR*av_line_add, 515, "solid", 8),
    (av_line_start_left+amino*av_line_add, 515, av_line_start_left+amino*av_line_add, 575, amino_line, 8), 
    (av_line_start_left+acid*av_line_add, 575, av_line_start_left+acid*av_line_add, 635, acid_line, 8),
    (av_line_start_left+svm*av_line_add, 635, av_line_start_left+svm*av_line_add, 695, svm_line, 8),
    (av_line_start_left+DorS*av_line_add, 695, av_line_start_left+DorS*av_line_add, 800, "solid", 8),
]

draw_custom_lines("advanced.png", lines)
