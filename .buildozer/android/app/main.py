from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
from bannerProduto import *
import requests
import os
import certifi
from datetime import date
import time
from kivy_garden.zbarcam import ZBarCam
import kivy_garden.xcamera



os.environ['SSL_CERT_FILE'] = certifi.where()

GUI = Builder.load_file("main.kv")

class MyApp(App):

    loja = 'Matriz'
    def build(self):

        return GUI

    def on_start(self):
        try:
            with open('login.txt', 'r') as arquivo:
                self.id_usuario = arquivo.read()
            self.root.ids['screen_manager'].current = 'homepage'
        except:
            pass

    def carregar_lista_referencias(self):
        homepage = self.root.ids['homepage']
        texto = homepage.ids['referencia'].text
        homepage.ids['lista_referencias'].add_widget(BannerProduto(codigo=texto))
        self.atualizar_qnt(+1)
        homepage.ids['referencia'].text = ''

    def incluir_item_camera(self, codigo):
        if codigo != '':
            codigo = codigo.replace("'",'').replace('b', '')
            self.root.ids['homepage'].ids['referencia'].text = codigo
            self.mudar_tela('homepage')


    def excluir_item(self,item,*args):
        homepage = self.root.ids['homepage']
        lista_produto = homepage.ids['lista_referencias']
        for produto in list(lista_produto.children):
            if produto.id == item:
                homepage.ids['lista_referencias'].remove_widget(produto)
                quantidade = int(homepage.ids['quantidade'].text.replace('Qnt.: [color=#000000]', '').replace('[/color]', '')) -1
                homepage.ids['quantidade'].text = f'Qnt.: [color=#000000]{quantidade}[/color]'
                self.root.ids['camerapage'].ids['quantidade'].text =  f'Qnt.: [color=#000000]{quantidade}[/color]'
                break



    def excluir_todos(self):
        homepage = self.root.ids['homepage']
        lista_produto = homepage.ids['lista_referencias']
        for referencia in list(lista_produto.children):
            homepage.ids['lista_referencias'].remove_widget(referencia)

        homepage.ids['quantidade'].text = f'Qnt.: [color=#000000]0[/color]'
        self.root.ids['camerapage'].ids['quantidade'].text = f'Qnt.: [color=#000000]0[/color]'

    def enviar_coleta(self):
        coleta = ''
        homepage = self.root.ids['homepage']
        lista_produto = homepage.ids['lista_referencias']
        for referencia in list(lista_produto.children):
            coleta = coleta + referencia.id + ','
        info = f'{{"coleta":"{coleta[:-1]}","leitura":"0"}}'
        link = f'https://appbalanco-27229-default-rtdb.firebaseio.com/{self.loja}/{self.id_usuario}/coletas.json'
        requests.post(link,data=info)

        self.excluir_todos()

    def logar(self):
        nome = self.root.ids['loginpage'].ids['nome'].text
        if(len(nome) >= 4):
            self.root.ids['screen_manager'].current = 'homepage'
            info = f'{{"nome":"{nome}","data":"{date.today().strftime("%d/%m/%Y")}"}}'
            link = f'https://appbalanco-27229-default-rtdb.firebaseio.com/{self.loja}.json'
            id_usuario = requests.post(link, data=info).json()['name']
            self.id_usuario = id_usuario
            with open('login.txt', 'w') as arquivo:
                arquivo.write(id_usuario)
        else:
            self.root.ids['loginpage'].ids['mensagem_login'].text = '[color=#FF0000]Erro:[/color] Nome tem que ter mais de 3 caracter'

    def mudar_tela(self,id_tela):
        self.root.ids['screen_manager'].current = id_tela

    def atualizar_qnt(self, qnt):
        homepage = self.root.ids['homepage']
        quantidade = int(homepage.ids['quantidade'].text.replace('Qnt.: [color=#000000]', '').replace('[/color]', '')) + qnt
        homepage.ids['quantidade'].text = f'Qnt.: [color=#000000]{quantidade}[/color]'
        self.root.ids['camerapage'].ids['quantidade'].text = f'Qnt.: [color=#000000]{quantidade}[/color]'



MyApp().run()
