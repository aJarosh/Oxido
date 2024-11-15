import requests


class GetFileRequest():
    def get_file(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print (e.response.text)
        return response.content
    
class SaveFile():
    def save(file_path, content):
        try:
            with open(file_path, 'wb') as file:
                file.write(content)
            print('Succesfully saved as: 'f'{file_path}')
        except IOError as e:
            print('Error occured during saving the file: {e}')


url = "https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt"
content_file = GetFileRequest.get_file(url)
file_path = "artykul.txt"
SaveFile.save(file_path, content_file)