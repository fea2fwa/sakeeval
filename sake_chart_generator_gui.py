import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass, field
from typing import List, Tuple

# --- This section is adapted from sakeblog-charts-creation.py ---

# Chart layout and style settings
@dataclass
class ChartLayout:
    simple_left: int = 274
    simple_right: int = 835
    simple_top: int = 110
    simple_bottom: int = 608
    star_size: int = 12
    adv_left: int = 222
    adv_right: int = 1270
    adv_wine_yeast_offset: int = 22
    line_width: int = 8
    line_color: str = "orange"
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
            print(f"Warning: Font file not found. Using default font.")
            return ImageFont.load_default()
        return ImageFont.truetype(font_path, self.font_size)

# Drawing Functions
def create_sake_simple_chart(layout: ChartLayout, params: dict, text: str, base_image_path: str, output_path: str):
    with Image.open(base_image_path) as image:
        draw = ImageDraw.Draw(image)
        font = layout.get_font()
        x_pct = params["dry_or_sweet"]["value"]
        y_pct = params["fruity_or_rich"]["value"]
        x = layout.simple_left + (layout.simple_width * x_pct / 100)
        y = layout.simple_top + (layout.simple_height * y_pct / 100)
        size = layout.star_size
        draw.polygon([(x - size, y), (x, y - size), (x + size, y), (x, y + size)], fill="blue")
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = x - (text_width / 2)
        text_y = y - size - text_height
        draw.text((text_x, text_y), text, fill=layout.font_color, font=font)
        image.save(output_path)

def _draw_dotted_line(draw, start: Tuple[float, float], end: Tuple[float, float], color: str, width: int):
    line_length = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
    dots = int(line_length / 12)
    if dots == 0: return
    for i in range(dots):
        seg_start_x = start[0] + (end[0] - start[0]) * i / dots
        seg_start_y = start[1] + (end[1] - start[1]) * i / dots
        seg_end_x = start[0] + (end[0] - start[0]) * (i + 0.5) / dots
        seg_end_y = start[1] + (end[1] - start[1]) * (i + 0.5) / dots
        draw.line([(seg_start_x, seg_start_y), (seg_end_x, seg_end_y)], fill=color, width=width)

def draw_chart_lines(layout: ChartLayout, lines: List[dict], base_image_path: str, output_path: str):
    with Image.open(base_image_path) as img:
        draw = ImageDraw.Draw(img)
        for line_info in lines:
            start, end, line_type = line_info["start"], line_info["end"], line_info["style"]
            if line_type == "solid":
                draw.line([start, end], fill=layout.line_color, width=layout.line_width)
            elif line_type == "dotted":
                _draw_dotted_line(draw, start, end, color=layout.line_color, width=layout.line_width)
        img.save(output_path)

# Chart Definitions
@dataclass
class LineDef:
    param_name: str; y_start: int; y_end: int; x_offset: int = 0

@dataclass
class ChartDef:
    name: str; base_image: str; output_image: str; line_defs: List[LineDef]

def get_chart_definitions(layout: ChartLayout, params: dict) -> List[dict]:
    def get_x_coord(param_name: str, offset: int = 0) -> float:
        return layout.adv_left + (layout.adv_width * params[param_name]["value"] / 100) + offset
    chart_defs = [
        ChartDef("basic_sake", "basic.png", "basic-lined.png", [LineDef("saketype", 2, 100), LineDef("rice", 100, 202), LineDef("fstarter", 202, 305), LineDef("fruity_or_rich", 340, 460)]),
        ChartDef("advanced_sake", "advanced.png", "advanced-lined.png", [LineDef("saketype", 2, 100), LineDef("rice", 100, 202), LineDef("fstarter", 202, 305), LineDef("yeast", 305, 398), LineDef("fruity_or_rich", 398, 515), LineDef("amino", 515, 575), LineDef("acid", 575, 635), LineDef("svm", 635, 695), LineDef("dry_or_sweet", 695, 800)]),
        ChartDef("basic_wine", "basic_wine.png", "basic_wine-lined.png", [LineDef("saketype", 2, 100), LineDef("rice", 100, 202), LineDef("fstarter", 202, 305), LineDef("dry_or_sweet", 325, 550)]),
        ChartDef("advanced_wine", "advanced_wine.png", "advanced_wine-lined.png", [LineDef("saketype", 2, 100), LineDef("rice", 100, 202), LineDef("fstarter", 202, 305), LineDef("yeast", 305, 390, x_offset=layout.adv_wine_yeast_offset), LineDef("amino", 390, 485), LineDef("acid", 485, 580), LineDef("svm", 580, 670), LineDef("dry_or_sweet", 670, 780)]),
    ]
    processed_charts = []
    for chart_def in chart_defs:
        lines_to_draw = []
        for line_def in chart_def.line_defs:
            x_coord = get_x_coord(line_def.param_name, line_def.x_offset)
            lines_to_draw.append({"start": (x_coord, line_def.y_start), "end": (x_coord, line_def.y_end), "style": params[line_def.param_name]["style"]})
        processed_charts.append({"base_image": chart_def.base_image, "output_image": chart_def.output_image, "lines": lines_to_draw})
    return processed_charts

# --- GUI Application ---

class ChartGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sake Chart Generator")
        self.geometry("600x500")

        # Default parameters
        self.sake_params = {
            "saketype": {"value": 45, "style": "solid"}, "rice": {"value": 50, "style": "dotted"},
            "fstarter": {"value": 70, "style": "solid"}, "yeast": {"value": 53, "style": "solid"},
            "fruity_or_rich": {"value": 20, "style": "solid"}, "amino": {"value": 82, "style": "solid"},
            "acid": {"value": 67, "style": "dotted"}, "svm": {"value": 51, "style": "solid"},
            "dry_or_sweet": {"value": 100, "style": "solid"},
        }
        self.simple_chart_text = tk.StringVar(value="獺祭45 BY24")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Text input
        text_frame = ttk.LabelFrame(main_frame, text="Simple Chart Text", padding="10")
        text_frame.pack(fill=tk.X, pady=5)
        ttk.Entry(text_frame, textvariable=self.simple_chart_text).pack(fill=tk.X)

        # Sliders for parameters
        sliders_frame = ttk.LabelFrame(main_frame, text="Sake Parameters", padding="10")
        sliders_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.sliders = {}
        for i, (name, data) in enumerate(self.sake_params.items()):
            row_frame = ttk.Frame(sliders_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(row_frame, text=f"{name}:", width=15).pack(side=tk.LEFT)
            
            var = tk.DoubleVar(value=data["value"])
            self.sliders[name] = var
            
            slider = ttk.Scale(row_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=var)
            slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            label = ttk.Label(row_frame, text=f"{data['value']:.0f}", width=4)
            label.pack(side=tk.LEFT)
            
            slider.configure(command=lambda v, l=label: l.config(text=f"{float(v):.0f}"))

        # Generate button
        button = ttk.Button(main_frame, text="Generate Charts", command=self.generate_charts)
        button.pack(pady=10)

    def generate_charts(self):
        # Update params from sliders
        for name, var in self.sliders.items():
            self.sake_params[name]["value"] = var.get()

        try:
            print("Starting chart generation...")
            layout = ChartLayout()

            # 1. Create simple chart
            create_sake_simple_chart(
                layout=layout, params=self.sake_params, text=self.simple_chart_text.get(),
                base_image_path="sake-basic-chart.png", output_path="sake-chart.png"
            )
            print("Saved simple chart to sake-chart.png")

            # 2. Create advanced charts
            chart_definitions = get_chart_definitions(layout, self.sake_params)
            for chart_info in chart_definitions:
                draw_chart_lines(
                    layout=layout, lines=chart_info["lines"],
                    base_image_path=chart_info["base_image"], output_path=chart_info["output_image"]
                )
                print(f"Saved chart to {chart_info['output_image']}")
            
            print("...chart generation complete.")
            messagebox.showinfo("Success", "All charts have been generated successfully!")

        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Required base image not found: {e.filename}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app = ChartGeneratorApp()
    app.mainloop()