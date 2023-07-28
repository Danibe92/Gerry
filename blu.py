#pip install winrt
import bluetooth
import socket
def connect_to_device(device_name):
   try:
    nearby_devices = bluetooth.discover_devices()
    for address in nearby_devices:
        name = bluetooth.lookup_name(address)
        if name == device_name:
            print("Trovato dispositivo:", name)
            print("Indirizzo MAC:", address)
            try:
                s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                s.connect((address,1))  # Il canale RFCOMM predefinito per la connessione Bluetooth
                return "Connesso al dispositivo Bluetooth!"
                # Puoi inserire qui il codice per interagire con il dispositivo connesso
                # Ad esempio, puoi inviare e ricevere dati tramite sock.send() e sock.recv()
            except bluetooth.BluetoothError as e:
                return "Errore durante la connessione:", str(e)
            except:
                return "Dispositivo non trovato."
   except:
      return "attiva il bluetooth" 