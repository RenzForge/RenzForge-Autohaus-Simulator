from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageTk


DEFAULT_TEXT = "RENZFORGE"
LOCAL_LOGO_PATH = Path(__file__).resolve().parent / "assets" / "logo.svg"
EXTERNAL_LOGO_PATH = Path(
    r"C:\Users\renzl\Documents\Coding Resourcen\WebDesign\renzforge_generator\backend\img\logo.svg"
)
SVG_NS = {"svg": "http://www.w3.org/2000/svg"}


def resolve_logo_path():
    if EXTERNAL_LOGO_PATH.exists():
        return EXTERNAL_LOGO_PATH
    return LOCAL_LOGO_PATH


def _parse_logo(svg_path):
    text = DEFAULT_TEXT
    start_color = "#7c3aed"
    end_color = "#06b6d4"

    try:
        root = ET.parse(svg_path).getroot()
        text_node = root.find(".//svg:text", SVG_NS)
        if text_node is not None and text_node.text:
            text = text_node.text.strip() or DEFAULT_TEXT

        stops = root.findall(".//svg:linearGradient/svg:stop", SVG_NS)
        if len(stops) >= 2:
            start_color = stops[0].attrib.get("stop-color", start_color)
            end_color = stops[-1].attrib.get("stop-color", end_color)
    except ET.ParseError:
        pass

    return text, start_color, end_color


def _pick_font(size):
    candidates = [
        Path(r"C:\Windows\Fonts\arialbd.ttf"),
        Path(r"C:\Windows\Fonts\segoeuib.ttf"),
        Path(r"C:\Windows\Fonts\bahnschrift.ttf"),
    ]

    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def _interpolate(start_rgb, end_rgb, ratio):
    return tuple(
        int(start_rgb[index] + (end_rgb[index] - start_rgb[index]) * ratio)
        for index in range(3)
    )


def _build_gradient(width, height, start_hex, end_hex):
    start_rgb = ImageColor.getrgb(start_hex)
    end_rgb = ImageColor.getrgb(end_hex)
    gradient = Image.new("RGBA", (width, height))
    pixels = gradient.load()

    width_factor = max(width - 1, 1)
    for x_pos in range(width):
        ratio = x_pos / width_factor
        color = _interpolate(start_rgb, end_rgb, ratio) + (255,)
        for y_pos in range(height):
            pixels[x_pos, y_pos] = color
    return gradient


def create_logo_photo(width=520, height=104):
    text, start_color, end_color = _parse_logo(resolve_logo_path())
    font_size = int(height * 0.66)
    font = _pick_font(font_size)

    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x_pos = int((width - text_width) / 2)
    y_pos = int((height - text_height) / 2) - 2

    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).text((x_pos, y_pos), text, font=font, fill=255)

    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_color = ImageColor.getrgb(start_color) + (150,)
    glow.paste(glow_color, (0, 0, width, height), mask=mask.filter(ImageFilter.GaussianBlur(8)))

    glow_two = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_two_color = ImageColor.getrgb(end_color) + (110,)
    glow_two.paste(glow_two_color, (0, 0, width, height), mask=mask.filter(ImageFilter.GaussianBlur(14)))

    gradient = _build_gradient(width, height, start_color, end_color)
    text_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    text_layer.paste(gradient, (0, 0), mask=mask)

    image = Image.alpha_composite(glow_two, glow)
    image = Image.alpha_composite(image, text_layer)
    return ImageTk.PhotoImage(image)
