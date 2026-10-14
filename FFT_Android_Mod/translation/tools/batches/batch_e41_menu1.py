import sys, json
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases
from translate_batch import apply

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry41_join.json"

EXACT = {
"{unitname}'s {EB} increased by {E4}!": "{EB} de {unitname} aumentou em {E4}!",
"{unitname}'s {EB} decreased by {E4}!": "{EB} de {unitname} diminuiu em {E4}!",
"{unitname}'s CT reduced to 0!": "O CT de {unitname} foi reduzido para 0!",
"{unitname}'s CT set to 100!": "O CT de {unitname} foi definido para 100!",
"Turn List{br}Unit List{br}Options{br}Paused game{br}Return to Title Screen":
    "Lista de Turnos{br}Lista de Unidades{br}Opcoes{br}Jogo pausado{br}Voltar a Tela Inicial",
"  1. Display Slide Control Button": "  1. Exibir Botao de Controle de Slide",
"  2. Multi-height Toggle Rate": "  2. Taxa de Alternancia de Altura",
"  3. Menu Cursor Speed": "  3. Velocidade do Cursor do Menu",
"  6. Display Ability Names": "  6. Exibir Nomes de Habilidades",
"  7. Display Effect Messages": "  7. Exibir Mensagens de Efeito",
"  8. Display Earned EXP/JP": "  8. Exibir EXP/JP Ganhos",
"10. Display Unequippable Items": "10. Exibir Itens Nao Equipaveis",
"11. Optimize on Job Change": "11. Otimizar na Troca de Classe",
"12. Simple Battle Animations": "12. Animacoes de Batalha Simples",
"13. Restore Default Settings": "13. Restaurar Configuracoes Padrao",
"  6. Number of Traps": "  6. Numero de Armadilhas",
"  8. Restore Default Settings": "  8. Restaurar Configuracoes Padrao",
"13. Display guide cursor": "13. Exibir cursor guia",
"12. Touch-Activated Menu Items": "12. Itens de Menu Ativados por Toque",
"{SP2}To move to a location on the map, {br}tap its corresponding marker.{br}{br}{br}{SP2}When at a city or castle, selecting its symbol and{br}tapping the OK button will open a menu displaying{br}the various establishments at that location.{br}{br}{SP2}If you are unsure what a particular menu option is{br}for, tap the Help button to view more information{br} about it.{br}{br}{SP2}Tapping the Menu button while on the world map{br}opens the main menu, from which you can access your{br}party roster or save the game.{br}{br}{SP2}The game's various tutorials can also be accessed{br}from the main menu. These tutorials provide in-depth{br}explanations of various aspects of the game. Consult{br}them if you have questions about how to play the game.{0xF566}{0xF60A}{0xF509}{0xF601}":
    "{SP2}Para se mover a um local no mapa, {br}toque no marcador correspondente.{br}{br}{br}{SP2}Ao estar numa cidade ou castelo, selecionar seu simbolo e{br}tocar no botao OK abrira um menu exibindo{br}os varios estabelecimentos daquele local.{br}{br}{SP2}Se voce nao tiver certeza para que serve uma opcao{br}de menu, toque no botao de Ajuda para ver mais{br}informacoes sobre ela.{br}{br}{SP2}Tocar no botao de Menu enquanto estiver no mapa-mundi{br}abre o menu principal, de onde voce pode acessar a{br}lista do seu grupo ou salvar o jogo.{br}{br}{SP2}Os varios tutoriais do jogo tambem podem ser acessados{br}pelo menu principal. Esses tutoriais oferecem explicacoes{br}detalhadas sobre varios aspectos do jogo. Consulte-os{br}se tiver duvidas sobre como jogar.{0xF566}{0xF60A}{0xF509}{0xF601}",
}

data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]
changed = 0
for i, (s, t) in enumerate(strings):
    if s in EXACT:
        strings[i] = [EXACT[s], t]
        changed += 1
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)
print("changed:", changed)
