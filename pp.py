import argparse
import socket
import time
import threading

open_ports = []


def loading(thread):
    animation = ['[   ]','[=  ]','[== ]','[===]','[ ==]','[  =]','[   ]']
    i = 0
    while thread.is_alive():
        print(animation[i],end="\r")
        time.sleep(0.2)
        i = i+1
        if i > 6:
            i = 0
            
def initArg():
    parser = argparse.ArgumentParser(prog='PyPort',description='A simple TCP port scanner in python')
    parser.add_argument('--target','-t',help='Specify the targets domain/ip',required=True)
    parser.add_argument('--brute','-b',help='Brute force through 1-1023 ports',action='store_true')
    parser.add_argument('--timeout','-to',type=float,help='Specify the timeout duration (default is 1 second)')
    args = parser.parse_args()
    if args.timeout is not None:
        if args.timeout <= 0:
            raise argparse.ArgumentTypeError('Timeout needs to be bigger than 0.')
    return args


def scan(target,brute,timeout):
    if brute == False:
        print("Scanning for common open TCP ports : ")
        ports = [80,443,8080,22,24,25,20,21,110,119,3306,123,3389,162,161]
    else:
        print('Scanning for port in the range of 1 to 1023 : ')
        ports = range(1,1024)
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(timeout)
        target = socket.gethostbyname(target)
        try :
            s.connect((target,port))
        except:
            time.sleep(0.1)
        else:
            try:
                service = socket.getservbyport(port)
            except:
                p = str(port)+':'+'unkown'
            else:
                p = str(port)+':'+service
            open_ports.append(p)
            time.sleep(0.1)
            pass
        s.close()

        
def main():
    
    args = initArg()
    if args.timeout is None:
        timeout = 1
    else:
        timeout = args.timeout
    
    scanner = threading.Thread(target=scan,args=(args.target,args.brute,timeout))
    scanner.start()
    loading(scanner)
    scanner.join()
    if open_ports:
        print("Found %s open TCP ports :\n %s"%(len(open_ports),open_ports))
    else:
        print('No open TCP ports found.')
    
if __name__ == '__main__':
    main()
