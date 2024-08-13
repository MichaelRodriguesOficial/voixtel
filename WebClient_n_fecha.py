import sys
import requests
import logging
import json
import tempfile
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QUrl, Qt, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from winotify import Notification

# Definir o caminho da pasta Webclient e o ícone
CACHE_DIR = os.path.join(tempfile.gettempdir(), 'Webclient')
ICON_PATH = os.path.join(CACHE_DIR, 'favicon.ico')
PERMISSION_FILE_PATH = os.path.join(CACHE_DIR, 'pemission.json')
PROFILE_PATH = os.path.join(CACHE_DIR, 'data')  # Adicionado para o perfil persistente
LOG_FILE_PATH = os.path.join(CACHE_DIR, 'debug.log')

# Garantir que a pasta Webclient exista
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(PROFILE_PATH, exist_ok=True)  # Criar diretório para o perfil

# Configurar o logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(LOG_FILE_PATH),
    logging.StreamHandler(sys.stdout)
])

def download_icon(url):
    """Baixar o ícone e salvar localmente."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(ICON_PATH, 'wb') as f:
                f.write(response.content)
            logging.debug(f"Ícone salvo em '{ICON_PATH}'.")
            return True
        else:
            logging.error(f"Falha ao baixar o ícone. Status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Erro ao baixar o ícone: {e}")
        return False

def start_app():
    """Iniciar o aplicativo PyQt."""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())

def main():
    """Função principal para baixar o ícone e iniciar o aplicativo."""
    icon_url = 'https://webclient.cloud.voixtel.net.br/static/panel/img/favicon.ico'  # Substitua pelo URL real do favicon
    if download_icon(icon_url):
        start_app()
    else:
        logging.error("Não foi possível baixar o ícone. O aplicativo não será iniciado.")

class CustomWebEnginePage(QWebEnginePage):
    """Página personalizada para manipular mensagens do console JavaScript e exibir notificações."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level: int, message: str, lineNumber: int, sourceID: str):
        """Manipular mensagens do console JavaScript."""
        logging.debug(f"Console Message - Level: {level}, Message: {message}, Line: {lineNumber}, Source ID: {sourceID}")
        
        # Verifica se o evento específico foi acionado
        if "CallManagerService::start_call broadcast event [call_added]" in message:
            logging.debug("Evento 'call_added' detectado.")
            self.show_popup_notification()

    def show_popup_notification(self):
        """Exibir um pop-up de notificação no Windows."""
        icon_path = ICON_PATH if os.path.exists(ICON_PATH) else None  # Verifica se o ícone está disponível

        if icon_path:
            notificacao = Notification(
                app_id="VoIP WebClient - Voixtel",
                title="Chamada de áudio",
                msg="Nova chamada recebida",
                duration="short",
                icon=icon_path
            )
            notificacao.add_actions(label="Fechar")
            notificacao.show()
            logging.debug("Notificação exibida com sucesso.")
        else:
            logging.error("O arquivo do ícone não foi encontrado ao tentar exibir a notificação.")

class MainWindow(QMainWindow):
    """Janela principal do aplicativo."""

    FEATURE_MAPPING = {
        'Notifications': QWebEnginePage.Feature.Notifications,
        'MediaAudioCapture': QWebEnginePage.Feature.MediaAudioCapture
        # Adicione mais mapeamentos se necessário
    }

    def __init__(self):
        super().__init__()
        logging.debug("Inicializando a janela principal.")

        # Criar um perfil com armazenamento persistente
        self.profile = QWebEngineProfile("Profile", None)
        self.profile.setPersistentStoragePath(PROFILE_PATH)
        logging.debug(f"Perfil criado com armazenamento persistente em '{PROFILE_PATH}'.")

        # Inicializar Permissions interno
        self.permissions = {
            'permissions': {},
            'credentials': {}
        }
        self.load_permissions()

        # Inicializar o ícone da bandeja
        self.setWindowTitle("VoIP WebClient - Voixtel")
        logging.debug("Ícone da bandeja do sistema inicializado.")

        # Definir o ícone da janela principal
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
            logging.debug("Ícone da janela principal definido com sucesso.")
        else:
            logging.error("O arquivo do ícone não foi encontrado ao tentar definir o ícone da janela.")

        # Remover botão de fechar
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        logging.debug("Botão de fechar removido da janela.")

        # Criar um layout
        layout = QVBoxLayout()

        # Criar uma visualização da web com a página personalizada e perfil
        self.web_view = QWebEngineView()
        self.web_page = CustomWebEnginePage(self.profile, self.web_view)
        self.web_view.setPage(self.web_page)

        # Conectar o sinal de solicitação de permissão
        self.web_view.page().featurePermissionRequested.connect(self.onFeaturePermissionRequested)
        logging.debug("Conexão estabelecida para o sinal de solicitação de permissão.")

        layout.addWidget(self.web_view)

        # Criar um widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        logging.debug("Layout e widget central configurados.")

        # Aplicar permissões salvas
        self.apply_saved_permissions()

        # Abrir a página da web diretamente ao inicializar
        self.open_web_page()

        # Abrir a janela maximizada
        self.showMaximized()
        logging.debug("Janela principal aberta maximizada.")

    
    def open_web_page(self):
        """Carregar a página da web no QWebEngineView."""
        url = QUrl("https://webclient.cloud.voixtel.net.br")
        self.web_view.load(url)
        logging.debug(f"Carregando a página da web: {url.toString()}")

    def onFeaturePermissionRequested(self, url: QUrl, feature: QWebEnginePage.Feature):
        """Manipular solicitações de permissão do QWebEnginePage."""
        logging.debug(f"Solicitação de permissão para feature: {feature.name} em {url.toString()}")

        # Conceder permissão automaticamente
        if feature in self.FEATURE_MAPPING.values():
            self.web_view.page().setFeaturePermission(url, feature, QWebEnginePage.PermissionPolicy.PermissionGrantedByUser)
            self.permissions['permissions'][feature.name] = 'granted'
            logging.debug(f"Permissão para {feature.name} concedida.")
        else:
            self.web_view.page().setFeaturePermission(url, feature, QWebEnginePage.PermissionPolicy.PermissionDeniedByUser)
            self.permissions['permissions'][feature.name] = 'denied'
            logging.debug(f"Permissão para {feature.name} negada.")
        
        # Salvar o Permissions após atualizar permissões
        self.save_permissions()

    def save_permissions(self):
        """Salvar o Permissions em um arquivo JSON."""
        try:
            logging.debug(f"Dados do Permissions antes de salvar: {self.permissions}")
            with open(PERMISSION_FILE_PATH, 'w') as f:
                json.dump(self.permissions, f, indent=4)
            logging.debug(f"Permissions salvo em '{PERMISSION_FILE_PATH}'.")
        except IOError as e:
            logging.error(f"Erro ao salvar o Permissions: {e}")

    def load_permissions(self):
        """Carregar o Permissions de um arquivo JSON."""
        try:
            if os.path.exists(PERMISSION_FILE_PATH):
                with open(PERMISSION_FILE_PATH, 'r') as f:
                    self.permissions = json.load(f)
                logging.debug(f"Permissions carregado de '{PERMISSION_FILE_PATH}'.")
            else:
                logging.debug(f"Permissions não encontrado. Criando um novo Permissions.")
                self.permissions = {'permissions': {}, 'credentials': {}}
        except IOError as e:
            logging.error(f"Erro ao carregar o Permissions: {e}")

    def apply_saved_permissions(self):
        """Aplicar permissões salvas."""
        logging.debug("Aplicando permissões salvas.")
        for feature, status in self.permissions['permissions'].items():
            feature_enum = getattr(QWebEnginePage.Feature, feature, None)
            if feature_enum:
                permission = QWebEnginePage.PermissionPolicy.PermissionGrantedByUser if status == 'granted' else QWebEnginePage.PermissionPolicy.PermissionDeniedByUser
                self.web_view.page().setFeaturePermission(QUrl("https://webclient.cloud.voixtel.net.br"), feature_enum, permission)
                logging.debug(f"Permissão aplicada: {feature} - Status: {status}")

    def closeEvent(self, event: QEvent):
        """Ignorar o evento de fechar a janela."""
        logging.debug("Tentativa de fechar a janela detectada. Ignorando o evento de fechamento.")
        # Ignorar o evento de fechar
        event.ignore()

if __name__ == "__main__":
    main()
