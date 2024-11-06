import requests
from kivy.app import App

class MyFirebase:
    API_KEY = "AIzaSyBz6l4yZAbHhdnao8g-v6yBs_DSsgBiiqY"

    def criar_conta(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            print("Usuario criado!")
            id_token = requisicao_dic['idToken'] # autenticação
            refresh_token = requisicao_dic['refreshToken'] # token que mantém o usuário logado
            local_id = requisicao_dic['localId']  # id_usuario

            meu_app = App.get_running_app()
            meu_app.id_token = id_token
            meu_app.local_id = local_id

            with open("refresh.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            link = f"https://aplicativovendashash-be58f-default-rtdb.firebaseio.com/{local_id}.json"

            info_usuario = """{"avatar": "foto1.png",
                            "equipe": "",
                            "total_vendas": "0",
                            "vendas": ""}"""

            requisicao_usuario = requests.patch(link, data=info_usuario)

            meu_app.carregar_infos_usuario()
            meu_app.mudar_tela('homepage')

        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_app = App.get_running_app()
            pagina_login = meu_app.root.ids["loginpage"]
            pagina_login.ids['mensagem_login'].text = mensagem_erro
            pagina_login.ids['mensagem_login'].color = (1, 0, 0, 1)
        print(requisicao_dic)

    def fazer_login(self, email, senha):
        pass

    def trocar_token(self, refresh_token):

        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"

        info = {"grant_type": "refresh_token",
                "refresh_token": refresh_token,}

        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        if requisicao.ok:
            local_id = requisicao_dic['user_id']
            id_token = requisicao_dic['id_token']
            return local_id, id_token

