from tkinter import Event
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Popup, Window
import pandas as pd
import os
from time import localtime

nome = os.getenv('USERNAME')
hoje = localtime()

lista = ['Avaria','Sobra','Falta','Erro']
motivo = ['Linha', 'Estação']
estação = ['M101','M102','M103','M104','M105','M106','M107','M108','M109','M110']
num_linha = 1
lista_artigo = []
lista_estação = []
lista_motivo = []
lista_qtd = []
lista_erro = []
usuario = so = artigo = qtd = tperror = ''

def janela_login():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Matricula                   '),sg.Input(size=(15,0))],
        [sg.Text('Data (ex:dd.mm.aaaa)'),sg.Input(size=(15,0), key='Data')],
        [sg.Button('Continuar')]
    ]
    return sg.Window('Login', layout=layout, finalize=True)
def janela_so():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Reservatório'),sg.Input(size=(25,0), key='SOs')],
        [sg.Button('Concluir'), sg.Button('Erro'), sg.Button('Bypass')],
    ]
    return sg.Window('Registro', layout=layout, finalize=True)
def janela_erro():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Artigo:         '),sg.Input(size=(25,0))],
        [sg.Text('Quantidade: '),sg.Combo(values=list(range(30)),default_value=1,size=(3, 1))],
        [sg.Text('Tipo de Erro:'),sg.Combo(values=lista)],
        [sg.Output(size=(40,6), key='-OUTPUT-')],
        [sg.Button('Voltar'), sg.Button('Adicionar')]
    ]
    return sg.Window('Erros', layout=layout, finalize=True)
def janela_bypass():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Motivo:'),sg.Combo(values=motivo)],
        [sg.Text('Estação:'),sg.Combo(values=estação)],
        [sg.Output(size=(22,6), key='-BYPASS-')],
        [sg.Button('Voltar'), sg.Button('Adicionar')]        
    ]
    return sg.Window('Bypass', layout=layout, finalize=True)

janela1, janela2, janela3, janela4 = janela_login(), None, None, None
dia = list(range(1,32))
diaexato = []
for d in dia:
    if d <= 9:
        d_ = '0' + str(d)
        diaexato.append(d_)
    else:
        diaexato.append(str(d))
mes = list(range(1,13))
mesexato = []
for m in mes:
    if m <= 9:
        m_ = '0' + str(m)
        mesexato.append(m_)
    else:
        mesexato.append(str(m))
ano = list(range(2000,2051))
anoexato = []
for a in ano:
    anoexato.append(str(a))

while True:
    window, event, values = sg.read_all_windows()
    if window == janela1 and event == sg.WIN_CLOSED or window == janela2 and event == sg.WIN_CLOSED or window == janela3 and event == sg.WIN_CLOSED or window == janela4 and event == sg.WIN_CLOSED:
        break
    if window == janela1 and event == 'Continuar':
        if values[0] == '' or values['Data'] == '':
            sg.popup('''Algum valor ficou sem
preenchimento, favor verificar''', title='Erro')
        else:
            usuario = values[0]
            dataatual = values['Data'].replace('/','.').replace(',','.').replace(' ','.').replace('-','.').replace('_','.').replace(';','.')
            if not usuario.isdigit():
                sg.popup('Digite apenas números na matricula', title='Erro')
                continue
            if dataatual[:2] not in diaexato or dataatual[3:5:] not in mesexato or dataatual[6::] not in anoexato:
                sg.popup("""Houve um erro na digitação da Data,
favor verificar (ex:01.06.2021):
dia = com 2 dígitos
mês = com 2 dígitos
ano = com 4 dígitos
utilizar a separação por Ponto (.)""", title='Erro')
                continue
            if hoje.tm_hour < 21:
                if int(dataatual[:2]) != hoje.tm_mday or int(dataatual[3:5:]) != hoje.tm_mon or int(dataatual[6::]) != hoje.tm_year:
                    valor = sg.popup('''Existe uma inconsistência com a data dígitada e a do sistema,
favor verifique antes de prosseguir:
aperte Ok para prosseguir, ou
aperte Cancel para verificar''', button_type=4, title='Atenção')
                    if valor == 'OK':
                        janela2 = janela_so()
                        janela1.hide()
                    else:
                        continue
            if hoje.tm_hour > 21:
                if int(dataatual[:2]) != (hoje.tm_mday + 1) or int(dataatual[3:5:]) != hoje.tm_mon or int(dataatual[6::]) != hoje.tm_year:
                    valor = sg.popup('''Existe uma inconsistência com a data dígitada e a do sistema,
favor verifique antes de prosseguir:
aperte Ok para prosseguir, ou
aperte Cancel para verificar''', button_type=4, title='Atenção')
                    if valor == 'OK':
                        janela2 = janela_so()
                        janela1.hide()
                    else:
                        continue
                else:
                    janela2 = janela_so()
                    janela1.hide()        
            else:
                janela2 = janela_so()
                janela1.hide()
    if window == janela2 and event == 'Erro':
        if values['SOs'] == '':
            sg.popup('Digitar um reservatório antes de prosseguir', title='Atenção')
        else:
            if not values['SOs'].isdigit():
                sg.popup('Digite apenas números', title='Erro')
                continue
            if len(str(values['SOs'])) != 6:
                sg.popup('''Verificar a numeração do reservatório,
por padrão o mesmo contém 6 digitos''', title='Erro')
                continue
            else:
                janela3 = janela_erro()
                so = values['SOs']
                txtso = so[::]
                janela2.hide()
    if window == janela3 and event == 'Voltar':
        if values[0] == '' and values[2] == '':
            artigo = ''
            qtd = ''
            tperror = ''
            janela3.hide()
            janela2.un_hide()
        elif values[0] != '' and values[2] == '' or values[2] != '' and values[0] == '':
            sg.popup('''Algum valor ficou sem preenchimento,
os dados não serão salvos.''', title='Atenção')
            artigo = ''
            qtd = ''
            tperror = ''
            janela3.hide()
            janela2.un_hide()
        else:
            artigo = values[0]
            qtd = values[1]
            tperror = values[2]
            janela3.hide()
            janela2.un_hide()
        
    if window == janela3 and event == 'Adicionar':
        if values[0] != '' and values[1] == '' or values[2] == '':
            sg.popup('''Algum valor ficou sem
preenchimento, favor verificar''', title='Erro')
        elif values[1] != '' and values[0] == '' or values[2] == '':
            sg.popup('''Algum valor ficou sem
preenchimento, favor verificar''', title='Erro')
        elif values[2] != '' and values[0] == '' or values[1] == '':
            sg.popup('''Algum valor ficou sem
preenchimento, favor verificar''', title='Erro')
        else:
            lista_artigo.append(values[0])
            lista_qtd.append(values[1])
            lista_erro.append(values[2])
            dicionario = {'Artigo:':lista_artigo, 'Qtd:':lista_qtd, 'Tipo:':lista_erro}
            df = pd.DataFrame(data=dicionario)
            window['-OUTPUT-'].update(df.to_string(index=False))
            num_linha += 1
    if window == janela2 and event == 'Bypass':
        if values['SOs'] == '':
            sg.popup('Digitar um reservatório antes de prosseguir', title='Atenção')
        else:
            if not values['SOs'].isdigit():
                sg.popup('Digite apenas números', title='Erro')
                continue
            if len(str(values['SOs'])) != 6:
                sg.popup('''Verificar a numeração do reservatório,
por padrão o mesmo contém 6 digitos''', title='Erro')
                continue
            else:
                so = values['SOs']
                txtso = so[::]
                janela2.hide()
                janela4 = janela_bypass()
    if window == janela4 and event == 'Adicionar':
        if values[0] != '' and values[1] == '':
            sg.popup('''Algum valor ficou sem
preenchimento, favor verificar''', title='Erro')
        elif values[1] != '' and values[0] == '':
            sg.popup('''Algum valor ficou sem
preenchimento, favor verificar''', title='Erro')
        elif values[0] == '' and values[1] == '':
            sg.popup('''Algum valor ficou sem
preenchimento, favor verificar''', title='Erro')
        else:
            lista_motivo.append(values[0])
            lista_estação.append("M" + values[1] if values[1][0].upper() != "M" else values[1].upper())
            dicionario2 = {'Motivo:':lista_motivo, 'Local:': lista_estação}
            df2 = pd.DataFrame(data=dicionario2)
            window['-BYPASS-'].update(df2.to_string(index=False))
            num_linha = 1001
    if window == janela4 and event == 'Voltar':
        if values[0] == '' and values[1] == '':
            lista_estação = []
            lista_motivo = []
            janela4.hide()
            janela2.un_hide()
        elif values[0] != '' and values[1] == '' or values[1] != '' and values[0] == '':
            sg.popup('''Algum valor ficou sem preenchimento,
os dados não serão salvos.''', title='Atenção')
            lista_estação = []
            lista_motivo = []
            janela4.hide()
            janela2.un_hide()
        else:
            janela4.hide()
            janela2.un_hide()
    if window == janela2 and event == 'Concluir':
        if values['SOs'] == "":
            sg.popup('Favor informar um número de SO', title='Erro')
            continue
        if not values['SOs'].isdigit():
            sg.popup('Digite apenas números', title='Erro')
            continue
        if len(str(values['SOs'])) != 6:
            sg.popup('''Verificar a numeração do reservatório,
por padrão o mesmo contém 6 digitos''', title='Erro')
            continue
        else:
            diapr = localtime().tm_mday
            mespr = localtime().tm_mon
            anopr = localtime().tm_year
            horapr = localtime().tm_hour
            mimpr = localtime().tm_min
            segpr = localtime().tm_sec
            datapr = f'{diapr}/{mespr}/{anopr} {horapr}:{mimpr}:{segpr}'
            if num_linha > 1 and num_linha < 1000:
                for c in range(len(lista_artigo)):
                    cadastro = {'usuario:':usuario, 'so:':txtso, 'QtdSO':c+1,'artigo:':lista_artigo[c],'quantidade:':lista_qtd[c], 'tipo de erro:':lista_erro[c], 'motivo:':'', 'estação:':'', 'horario:':datapr}
                    dados = pd.DataFrame(data = cadastro, index=[0])
                    try:
                        dados.to_csv(rf'C:\Users\{nome}\Desktop\{dataatual}\{usuario}-{dataatual}.txt', encoding = 'UTF-8', mode='a', index=False, header=None) 
                    except FileNotFoundError:
                        os.mkdir(rf'C:\Users\{nome}\Desktop\{dataatual}')
                        dados.to_csv(rf'C:\Users\{nome}\Desktop\{dataatual}\{usuario}-{dataatual}.txt', encoding = 'UTF-8', mode='a', index=False, header=None)

                    so = artigo = qtd = tperror = ''
                num_linha = 1       
                lista_artigo = []
                lista_qtd = []
                lista_erro = []
            elif num_linha == 1:
                so = values['SOs']
                cadastro = {'usuario:':usuario, 'so:':so, 'QtdSO': num_linha ,'artigo:':artigo,'quantidade:':qtd, 'tipo de erro:':tperror, 'motivo:': '', 'estação:': '', 'horario:':datapr}
                dados = pd.DataFrame(data = cadastro, index=[0])
                try:
                    dados.to_csv(rf'C:\Users\{nome}\Desktop\{dataatual}\{usuario}-{dataatual}.txt', encoding = 'UTF-8', mode='a', index=False, header=None) 
                except FileNotFoundError:
                    os.mkdir(rf'C:\Users\{nome}\Desktop\{dataatual}')
                    dados.to_csv(rf'C:\Users\{nome}\Desktop\{dataatual}\{usuario}-{dataatual}.txt', encoding = 'UTF-8', mode='a', index=False, header=None)
                so = artigo = qtd = tperror = ''
                num_linha = 1
                lista_artigo = []
                lista_qtd = []
                lista_erro = []
                lista_motivo = []
                lista_estação = []
            elif num_linha > 1000:
                for b in range(len(lista_estação)):
                    cadastro = {'usuario:':usuario, 'so:': so, 'QtdSO': b + 1001, 'artigo:': '', 'quantidade:':'', 'tipo de erro:': '', 'motivo:':lista_motivo[b], 'estação:':lista_estação[b], 'horario:':datapr}
                    dados = pd.DataFrame(data = cadastro, index=[0])
                    try:
                        dados.to_csv(rf'C:\Users\{nome}\Desktop\{dataatual}\{usuario}-{dataatual}.txt', encoding = 'UTF-8', mode='a', index=False, header=None) 
                    except FileNotFoundError:
                        os.mkdir(rf'C:\Users\{nome}\Desktop\{dataatual}')
                        dados.to_csv(rf'C:\Users\{nome}\Desktop\{dataatual}\{usuario}-{dataatual}.txt', encoding = 'UTF-8', mode='a', index=False, header=None)
                num_linha = 1
                lista_motivo = []
                lista_estação = []

            with open(rf'C:\Users\{nome}\Desktop\{dataatual}\{usuario}-{dataatual}.txt') as f:
                ContRes = sum(1 for _ in f)
            sg.popup(f'''                 Concluído!
Nº de Registros Conferidos: {ContRes}''', title='Concluído')
            window['SOs'].update('')
