import subprocess as sub
import re

class Analyzer:
    sub.call("./create_capture.sh")
    p = sub.Popen(('sudo', 'tcpdump', 'ip', '-l', '-nn', '-r', './output'), stdout=sub.PIPE)

    regex_string = r'(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port1>\d+) > (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port2>\d+): (?P<protocol>(?:TCP|UDP|ICMP))'

    reg = re.compile(regex_string)
    i = 0
    
    for line in iter(p.stdout.readline, b''):
        m = reg.match(line)
        print i
        #print(m.group("timestamp"))
        #print(m.group("IP1"))
        #print(m.group("Port1"))
        #print(m.group("IP2"))
        #print(m.group("Port2"))
        #print(m.group("protocol"))
        print line
        i = i+1
