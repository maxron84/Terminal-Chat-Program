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