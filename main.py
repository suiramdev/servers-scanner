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
            for port in nm.scan(ip, "1-7777")["scan"][ip]["tcp"].keys():
                try:
                    server = MinecraftServer.lookup(ip + ":" + port)
                    print("Server found:", server.host, ":", port)
                except:
                    pass
        except:
            pass
    print("End thread", threading.current_thread().name)

if __name__ == '__main__':
    startTime = time.time()
    for i in range(1, 10):
        threading.Thread(name=i, target=thread, args=[i]).start()
    print("Executed in", (time.time() - startTime), "seconds")