import requests
from openai import OpenAI

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
            ### Instrukcje do zadania:
                Przekształć poniższą treść artykułu na HTML z odpowiednimi nagłówkami, akapitami oraz miejscami na ilustracje. 
                Dodaj tagi <img> z atrybutem src='image_placeholder(tutaj nmuer ktore to zdjecie np. 1, 2 itd.).jpg' i atrybutem alt opisującym obrazek. 
                Umieść podpisy pod grafikami w tagu <figcaption>. Nie dodawaj CSS ani JS.
            ### Wytyczne do zadania: 
            - Kod HTML jest przeznaczony wyłącznie do wklejenia wewnątrz tagów `<body>` i nie zawiera tagów <body></body>
            - do not add ```html in start and ``` in the end in output            
            ### Treść do przetworzenia:
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