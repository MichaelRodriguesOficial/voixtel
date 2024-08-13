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
