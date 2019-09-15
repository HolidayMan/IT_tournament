from PIL import Image
import array
ORIGINAL = Image.open('temp.jpg')
AREA = 16 # будет исследоваться квадрат 16х16 пикселей
ans_img = Image.new('RGB', (200, 200)) # создание нового постого
START_PIXEL = (85, 114) # отсчет начнется с этого пикселя вправо и вниз


matrix = []
for i in range(AREA): # создается массив пикселей, которые исследуются
	for j in range(AREA):
		matrix.append((START_PIXEL[0]+i, START_PIXEL[1]+j))


rs = array.array('h', []) # массивы с цветовыми каналами каждого пикселя
gs = array.array('h', [])
bs = array.array('h', [])
for pixel in matrix:
	r, g, b = ORIGINAL.getpixel(pixel)
	rs.append(r)
	gs.append(g)
	bs.append(b)
average_color_pixel = (sum(rs)//len(rs), sum(gs)//len(gs), sum(bs)//len(bs)) # находим средний цвет пикселей из исследуемой области

# сделано для демонстрации исследуемого квадрата
area_img = ORIGINAL.crop((*START_PIXEL, START_PIXEL[0]+AREA, START_PIXEL[1]+AREA)) # вырезаем исследуемый квадрат
area_img.save('area.jpg') # сохраняем исследуемый квадрат 

for i in range(200): # заполнение пустого изображения цветом пикселя average_color_pixel
	for j in range(200):
		ans_img.putpixel((i, j), average_color_pixel)
ans_img.save('ans.jpg')

