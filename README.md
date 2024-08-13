
# VoIP WebClient - Voixtel

Este projeto é uma aplicação desktop baseada em Python que utiliza PyQt6 para criar uma interface gráfica para um cliente web VoIP. A aplicação carrega uma página web específica e lida com permissões, notificações e outros recursos de forma personalizada.

## Funcionalidades

* Carregamento da Web: A aplicação carrega uma página web especificada e exibe-a em uma janela do aplicativo.
* Notificações: A aplicação exibe notificações do sistema para eventos específicos, como chamadas de áudio recebidas.
* Gestão de Permissões: Permissões de recursos, como notificações e captura de áudio, são gerenciadas e persistidas entre execuções.
* Perfil Persistente: O perfil de navegação do usuário é salvo localmente para persistência de dados.
* Logs: A aplicação registra logs detalhados de suas operações, facilitando o diagnóstico e depuração.

## Dependências

O projeto depende das seguintes bibliotecas:

* **PyQt6**: Para a interface gráfica do usuário e manipulação de páginas web.
* **requests**: Para baixar o ícone da aplicação.
* **winotify**: Para exibir notificações no Windows.
* **logging**: Para registro de logs

Para instalar as dependências, execute:

```
pip install PyQt6 requests winotify
```

## Estrutura do Projeto

* **WebClient.py**: Arquivo principal que contém a lógica da aplicação.
* **Webclient**: Diretório temporário criado para armazenar o ícone, permissões e perfil do usuário.
    * `favicon.ico`: Ícone da aplicação.
    * `pemission.json`: Arquivo JSON onde as permissões concedidas/negadas são salvas.
    * `data`: Diretório onde o perfil do usuário é salvo.
    * `debug.log`: Arquivo de log onde as mensagens de depuração são registradas.

## Como Executar

1. Certifique-se de que todas as dependências estão instaladas.
2. Execute o script principal:

```
python WebClient.py
```
A aplicação será iniciada, carregando a página web especificada e gerenciando permissões e notificações conforme configurado.

## Logging

Todos os eventos significativos e erros são registrados em um arquivo de log localizado em:

```
<diretório temporário>/Webclient/debug.log
```

## Notificações

A aplicação exibe uma notificação quando um evento específico, como uma nova chamada, é detectado na página carregada.

## Gerenciamento de Permissões

As permissões concedidas ou negadas para funcionalidades específicas da página web são armazenadas em um arquivo JSON, permitindo que sejam persistidas entre execuções da aplicação.

## Criar um .exe no Python

```
pyinstaller --noconfirm --onefile --windowed --icon "C:\Github\WebClient\favicon.ico" "C:/Github/WebClient/WebClient.py"
```

# Criando um Instalador com Inno Setup

Para distribuir sua aplicação, você pode usar o Inno Setup para criar um instalador. O Inno Setup é uma ferramenta poderosa e gratuita para criar instaladores do Windows.

## Pré-requisitos

Inno Setup: Certifique-se de que o Inno Setup está instalado em seu sistema. Você pode baixá-lo [aqui](https://jrsoftware.org/download.php/is.exe?site=1).

## Passos para Criar o Instalador
1. Abra o Inno Setup: Inicie o Inno Setup Compiler no seu computador.

2. Carregue o Script: Abra o arquivo .iss que você já criou:

* No menu do Inno Setup, vá em File > Open... e selecione o seu arquivo .iss.

3. Verifique o Script: Revise o arquivo .iss para garantir que todos os caminhos e configurações estão corretos. Em particular, verifique:

* SourceDir: O diretório onde seus arquivos de origem (binários, ícones, etc.) estão localizados.

* OutputDir: O diretório onde o instalador gerado será salvo.

* AppName e AppVersion: O nome e a versão do seu aplicativo.

4. Compilar o Script: Para gerar o instalador:

* No menu do Inno Setup, clique em Build > Compile.
* O Inno Setup irá compilar o script e gerar um instalador .exe na pasta especificada no campo OutputDir.
5. Teste o Instalador: Após a compilação, vá até o diretório de saída e execute o instalador gerado para garantir que tudo está funcionando corretamente.

```
[Setup]
AppId={{84B51460-1C38-49A3-B826-C9628A7031B7}
AppName=VoIP WebClient - Voixtel
AppVersion=1.0
AppPublisher=Voixtel, Inc.
AppPublisherURL=https://www.voixtel.com.br
AppSupportURL=https://www.voixtel.com.br
AppUpdatesURL=https://www.voixtel.com.br
DefaultDirName={pf}\VoIP WebClient - Voixtel
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
ChangesAssociations=yes
DisableProgramGroupPage=yes
OutputDir=C:\Github\Inno Setup
OutputBaseFilename=VoixtelInstall
SetupIconFile=C:\Github\WebClient\favicon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Github\WebClient\WebClient.exe"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\VoIP WebClient - Voixtel"; ValueType: string; ValueData: "{app}\WebClient.exe"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\VoIP WebClient - Voixtel"; ValueType: string; ValueData: "VoIP WebClient - Voixtel"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueData: "{app}\WebClient.exe"; Flags: uninsdeletekey

[Icons]
Name: "{autoprograms}\VoIP WebClient - Voixtel"; Filename: "{app}\WebClient.exe"
Name: "{autodesktop}\VoIP WebClient - Voixtel"; Filename: "{app}\WebClient.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\WebClient.exe"; Description: "{cm:LaunchProgram,VoIP WebClient - Voixtel}"; Flags: nowait postinstall skipifsilent

```

## Dicas Adicionais
* Adicionar Dependências: Se o seu aplicativo precisar de dependências como bibliotecas do Visual C++ ou Python, você pode configurá-las na seção [Run] do seu arquivo .iss.

* Atualizações Automáticas: Se você planeja adicionar atualizações automáticas ao seu instalador, considere configurar um mecanismo de verificação de versões.

Com essas instruções, você deve ser capaz de gerar um instalador funcional para sua aplicação usando o Inno Setup.