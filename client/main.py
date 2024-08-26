import uuid

from kivy.app import App
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from plyer import vibrator

SERVER_URL = "http://78.31.74.66:25565"
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
        def on_success(req, result):
            print("Hug started!")

        def on_failure(req, result):
            print("Failed to start hug!")

        UrlRequest(
            f"{SERVER_URL}/start_hug",
            req_body=f'{{"device_id": "{DEVICE_ID}"}}',
            on_success=on_success,
            on_failure=on_failure,
            method="POST",
            req_headers={"Content-type": "application/json"},
        )

    def stop_hug(self, instance):
        def on_success(req, result):
            print("Hug stopped!")

        def on_failure(req, result):
            print("Failed to stop hug!")

        UrlRequest(
            f"{SERVER_URL}/stop_hug",
            req_body=f'{{"device_id": "{DEVICE_ID}"}}',
            on_success=on_success,
            on_failure=on_failure,
            method="POST",
            req_headers={"Content-type": "application/json"},
        )

    def check_hug(self, instance):
        def on_success(req, result):
            if result.get("should_vibrate"):
                vibrator.vibrate(3)
            elif result.get("should_cancel"):
                vibrator.cancel()

        def on_failure(req, result):
            print("Failed to check hug status!")

        UrlRequest(
            f"{SERVER_URL}/check_hug?device_id={DEVICE_ID}",
            on_success=on_success,
            on_failure=on_failure,
        )


if __name__ == "__main__":
    HugApp().run()
