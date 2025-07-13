import subprocess
import os

def caption_image(image_path):
    while not os.path.exists(image_path):
        print(f"Error: The file {image_path} does not exist.")
        image_path = input("Please enter the path to your image file: ").strip()

    user_description = input("Please descripbe the image: ").strip()    
    
    # Create prompt to send to Ollama
    # prompt = f"describe what you can see in this picture {image_path}"
    prompt = f"Analyze this image of a dish and list each visible ingredient. \
            For each ingredient, estimate the percentage by weight it contributes to the overall dish. \
            Also estimate the total weight of the dish in grams. \
            Present your answer as a list with approximate percentages summing to 100%. \
            Here is also a description of the image: {user_description}. \
            {image_path}"
    
    print("Generating caption with Ollama...")
    
    # Call ollama command
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma3:4b", prompt],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print("Error running Ollama:", result.stderr)
            return None
        
        return result.stdout.strip()
    
    except Exception as e:
        print("Exception occurred:", e)
        return None


def main():
    print("Let's track your food intake!")
    while True:
        image_path = input("\nPlease enter the path to your image file: ").strip()
        caption = caption_image(image_path)
        
        if caption:
            print("Image Caption:")
            print(caption)

if __name__ == "__main__":
    main()
