
coordCmd = ('X','Y','Z','F')
ignoredCmd = ('M5','M6','M3','M30')

useTqdm = True
try:
    import tqdm
except ImportError as ex:
    useTqdm = False

class gcodeFile(object):
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
            self.rawCode = f.readlines()
    
    def convert(self, progress=False):
        output = ['(GENERATED by CarbideConvert)']
        rc = self.rawCode
        if progress and useTqdm:
            rc = tqdm.tqdm(self.rawCode)
        
        for line in rc:
            line = line.strip()
            cmd = ""
            if len(line) == 0:
                continue
            if line[0] == ';' or line[0] == '(':
                output.append(line)
                continue

            ignore = False
            for ic in ignoredCmd:
                if line.startswith(ic):
                    ignore = True
                    continue
            if ignore:
                continue
            
            if line[0] in coordCmd:
                cmd = "G1"+line
            else:
                cmd = line
            
            for c in coordCmd:
                cmd = cmd.replace(c, ' '+c)
            
            if cmd == 'G0':
                continue
            output.append(cmd)
        self.convertedCode = output
    
    def getCode(self):
        return self.convertedCode

from sys import argv

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: "+argv[0]+' Filename')
        exit(1)
    filename = argv[1]
    gc = gcodeFile(filename)
    gc.convert(True)

    for line in gc.getCode():
        print(line)
    pass