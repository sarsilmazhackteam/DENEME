import os
import subprocess
import time

# Wi-Fi arayüzünüzü (wlan0 veya wlp2s0 vb.) buraya yazın
interface = "wlan0"
ssid = "SahteAğ"  # Sahte ağ adı
password = "12345678"  # Wi-Fi şifresi
channel = 6  # Kanal numarası
interface_ip = "192.168.1.1"  # Ağ IP'si

def start_hostapd():
    """Hostapd'yi başlatır."""
    # Hostapd yapılandırma dosyasını oluşturma
    hostapd_conf = f"""
interface={interface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel={channel}
wpa=2
wpa_passphrase={password}
"""
    # Hostapd yapılandırmasını kaydetme
    with open("/etc/hostapd/hostapd.conf", "w") as f:
        f.write(hostapd_conf)
    
    # Hostapd'yi başlatma
    print("Hostapd başlatılıyor...")
    subprocess.run(["sudo", "hostapd", "/etc/hostapd/hostapd.conf"])

def start_dnsmasq():
    """Dnsmasq'ı başlatır."""
    # Dnsmasq yapılandırma dosyasını oluşturma
    dnsmasq_conf = f"""
interface={interface}
dhcp-range=192.168.1.50,192.168.1.150,12h
"""
    # Dnsmasq yapılandırmasını kaydetme
    with open("/etc/dnsmasq.conf", "w") as f:
        f.write(dnsmasq_conf)
    
    # Dnsmasq'ı başlatma
    print("Dnsmasq başlatılıyor...")
    subprocess.run(["sudo", "dnsmasq"])

def enable_ip_forwarding():
    """IP yönlendirmeyi etkinleştirir."""
    print("IP yönlendirmesi etkinleştiriliyor...")
    subprocess.run(["sudo", "sysctl", "net.ipv4.ip_forward=1"])
    subprocess.run(["sudo", "iptables", "-t", "nat", "-A", "POSTROUTING", "-o", "eth0", "-j", "MASQUERADE"])

def setup_wifi():
    """Wi-Fi ağını oluşturur."""
    print("Sahte ağ kuruluyor...")
    
    # Wi-Fi arayüzünü Ad-Hoc moduna al
    subprocess.run(f"sudo iw dev {interface} set type managed", shell=True)
    
    # Ağ arayüzünü aç
    subprocess.run(f"sudo ifconfig {interface} up", shell=True)
    
    # Sahte Wi-Fi ağı kurma
    start_hostapd()
    start_dnsmasq()
    enable_ip_forwarding()

    print(f"Sahte ağ {ssid} başlatıldı ve şifresi: {password}")

if __name__ == "__main__":
    setup_wifi()
