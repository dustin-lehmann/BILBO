from PIL import Image

# Load the uploaded image
input_path = "./hobbitdoor.png"
output_path = "./hobbitdor_small.png"

# Open the image
image = Image.open(input_path)

# Convert to 1-bit monochrome
image = image.convert("1")

# Resize to fit 128x64 display
image = image.resize((60, 60), Image.Resampling.LANCZOS)

# Save the processed image
image.save(output_path)

print(f"Rasterized image saved as {output_path}")
