from PIL import Image

def convolute(img_matrix, c_matrix, div, offset):
	ans_matrix = []
	margin = len(c_matrix) // 2
	for row in range(margin, len(img_matrix)-margin):
		ans_row = []
		for col in range(margin, len(img_matrix[0])-margin):
			matrix = [i[col-margin:col+margin+1] for i in img_matrix[row-margin:row+margin+1]]
			s = int(sum([matrix[i][j] * c_matrix[i][j] for i in range(len(c_matrix)) for j in range(len(c_matrix[0]))]) // div + offset)
			# s = 0 
			# for row1, row2 in zip(range(row-margin, row+margin+1), range(0, len(c_matrix))):
			# 	for col1, col2 in zip(range(col-margin, col+margin+1), c_matrix[row2]):
			# 		s += img_matrix[row1][col1] * col2
			# s = int(s // div + offset)
			ans_row.append(s)
		ans_matrix.append(ans_row)
	return ans_matrix


def build_matrix_from_image(img):
	width = img.size[0]
	height = img.size[1]
	matrix = []
	for j in range(height):
		row = []
		for i in range(width):
			row.append(img.getpixel((i, j)))
		matrix.append(row)
	return matrix


def build_image_from_matrix(matrix):
	width = len(matrix[0])
	height = len(matrix)
	img = Image.new('L', (width, height))
	for i in range(height):
		for j in range(width):
			img.putpixel((j, i), matrix[i][j])
	return img


def expand_matrix(matrix, margin):
	for j in range(margin):
		for i in range(len(matrix)):
			matrix[i] = [matrix[i][0]] + matrix[i] + [matrix[i][-1]]
		matrix.insert(0, matrix[0])
		matrix.append(matrix[-1])


def convolute_image(img, c_matrix, div, offset):
	r, g, b = map(build_matrix_from_image, img.split())
	margin = len(c_matrix) // 2
	expand_matrix(r, margin)
	expand_matrix(g, margin)
	expand_matrix(b, margin)
	r = build_image_from_matrix(convolute(r, c_matrix, div, offset))
	g = build_image_from_matrix(convolute(g, c_matrix, div, offset))
	b = build_image_from_matrix(convolute(b, c_matrix, div, offset))
	return Image.merge('RGB', (r, g, b))

orig = Image.open('temp.jpg')

gauss_kernel = [[0.000789, 0.006581, 0.013347, 0.006581, 0.000789],
				[0.006581, 0.054901, 0.111345, 0.054901, 0.006581],
				[0.013347, 0.011345, 0.255821, 0.111345, 0.013347],
				[0.006581, 0.054901, 0.111345, 0.054901, 0.006581],
				[0.000789, 0.006581, 0.013347, 0.006581, 0.000789]]

negative_kernel = [[0, 0, 0], # div = 1, offset = 256
				   [0, -1, 0],
				   [0, 0, 0]]


sobel_kernel = [[1, 0, -1], # div = 1, offset = 127
				[2, 0, -2],
				[1, 0, -1]]


relief_kernel = [[-2, -1, 0],
				[-1, 1, 1],
				[0, 1, 2]]


blur_kernel = [	[0, 0, 0, 0, 0], # div = 9, offset = 1
				[0, 1, 1, 1, 0],
				[0, 1, 1, 1, 0],
				[0, 1, 1, 1, 0],
				[0, 0, 0, 0, 0],]


growth_kernel = [	[0, 0, 1, 0, 0], # div = 13, offset = 1
				    [0, 1, 1, 1, 0],
				    [1, 1, 1, 1, 1],
				    [0, 1, 1, 1, 0],
				    [0, 0, 1, 0, 0],]


errosion_kernel = [	[1, 1, 0, 1, 1], # div = 12, offset = 1
				    [1, 0, 0, 0, 1],
				    [0, 0, 0, 0, 0],
				    [1, 0, 0, 0, 1],
				    [1, 1, 0, 1, 1],]


ans_img = convolute_image(orig, errosion_kernel, 12, 0)
ans_img.save('ans.jpg')

