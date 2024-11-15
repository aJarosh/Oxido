import requests
from openai import OpenAI
import re

class GetFileRequest():
    def get_file(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)
    
class SaveFileTXT():
    def __init__(self, file_path, content):
        self.file_path = file_path
        self._content = content

    def save(self):
        if self._content:
            try:
                with open(self.file_path, 'wb') as file:
                    file.write(self._content)
                print(f"Succesfully save file to: {self.file_path}")
            except IOError as e:
                print(f"Error ocured during saving: {e}")
        else:
            print('Content is incorrect')

class SaveFileHTML:
    def __init__(self, file_path, content):
        self.file_path = file_path
        self._content = content

    def save(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(self._content)
            print(f"Succesfully save file to: {self.file_path}")
        except IOError as e:
            print(f"Error ocured during saving: {e}")

class ReadFile():
    def read(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

class OpenAIRequest:
    def __init__(self, api_key, article_content):
        self._api_key = api_key
        self._article_content = article_content

    def generate_html(self):
        prompt = '''
            ### Instructions for the task:
                Convert the following article content into HTML with appropriate headings, paragraphs and image placeholders. 
                Add <img> tags with src=‘image_placeholder(here nmuer which image it is e.g. 1, 2 etc.).jpg’ and an alt attribute describing the image. 
                Place captions under the graphics in the <figcaption> tag. Do not add CSS or JS.
            ### Task guidelines: 
            - in the alt attribute, prepare a hint for the dahlia engine to create an image to match the article 
            - HTML code is only intended to be pasted inside `<body>` tags and does not include <body></body> tags.
            - do not add ``html in start and `` in the end in output            
            ### Content to be processed:
            '''f'''{self._article_content}'''
        
        client = OpenAI(
            api_key = self._api_key
        )
        chat = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt,
                }    
            ],
            model="gpt-4o-mini",
            max_tokens=2000
        )
        return chat.choices[0].message.content


class GetPromptForImage:
    def __init__(self, content):
        self.content = content

    def extract_prompts(self):
        try:
            prompts = re.findall(r'<img [^>]*alt=["\']([^"\']+)["\']', self.content)
            return [prompt.strip() for prompt in prompts if prompt.strip()]
        except Exception as e:
            print(f"An error occurred while extracting prompts: {e}")
            return []


class CreateImagesOpenAI():
    def __init__(self, api_key, prompts):
        self._api_key = api_key
        self._prompts = prompts
    
    
    def create_image(self):
        generated_images_url = []
        for idx, prompt in enumerate(self._prompts, start=1):
            print(f"Generating image {idx}/{len(self._prompts)}: {prompt}")
            client = OpenAI(
            api_key = self._api_key    
            )
            response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
            )
            image_url = response.data[0].url
            generated_images_url.append((prompt, image_url))
            print(f"Image {idx} generated successfully: {image_url}")

        return generated_images_url

class ImageDownloader:
    def __init__(self, url):
        self.url = url

    def is_link_active(self):
        try:
            # Weryfikacja statusu linku bez pobierania całej zawartości
            response = requests.head(self.url)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error checking link: {e}")
            return False

    def download_image(self):
        if not self.is_link_active():
            print("Link is no longer active.")
            return None
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return None

class FileSaver:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_file(self, data):
        try:
            with open(self.file_path, 'wb') as file:
                file.write(data)
            print(f"File saved successfully as {self.file_path}")
        except IOError as e:
            print(f"Error saving file: {e}")

url = "https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt"
content_file = GetFileRequest.get_file(url)
file_path = "artykul.txt"
SaveFileTXT(file_path, content_file).save()
API_KEY = ReadFile.read("API_KEY")
article = ReadFile.read("artykul.txt")
generated_AI = OpenAIRequest(API_KEY, article).generate_html()
#print(generated_AI)
file_path = "artykul.html"
SaveFileHTML(file_path, generated_AI).save()


article = ReadFile.read("artykul.html")
prompt_extractor = GetPromptForImage(article)
prompts = prompt_extractor.extract_prompts()
print("Extracted Prompts:", prompts)
image_generator = CreateImagesOpenAI(API_KEY, prompts)
images = image_generator.create_image()

for x, (prompt, url) in enumerate(images, start=1):
    print(f"Prompt: {prompt}\nGenerated Image URL: {url}")
    file_path = f"image_placeholder{x}.jpg"
    downloader = ImageDownloader(url)
    image_data = downloader.download_image()  
    if image_data:
        saver = FileSaver(file_path)
        saver.save_file(image_data)
    else:
        print(f"Failed to download image from: {url}")