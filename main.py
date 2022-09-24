import os

import requests
from bs4 import BeautifulSoup as bs4
from tqdm import tqdm

lines = []
categories = {
    'headphones-and-microphones': 2354,
    'headphones': 2366,
    'headset': 2372,
    'microphones': 2355,
    'headhpone-microphone-accessories': 2359,
    'mice-gaming': 2180,
    'mice': 2179,
    'keyboards': 2279,
    'keyboards-gaming': 2280,
    'gpus': 2561,
    'monitors': 1659,
    'gaming-monitors': 2161,
    'monitors-gaming': 2161,
    'gaming-gpus': 2562,
    'gaming': 1623,
    'gaming-keyboards': 1724,
    'gaming-headphones': 1749,
    'gaming-mice': 1740,
    'multimedia-gpus': 2567,
    'gpus-accessories': 2569
}
print('Available categories:')
for i, category in enumerate(categories.keys()):
    print(f'{i}: {category}')

indexes = input(
    'Eneter categories (use , for multiple categories): ').split(',')

if not os.path.exists('discounted_products'):
    os.mkdir('discounted_products')

for index in indexes:
    category = list(categories.items())[int(index)]

    url = 'https://gjirafa50.mk/category/products'
    total_pages = requests.get(f"{url}?categoryId={category[1]}").json()[
        'totalpages']
    for i in tqdm(range(total_pages)):
        response = requests.get(
            f"{url}?categoryId={category[1]}&pagenumber={i}")
        soup = bs4(response.json()['html'], 'html.parser')
        items = soup.find_all('div', {'class': 'item-box'})
        for item in items:
            href = item.find('a')['href']
            prices = item.find_all('span', {'class': 'price'})
            discount = item.find('div', {'discount__label'})
            if not discount:
                continue
            lines.append({
                'discount': discount.span.text.strip(),
                'old_price': prices[1].text.strip(),
                'new_price': prices[0].text.strip(),
                'href': f"https://gjirafa50.mk{href}"
            })
    lines.sort(key=lambda x: int(x['discount'].replace('%', '')))
    string_lines = map(
        lambda x: f"{x['discount']} ({x['old_price']} -> {x['new_price']}) - {x['href']}", lines)
    with open(f"discounted_products/{category[0]}.txt", 'w') as f:
        f.write('\n'.join(string_lines))
