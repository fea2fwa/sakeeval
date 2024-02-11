from PIL import Image, ImageDraw, ImageFont

ForR = 20  # 0:Fruit 100:Rice
DorS = 30  # 0:Dry 100:Sweet

# ラインの一番左のピクセル
av_line_start_left = 274
# ラインの一番右のピクセル
av_line_end_right = 835
# ラインの一番左から一番右までの長さ
av_line_length = av_line_end_right - av_line_start_left
# パーセンテージを掛けて長さを計算するための定数
av_line_add = av_line_length/100


# ラインの一番上のピクセル
av_line_start_top = 110
# ラインの一番下のピクセル
av_line_end_bottom = 608
# ラインの一番上から一番下までの長さ
av_line_height = av_line_end_bottom - av_line_start_top
# パーセンテージを掛けて長さを計算するための定数
av_line_height_add = av_line_height/100


# 画像の読み込み
image_path = "sake-basic-chart.png"
image = Image.open(image_path)

# 描画オブジェクトの作成
draw = ImageDraw.Draw(image)

# 星マークを描画
x , y = av_line_start_left+av_line_add*DorS, av_line_start_top+av_line_height_add*ForR
size = 12  # 星マークのサイズ
draw.polygon([(x-size, y), (x, y-size), (x+size, y), (x, y+size)], fill="blue")

# テキストを描画
text = "獺祭45 BY24"
# font = ImageFont.truetype("arial.ttf", 20)  # フォントとサイズの指定
font_path = "C:\Windows^Fonts\meiryo.ttc"  # 日本語フォントのパス
font_size = 24
font = ImageFont.truetype(font_path, font_size)
text_width, text_height = draw.textsize(text, font=font)
text_x = x - text_width/2  # テキストのX座標を計算して中央揃えにする
text_y = y - size - text_height  # 星マークの上にテキストを配置
draw.text((text_x, text_y), text, fill="black", font=font)

# 画像の保存
output_path = "sake-chart.png"
image.save(output_path)

# 画像の表示（テスト用）
image.show()
