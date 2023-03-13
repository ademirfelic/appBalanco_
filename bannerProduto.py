from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.app import App
from botoes import *
from functools import partial

class BannerProduto(GridLayout):

    def __init__(self,**kwargs):
        self.rows = 1
        super().__init__()
        with self.canvas:
            Color(rgb=(0,0,0,1))
            self.rec = Rectangle(size= self.size, pos= self.pos)

        self.bind(pos=self.atualiza_rec, size=self.atualiza_rec)

        codigo = kwargs['codigo']
        self.id = codigo
        produto = FloatLayout()
        label_referencia = Label(text=f'Referencia: 777777', pos_hint={'right': 0.25, 'top': 0.95}, size_hint=(0.3, 0.33))
        label_nome = Label(text=f'Nome: produto', pos_hint={'right': 0.55, 'top': 0.95}, size_hint=(0.58, 0.33))
        label_preco = Label(text=f'Preço: 0,00', pos_hint={'right': 0.25, 'top': 0.60}, size_hint=(0.2 , 0.33))
        label_cor = Label(text=f'Cor: amarelo', pos_hint={'right': 1, 'top': 1}, size_hint=(1 , 1))
        label_codigo = Label(text=f'Codigo: {codigo}', pos_hint={'right': 0.26, 'top': 0.3}, size_hint=(0.4, 0.33))

        app = App.get_running_app()
        imagem = ImageButton(source='icones/excluir.png',
                             pos_hint={"right": 1, "top": 0.90}, size_hint=(0.12, 0.5),
                             on_release=partial(app.excluir_item,codigo))

        produto.add_widget(label_referencia)
        produto.add_widget(label_nome)
        produto.add_widget(label_preco)
        produto.add_widget(label_cor)
        produto.add_widget(label_codigo)
        produto.add_widget(imagem)

        self.add_widget(produto)


    def atualiza_rec(self,*args):
        self.rec.pos = self.pos
        self.rec.size = self.size