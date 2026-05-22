import cv2
import numpy as np
import os
import re

# ------------------------------
# Load Image
# ------------------------------
image_path = "ai-churns-out-funnier.jpg"  
original = cv2.imread(image_path)

if original is None:
    print("Error: Could not load image.")
    exit()

original = cv2.resize(original, (800, 600))

# Working image
image = original.copy()

# ------------------------------
# Color Channel Intensities
# ------------------------------
red_intensity = 0
green_intensity = 0
blue_intensity = 0

step = 20

# ------------------------------
# Function to Apply Filters
# ------------------------------
def apply_filters(img, r, g, b):
    filtered = img.copy().astype(np.int16)

    # OpenCV uses BGR format
    filtered[:, :, 2] = np.clip(filtered[:, :, 2] + r, 0, 255)  # Red
    filtered[:, :, 1] = np.clip(filtered[:, :, 1] + g, 0, 255)  # Green
    filtered[:, :, 0] = np.clip(filtered[:, :, 0] + b, 0, 255)  # Blue

    return filtered.astype(np.uint8)


# ------------------------------
# Save Image Function
# ------------------------------
def save_image(img):
    filename = input("Enter filename to save image: ")

    # Remove invalid characters
    filename = re.sub(r'[^a-zA-Z0-9_-]', '_', filename)

    if filename == "":
        filename = "filtered_image"

    folder = "images"
    os.makedirs(folder, exist_ok=True)

    save_path = os.path.join(folder, filename + ".png")

    cv2.imwrite(save_path, img)
    print(f"Image saved successfully at: {save_path}")


# ------------------------------
# Instructions
# ------------------------------
print("\n======= KEY CONTROLS =======")
print("r  -> Apply Red Tint")
print("g  -> Apply Green Tint")
print("b  -> Apply Blue Tint")
print("i  -> Increase Red Intensity")
print("d  -> Decrease Blue Intensity")
print("UP ARROW    -> Increase Green Intensity")
print("DOWN ARROW  -> Decrease Red Intensity")
print("s  -> Save Image")
print("q  -> Quit")
print("============================\n")


# ------------------------------
# Main Loop
# ------------------------------
while True:

    # Apply current filters
    image = apply_filters(original, red_intensity, green_intensity, blue_intensity)

    # Display intensities on screen
    display_text = (
        f"Red: {red_intensity} | "
        f"Green: {green_intensity} | "
        f"Blue: {blue_intensity}"
    )

    cv2.putText(
        image,
        display_text,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow("Real-Time Color Filter", image)

    key = cv2.waitKeyEx(1)

    # Quit
    if key == ord('q'):
        print("Exiting application...")
        break

    # Save image
    elif key == ord('s'):
        save_image(image)

    # Apply red tint
    elif key == ord('r'):
        red_intensity += step
        print(f"Red Tint Applied: {red_intensity}")

    # Apply green tint
    elif key == ord('g'):
        green_intensity += step
        print(f"Green Tint Applied: {green_intensity}")

    # Apply blue tint
    elif key == ord('b'):
        blue_intensity += step
        print(f"Blue Tint Applied: {blue_intensity}")

    # Increase red intensity
    elif key == ord('i'):
        red_intensity += step
        print(f"Red Intensity Increased: {red_intensity}")

    # Decrease blue intensity
    elif key == ord('d'):
        blue_intensity -= step
        print(f"Blue Intensity Decreased: {blue_intensity}")

    # UP ARROW = Increase green intensity
    elif key == 2490368:
        green_intensity += step
        print(f"Green Intensity Increased: {green_intensity}")

    # DOWN ARROW = Decrease red intensity
    elif key == 2621440:
        red_intensity -= step
        print(f"Red Intensity Decreased: {red_intensity}")

    # Limit intensity values
    red_intensity = max(-255, min(255, red_intensity))
    green_intensity = max(-255, min(255, green_intensity))
    blue_intensity = max(-255, min(255, blue_intensity))


# Close all windows
cv2.destroyAllWindows()
