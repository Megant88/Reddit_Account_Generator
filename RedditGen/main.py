from source.generatorcode import generator
import threading
from colorama import Fore
import ctypes

def create_threads(i):
    def start():
        generator()
    while True:
        if threading.active_count() <= i:
            threading.Thread(target=start).start()

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("Megant Reddit Generator")
    print(f'''{Fore.LIGHTMAGENTA_EX}
██████╗ ███████╗██████╗ ██████╗ ██╗████████╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝██╔════╝ ██╔════╝████╗  ██║
██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║   ██║  ███╗█████╗  ██╔██╗ ██║
██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║   ██║   ██║██╔══╝  ██║╚██╗██║
██║  ██║███████╗██████╔╝██████╔╝██║   ██║   ╚██████╔╝███████╗██║ ╚████║
╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝
                                                         {Fore.WHITE}Made by Megant''')
    Threads = int(input(f"{Fore.WHITE}[{Fore.BLUE}+{Fore.WHITE}] {Fore.GREEN}Enter thread count: "))
    create_threads(Threads)
        
    