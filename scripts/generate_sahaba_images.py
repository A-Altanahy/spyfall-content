import os
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# Configuration
names = [
    ("abu_bakr", "أبو بكر الصديق"),
    ("umar", "عمر بن الخطاب"),
    ("uthman", "عثمان بن عفان"),
    ("ali", "علي بن أبي طالب")
]

output_dir = "/Users/abdullah/Development/projects/spyfall-content/content/sahaba"
os.makedirs(output_dir, exist_ok=True)

# Image settings
width, height = 512, 512
bg_color = (20, 20, 30) # Dark blue-ish grey
text_color = (0, 255, 255) # Cyan/Neon
font_size = 60

# Try to load a font that supports Arabic
font_path = "/System/Library/Fonts/GeezaPro.ttc" # Common on macOS
try:
    font = ImageFont.truetype(font_path, font_size)
except:
    print(f"Could not load {font_path}, trying Arial")
    try:
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)
    except:
        print("Could not load Arial, using default")
        font = ImageFont.load_default()

for filename, text in names:
    # Create image
    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Reshape and reorder Arabic text
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    
    # Calculate text position to center it
    # getbbox returns (left, top, right, bottom)
    bbox = d.textbbox((0, 0), bidi_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    
    # Draw text
    d.text((x, y), bidi_text, font=font, fill=text_color)
    
    # Add a "neon" glow effect (simple stroke for now)
    # For a real glow we'd need blur, but simple is fine for now
    
    # Save
    save_path = os.path.join(output_dir, f"{filename}.png")
    img.save(save_path)
    print(f"Saved {save_path}")
