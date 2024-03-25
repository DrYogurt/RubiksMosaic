import numpy as np
import cv2


def posterize(image, levels):
    # Reduce the image to 'levels' colors
    factor = 256 // levels
    return (image // factor) * factor


def floyd_steinberg_dithering(image, palette):
    for y in range(image.shape[0] - 1):
        for x in range(image.shape[1] - 1):
            old_pixel = image[y, x, :]
            new_pixel = palette[np.argmin(np.sqrt(np.sum((palette.astype(np.float32) - old_pixel.astype(np.float32)) ** 2, axis=1)))]
            image[y, x, :] = new_pixel
            quant_error = old_pixel - new_pixel
            image[y, x+1, :] += quant_error * 7 // 16
            image[y+1, x-1, :] += quant_error * 3 // 16
            image[y+1, x, :] += quant_error * 5 // 16
            image[y+1, x+1, :] += quant_error * 1 // 16
    return image


def scale_img(img, new_size):
    return cv2.resize(img, (int(new_size * img.shape[1] / img.shape[0]), new_size))


def main():
    
    FILENAME = '/home/dryogurt/Desktop/profile_clickup.jpg'

    image = cv2.imread(FILENAME)
    
    image = scale_img(image, 200)
    
    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    palette_rgb = np.array([
       [255, 0, 0],    # Red
       [0, 255, 0],    # Green
        [0, 0, 255],    # Blue
        [255, 255, 0],  # Yellow
        [255, 255, 255],  # White
        [255, 165, 0],  # Orange
    ], dtype='uint8')

    palette_lab = cv2.cvtColor(palette_rgb.reshape(1, -1, 3), cv2.COLOR_RGB2LAB).reshape(-1, 3)


    posterized_image = posterize(image_lab.copy(), levels=10)  # Adjust levels as needed
    posterized_image_rgb = cv2.cvtColor(posterized_image, cv2.COLOR_LAB2BGR)

    cv2.imwrite(f"posterized.jpg", posterized_image_rgb)
    #palette_lab_float = palette_lab.astype('float64')
    dithered_image = floyd_steinberg_dithering(posterized_image.copy(), palette_lab)
    dithered_image_rgb = cv2.cvtColor(dithered_image, cv2.COLOR_LAB2BGR)

    cv2.imwrite(f"dithered.jpg", dithered_image_rgb)



if __name__ == "__main__":
    main()
