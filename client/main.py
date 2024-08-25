from kivy.app import App
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from plyer import vibrator

SERVER_URL = "http://192.168.0.139:5000"


class HugApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")

        self.hug_button = Button(
            text="Отправить обнимашку", on_press=self.send_hug, on_release=self.stop_hug
        )

        layout.add_widget(self.hug_button)

        self.user_id = None  # Инициализация user_id

        # Регистрируем устройство на сервере
        self.register_device()

        # Запускаем проверку на получение "обнимашек" в фоновом режиме
        Clock.schedule_interval(self.check_for_hug, 1)

        return layout

    def register_device(self):
        def on_success(req, result):
            self.user_id = int(result.split(": ")[-1])
            print(f"Device registered with ID: {self.user_id}")

        def on_failure(req, result):
            print("Failed to register device")

        UrlRequest(
            f"{SERVER_URL}/register", on_success=on_success, on_failure=on_failure
        )

    def send_hug(self, instance):
        print("Attempting to send hug...")

        def on_success(req, result):
            print("Hug sent successfully")

        def on_failure(req, result):
            print("Failed to send hug")

        UrlRequest(
            f"{SERVER_URL}/send_hug",
            on_success=on_success,
            on_failure=on_failure,
            method="POST",
        )

    def stop_hug(self, instance):
        print("Attempting to stop hug...")

        def on_success(req, result):
            print("Hug stopped successfully")

        def on_failure(req, result):
            print("Failed to stop hug")

        UrlRequest(
            f"{SERVER_URL}/stop_hug",
            on_success=on_success,
            on_failure=on_failure,
            method="POST",
        )

    def check_for_hug(self, dt):
        if self.user_id is None:
            print("User ID not set yet, skipping check.")
            return  # Пропустить проверку, если user_id еще не установлен

        print("Checking for hug...")

        def on_success(req, result):
            print(f"Received check_hug response: {result}")
            if result == "Hug received!":
                print("Triggering vibration...")
                self.trigger_vibration()
            elif result == "Stop hug":
                print("Stopping vibration...")
                self.stop_vibration()

        def on_failure(req, result):
            print("Failed to check for hug")

        UrlRequest(
            f"{SERVER_URL}/check_hug?id={self.user_id}",
            on_success=on_success,
            on_failure=on_failure,
        )

    def trigger_vibration(self):
        print("Vibrating the device...")
        vibrator.vibrate(10000)  # Вибрация на 10 секунд, но мы остановим её вручную

    def stop_vibration(self):
        print("Canceling vibration...")
        vibrator.cancel()


if __name__ == "__main__":
    HugApp().run()
