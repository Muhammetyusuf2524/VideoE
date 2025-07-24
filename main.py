import network
import socket
import ure
import machine
import time

SSID = " ****** "   
PASSWORD = " ****** "

# WiFi bağlanma
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("WiFi bağlanılıyor...")
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
print("Bağlandı, IP:", wlan.ifconfig()[0])

# site.html dosyasını belleğe yükle
with open("site.html", "r", encoding="utf-8") as f:
    html = f.read()

def serve(client_sock):
    req = client_sock.recv(1024).decode('utf-8')
    try:
        path = ure.search(r"GET /(.*) HTTP", req).group(1)
    except:
        path = ""

    if path == "" or path == "index.html":
        client_sock.send("HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n")
        client_sock.send(html.encode('utf-8'))
    else:
        client_sock.send("HTTP/1.0 404 Not Found\r\n\r\n")
    client_sock.close()

def main():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Sunucu başlatıldı. IP adresi:", wlan.ifconfig()[0])

    while True:
        cl, addr = s.accept()
        serve(cl)

main()


