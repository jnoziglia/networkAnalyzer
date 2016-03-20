import subprocess as sub

class Analyzer:
    p = sub.Popen(('sudo', 'tcpdump', '-nnvvXSs', '1514', '-r', '../output'), stdout=sub.PIPE)
    for line in iter(p.stdout.readline, b''):
        print line

