
# Date Created: 04/26/2022
# Last Updated: 04/26/2022
# Authors: Riley McCann and Tyler Montgomery

import pandas as pd 
import json

# Read in CSV
df = pd.read_csv('filename.csv')

# Grab only custom cards
custom_cards = df[df['Image URL'].notnull()]

# Rename fields to MTGADraft format
custom_cards = custom_cards.rename({'Image URL' : 'image_uris', 'Name' : 'name', 'Rarity' : 'rarity', 'Type' : 'type', 'Set' : 'set', 'Collector Number' : 'collector_number'}, axis='columns')

# Replace card names with name inside Notes from CubeCobra
custom_cards.loc[custom_cards['Notes'].notnull(), 'name'] = custom_cards[custom_cards['Notes'].notnull()]['Notes']

# Split cubecobra type into type and subtype
types = custom_cards['type'].str.split(" - ", expand=True)

# Set type
custom_cards['type'] = types[0]

# Set subtypes as list
custom_cards['subtype'] = types[1].str.split(" ")

# If no subtypes specified, set subtype equal to type
custom_cards.loc[custom_cards['subtype'].isnull(), 'subtype'] = types[0].str.split("\n")

# Grab only image_uris
images = json.loads(custom_cards['image_uris'].to_json(orient='index'))

images_dict = {}

# Convert image_uris field to dictionary with 'en:'
for key, value in images.items():
    images_dict[key]= {'en': value}

# Set image_uris in dataframe to dictionary created above
custom_cards['image_uris'] = images_dict.values()

# Look for mana cost in dataframe and set to "{1}" if not specified
if 'mana_cost' not in custom_cards:
    custom_cards['mana_cost'] = "{1}"
else:
    custom_cards.loc[custom_cards['mana_cost'].isnull(), 'mana_cost'] = "{1}"


# Make custom cards into json
custom_dictionary = json.loads(custom_cards.to_json(orient = "index"))

custom_cards_list = []

# Format into list of json objects
for item in custom_dictionary.values():
    custom_cards_list.append(item)


# Grab non-custom cards
wotc_cards = df[df['Image URL'].isnull()]

# Make non-custom cards into json
wotc_dictionary = json.loads(wotc_cards.to_json(orient = "index"))

wotc_cards_list = []

# Format into list of json objects
for item in wotc_dictionary.values():
    wotc_cards_list.append(item)


# Write to text file in proper format custom cards and non-custom cards
with open('custom_cards.txt', 'w') as f:
    f.write("[Custom Cards]\n")
    json.dump(custom_cards_list, f, indent=1)
    f.write("\n[MainSlot(15)]")
    for card in custom_cards_list:
        f.write("\n" + card['name'])
    for card in wotc_cards_list:
        f.write("\n" + card['Name'])

f.close()