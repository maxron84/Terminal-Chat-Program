"""
Translation module for Terminal Chat
Supports English and German languages
"""

TRANSLATIONS = {
    'en': {
        # Launcher
        'launcher_title': '🎨 Terminal Chat Launcher 🎨',
        'launcher_subtitle': 'Secure Encrypted Chat Experience',
        'choose_language': 'Choose language / Sprache wählen:',
        'language_en': 'English',
        'language_de': 'Deutsch (German)',
        'choose_mode': 'Choose mode:',
        'mode_server': 'Start Server (host a chat room)',
        'mode_client': 'Connect to Server (join a chat room)',
        'enter_choice': 'Enter choice',
        'invalid_choice': 'Invalid choice! Please enter',
        'server_setup': '╔════ Server Setup ════╗',
        'client_setup': '╔════ Client Setup ════╗',
        'port_number': 'Port number',
        'password': 'Password',
        'password_shared': 'Password (shared with clients)',
        'password_from_server': 'Password (from server)',
        'your_username': 'Your username',
        'server_ip': 'Server IP address',
        'starting_server': 'Starting server...',
        'connecting': 'Connecting to chat...',
        'share_password': 'Share the password with clients',
        'cancelled': 'Cancelled by user',
        'error': 'Error',
        
        # Common
        'port': 'Port',
        'server': 'Server',
        'username': 'Username',
        'required_field': 'This field is required!',
        
        # Chat Commands
        'cmd_list': '/list',
        'cmd_inbox': '/inbox',
        'cmd_outbox': '/outbox',
        'cmd_upload': '/upload',
        'cmd_download': '/download',
        'cmd_quit': '/quit',
        'cmd_help': '/help',
        
        # Help Command
        'help_title': 'AVAILABLE COMMANDS',
        'help_list': 'List files in shared folder',
        'help_inbox': 'List files in your inbox',
        'help_outbox': 'List files in your outbox',
        'help_upload': 'Upload file to shared folder (public)',
        'help_upload_private': 'Send private file to specific user',
        'help_download': 'Download file from shared or inbox',
        'help_quit': 'Exit the chat',
        'help_help': 'Show this help message',
        'help_regular_msg': 'Regular messages:',
        'help_regular_desc': 'Just type and press Enter to chat',
        'help_files': 'Files:',
        'help_files_desc': "Place files in 'data/outbox/' before uploading",
        'help_private_title': 'Private File Sharing:',
        'help_private_desc': 'Use @username to send files privately (only recipient can see)',
        'help_private_example': 'Example:',
        'help_private_download': 'Recipient downloads with:',
        
        # Chat Messages
        'connecting': 'Connecting to',
        'connected_as': 'Connected as',
        'commands_available': 'Commands: /upload <file> [@user], /download <file>, /list, /inbox, /outbox, /help, /quit',
        'shared_folder': 'Shared folder contents:',
        'shared_empty': 'Shared folder is empty',
        'inbox_contents': 'Inbox contents:',
        'inbox_empty': 'Inbox is empty',
        'inbox_desc': 'Downloaded files will appear here',
        'outbox_contents': 'Outbox contents:',
        'outbox_empty': 'Outbox is empty',
        'outbox_desc': "Place files in 'data/outbox/' folder to upload them",
        'file_not_found': 'File not found in outbox:',
        'file_hint': "Hint: Files must be in the 'data/outbox/' folder",
        'requesting_file': 'Requesting',
        'from_shared': 'from shared folder...',
        'uploaded': 'Uploaded',
        'to_shared': 'to shared folder',
        'receiving': 'Receiving',
        'saved_to': 'Saved to',
        'sent': 'Sent',
        'sent_privately': 'Sent {filename} privately to {user}',
        'disconnecting': 'Disconnecting...',
        'disconnected': 'Disconnected.',
        'server_shutdown': 'Server is shutting down',
        'joined_chat': 'joined the chat',
        'left_chat': 'left the chat',
    },
    'de': {
        # Launcher
        'launcher_title': '🎨 Terminal Chat Launcher 🎨',
        'launcher_subtitle': 'Sichere Verschlüsselte Chat-Erfahrung',
        'choose_language': 'Choose language / Sprache wählen:',
        'language_en': 'English',
        'language_de': 'Deutsch (German)',
        'choose_mode': 'Modus wählen:',
        'mode_server': 'Server starten (Chat-Raum hosten)',
        'mode_client': 'Mit Server verbinden (Chat-Raum beitreten)',
        'enter_choice': 'Auswahl eingeben',
        'invalid_choice': 'Ungültige Auswahl! Bitte geben Sie ein',
        'server_setup': '╔════ Server-Einrichtung ════╗',
        'client_setup': '╔════ Client-Einrichtung ════╗',
        'port_number': 'Port-Nummer',
        'password': 'Passwort',
        'password_shared': 'Passwort (mit Clients geteilt)',
        'password_from_server': 'Passwort (vom Server)',
        'your_username': 'Ihr Benutzername',
        'server_ip': 'Server-IP-Adresse',
        'starting_server': 'Server wird gestartet...',
        'connecting': 'Verbinde mit Chat...',
        'share_password': 'Teilen Sie das Passwort mit den Clients',
        'cancelled': 'Vom Benutzer abgebrochen',
        'error': 'Fehler',
        
        # Common
        'port': 'Port',
        'server': 'Server',
        'username': 'Benutzername',
        'required_field': 'Dieses Feld ist erforderlich!',
        
        # Chat Commands (keep English commands, translate descriptions)
        'cmd_list': '/list',
        'cmd_inbox': '/inbox',
        'cmd_outbox': '/outbox',
        'cmd_upload': '/upload',
        'cmd_download': '/download',
        'cmd_quit': '/quit',
        'cmd_help': '/help',
        
        # Help Command
        'help_title': 'VERFÜGBARE BEFEHLE',
        'help_list': 'Dateien im gemeinsamen Ordner auflisten',
        'help_inbox': 'Dateien in Ihrem Posteingang auflisten',
        'help_outbox': 'Dateien in Ihrem Postausgang auflisten',
        'help_upload': 'Datei in gemeinsamen Ordner hochladen (öffentlich)',
        'help_upload_private': 'Private Datei an bestimmten Benutzer senden',
        'help_download': 'Datei von gemeinsam oder Posteingang herunterladen',
        'help_quit': 'Chat beenden',
        'help_help': 'Diese Hilfemeldung anzeigen',
        'help_regular_msg': 'Normale Nachrichten:',
        'help_regular_desc': 'Einfach tippen und Enter drücken zum Chatten',
        'help_files': 'Dateien:',
        'help_files_desc': "Dateien vor dem Hochladen in 'data/outbox/' ablegen",
        'help_private_title': 'Privater Dateiaustausch:',
        'help_private_desc': '@benutzername verwenden um Dateien privat zu senden (nur Empfänger kann sehen)',
        'help_private_example': 'Beispiel:',
        'help_private_download': 'Empfänger lädt herunter mit:',
        
        # Chat Messages
        'connecting': 'Verbinde mit',
        'connected_as': 'Verbunden als',
        'commands_available': 'Befehle: /upload <datei> [@benutzer], /download <datei>, /list, /inbox, /outbox, /help, /quit',
        'shared_folder': 'Gemeinsamer Ordner Inhalt:',
        'shared_empty': 'Gemeinsamer Ordner ist leer',
        'inbox_contents': 'Posteingang Inhalt:',
        'inbox_empty': 'Posteingang ist leer',
        'inbox_desc': 'Heruntergeladene Dateien erscheinen hier',
        'outbox_contents': 'Postausgang Inhalt:',
        'outbox_empty': 'Postausgang ist leer',
        'outbox_desc': "Dateien in 'data/outbox/' Ordner ablegen um sie hochzuladen",
        'file_not_found': 'Datei nicht gefunden im Postausgang:',
        'file_hint': "Hinweis: Dateien müssen im 'data/outbox/' Ordner sein",
        'requesting_file': 'Fordere an',
        'from_shared': 'vom gemeinsamen Ordner...',
        'uploaded': 'Hochgeladen',
        'to_shared': 'in gemeinsamen Ordner',
        'receiving': 'Empfange',
        'saved_to': 'Gespeichert in',
        'sent': 'Gesendet',
        'sent_privately': '{filename} privat an {user} gesendet',
        'disconnecting': 'Verbindung wird getrennt...',
        'disconnected': 'Verbindung getrennt.',
        'server_shutdown': 'Server wird heruntergefahren',
        'joined_chat': 'ist dem Chat beigetreten',
        'left_chat': 'hat den Chat verlassen',
    }
}


class Translator:
    """Handle translations for the chat application"""
    
    def __init__(self, language='en'):
        """
        Initialize translator
        
        Args:
            language (str): Language code ('en' or 'de')
        """
        self.language = language if language in TRANSLATIONS else 'en'
    
    def t(self, key, **kwargs):
        """
        Translate a key
        
        Args:
            key (str): Translation key
            **kwargs: Format arguments for the translation
            
        Returns:
            str: Translated string
        """
        translation = TRANSLATIONS.get(self.language, {}).get(key, key)
        if kwargs:
            return translation.format(**kwargs)
        return translation
    
    def get_language(self):
        """Get current language code"""
        return self.language