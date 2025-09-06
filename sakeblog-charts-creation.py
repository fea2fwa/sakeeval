import os
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass, field
from typing import List, Tuple, Literal

# --- 1. Configuration ---

# Sake parameters
SAKE_PARAMS = {
    "saketype": {"value": 45, "style": "solid"},  # 15:大吟醸 45:吟醸 52:特別純米 60:純米 76:普通
    "rice": {"value": 50, "style": "dotted"},  # 18:山田錦 50:美山錦 80:五百万石
    "fstarter": {"value": 70, "style": "solid"},  # 30:速醸酛 70:山廃 78:生酛
    "yeast": {"value": 53, "style": "solid"},  # 12:1801 23:15(01) 38:9 50:7 53:6
    "fruity_or_rich": {"value": 20, "style": "solid"},  # 0:Fruit 100:Rice
    "amino": {"value": 82, "style": "solid"},  # 26:1 66:2 82:3
    "acid": {"value": 67, "style": "dotted"},  # 13:4 15:3 26:2 67:1
    "svm": {"value": 51, "style": "solid"},  # 15:-10 51:0 86:10
    "dry_or_sweet": {"value": 100, "style": "solid"},  # 0:Dry 100:Sweet
}

# Text to display on the simple chart
SIMPLE_CHART_TEXT = "獺祭45 BY24"

# Chart layout and style settings
@dataclass
class ChartLayout:
    # Simple chart (scatter plot)
    simple_left: int = 274
    simple_right: int = 835
    simple_top: int = 110
    simple_bottom: int = 608
    star_size: int = 12

    # Advanced charts (line graphs)
    adv_left: int = 222
    adv_right: int = 1270
    adv_wine_yeast_offset: int = 22 # Offset for yeast line in wine chart
    line_width: int = 8
    line_color: str = "orange"

    # Font settings
    font_path_mac: str = "/Library/Fonts/Arial Unicode.ttf"
    font_path_win: str = "C:/Windows/Fonts/meiryo.ttc"
    font_size: int = 24
    font_color: str = "black"

    @property
    def simple_width(self) -> int:
        return self.simple_right - self.simple_left

    @property
    def simple_height(self) -> int:
        return self.simple_bottom - self.simple_top

    @property
    def adv_width(self) -> int:
        return self.adv_right - self.adv_left

    def get_font(self):
        font_path = self.font_path_mac if os.path.exists(self.font_path_mac) else self.font_path_win
        if not os.path.exists(font_path):
            # Fallback to default font if specified fonts are not found
            print(f"Warning: Font file not found at {self.font_path_mac} or {self.font_path_win}. Using default font.")
            return ImageFont.load_default()
        return ImageFont.truetype(font_path, self.font_size)


# --- 2. Drawing Functions ---

def create_sake_simple_chart(layout: ChartLayout, params: dict, text: str, base_image_path: str, output_path: str):
    """Creates the simple sake chart with a star marker and text."""
    with Image.open(base_image_path) as image:
        draw = ImageDraw.Draw(image)
        font = layout.get_font()

        # Calculate coordinates based on percentages
        x_pct = params["dry_or_sweet"]["value"]
        y_pct = params["fruity_or_rich"]["value"]
        x = layout.simple_left + (layout.simple_width * x_pct / 100)
        y = layout.simple_top + (layout.simple_height * y_pct / 100)

        # Draw star marker
        size = layout.star_size
        draw.polygon([(x - size, y), (x, y - size), (x + size, y), (x, y + size)], fill="blue")

        # Draw text
        # Use textbbox for accurate size calculation (replaces deprecated textsize)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        text_x = x - (text_width / 2)
        text_y = y - size - text_height # Position text above the star
        draw.text((text_x, text_y), text, fill=layout.font_color, font=font)

        image.save(output_path)
        print(f"Saved simple chart to {output_path}")
        # image.show() # Uncomment for testing

def _draw_dotted_line(draw, start: Tuple[float, float], end: Tuple[float, float], color: str, width: int):
    """Helper function to draw a dotted line."""
    line_length = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
    dots = int(line_length / 12) # Adjust density of dots here
    if dots == 0:
        return
    for i in range(dots):
        # Calculate start and end of each small dash
        seg_start_x = start[0] + (end[0] - start[0]) * i / dots
        seg_start_y = start[1] + (end[1] - start[1]) * i / dots
        seg_end_x = start[0] + (end[0] - start[0]) * (i + 0.5) / dots
        seg_end_y = start[1] + (end[1] - start[1]) * (i + 0.5) / dots
        draw.line([(seg_start_x, seg_start_y), (seg_end_x, seg_end_y)], fill=color, width=width)


def draw_chart_lines(layout: ChartLayout, lines: List[dict], base_image_path: str, output_path: str):
    """Draws solid or dotted lines on a base image for advanced charts."""
    with Image.open(base_image_path) as img:
        draw = ImageDraw.Draw(img)

        for line_info in lines:
            start = line_info["start"]
            end = line_info["end"]
            line_type = line_info["style"]
            
            if line_type == "solid":
                draw.line([start, end], fill=layout.line_color, width=layout.line_width)
            elif line_type == "dotted":
                _draw_dotted_line(draw, start, end, color=layout.line_color, width=layout.line_width)

        img.save(output_path)
        print(f"Saved chart to {output_path}")
        # img.show() # Uncomment for testing


# --- 3. Chart Definitions ---

@dataclass
class LineDef:
    param_name: str
    y_start: int
    y_end: int
    x_offset: int = 0

@dataclass
class ChartDef:
    name: str
    base_image: str
    output_image: str
    line_defs: List[LineDef]

def get_chart_definitions(layout: ChartLayout, params: dict) -> List[dict]:
    """Returns a list of dictionaries, each defining a chart to be generated."""
    
    def get_x_coord(param_name: str, offset: int = 0) -> float:
        return layout.adv_left + (layout.adv_width * params[param_name]["value"] / 100) + offset

    chart_defs = [
        ChartDef(
            name="basic_sake",
            base_image="basic.png",
            output_image="basic-lined.png",
            line_defs=[
                LineDef("saketype", 2, 100),
                LineDef("rice", 100, 202),
                LineDef("fstarter", 202, 305),
                LineDef("fruity_or_rich", 340, 460),
            ]
        ),
        ChartDef(
            name="advanced_sake",
            base_image="advanced.png",
            output_image="advanced-lined.png",
            line_defs=[
                LineDef("saketype", 2, 100),
                LineDef("rice", 100, 202),
                LineDef("fstarter", 202, 305),
                LineDef("yeast", 305, 398),
                LineDef("fruity_or_rich", 398, 515),
                LineDef("amino", 515, 575),
                LineDef("acid", 575, 635),
                LineDef("svm", 635, 695),
                LineDef("dry_or_sweet", 695, 800),
            ]
        ),
        ChartDef(
            name="basic_wine",
            base_image="basic_wine.png",
            output_image="basic_wine-lined.png",
            line_defs=[
                LineDef("saketype", 2, 100),
                LineDef("rice", 100, 202),
                LineDef("fstarter", 202, 305),
                LineDef("dry_or_sweet", 325, 550),
            ]
        ),
        ChartDef(
            name="advanced_wine",
            base_image="advanced_wine.png",
            output_image="advanced_wine-lined.png",
            line_defs=[
                LineDef("saketype", 2, 100),
                LineDef("rice", 100, 202),
                LineDef("fstarter", 202, 305),
                LineDef("yeast", 305, 390, x_offset=layout.adv_wine_yeast_offset),
                LineDef("amino", 390, 485),
                LineDef("acid", 485, 580),
                LineDef("svm", 580, 670),
                LineDef("dry_or_sweet", 670, 780),
            ]
        ),
    ]

    # Convert LineDefs to the format expected by draw_chart_lines
    processed_charts = []
    for chart_def in chart_defs:
        lines_to_draw = []
        for line_def in chart_def.line_defs:
            x_coord = get_x_coord(line_def.param_name, line_def.x_offset)
            lines_to_draw.append({
                "start": (x_coord, line_def.y_start),
                "end": (x_coord, line_def.y_end),
                "style": params[line_def.param_name]["style"],
            })
        processed_charts.append({
            "base_image": chart_def.base_image,
            "output_image": chart_def.output_image,
            "lines": lines_to_draw,
        })
    return processed_charts


# --- 4. Main Execution ---

def main():
    """
    Main function to generate all sake charts.
    """
    print("Starting chart generation...")
    
    # Initialize layout and parameters
    layout = ChartLayout()
    
    # 1. Create the simple scatter plot chart
    create_sake_simple_chart(
        layout=layout,
        params=SAKE_PARAMS,
        text=SIMPLE_CHART_TEXT,
        base_image_path="sake-basic-chart.png",
        output_path="sake-chart.png"
    )

    # 2. Create the advanced line charts
    chart_definitions = get_chart_definitions(layout, SAKE_PARAMS)
    for chart_info in chart_definitions:
        draw_chart_lines(
            layout=layout,
            lines=chart_info["lines"],
            base_image_path=chart_info["base_image"],
            output_path=chart_info["output_image"]
        )
        
    print("...chart generation complete.")


if __name__ == "__main__":
    main()