import numpy as np
import cv2

print("Mission Make Geervan Invisible")

cap = cv2.VideoCapture(0)
back = cv2.imread('./image.jpg')

# Check if the background image is loaded correctly
if back is None:
    print("Error: Background image not found or could not be loaded.")
    exit()

# Function to convert RGB to HSV
def rgb_to_hsv(r, g, b):
    color_rgb = np.uint8([[[r, g, b]]])
    color_hsv = cv2.cvtColor(color_rgb, cv2.COLOR_BGR2HSV)
    return color_hsv[0][0]

# Define the RGB color
r, g, b = 205, 190, 169  # Given RGB values for cream color

# Convert to HSV
hsv_color = rgb_to_hsv(r, g, b)
h, s, v = hsv_color

# Define a range around the HSV color (adjust as needed)
hue_range = 10
saturation_range = 40
value_range = 40

lower_hsv = np.array([90, 50, 70])
upper_hsv = np.array([128, 255, 255])
print("Lower HSV Range:", lower_hsv)
print("Upper HSV Range:", upper_hsv)

while cap.isOpened():
    ret, frame = cap.read()  # Take each frame

    if ret:
        # Resize the background image to match the frame size
        back_resized = cv2.resize(back, (frame.shape[1], frame.shape[0]))

        # Convert frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV values to get only the desired color
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        
        # All things of the target color
        part1 = cv2.bitwise_and(back_resized, back_resized, mask=mask)

        mask_inv = cv2.bitwise_not(mask)
        # All things not of the target color
        part2 = cv2.bitwise_and(frame, frame, mask=mask_inv)

        # Combine the two parts
        combined = cv2.add(part1, part2)

        # Display the result
        cv2.imshow("cloak", combined)

        if cv2.waitKey(5) == ord('q'):  # Press 'Q' to exit
            break

cap.release()
cv2.destroyAllWindows()
