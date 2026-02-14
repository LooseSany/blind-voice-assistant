import json
import os
from datetime import datetime
from urllib.parse import quote

from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from plyer import tts

KV = '''
#:import dp kivy.metrics.dp

<RootUI>:
    orientation: 'vertical'
    padding: dp(14)
    spacing: dp(10)

    Label:
        text: 'Blind Voice Assistant - Test APK'
        size_hint_y: None
        height: dp(44)
        font_size: '20sp'
        bold: True

    Label:
        text: root.status
        text_size: self.width, None
        halign: 'left'
        valign: 'top'

    TextInput:
        id: command_input
        hint_text: 'Type command or tap Listen and speak...'
        multiline: False
        size_hint_y: None
        height: dp(48)

    BoxLayout:
        size_hint_y: None
        height: dp(50)
        spacing: dp(8)

        Button:
            text: 'Listen'
            on_release: root.listen_android()

        Button:
            text: 'Run Command'
            on_release: root.run_text_command()

    BoxLayout:
        size_hint_y: None
        height: dp(50)
        spacing: dp(8)

        Button:
            text: 'Help'
            on_release: root.execute_command('help')

        Button:
            text: 'Show To-Dos'
            on_release: root.execute_command('show todos')

    Label:
        text: 'Quick examples: add todo buy milk | open youtube | navigate to city hospital'
        size_hint_y: None
        height: dp(54)
        text_size: self.width, None
        halign: 'left'
        valign: 'top'
        color: .6, .6, .6, 1
'''


class RootUI(BoxLayout):
    status = StringProperty('Ready. Say or type "help" to list commands.')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.todo_file = os.path.join(App.get_running_app().user_data_dir, 'todos.json')
        self.request_code = 9137
        self.android_available = False
        self._setup_android()

    def _setup_android(self):
        try:
            from android import activity  # type: ignore
            from jnius import autoclass  # type: ignore

            self.activity = activity
            self.Intent = autoclass('android.content.Intent')
            self.RecognizerIntent = autoclass('android.speech.RecognizerIntent')
            self.Locale = autoclass('java.util.Locale')
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.PackageManager = autoclass('android.content.pm.PackageManager')
            self.Uri = autoclass('android.net.Uri')
            self.android_available = True
            self.activity.bind(on_activity_result=self._on_activity_result)
        except Exception:
            self.android_available = False

    def speak(self, text):
        try:
            tts.speak(text)
        except Exception:
            pass

    @mainthread
    def update_status(self, text, speak=True):
        self.status = text
        if speak:
            self.speak(text)

    def _load_todos(self):
        if not os.path.exists(self.todo_file):
            return []
        try:
            with open(self.todo_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _save_todos(self, todos):
        os.makedirs(os.path.dirname(self.todo_file), exist_ok=True)
        with open(self.todo_file, 'w', encoding='utf-8') as f:
            json.dump(todos, f, indent=2)

    def run_text_command(self):
        cmd = self.ids.command_input.text.strip()
        if not cmd:
            self.update_status('Please say or type a command.')
            return
        self.execute_command(cmd)

    def listen_android(self):
        if not self.android_available:
            self.update_status('Voice listen works on Android APK. Use text command on desktop.')
            return

        intent = self.Intent(self.RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(
            self.RecognizerIntent.EXTRA_LANGUAGE_MODEL,
            self.RecognizerIntent.LANGUAGE_MODEL_FREE_FORM,
        )
        intent.putExtra(self.RecognizerIntent.EXTRA_LANGUAGE, self.Locale.getDefault())
        intent.putExtra(self.RecognizerIntent.EXTRA_PROMPT, 'Speak your command')

        self.update_status('Listening now...', speak=False)
        self.PythonActivity.mActivity.startActivityForResult(intent, self.request_code)

    def _on_activity_result(self, request_code, result_code, intent):
        if request_code != self.request_code:
            return

        if result_code != -1 or intent is None:
            self.update_status('Could not understand. Try again.')
            return

        try:
            results = intent.getStringArrayListExtra(self.RecognizerIntent.EXTRA_RESULTS)
            if results and results.size() > 0:
                text = str(results.get(0))
                self.ids.command_input.text = text
                self.execute_command(text)
                return
        except Exception:
            pass

        self.update_status('No speech result found. Try again.')

    def execute_command(self, raw):
        command = raw.strip().lower()

        if command == 'help':
            msg = (
                'Commands: add todo <task>, show todos, clear todos, '
                'open youtube, open calculator, open chrome, navigate to <place>, '
                'time, date.'
            )
            self.update_status(msg)
            return

        if command.startswith('add todo '):
            task = raw[9:].strip()
            if not task:
                self.update_status('Please say the task after add todo.')
                return
            todos = self._load_todos()
            todos.append(task)
            self._save_todos(todos)
            self.update_status(f'Added to-do: {task}')
            return

        if command == 'show todos':
            todos = self._load_todos()
            if not todos:
                self.update_status('Your to-do list is empty.')
                return
            msg = 'Your tasks are: ' + ', '.join(f'{i + 1}. {t}' for i, t in enumerate(todos))
            self.update_status(msg)
            return

        if command == 'clear todos':
            self._save_todos([])
            self.update_status('All to-dos cleared.')
            return

        if command.startswith('open '):
            app_name = command.replace('open ', '', 1).strip()
            self.open_app(app_name)
            return

        if command.startswith('navigate to '):
            place = raw[12:].strip()
            if not place:
                self.update_status('Please say a destination after navigate to.')
                return
            self.navigate_to(place)
            return

        if command == 'time':
            self.update_status('Current time is ' + datetime.now().strftime('%I:%M %p'))
            return

        if command == 'date':
            self.update_status('Today is ' + datetime.now().strftime('%B %d, %Y'))
            return

        self.update_status('Command not recognized. Say help for available commands.')

    def open_app(self, app_name):
        app_packages = {
            'youtube': 'com.google.android.youtube',
            'calculator': 'com.google.android.calculator',
            'chrome': 'com.android.chrome',
            'whatsapp': 'com.whatsapp',
            'maps': 'com.google.android.apps.maps',
            'phone': 'com.google.android.dialer',
        }

        package_name = app_packages.get(app_name)
        if not package_name:
            self.update_status(f'I do not know app: {app_name}. Try youtube or calculator.')
            return

        if not self.android_available:
            self.update_status(f'Open app works on Android APK only: {app_name}.')
            return

        try:
            pm = self.PythonActivity.mActivity.getPackageManager()
            launch_intent = pm.getLaunchIntentForPackage(package_name)
            if launch_intent is None:
                self.update_status(f'{app_name} is not installed.')
                return
            self.PythonActivity.mActivity.startActivity(launch_intent)
            self.update_status(f'Opening {app_name}.')
        except Exception:
            self.update_status(f'Failed to open {app_name}.')

    def navigate_to(self, place):
        if not self.android_available:
            self.update_status(f'Navigation works on Android APK. Destination: {place}.')
            return

        try:
            uri_string = f'google.navigation:q={quote(place)}'
            nav_uri = self.Uri.parse(uri_string)
            intent = self.Intent(self.Intent.ACTION_VIEW, nav_uri)
            intent.setPackage('com.google.android.apps.maps')
            self.PythonActivity.mActivity.startActivity(intent)
            self.update_status(f'Starting navigation to {place}.')
        except Exception:
            self.update_status('Failed to start navigation. Check Google Maps installation.')


class VoiceAssistantApp(App):
    def build(self):
        self.title = 'Blind Voice Assistant'
        return Builder.load_string(KV)


if __name__ == '__main__':
    VoiceAssistantApp().run()