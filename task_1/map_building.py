from PIL import Image
from math import ceil

class Map:
	def __init__(self, size, photo_size, new_image_name, image_name=None):
		self.photo_size = photo_size
		self.image = Image.new('RGB', (size[0] + photo_size[0], size[1]+photo_size[1]), (255, 255, 255))
		if image_name:
			image = Image.open(image_name)
			image = image.resize((image.size[0]//3, image.size[1]//3))
			image = image.crop((0, 0, *size))
			self.image.paste(image, (0, 0, image.width, image.height))
		self.image.save(new_image_name)
		self.image_name = new_image_name


	def get_fragment(self, photo_point):
		x = ceil(photo_point.x - self.photo_size[0]/2 - 50)
		y = ceil(photo_point.y - self.photo_size[1]/2 - 50)
		return self.image.crop((x, y, x+int(self.photo_size[0]), y+int(self.photo_size[1])))


	def build_image(self, photo_point, fragment):
		x = ceil(photo_point.x - self.photo_size[0]/2 - 50)
		y = ceil(photo_point.y - self.photo_size[1]/2 - 50)
		self.image.paste(fragment, (x, y))
		self.image.save(self.image_name)



