import uuid

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from plyer import vibrator
from requests import get, post

SERVER_URL = "http://78.31.74.66:5000"
DEVICE_ID = str(uuid.uuid4())


class HugApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")
        self.hug_button = Button(
            text="отправить обнимашку..",
            on_press=self.start_hug,
            on_release=self.stop_hug,
        )
        layout.add_widget(self.hug_button)
        Clock.schedule_interval(self.check_hug, 1)
        return layout

    def start_hug(self, instance):
        post(
            f"{SERVER_URL}/start_hug",
            json={"device_id": DEVICE_ID},
            headers={"Content-type": "application/json"},
        )

    def stop_hug(self, instance):
        post(
            f"{SERVER_URL}/stop_hug",
            json={"device_id": DEVICE_ID},
            headers={"Content-type": "application/json"},
        )

    def check_hug(self, instance):
        response = get(f"{SERVER_URL}/check_hug?device_id={DEVICE_ID}")
        if response.ok:
            result = response.json()
            print(result)
            if result.get("should_vibrate"):
                vibrator.vibrate(3)
            elif result.get("should_cancel"):
                vibrator.cancel()


if __name__ == "__main__":
    HugApp().run()
