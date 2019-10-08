import sys

from imageio import imread
from scipy.linalg import norm
from scipy import sum, average

def main():
    file1, file2 = sys.argv[1:3]
    # прочитать картинки как 2D массивы (преобразовать в оттенки серого для простоты)
    img1 = to_grayscale(imread(file1).astype(float))
    img2 = to_grayscale(imread(file2).astype(float))
    # сравнить
    n_m, n_0 = compare_images(img1, img2)
    print("First norm:", n_m, "/ per pixel:", n_m/img1.size)
    print("Second norm:", n_0, "/ per pixel:", n_0*1.0/img1.size)

def compare_images(img1, img2): # сравнить изображения
    # нормализовать, чтобы компенсировать разницу экспозиции
    img1 = normalize(img1)
    img2 = normalize(img2)
    # рассчитать разницу и ее нормы
    diff = img1 - img2  # поэлементно для массивов scipу
    m_norm = sum(abs(diff))  # First norm
    z_norm = norm(diff.ravel(), 0)  # Second norm
    return (m_norm, z_norm)

def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # среднее по последней оси (цветные каналы)
    else:
        return arr

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng


def test():
    pass


if __name__ == "__main__":
    main()

