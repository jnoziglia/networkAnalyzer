import subprocess as sub

class Analyzer:
    sub.call("../create_output.sh")
    p = sub.Popen(('sudo', 'tcpdump', '-nn', '-r', '../output'), stdout=sub.PIPE)

    import re

    reg = re.compile(r"(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port1>\d+) > (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port2>\d+): (?P<protocol>(?:tcp|udp|icmp))")

    for line in iter(p.stdout.readline, b''):
        m = reg.match(line)
        print(m.group("timestamp"))
        print(m.group("IP1"))
        print(m.group("Port1"))
        print(m.group("IP2"))
        print(m.group("Port2"))
        print(m.group("protocol"))
