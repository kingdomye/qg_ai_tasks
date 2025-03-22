import tkinter as tk
import main
from PIL import Image, ImageDraw
from PIL import ImageTk

# 初始化图像和绘图对象
image = Image.new("RGB", (270, 270), 'white')  # '1'表示黑白图像
draw = ImageDraw.Draw(image)

# 创建Tkinter窗口
root = tk.Tk()
root.title("手绘输入")

# 画布大小
canvas_width = 270
canvas_height = 270

# 创建画布
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# 开始绘制的标志
drawing = False

# 最后绘制点的坐标
last_x = None
last_y = None

# 将PIL图像转换为Tkinter图像
tk_image = ImageTk.PhotoImage(image)


# 鼠标点击事件
def start_draw(event):
    global drawing, last_x, last_y
    drawing = True
    last_x = event.x
    last_y = event.y


# 鼠标移动事件
def draw_line(event):
    global draw, last_x, last_y, image, tk_image
    if drawing:
        x = event.x
        y = event.y
        if last_x is not None and last_y is not None:
            draw.line([last_x, last_y, x, y], fill=0, width=5)
            last_x = x
            last_y = y
            # 更新画布上的图像
            tk_image = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, image=tk_image, anchor='nw')
            canvas.image = tk_image  # 保持对图像的引用


# 鼠标释放事件
def stop_draw(event):
    global drawing
    drawing = False


# 清除画布
def clear_canvas():
    global image, draw, tk_image
    image = Image.new("RGB", (270, 270), 'white')
    draw = ImageDraw.Draw(image)
    tk_image = ImageTk.PhotoImage(image)
    canvas.delete('all')  # 删除所有画布上的对象
    canvas.create_image(0, 0, image=tk_image, anchor='nw')
    canvas.image = tk_image  # 保持对图像的引用


# 保存按钮
def save_image():
    global image
    file_name = 'input/' + input_area.get() + '.jpg'
    image.save(file_name)

    global draw, tk_image
    image = Image.new("RGB", (270, 270), 'white')
    draw = ImageDraw.Draw(image)
    tk_image = ImageTk.PhotoImage(image)
    canvas.delete('all')  # 删除所有画布上的对象
    canvas.create_image(0, 0, image=tk_image, anchor='nw')
    canvas.image = tk_image  # 保持对图像的引用

    main.memory_img(input_area.get(), file_name)


def recognize():
    global image
    image.save('input/input.jpg')
    main.recognize_weight('input/input.jpg')


# 数字输入框
input_area = tk.Entry(root)
input_area.pack()

# 添加保存按钮
save_button = tk.Button(root, text="保存图像", command=save_image)
save_button.pack()

# 添加清除按钮
clear_button = tk.Button(root, text="清除画布", command=clear_canvas)
clear_button.pack()

# 添加识别按钮
recognize_button = tk.Button(root, text="识别", command=recognize)
recognize_button.pack()

# 绑定事件
canvas.bind('<B1-Motion>', draw_line)
canvas.bind('<Button-1>', start_draw)
canvas.bind('<ButtonRelease-1>', stop_draw)

# 运行Tkinter主循环
root.mainloop()
