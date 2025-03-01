import os
import subprocess
import time

# Kullanıcıdan giriş alalım (Wi-Fi arayüzü ve USB tethering arayüzü için)
wifi_interface = "wlan0"  # Wi-Fi arayüzü (Wi-Fi adaptörünüzün adı)
usb_interface = "eth0"  # USB tethering üzerinden gelen internetin arayüzü

# Adım 1: İnternet paylaşımını sağlamak için IP yönlendirmesini etkinleştir
def enable_ip_forwarding():
    print("IP yönlendirmesi etkinleştiriliyor...")
    os.system("sudo sysctl -w net.ipv4.ip_forward=1")

# Adım 2: İptables kurallarını ekleyerek interneti paylaşmak
def set_iptables():
    print("IPTables ayarları yapılıyor...")
    os.system(f"sudo iptables -t nat -A POSTROUTING -o {wifi_interface} -j MASQUERADE")
    os.system(f"sudo iptables -A FORWARD -i {usb_interface} -o {wifi_interface} -m state --state RELATED,ESTABLISHED -j ACCEPT")
    os.system(f"sudo iptables -A FORWARD -i {wifi_interface} -o {usb_interface} -j ACCEPT")

# Adım 3: Dnsmasq (DHCP) servisini başlatma
def start_dnsmasq():
    print("dnsmasq başlatılıyor...")
    os.system("sudo systemctl start dnsmasq")
    os.system("sudo systemctl enable dnsmasq")

# Adım 4: Hostapd (Wi-Fi AP) yapılandırmasını başlatma
def start_hostapd():
    print("Hostapd başlatılıyor...")
    
    # Hostapd yapılandırma dosyasını yazalım
    with open("/etc/hostapd/hostapd.conf", "w") as f:
        f.write(f"""
interface={wifi_interface}
driver=nl80211
ssid=SahteAğ
hw_mode=g
channel=6
wpa=2
wpa_passphrase=12345678
        """)

    # Hostapd'yi başlatıyoruz
    os.system(f"sudo hostapd /etc/hostapd/hostapd.conf")

# Ana fonksiyon
def main():
    print("Sahte ağ kuruluyor...")
    enable_ip_forwarding()
    set_iptables()
    start_dnsmasq()
    time.sleep(2)  # dnsmasq'ın düzgün başlatılması için kısa bir bekleme
    start_hostapd()

    print("Sahte ağ başarıyla başlatıldı ve şifresi: 12345678")

if __name__ == "__main__":
    main()
    
