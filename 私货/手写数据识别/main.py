from PIL import Image
import numpy as np
import json


def img_to_black_array(img_file):
    result_array = []
    img = Image.open(img_file)
    img = img.resize((270, 270))
    img_array = np.array(img)
    for col in img_array:
        result_array.append('')
        for pixel in col:
            if pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200:
                result_array[-1] += '0'
            else:
                result_array[-1] += '1'
    return result_array


def encode_list(ls):
    def encode_item(item):
        res, cnt, current_number = '', 0, item[0]
        for char in item:
            if char == current_number:
                cnt += 1
            else:
                res += str(cnt) + ('x' if current_number == '0' else 'y')
                cnt, current_number = 1, char
        res += str(cnt) + ('x' if current_number == '0' else 'y')
        return res

    return [encode_item(item) for item in ls]


def decode_list(ls):
    def decode_item(item):
        i, cnt, res = 0, 0, ''
        while i < len(item):
            while item[i].isdigit():
                cnt = cnt * 10 + int(item[i])
                i += 1
            res += ('0' * cnt if item[i] == 'x' else '1' * cnt)
            i += 1
            cnt = 0
        return res

    return [decode_item(item) for item in ls]


def memory_img(answer, img_file):
    img_array = img_to_black_array(img_file)
    with open("data/memory.json", "r") as f:
        data = json.load(f)
        data[answer].append(encode_list(img_array))
    with open("data/memory.json", "w") as f:
        json.dump(data, f)
    memory_to_weight()
    print(f'记忆成功, {answer} 已添加')


def calculate_familiarity(input_list, target_list):
    target_list = decode_list(target_list)
    result = 0
    total_num = len(input_list) * len(input_list[0])
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            if input_list[i][j] == target_list[i][j]:
                if input_list[i][j] == '1':
                    result += 500 / total_num
                else:
                    result += 1 / total_num
    return result


def recognize_img(img_file):
    img_array = img_to_black_array(img_file)
    ans_dict = {"0": None, "1": None, "2": None, "3": None, "4": None, "5": None, "6": None, "7": None, "8": None,
                "9": None}
    with open("data/memory.json", "r") as f:
        data = json.load(f)
        max_familiarity_key, max_familiarity = '0', 0
        for key in data.keys():
            if len(data[key]) == 0:
                continue
            sum = 0
            for item in data[key]:
                sum += calculate_familiarity(img_array, item)
            result = sum / len(data[key])
            if result > max_familiarity:
                max_familiarity = result
                max_familiarity_key = key
            ans_dict[key] = result
            f.close()
    print(f'识别结果为: {max_familiarity_key}')

    # 降序输出结果
    for key in sorted(ans_dict, key=ans_dict.get, reverse=True):
        print(f'{key}: {ans_dict[key]}')


def show_memory_number():
    with open("data/memory.json", "r") as f:
        data = json.load(f)
        for key in data.keys():
            print(f'{key}: {len(data[key])}')


def memory_to_weight_array(ls):
    weight_array = [[0 for _ in range(270)] for _ in range(270)]
    one_count = 0
    for item in ls:
        item = decode_list(item)
        for s in item:
            one_count += s.count('1')
    
    for item in ls:
        item = decode_list(item)
        for i in range(len(item)):
            for j in range(len(item[0])):
                if item[i][j] == '1':
                    weight_array[i][j] += 1
    
    for i in range(270):
        for j in range(270):
            weight_array[i][j] = weight_array[i][j] / one_count
    
    return weight_array


def memory_to_weight():
    with open("data/weight_array.json", "r") as f:
        weight_array = json.load(f)
        f.close()
    with open("data/memory.json", "r") as f:
        data = json.load(f)
        for key in data.keys():
            weight_array[key] = memory_to_weight_array(data[key])
        f.close()
    with open("data/weight_array.json", "w") as f:
        json.dump(weight_array, f)
        f.close()


def calculate_weight(input_list, weight_array):
    multiply_array = input_list * weight_array
    result = 0
    for i in range(len(multiply_array)):
        if weight_array[i].sum() == 0:
            continue
        if multiply_array[i].sum() / weight_array[i].sum() > 0.06:
            result += 1.8
        else:
            result -= 0.5

    for j in range(len(multiply_array[0])):
        if weight_array[:, j].sum() == 0:
            continue
        if multiply_array[:, j].sum() / weight_array[:, j].sum() > 0.06:
            result += 1.8
        else:
            result -= 0.5

    result = (result / 2) / len(weight_array) * 100
    return result


def recognize_weight(img_file):
    ans_dict = {"0": None, "1": None, "2": None, "3": None, "4": None, "5": None, "6": None, "7": None, "8": None,
                "9": None}
    img_array = img_to_black_array(img_file)
    for i in range(len(img_array)):
        img_array[i] = list(map(int, img_array[i]))
    img_array = np.array(img_array)

    with open("data/weight_array.json", "r") as f:
        data = json.load(f)
        for key in data.keys():
            data[key] = np.array(data[key])
            ans_dict[key] = calculate_weight(img_array, data[key])
        f.close()

    print(f'识别结果为: {max(ans_dict, key=ans_dict.get)}')
    for key in sorted(ans_dict, key=ans_dict.get, reverse=True):
        print(f'【{key}】{round(ans_dict[key], 4)}%')


def show_memory_img():
    new_img = Image.new("RGB", (270 * 10, 270), (255, 255, 255))
    with open("data/weight_array.json") as f:
        data = json.load(f)
        for key in data.keys():
            weight_array = np.array(data[key])
            for i in range(len(weight_array)):
                for j in range(len(weight_array[0])):
                    if weight_array[i][j] > 0.0000875:
                        new_img.putpixel((j + 270 * int(key), i), (0, 0, 0))
    f.close()
    new_img.show()


if __name__ == "__main__":
    recognize_weight("input/5-3.jpg")
