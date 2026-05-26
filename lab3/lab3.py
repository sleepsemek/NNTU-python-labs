import os
from PIL import Image

def main():
    
    image_file = "new23.png"
    keys_file = "keys23.txt"

    
    if not os.path.exists(image_file):
        print(f"Файл картинки '{image_file}' не найден")
        return
    if not os.path.exists(keys_file):
        print(f"Файл ключей '{keys_file}' не найден")
        return

    print("Декодирование по ключу")
    try:
        coords = []
        with open(keys_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                cleaned_line = line.strip('()')
                parts = cleaned_line.split(',')
                
                if len(parts) == 2:
                    x = int(parts[0].strip())
                    y = int(parts[1].strip())
                    coords.append((x, y))
        
        print(f"Прочитано {len(coords)} координат из {keys_file}")
        
    except:
        print(f"Не удалось прочитать файл ключей")
        return

    try:
        img_1 = Image.open(image_file).convert('RGB')
        pixels_1 = img_1.load()
        
        decoded_message_1 = ""
        for x, y in coords:
            #Извлекаем пиксель
            r, g, b = pixels_1[x, y]
            #Каждый байт текста записан в каждый пиксель синего цвета
            decoded_message_1 += chr(b)
            
        print(f"Закодированное сообщение: {decoded_message_1}")
        
    except:
        print(f"Ошибка при декодировании")
        return


    print("Кодирование и декодирование LSB нулевой бит (b0-B)")
    
    text_to_encode = "NNTU Bayukov Danial" 
    #Символ конца строки, чтобы при раскодировании по нему остановиться
    text_to_encode += '\0' 
    
    #Переводим текст в строку из 0 и 1, по 8 бит на символ
    bits_to_hide = ""
    for char in text_to_encode:
        char_code = ord(char)
        binary_string = format(char_code, '08b')  #Форматируем в 8 битный двоичный вид
        bits_to_hide += binary_string
    
    img_2 = Image.open(image_file).convert('RGB')
    pixels_2 = img_2.load()
    width, height = img_2.size
    
    original_pixels = []
    changed_pixels = []
    
    first_char = text_to_encode[0]
    print(f"Биты первого символа '{first_char}': {bits_to_hide[:8]}")
    
    #Встраиваем биты в картинку
    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index < len(bits_to_hide):
                r, g, b = pixels_2[x, y]
                
                #Сохраняем исходные пиксели для вывода
                if bit_index < 8:
                    original_pixels.append((r, g, b))
                
                #Пишем в нулевой бит синего цвета
                if int(bits_to_hide[bit_index]) == 1:
                    new_b = b | 1
                else:
                    new_b = b & ~1 
                
                #Пишем измененный пиксель обратно
                pixels_2[x, y] = (r, g, new_b)
                
                #Сохраняем измененные пиксели для вывода
                if bit_index < 8:
                    changed_pixels.append((r, g, new_b))
                    
                bit_index += 1
            else:
                break
        if bit_index >= len(bits_to_hide):
            break

    print(f"b. Исходные значения пикселей (RGB):   {original_pixels}")
    print(f"c. Измененные значения пикселей (RGB): {changed_pixels}")
    
    #Декодируем обратно
    decoded_bits = ""
    decoded_text_2 = ""
    is_finished = False
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels_2[x, y]
            
            #Читаем 0 бит синего цвета
            decoded_bits += str(b & 1)
            
            #Как только 8 бит, переводим в символ
            if len(decoded_bits) % 8 == 0:
                char_code = int(decoded_bits[-8:], 2)
                char = chr(char_code)
                
                if char == '\0': #Символ конца сообщения
                    is_finished = True
                    break
                decoded_text_2 += char
                
        if is_finished:
            break

    print(f"Раскодированный текст: {decoded_text_2}")
    
    #Сохраняем стеганографию
    output_name = f"encoded_{image_file}"
    img_2.save(output_name)
    print(f"\nИзображение с закодированным текстом сохранено как '{output_name}'")

if __name__ == "__main__":
    main()
