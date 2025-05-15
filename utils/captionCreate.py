import os
from PIL import Image, ImageDraw, ImageFont
from utils.audioGenerator import soundifyPost

# Use absolute path to your font file
FONT_BOLD_PATH = os.path.abspath("assets/fonts/Arial Bold.ttf")

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = f"{current_line} {word}"
        if font.getlength(test_line) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines

def create_title_card(title, user, subreddit, theme, output_folder):
    W, H = 720, 1280
    image = Image.new("RGBA", (W, H), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(image)

    font_title = ImageFont.truetype(FONT_BOLD_PATH, 40)
    font_meta = ImageFont.truetype(FONT_BOLD_PATH, 30)

    draw.text((50, 100), subreddit, font=font_meta, fill="gray")
    draw.text((50, 150), f"u/{user}", font=font_meta, fill="gray")

    lines = wrap_text(title, font_title, W - 100)
    y = 250
    for line in lines:
        w = font_title.getlength(line)
        draw.text(((W - w) / 2, y), line, font=font_title, fill="white", stroke_width=2, stroke_fill="black")
        y += 60

    image.save(os.path.join(output_folder, "title.png"))

def create_comment_card(user, text, index, theme, output_folder):
    W, H = 720, 200
    image = Image.new("RGBA", (W, H), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(FONT_BOLD_PATH, 30)
    draw.text((20, 20), f"u/{user}", font=font, fill="gray")

    lines = wrap_text(text.strip(), font, W - 40)
    y = 60
    for line in lines:
        draw.text((20, y), line, font=font, fill="white")
        y += 40

    image.save(os.path.join(output_folder, f"comment_{index}.png"))
    soundifyPost(text, f"section_{index}", output_folder)
