import os
import csv
from operator import itemgetter


def load_prices(directory):
    data = []
    for filename in os.listdir(directory):
        if 'price' in filename and filename.endswith('.csv'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                print(reader.fieldnames)
                for row in reader:
                    product_name = row.get('название') or row.get('продукт') or row.get('товар') or row.get('наименование')
                    price = float(row.get('цена') or row.get('розница'))
                    weight = float(row.get('фасовка') or row.get('масса') or row.get('вес'))
                    data.append({
                        'name': product_name,
                        'price': price,
                        'weight': weight,
                        'file': filename,
                        'price_per_kg': price / weight
                    })
                    print(data[-1].values())
    return data


def find_text(text, data):
    return sorted(
        [item for item in data if text.lower() in item['name'].lower()],
        key=itemgetter('price_per_kg')
    )


def export_html(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        ''')
        for n, item in enumerate(data, start=1):
            file.write(f'''<tr>
            <td>{n}</td>
            <td>{item["name"]}</td>
            <td>{item["price"]}</td>
            <td>{item["weight"]}</td>
            <td>{item["file"]}</td>
            <td>{item["price_per_kg"]:.2f}</td>
            </tr>\n''')
        file.write('</table>\n</body>\n</html>')


def export_txt(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for n, item in enumerate(data, start=1):
            file.write(f'{n}\t{item["name"]}\t{item["price"]}\t{item["weight"]}\t{item["file"]}\t{item["price_per_kg"]:.2f}\n')


def main():
    directory = './data/'
    data = load_prices(directory)
    while True:
        text = input("Введите текст для поиска (или 'exit' для выхода): ")
        if text.lower() == 'exit':
            print("Работа завершена.")
            break
        found_data = find_text(text, data)
        if found_data:
            for item in found_data:
                print(f'{item["name"]}\t{item["price"]}\t{item["file"]}\t{item["price_per_kg"]:.2f}')
            export_choice = input("Экспортировать результаты? (txt/html/нет): ").lower()
            if export_choice == 'txt':
                export_txt(found_data, 'result.txt')
            elif export_choice == 'html':
                export_html(found_data, 'result.html')
        else:
            print("Ничего не найдено.")


if __name__ == "__main__":
    main()
