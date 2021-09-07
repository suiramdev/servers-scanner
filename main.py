import threading
import time
from dns.rdatatype import NULL
import nmap
from mcstatus import MinecraftServer

blacklistedPools = [
    [167772160, 184549375], # 10.0.0.0 – 10.255.255.255
    [2886729728, 2887778303], # 172.16.0.0 – 172.31.255.255
    [3232235520, 3232301055], # 192.168.0.0 – 192.168.255.255
    [2130706433, 2130706433] # 127.0.0.1
]

def intToIP(num):
    return (str((num >> 24) & 0xFF) + "."
            + str((num >> 16) & 0xFF) + "."
            + str((num >> 8) & 0xFF) + "."
            + str(num & 0xFF))

def intIsBlacklisted(num):
    for pool in blacklistedPools:
        if pool[0] <= num <= pool[1]:
            return pool
        continue
    return None

def thread(num):
    print("Start thread", threading.current_thread().name)
    nm = nmap.PortScanner()
    max = 4294967295
    curr = round(max/(num+1))
    while curr < round(max/num):
        curr += 1
        blacklistedPool = intIsBlacklisted(curr)
        if blacklistedPool is not None:
            curr += blacklistedPool[1] - blacklistedPool[0] - 1 # Minus one because we are going to increase at the begin of the loop
            continue
        ip = intToIP(curr)
        print("Scanning", ip)
        try:
            for port in nm.scan(ip, "1-7777")["scan"][ip]["tcp"].keys():
                try:
                    server = MinecraftServer.lookup(ip + ":" + port)
                    print("Server found:", server.host, ":", port)
                except:
                    pass
        except:
            time.sleep(2)
            pass
    print("End thread", threading.current_thread().name)

if __name__ == '__main__':
    startTime = time.time()
    for i in range(1, 10):
        threading.Thread(name=i, target=thread, args=[i]).start()
    print("Executed in", (time.time() - startTime), "seconds")