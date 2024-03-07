import re

EID_FOLDER = r'..\External-Item-Descriptions\descriptions'

def load_table(text, name, trans_id=False):
    if match := re.search(name + r'\s*=\s*{.*?}\s*\n', text, re.DOTALL):
        table = match[0]
        table = table.replace('  ', ' ')
        table = table.replace('#"', '"')
        table = re.sub(r'--.*$', '', table, flags=re.MULTILINE)
        if trans_id:
            table = re.sub(r'\[([\d".]+)]\s*=\s*(.*)\s*,\s*$', r'["\1", \2],', table, flags=re.MULTILINE)
        else:
            table = re.sub(r'\[[\d".]+]\s*=\s*', '', table, flags=re.MULTILINE)
            table = re.sub(r'^\s*{', '[', table, flags=re.MULTILINE)
            table = re.sub(r'},\s*$', '],', table, flags=re.MULTILINE)
        table = re.sub(r'.*EID.*', '', table, flags=re.MULTILINE)
        table = re.sub(r'\s*#+\s*', r'\\n', table, flags=re.MULTILINE)
        table = table.replace('{', '[', 1)
        table = table[:table.rfind('}')] + ']'
        return eval(table[table.find('=') + 1:])


def merge_table(table_1, table_2):
    merged = {}
    for id, name, desc in table_1:
        merged[id] = (name, desc.strip())
    for id, name, desc in table_2:
        merged[id] = (name, desc.strip())
    return merged


def convert_table(table):
    merged = {}
    for id, *content in table:
        merged[id] = content
    return merged


with open(EID_FOLDER + r'\ab+\en_us.lua', encoding='utf8') as file:
    text = file.read()
    ab_en_collectibles = load_table(text, 'collectibles')
    ab_en_trinkets = load_table(text, 'trinkets')
    ab_en_cards = load_table(text, 'cards')
    ab_en_pills = load_table(text, 'pills')
    ab_en_sacrifice = load_table(text, 'sacrifice')
    ab_en_dice = load_table(text, 'dice')
    ab_en_transformations = load_table(text, 'transformations')

with open(EID_FOLDER + r'\ab+\en_us_detailed.lua', encoding='utf8') as file:
    text = file.read()
    ab_en_detailed_collectibles = load_table(text, 'collectibles')
    ab_en_detailed_trinkets = load_table(text, 'trinkets')
    ab_en_detailed_cards = load_table(text, 'cards')
    ab_en_detailed_pills = load_table(text, 'pills')
    ab_en_detailed_sacrifice = load_table(text, 'sacrifice')
    ab_en_detailed_dice = load_table(text, 'dice')

with open(EID_FOLDER + r'\ab+\zh_cn.lua', encoding='utf8') as file:
    text = file.read()
    ab_zh_collectibles = load_table(text, 'collectibles')
    ab_zh_trinkets = load_table(text, 'trinkets')
    ab_zh_cards = load_table(text, 'cards')
    ab_zh_pills = load_table(text, 'pills')
    ab_zh_sacrifice = load_table(text, 'sacrifice')
    ab_zh_dice = load_table(text, 'dice')
    ab_zh_transformations = load_table(text, 'transformations')

with open(EID_FOLDER + r'\rep\en_us.lua', encoding='utf8') as file:
    text = file.read()
    rep_en_collectibles = load_table(text, 'repCollectibles')
    rep_en_birthright = load_table(text, 'birthright')
    rep_en_binge_eater = load_table(text, 'bingeEaterBuffs', True)
    rep_en_book_of_belial = load_table(text, 'bookOfBelialBuffs', True)
    rep_en_book_of_virtues = load_table(text, 'bookOfVirtuesWisps', True)
    rep_en_abyss = load_table(text, 'abyssSynergies', True)
    rep_en_trinkets = load_table(text, 'repTrinkets')
    rep_en_cards = load_table(text, 'repCards')
    rep_en_pills = load_table(text, 'repPills')
    rep_en_horse_pills = load_table(text, 'horsepills')
    rep_en_poop_spells = load_table(text, 'poopSpells')

with open(EID_FOLDER + r'\rep\en_us_detailed.lua', encoding='utf8') as file:
    text = file.read()
    rep_en_detailed_collectibles = load_table(text, 'repCollectibles')
    rep_en_detailed_trinkets = load_table(text, 'repTrinkets')
    rep_en_detailed_cards = load_table(text, 'repCards')
    rep_en_detailed_pills = load_table(text, 'repPills')

with open(EID_FOLDER + r'\rep\zh_cn.lua', encoding='utf8') as file:
    text = file.read()
    rep_zh_collectibles = load_table(text, 'repCollectibles')
    rep_zh_birthright = load_table(text, 'birthright')
    rep_zh_binge_eater = load_table(text, 'bingeEaterBuffs', True)
    rep_zh_book_of_belial = load_table(text, 'bookOfBelialBuffs', True)
    rep_zh_book_of_virtues = load_table(text, 'bookOfVirtuesWisps', True)
    rep_zh_abyss = load_table(text, 'abyssSynergies', True)
    rep_zh_trinkets = load_table(text, 'repTrinkets')
    rep_zh_cards = load_table(text, 'repCards')
    rep_zh_pills = load_table(text, 'repPills')
    rep_zh_horse_pills = load_table(text, 'horsepills')
    rep_zh_poop_spells = load_table(text, 'poopSpells')

print('=' * 10, 'Collectibles', '=' * 10, '\n')

en_collectibles = merge_table(ab_en_collectibles, rep_en_collectibles)
detailed_collectibles = merge_table(ab_en_detailed_collectibles, rep_en_detailed_collectibles)
zh_collectibles = merge_table(ab_zh_collectibles, rep_zh_collectibles)

en_collectibles = {k: v for k, v in en_collectibles.items() if
                   not v[1].startswith('<') and not zh_collectibles[k][1].startswith('<')}

for k, v in en_collectibles.items():
    print(k + '.', v[0], ':', v[1])
    print(zh_collectibles[k][0], ':', zh_collectibles[k][1])
    if k in detailed_collectibles:
        print(detailed_collectibles[k][1])
    print()

print('=' * 10, 'Trinkets', '=' * 10, '\n')

en_trinkets = merge_table(ab_en_trinkets, rep_en_trinkets)
detailed_trinkets = merge_table(ab_en_detailed_trinkets, rep_en_detailed_trinkets)
zh_trinkets = merge_table(ab_zh_trinkets, rep_zh_trinkets)

en_trinkets = {k: v for k, v in en_trinkets.items() if not v[1].startswith('<')}

for k, v in en_trinkets.items():
    print(k + '.', v[0], ':', v[1])
    print(zh_trinkets[k][0], ':', zh_trinkets[k][1])
    print(detailed_trinkets[k][1])
    print()

print('=' * 10, 'Cards', '=' * 10, '\n')

en_cards = merge_table(ab_en_cards, rep_en_cards)
detailed_cards = merge_table(ab_en_detailed_cards, rep_en_detailed_cards)
zh_cards = merge_table(ab_zh_cards, rep_zh_cards)

for k, v in en_cards.items():
    print(k + '.', v[0], ':', v[1])
    print(zh_cards[k][0], ':', zh_cards[k][1])
    print(detailed_cards[k][1])
    print()

print('=' * 10, 'Pills', '=' * 10, '\n')

en_pills = merge_table(ab_en_pills, rep_en_pills)
detailed_pills = merge_table(ab_en_detailed_pills, rep_en_detailed_pills)
zh_pills = merge_table(ab_zh_pills, rep_zh_pills)

en_pills = {k: v for k, v in en_pills.items() if k}

for k, v in en_pills.items():
    print(k + '.', v[0], ':', v[1])
    print(zh_pills[k][0], ':', zh_pills[k][1])
    print(detailed_pills[k][1])
    print()

print('=' * 10, 'Sacrifice', '=' * 10, '\n')

en_sacrifice = convert_table(ab_en_sacrifice)
detailed_sacrifice = convert_table(ab_en_detailed_sacrifice)
zh_sacrifice = convert_table(ab_zh_sacrifice)

for k, v in en_sacrifice.items():
    print(k, '=>', v[1])
    print(zh_sacrifice[k][1])
    print(detailed_sacrifice[k][1])
    print()

print('=' * 10, 'Dice', '=' * 10, '\n')

en_dice = convert_table(ab_en_dice)
detailed_dice = convert_table(ab_en_detailed_dice)
zh_dice = convert_table(ab_zh_dice)

for k, v in en_dice.items():
    print(k, '=>', v[1])
    print(zh_dice[k][1])
    print(detailed_dice[k][1])
    print()

print('=' * 10, 'Transformations', '=' * 10, '\n')

for i in range(len(ab_en_transformations)):
    if ab_en_transformations[i]:
        print(ab_en_transformations[i])
        print(ab_zh_transformations[i])
        print()

print('=' * 10, 'Birthright', '=' * 10, '\n')

for i in range(len(rep_en_birthright)):
    print(rep_en_birthright[i][0], ':', rep_en_birthright[i][2])
    print(rep_zh_birthright[i][0], ':', rep_zh_birthright[i][2])
    print()

print('=' * 10, 'Binge Eater', '=' * 10, '\n')

en_binge_eater = convert_table(rep_en_binge_eater)
zh_binge_eater = convert_table(rep_zh_binge_eater)

for k, v in en_binge_eater.items():
    print(en_collectibles[k][0], '=>', v[0])
    print(zh_collectibles[k][0], '=>', zh_binge_eater[k][0])
    print()

print('=' * 10, 'Book of Belial', '=' * 10, '\n')

en_book_of_belial = convert_table(rep_en_book_of_belial)
zh_book_of_belial = convert_table(rep_zh_book_of_belial)

for k, v in en_book_of_belial.items():
    print(en_collectibles[k][0], '=>', v[0])
    if k in zh_book_of_belial:
        print(zh_collectibles[k][0], '=>', zh_book_of_belial[k][0])
    print()

print('=' * 10, 'Book of Virtues', '=' * 10, '\n')

en_book_of_virtues = convert_table(rep_en_book_of_virtues)
zh_book_of_virtues = convert_table(rep_zh_book_of_virtues)

for k, v in en_book_of_virtues.items():
    print(en_collectibles[k][0], '=>', v[0])
    print(zh_collectibles[k][0], '=>', zh_book_of_virtues[k][0])
    print()

print('=' * 10, 'Abyss', '=' * 10, '\n')

en_abyss = convert_table(rep_en_abyss)
zh_abyss = convert_table(rep_zh_abyss)

for k, v in en_abyss.items():
    print(en_collectibles[k][0], '=>', v[0])
    print(zh_collectibles[k][0], '=>', zh_abyss[k][0])
    print()

print('=' * 10, 'Horse Pills', '=' * 10, '\n')

en_horse_pills = convert_table(rep_en_horse_pills)
zh_horse_pills = convert_table(rep_zh_horse_pills)

for k, v in en_horse_pills.items():
    if k:
        print(k + '.', v[0], ':', v[1])
        print(zh_horse_pills[k][0], ':', zh_horse_pills[k][1])
        print()

print('=' * 10, 'Poop Spells', '=' * 10, '\n')

for i in range(len(rep_en_poop_spells)):
    print(rep_en_poop_spells[i][0], ':', rep_en_poop_spells[i][1])
    print(rep_zh_poop_spells[i][0], ':', rep_zh_poop_spells[i][1])
    print()
