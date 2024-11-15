import requests


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


url = "https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt"

content_file = GetFileRequest.get_file(url)
file_path = "artykul.txt"
SaveFile.save(file_path, content_file)