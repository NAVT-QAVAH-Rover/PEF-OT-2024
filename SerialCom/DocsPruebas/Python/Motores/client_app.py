from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket

class UDPClientApp(App):
    def build(self):
        self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('192.168.0.100', 2222)
        self.buffer_size = 1024

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Instrucciones
        instructions = Label(text='Enter velocity and angle (Velocity 0 - 255 [Recomended more than 100], Angle 0 - 750 [Center 375]):')
        layout.add_widget(instructions)

        # Entrada para la velocidad
        self.velocity_input = TextInput(multiline=False, hint_text='Velocity')
        layout.add_widget(self.velocity_input)

        # Entrada para el ángulo
        self.angle_input = TextInput(multiline=False, hint_text='Angle')
        layout.add_widget(self.angle_input)

        # Botón para enviar
        send_button = Button(text='Send Data')
        send_button.bind(on_press=self.send_data)
        layout.add_widget(send_button)

        return layout

    def send_data(self, instance):
        velocity = self.velocity_input.text
        angle = self.angle_input.text
        message = f"{velocity},{angle}".encode('utf-8')

        # Enviar el mensaje al servidor
        self.udp_client.sendto(message, self.server_address)

        # Recibir y decodificar la respuesta del servidor
        data, address = self.udp_client.recvfrom(self.buffer_size)
        data = data.decode('utf-8')

        print('Data from Server:', data)
        print('Server IP Address:', address[0])
        print('Server Port:', address[1])

if __name__ == '__main__':
    UDPClientApp().run()
