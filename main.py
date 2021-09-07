import threading
import time
import nmap
from mcstatus import MinecraftServer

# Determines the IP address from the given integer using bitwise operations
def intToIP(num):
    return (str((num >> 24) & 0xFF) + "."
            + str((num >> 16) & 0xFF) + "."
            + str((num >> 8) & 0xFF) + "."
            + str(num & 0xFF))

blacklistedPools = [
    [167772160, 184549375], # 10.0.0.0 – 10.255.255.255
    [2886729728, 2887778303], # 172.16.0.0 – 172.31.255.255
    [3232235520, 3232301055], # 192.168.0.0 – 192.168.255.255
    [2130706433, 2130706433] # 127.0.0.1
]

def intIsBlacklisted(num):
    for pool in blacklistedPools:
        if pool[0] <= num <= pool[1]:
            return pool
        continue
    return None

def thread(num):
    startTime = time.time()
    print("Start thread", threading.current_thread().name)
    nm = nmap.PortScanner()
    max = 4294967295 # Maximal IP address in integer to reach
    curr = round(max/(num+1)) # Current IP address in integer depeding on thread number
    while curr < round(max/num):
        curr += 1 # Not at the end of the loop beacuse of the next condition passing the while loop
        blacklistedPool = intIsBlacklisted(curr)
        if blacklistedPool is not None: # Is ip in blacklisted pool?
            curr += blacklistedPool[1] - blacklistedPool[0] - 1 # Minus one because we are going to increase at the begin of the loop
            continue
        ip = intToIP(curr)
        try:
            for port in nm.scan(ip, "25565")["scan"][ip]["tcp"].keys():
                try: # Is a minecraft server running on that port?
                    server = MinecraftServer.lookup(ip + ":" + port)
                    print("Server found:", server.host, ":", port)
                except:
                    pass
        except:
            print("nope")
            pass
        time.sleep(2) # Wait 2 seconds before scanning the next IP
    print("End thread", threading.current_thread().name, (time.time() - startTime)) # Display execution time

if __name__ == '__main__':
    for i in range(0, 10): # Start X threads
        threading.Thread(name=i, target=thread, args=[i]).start()