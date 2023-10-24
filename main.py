# Modulos
import flet
from flet import *
import datetime
import time
from firebase_config import initialize_firebase

# Acesso a autenticação e e dabase via pyrebase
auth, db = initialize_firebase()

# Inicializando a autenticação, e trabalhando no caminho para aplicação
class Authentication(UserControl):
    def __init__(self):
        # crirando a instancia para o front
        self.auth_box = Container(
            width=0,
            height=350,
            bgcolor='#ffffff',
            animate=animation.Animation(550, 'easeOutBack'),
            border_radius=8,
            padding=10,
        )
        self.auth_box_row = Row(
            alignment=MainAxisAlignment.CENTER,
            spacing=30,
            opacity=100,
            animate_opacity=800,
        )

        # Agora iniciar o campos antes do loop toda vez
        self.sign_in_email = self.auth_options('Entre com seu Email', False)
        self.sign_in_password = self.auth_options('Entre com sua senha', True)

        #
        self.register_email = self.auth_options('Criar um novo email', False)
        self.register_password = self.auth_options('Criar uma senha', True)
        super().__init__()

    def auth_options(self, label, password):
        return TextField(
            label=label,
            label_style=TextStyle(size=8, color='black', weight='bold'),
            width=240,
            height=50
        )

    def open_auth_box(self):
        time.sleep(1),
        self.auth_box.width = 620
        self.auth_box.update()

    def build(self):
        # so a the genereal layout is 1x row 2 column, each colum will have a title, 2x input fields, and 1x button
        # this is how we create this layout whit goofe coding practices
        labels: list = ['Sign In', 'Register']
        texts: list = [
            self.sign_in_email,
            self.sign_in_password,
            self.register_email,
            self.register_password,
            Text('Placeholder', color='black'),
            Text('Placeholder', color='black'),
        ]

        for label in labels:
            column = Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
                spacing=30,
            )
            items = []
            items.append(Text(label, color='black', size=21, weight='bold'))
            for _ in range(3):
                items.append(texts.pop(0))
            column.controls = items
            self.auth_box_row.controls.append(column)

        self.auth_box_row.controls.insert(
            1, Text('OU', size=9, color='black', weight='bold')
        )

        self.auth_box.content = self.auth_box_row
        return self.auth_box


def main(page : Page):
    # Page
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'

    # Init Classes
    auth = Authentication()

    # Set Page
    page.add(auth)
    page.update()

    # Abrindo a Page
    auth.open_auth_box()

if __name__ =='__main__':
    flet.app(target=main)