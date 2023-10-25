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
        # Entrando
        self.sign_in_email = self.auth_options('Entre com seu Email', False)
        self.sign_in_password = self.auth_options('Entre com sua senha', True)
        self.sign_in_button = self.auth_buttons('Entre', lambda e: self.authenticate_users(e))

        # Registrando
        self.register_email = self.auth_options('Criar um novo email', False)
        self.register_password = self.auth_options('Criar uma senha', True)
        self.register_button = self.auth_buttons('Registre', None)

        # Sessão do usuario
        self.user_id = ''
        self.email = ''

        super().__init__()

    def auth_options(self, label, password):
        return TextField(
            label=label,
            label_style=TextStyle(size=8, color='black', weight='bold'),
            width=240,
            height=50,
            text_size=12,
            cursor_width=1,
            color='black',
            border_color='black',
            border='underline',
            border_width=1,
            password=password,
        )

    def authenticate_users(self, event):
        try:
            user = auth.sign_in_with_email_and_password(
                self.sign_in_email.value, self.sign_in_password.value
            )
            # Detalhes para os chat
            self.user_id = user['localId']
            self.email = user['email']

            # Se a autenticação for bem sucedida, fechar o login e abrir o chat
            self.close_auth_box()

            pass
        except Exception as e:
            print(e)

    def auth_buttons(self, label, btn_function):
        return ElevatedButton(
            content=Text(label, size=13, color='black', weight='bold'),
            width=240,
            height=40,
            style=ButtonStyle(shape={'': RoundedRectangleBorder(radius=8)}),
            on_click=btn_function,
        )

    def open_auth_box(self):
        time.sleep(1),
        self.auth_box.width = 620
        self.auth_box.update()
        time.sleep(0.35),
        self.auth_box_row.opacity = 1
        self.auth_box_row.update()

    def close_auth_box(self):
        self.auth_box_row.opacity = 0
        self.auth_box_row.update()
        time.sleep(0.8)
        self.auth_box.width=0
        self.auth_box.update()
        time.sleep(0.75)
        self.page.controls.remove(self)
        time.sleep(0.25)

        # Initicializando o chat pela class
        self.chat = Chat(self.user_id, self.email)

        # Adicionando o chat a page
        self.page.controls.insert(0, self.chat)
        self.page.update()
        time.sleep(0.25)

        # Abridno o chat box
        self.chat.open_chat_box()
        pass

    def build(self):
        # so a the genereal layout is 1x row 2 column, each colum will have a title, 2x input fields, and 1x button
        # this is how we create this layout whit goofe coding practices
        labels: list = ['Sign In', 'Register']
        texts: list = [
            self.sign_in_email,
            self.sign_in_password,
            self.sign_in_button,
            self.register_email,
            self.register_password,
            self.register_button,
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

# Criando o Chat UI/Logic
class Chat(UserControl):
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email
        self.count = 0

        self.chat_box = Container(
            width=620,
            height=0,
            bgcolor='#ffffff',
            border_radius=8,
            animate=animation.Animation(550, 'easeOutBack'),
            clip_behavior=ClipBehavior.HARD_EDGE,
        )

        self.chat_arena = Column(
            expand=True,
            scroll='hidden',
            auto_scroll=True,
        )

        self.chat_input = TextField(
            width=540,
            height=45,
            text_size=12,
            cursor_width=1,
            color='black',
            cursor_color='black',
            border_color='black',
            border_width=1,
            content_padding=8,
        )

        self.chat_send_button = ElevatedButton(
            content=Icon(
                name=icons.SEND,
                size=13,
                color='white',
                rotate=transform.Rotate(5.5, alignment.center),
            ),
            width=45,
            height=45,
            style=ButtonStyle(shape={'': RoundedRectangleBorder(radius=8)}),
            bgcolor='#202224',
            on_click= lambda e: self.push_message_to_db(e),
        )

        # Inicializando o chat historico aqui
        self.set_chat_history()

        self.star_listening()

        super().__init__()

    def open_chat_box(self):
        self.chat_box.height = 630
        self.chat_box.update()

    def chat_box_header(self):
        return Card(
            width=620,
            height=65,
            elevation=10,
            margin=-10,
            content=Container(
                alignment=alignment.center,
                padding=padding.only(top=10),
                bgcolor='#202224',
                content=Text('Chat', weight='bold', size=21, color='white')
            )
        )

    def push_message_to_db(self, event):
        try:
            # Recarregar o database do pyrebase
            data = {
                # Tempo para o text ser enviado pelo historico
                "timestamp": int(time.time() * 1000),
                "message": self.chat_input.value,
                # Gerado quando o user autentica e isso é passado para a classe
                "uuid": self.user_id,
                # Usando o email como nome para testar
                # Depois alterar para o Nome
                "email": self.email,
            },
            # Agora puxando o database
            # child("message") is the main node here
            # child(int(time.time())) sets up a new node with the time stamp
            # this makes it easier to sort when we retrive the data
            db.child("message").child(int(time.time()* 1000)).set(data)

            pass
        except Exception as e:
            print(e)

        finally:
            self.chat_input.value = ""
            self.chat_input.update()
            # Enviando messagem como teste para o database
        pass

    # Agora obtendo a atual mensaem ui, i.e.e como no display
    def chat_message_ui(self, sent_time, name, text_message, col_pos, row_pos, bg):
        return Container(
            padding=padding.only(left=25, top=12, bottom=12, right=25),
            bgcolor=bg,
            border_radius=8,
            margin=5,
            content=Column(
                horizontal_alignment=col_pos,
                spacing=5,
                controls=[
                    Row(alignment=row_pos,
                        controls=[
                            Text(
                                name + " @ " + sent_time,
                                color='black',
                                size=8,
                                weight="bold",
                            )
                        ],
                        ),
                    Row(
                        alignment=row_pos,
                        controls=[
                            Text(
                                text_message,
                                color='black',
                                size=16
                            )
                        ]
                    )
                ]
            )
        )

    # Agora quase poront tem dados in DB quando enviado a configuração para cima nos podemos testar o historico do chat
    # Isso é vital para a função para qualquer aplicação

    def set_chat_history(self):
        try:
            """ a logica segue alguns passos:
            1 obter as anotaçõs, i.e timestamps das mensagens como a lista
            2 sortia a lista, automaticament pelo mais velho para o mais novo. Usando o timestamps como a anotação,
            isso faz ser mais facil sortear pela data
            3 depois de sorted, no podemo checar se as messagem é do usuario, ou parte do numero menber, e bases nessa infomação
            ordenar no UI de acordo accordingly
            """

            keys = list(db.child("message").get().val().keys())
            sorted_keys = sorted(keys, key=lambda x: int(x))

            if sorted_keys is not None: # Check para ver se tem informação
                items = []
                for key in sorted_keys:
                    # Value e agora um dicionario objeto com dados por anotação
                    value = db.child("message").child(key).get().val()
                    # Nos precisamo converter o timestamp ára um valor legibel

                    time = datetime.datetime.fromtimestamp(value["timestamp"]/ 1000.0).strftime("%H:%M")
                    print("aqui")
                    # Próxima verificação the uif se o user ou algo
                    if value["uuid"] == self.user_id:
                        items.append(
                            self.chat_message_ui(
                                time,
                                value["email"],
                                value["message"],
                                CrossAxisAlignment.END,
                                MainAxisAlignment.END,
                                "teal100"
                            ),
                        )
                    else:
                        items.append(
                            self.chat_message_ui(
                                time,
                                value["email"],
                                value["message"],
                                CrossAxisAlignment.START,
                                MainAxisAlignment.START,
                                "blue100"
                            ),
                        )
                # Finalmente adicionando ao main a area do chat
                self.chat_arena.controls = items
                #self.chat_arena.update()
            else:
                pass
        except Exception as e:
            print(e)

    def stream_handler(self, value):
        # configuramos uma contagem porque imprime
        # todo o banco de dados quando ele é iniciado, por algum motivo, então faço isso para evitar erros
        if self.count > 0:
            # Próxima verificação the uif se o user ou algo
            time = datetime.datetime.fromtimestamp(value['data']["timestamp"] / 1000.0).strftime("%H:%M")

            if value['data']["uuid"] == self.user_id:
                self.chat_arena.controls.append(
                    self.chat_message_ui(
                        time,
                        value['data']["email"],
                        value['data']["message"],
                        CrossAxisAlignment.END,
                        MainAxisAlignment.END,
                        "teal100"
                    ),
                )
            else:
                self.chat_arena.controls.append(
                    self.chat_message_ui(
                        time,
                        value['data']["email"],
                        value['data']["message"],
                        CrossAxisAlignment.START,
                        MainAxisAlignment.START,
                        "blue100"
                    ),
                )
                self.chat_arena.update()

        else:
            pass
        self.count +=1

    def star_listening(self):
        # o que acontece aqui é que o firebase nos permite ouvir as alterações em um nó específico em tempo real db
        # estamos ouvindo conversas no nó da mensagem
        # se novos dados aparecerem, podemos lidar com esses dados usando o manipulador de stream
        self.stream = db.child("message").stream(self.stream_handler)


    def build(self):
        chat_colum = Column(
            controls=[
                self.chat_box_header(),
                Divider(height=2, color='transparent'),
                Container(
                    width=620,
                    height=480,
                    bgcolor='lightblue',
                    border=border.only(
                        bottom=border.BorderSide(0.25, 'black'),
                    ),
                    content=self.chat_arena,
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[self.chat_input, self.chat_send_button]
                ),
            ],
        )
        self.chat_box.content = chat_colum

        return self.chat_box


def main(page : Page):
    # Page
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'

    # Init Classes
    auth = Authentication()
    chat = Chat('wfHc0wgPLKd0M6zC9ZuBVbBPKna2', 'luzoaki@gmail.com')

    # Set Page
    page.add(chat)
    #page.add(auth)
    page.update()

    # Abrindo a Page
    #auth.open_auth_box()
    chat.open_chat_box()

if __name__ =='__main__':
    flet.app(target=main)