import sys, json
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"

T = {
"Walk across and even stop on the surface of water.":
    "Caminha sobre a agua e pode ate parar na superficie.",
"Swim through and even act in deep water.":
    "Nada e pode ate agir em aguas profundas.",
"Walk across and even stop on the surface of lava.":
    "Caminha sobre a lava e pode ate parar na superficie.",
"Move and stop even when fully{br}submerged in water of depth 3.":
    "Move-se e para mesmo totalmente{br}submerso em agua de profundidade 3.",
"Move while floating a height of 1h above the ground.":
    "Move-se flutuando a uma altura de 1h acima do solo.",
"Move while transparent and invisible to the enemy.":
    "Move-se transparente e invisivel para o inimigo.",
"Attack with equipped weapon, or{br}bare fists if no weapon is equipped.":
    "Ataca com a arma equipada, ou{br}com os punhos nus se nenhuma arma estiver equipada.",
"Take a defensive stance{br}and end current turn.":
    "Assume uma postura defensiva{br}e encerra o turno atual.",
"Squire job command. These are the most{br}fundamental of all battle techniques.":
    "Comando de classe do Soldado. Estas sao as{br}tecnicas de batalha mais fundamentais de todas.",
"(Bow and crossbow attacks excluded.)":
    "(Ataques de arco e besta excluidos.)",
"Unit's Speed × 2":
    "Velocidade da unidade × 2",
}

data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]
changed = 0
for i, (s, t) in enumerate(strings):
    new_s = apply_phrases(s, T)
    if new_s != s:
        strings[i] = [new_s, t]
        changed += 1
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)
print("changed:", changed)
