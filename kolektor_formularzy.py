import requests
from bs4 import BeautifulSoup as bs

#%% Glowna funkcja
'''
    Wywoluje sie do momentu wpisania 0
    Pobiera od uzytkownika strone do zeskanowania pod katem formularzy oraz nazwe pliku w jakim maja zostac zapisane dane (.txt)
'''
def main():
    while True:
        url = input("Podaj pelny adres strony (np. https://www.web.com), (0 - zakoncz): ")
        if '0' in url:
            return None
        txt = input("Podaj nazwe pliku txt do ktorego mam zapisac znaelzione formularze (razem z rozszerzeniem): ")
        print("Skanuje strone...")
        html_content = get_html_content(url)
        parse_html_form(html_content, txt)
        print(f"Zapisano znalezione formularze do pliku {txt}")
        

#%% Pobiera hipertekst strony i zwraca go jako string
def get_html_content(url):
    # Pobierz zawartość strony
    response = requests.get(url)
    
    # Sprawdź, czy pobranie było udane (status 200 OK)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Unable to fetch content. Status code: {response.status_code}")
        return None

#%% Wycina fragmenty z formularzami oraz generuje plik txt
'''
    Input:
        html_content - string z hipertekstem
        file_name - nazwa pliku, ktory zostanie utworzony i zostana do niego zapisane dane
    Wynikiem ponizszej funkcji jest plikt txt z zapisanymi danymi o formularzach znalezionych na stronie
'''
def parse_html_form(html_content, file_name):
    soup = bs(html_content, 'html.parser')

    forms = soup.find_all('form')   # Znajdź wszystkie formularze na stronie
    final_text = []                 # Finalna tablica - w kazdej komorce jest oddzielny string
    
    # Iterujemy po wszystkich znalezionych formularzach
    for form in forms:
        # Zapisujemy do tablicy Formularz, Metode jakiej uzywa, Akcje jaka wykonuje (url do jakiego wysyla)
        
        final_text.append("Formularz:")
        final_text.append(f"Metoda: {form.get('method')}")
        final_text.append(f"Akcja: {form.get('action')}")

        # Znajdujemy interesujace nas pola w kazdym formularzu i zapisujemy te dane do tablicy jako oddzielne komorki
        fields = form.find_all(['input', 'textarea', 'select'])
        for field in fields:
            field_type = field.get('type') if field.has_attr('type') else None
            field_name = field.get('name') if field.has_attr('name') else None
            field_value = field.get('value') if field.has_attr('value') else None

            final_text.append(f"  Pole:")
            final_text.append(f"    Typ: {field_type}")
            final_text.append(f"    Nazwa: {field_name}")
            final_text.append(f"    Wartość: {field_value}")

        final_text.append("="*30)  # Oddziel poszczególne formularze
        
    # Zapisujemy wszystko do pliku, kazda komorka jest oddzielna linia
    with open(file_name, 'w', encoding='utf-8') as file:
        for line in final_text:
            file.write(line + '\n')
#%%
main()
