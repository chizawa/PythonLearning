from scipy import ndimage
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def get_char(image, r, g, b, alpha=256):
    gray = r * image[:, :, 0] + g * image[:, :, 1] + b * image[:, :, 2]  # transfer a RGB image to a gray image
    length = len(ascii_char)
    unit = (alpha+1) / length
    return gray/unit


if __name__ == '__main__':

    filename = 'wm.png'
    ori_image = ndimage.imread(filename)
    m, n, _ = ori_image.shape
    index = get_char(ori_image, 0.3, 0.4, 0.3)
    txt = ''
    for i in range(m):
        for j in range(n):
            txt += ascii_char[int(index[i, j])]
        txt += '\n'

    with open('output.txt','w') as f:
        f.write(txt)

