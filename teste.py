import cv2
import numpy as np
from PIL import Image
import threading
import keyboard
import time

#Do the convolution
def convolution(image, kernel):
    width, height = image.size
    result = Image.new("L", (width, height))  #new grayscale image the same size as the input image
    
    #walks each pixel in the image, excluding the 1-pixel border
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            pixel_sum = 0
            #walks the elements of the 3x3 kernel to calculate the resulting pixel value
            for i in range(3):
                for j in range(3):
                    pixel_sum += image.getpixel((x - 1 + i, y - 1 + j)) * kernel[i][j]
            
            #sets the pixel value in the new image after convolution
            result.putpixel((x, y), min(max(int(abs(pixel_sum)), 0), 255))  #ensuring the pixel value is in the range [0, 255]
    
    return result

#Apply a limit on the magnitude of calculated borders
def apply_threshold(image, threshold):
    width, height = image.size
    thresholded = Image.new("L", (width, height))  #creates a new grayscale image the same size as the input image
    
    #walks each pixel in the image to apply the threshold
    for x in range(width):
        for y in range(height):
            pixel_value = image.getpixel((x, y))
            if pixel_value >= threshold:
                thresholded.putpixel((x, y), 255)  #sets to white if the value is greater than or equal to the threshold
            else:
                thresholded.putpixel((x, y), 0)  #sets to black if the value is less than the threshold
    
    return thresholded

#Finds corners with 90 degree angles
def find_corners(image):
    corners = np.zeros_like(image, dtype=np.uint8)  #creates array of zeros the same size as the image
    for x in range(1, image.width - 1):
        for y in range(1, image.height - 1):
            if image.getpixel((x, y)) == 255:  #checks if the pixel is a highlighted corner
                #checks if the surrounding pixels form a 90 degree angle
                if (
                    image.getpixel((x - 1, y)) == 255
                    and image.getpixel((x + 1, y)) == 255
                    and image.getpixel((x, y - 1)) == 255
                    and image.getpixel((x, y + 1)) == 255
                ):
                    corners[y, x] = 255  #sets the pixel to white in the corner matrix
    return corners

#Use webcam to capture images 
cap = cv2.VideoCapture(0)  
capture_count = 0  #catch counter

def key_capture_thread():
    global is_key_pressed
    while True:
        if keyboard.is_pressed('q'):  #checks if the 'q' key was pressed
            is_key_pressed = True
            break
        time.sleep(0.1)

keyboard_thread = threading.Thread(target=key_capture_thread)
keyboard_thread.start()

is_key_pressed = False
while True:
    ret, frame = cap.read()  
    
    #image conversion to luminance
    luminance_image = 0.2126 * frame[:, :, 2] + 0.7152 * frame[:, :, 1] + 0.0722 * frame[:, :, 0]
    
    #Gaussian filter for smoothing the luminance image
    frame_gray_smoothed = cv2.GaussianBlur(luminance_image, (5, 5), 0)
    
    pil_frame = Image.fromarray(frame_gray_smoothed)
    
    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    border_x = convolution(pil_frame, sobel_x)
    border_y = convolution(pil_frame, sobel_y)

    magnitude = Image.new("L", pil_frame.size)
    for x in range(pil_frame.size[0]):
        for y in range(pil_frame.size[1]):
            gx = border_x.getpixel((x, y))
            gy = border_y.getpixel((x, y))
            magnitude.putpixel((x, y), min(int((gx ** 2 + gy ** 2) ** 0.5), 255))

    threshold_value = 100  
    highlighted_borders = apply_threshold(magnitude, threshold_value)

    corners = find_corners(highlighted_borders)  #find corners

    #saves the border image
    output_path = rf"C:\Shelf_Supervisor\New_images\captured_image_{capture_count}.png"
    cv2.imwrite(output_path, np.array(highlighted_borders))
    print("Saved in:", output_path)

    #check if the 'q' key was pressed to stop the capture
    if is_key_pressed:
        break

    capture_count += 1  #increments the capture counter

cap.release()  #close camera
cv2.destroyAllWindows()  #fecha all OpenCV windows
