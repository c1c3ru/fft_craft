import sys
sys.path.insert(0, "tools")
from translate_batch import apply

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry41_join.json"

T = {
"Potion": "Pocao",
"Hi-Potion": "Hiperpocao",
"X-Potion": "X-Pocao",
"Ether": "Eter",
"Hi-Ether": "Hipereter",
"Elixir": "Elixir",
"Antidote": "Antidoto",
"Eye Drops": "Colirio",
"Echo Herbs": "Ervas do Eco",
"Maiden's Kiss": "Beijo de Donzela",
"Gold Needle": "Agulha Dourada",
"Holy Water": "Agua Sagrada",
"Remedy": "Remedio",
"Phoenix Down": "Pena Fenix",

"Magick Ring": "Anel Magico",
"Cursed Ring": "Anel Amaldicoado",
"Angel Ring": "Anel do Anjo",
"Diamond Bracelet": "Bracelete de Diamante",
"Jade Armlet": "Bracelete de Jade",
"Guardian Bracelet": "Bracelete Guardiao",
"Shoulder Cape": "Capa de Ombro",
"Leather Cloak": "Manto de Couro",
"Mage's Cloak": "Manto do Mago",
"Elven Cloak": "Manto Elfico",
"Vampire Cape": "Capa de Vampiro",
"Featherweave Cloak": "Manto Entrelacado de Penas",
"Invisibility Cloak": "Manto da Invisibilidade",

"Onion Sword": "Espada Cebola",
"Onion Shield": "Escudo Cebola",
"Onion Helm": "Elmo Cebola",
"Onion Armor": "Armadura Cebola",
"Onion Gloves": "Luvas Cebola",

"Moonblade": "Lamina da Lua",
"Golden Axe": "Machado Dourado",
"Moonsilk Blade": "Lamina de Seda Lunar",
"Dreamwaker": "Despertador de Sonhos",
"Stardust Rod": "Cajado de Poeira Estelar",
"Crown Scepter": "Cetro da Coroa",
"Sagittarius Bow": "Arco de Sagitario",

"Reverie Shield": "Escudo do Devaneio",
"Vanguard Helm": "Elmo da Vanguarda",
"Acacia Hat": "Chapeu de Acacia",
"Brass Coronet": "Coroa de Latao",
"Grand Armor": "Grande Armadura",
"Minerva Bustier": "Espartilho de Minerva",
"Mirage Vest": "Colete Miragem",
"Brave Suit": "Traje Valente",
"Sage's Robe": "Veste do Sabio",
"Brigand's Gloves": "Luvas do Bandido",
"Empyreal Armband": "Bracelete Empireo",
"Sage's Ring": "Anel do Sabio",
}

apply(PATH, T, "entry41 equipment names batch3 (accessories, potions, onion gear, ultimates)")
