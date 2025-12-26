; Script Inno Setup para PinFlow Pro
; Cria um instalador profissional para Windows

#define MyAppName "PinFlow Pro"
#define MyAppVersion "3.0"
#define MyAppPublisher "Ede Machado"
#define MyAppURL "https://www.pinflowpro.com"
#define MyAppExeName "PinFlow_Pro.exe"

[Setup]
; Informações básicas
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppCopyright=© 2025 - Criado por Ede Machado

; Diretório padrão de instalação
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

; Arquivo de saída
OutputDir=dist\installer
OutputBaseFilename=PinFlow_Pro_Setup
SetupIconFile=alfinete_vermelho.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Compressão
Compression=lzma2/ultra64
SolidCompression=yes

; Privilégios
PrivilegesRequired=admin

; Interface
WizardStyle=modern
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

; Licença
LicenseFile=EULA.txt

; Informações de versão
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} - Instalador
VersionInfoCopyright=© 2025 Ede Machado

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar ícone na Área de Trabalho"; GroupDescription: "Ícones adicionais:"; Flags: checked
Name: "quicklaunchicon"; Description: "Criar ícone na Barra de Tarefas"; GroupDescription: "Ícones adicionais:"; Flags: unchecked
Name: "startup"; Description: "Iniciar automaticamente com o Windows"; GroupDescription: "Opções de inicialização:"

[Files]
; Executável principal
Source: "dist\PinFlow_Pro.exe"; DestDir: "{app}"; Flags: ignoreversion
; Arquivo de licenças válidas (necessário para validação)
Source: "valid_licenses.json"; DestDir: "{app}"; Flags: ignoreversion
; Ícone do alfinete vermelho
Source: "alfinete_vermelho.ico"; DestDir: "{app}"; Flags: ignoreversion
; Pasta de traduções (i18n) - copiar da pasta raiz se não estiver no dist
Source: "i18n\*"; DestDir: "{app}\i18n"; Flags: ignoreversion recursesubdirs createallsubdirs
; Documentação
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion; DestName: "LEIA-ME.txt"
Source: "EULA.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Ícone no Menu Iniciar
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"
; Ícone na Área de Trabalho (SEMPRE criado com ícone vermelho do alfinete)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\alfinete_vermelho.ico"; Tasks: desktopicon
; Ícone na Barra de Tarefas (opcional)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Registry]
; Inicialização automática com Windows
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: startup

[Run]
; Executar após instalação
Filename: "{app}\{#MyAppExeName}"; Description: "Iniciar {#MyAppName}"; Flags: nowait postinstall skipifsilent
; Abrir pasta de instalação após instalação
Filename: "explorer.exe"; Parameters: "{app}"; Description: "Abrir pasta de instalação"; Flags: postinstall skipifsilent

[UninstallDelete]
; Limpar dados ao desinstalar (opcional - comente se quiser manter os dados do usuário)
Type: filesandordirs; Name: "{userappdata}\PinFlow_Pro"

[Code]
// Verificar se já está instalado
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
  UninstallPath: String;
begin
  // Verificar se versão anterior está instalada
  if RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'Software\Microsoft\Windows\CurrentVersion\Uninstall\{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}_is1',
    'UninstallString', UninstallPath) then
  begin
    if MsgBox('Uma versão anterior do PinFlow Pro foi detectada. Deseja desinstalá-la antes de continuar?',
      mbConfirmation, MB_YESNO) = IDYES then
    begin
      Exec(RemoveQuotes(UninstallPath), '/SILENT', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
    end;
  end;
  Result := True;
end;

// Mensagem ao finalizar instalação
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Abrir pasta de instalação automaticamente
    ShellExec('open', 'explorer.exe', ExpandConstant('{app}'), '', SW_SHOWNORMAL, ewNoWait, ErrorCode);
    
    MsgBox('PinFlow Pro foi instalado com sucesso!' + #13#10#13#10 +
           'Localização: ' + ExpandConstant('{app}') + #13#10#13#10 +
           'O programa foi instalado em:' + #13#10 +
           ExpandConstant('{app}') + #13#10#13#10 +
           'Um atalho foi criado na Área de Trabalho com o ícone do alfinete.' + #13#10#13#10 +
           'A pasta de instalação será aberta automaticamente.' + #13#10#13#10 +
           'Obrigado por escolher nosso produto!' + #13#10#13#10 +
           '© 2025 - Criado por Ede Machado',
           mbInformation, MB_OK);
  end;
end;


