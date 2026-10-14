import sys
sys.path.insert(0, "tools")
from translate_batch import apply

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry41_join.json"

# Only translate clearly descriptive (material+weapon) compound names.
# Mythological/legendary proper nouns (Excalibur, Ragnarok, Ashura, Masamune-style
# katana names, Materia Blade, Defender, Chaos Blade, etc.) are left in English,
# matching how official PT-BR FF localizations usually keep those unchanged.
T = {
"Dagger": "Adaga",
"Mythril Knife": "Faca de Mithril",
"Blind Knife": "Faca Cegante",
"Platinum Dagger": "Adaga de Platina",
"Air Knife": "Faca do Vento",
"Ninja Blade": "Lamina Ninja",
"Broadsword": "Espada Larga",
"Longsword": "Espada Longa",
"Iron Sword": "Espada de Ferro",
"Mythril Sword": "Espada de Mithril",
"Blood Sword": "Espada de Sangue",
"Coral Sword": "Espada de Coral",
"Ancient Sword": "Espada Ancestral",
"Sleep Blade": "Lamina do Sono",
"Platinum Sword": "Espada de Platina",
"Diamond Sword": "Espada de Diamante",
"Dark Dragon": "Dragao das Trevas",
"Blue Dragon": "Dragao Azul",
"Red Dragon": "Dragao Vermelho",
"Hydra": "Hidra",
"Greater Hydra": "Hidra Maior",
"Dark Knight": "Cavaleiro Negro",
"Onion Knight": "Cavaleiro Cebola",
"Sky Pirate": "Pirata do Ceu",
"Game Hunter": "Cacador de Monstros",
}

apply(PATH, T, "entry41 descriptive weapon/dragon names")
