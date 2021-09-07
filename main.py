import threading
import time
import nmap
from mcstatus import MinecraftServer

def intToIP(num):
    ip = []
    for i in range(4):
        ip.append(str(num & 0xFF))
        num = num >> 8
    return '.'.join(ip)

def thread(num):
    print("Start thread", threading.current_thread().name)
    nm = nmap.PortScanner()
    max = 4294967295
    for i in range(round(max/(num+1)+1), round(max/num)):
        ip = intToIP(i)
        try:
            nmScan = nm.scan(ip)
            server = MinecraftServer.lookup(ip)
            if (server.ping()):
                status = server.status()
                print(ip)
                print("     Description :", status.description)
                print("     Players online :", status.players.online)
        except:
            pass

if __name__ == '__main__':
    #startTime = time.time()
    #for i in range(1, 10):
    #    threading.Thread(name=i, target=thread, args=[i]).start()
    #print("Executed in", (time.time() - startTime), "seconds")
    nm = nmap.PortScanner()
    nmScan = nm.scan("194.163.182.242")
    print(nmScan)