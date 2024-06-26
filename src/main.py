from syllacut import tokenize
from FST import MultipleOutputFST

class LSTSpellChecker(object):

    def __init__(self,rulefile=""):
        root = MultipleOutputFST("ROOT")
        fp = open("./dict/incorrect.txt","r").read().splitlines()

        for line in fp:
            r = line.split(" ||| ")
            root.addRule(tokenize(r[0]),str(len(r[0])) + "|" + r[1])
        
        self.rule = root
            
    def process(self,text):
        incorrectList = []
        tok = tokenize(text).split()
        i = 0
        while i < len(tok):
            match = self.rule.process(tok,i)
            if len(match) > 0:
                longest_match = match[-1]
                incorrectList.append([i,longest_match])
                i = longest_match[0] + 1
            else:
                i += 1

        #Post-processing
        output = []
        for item in incorrectList:
            src = "".join(tok[item[0]:item[1][0]+1])
            trg = item[1][1].split("|")[1]
            output.append([src,trg])

        return output

if __name__ == "__main__":
    checker = LSTSpellChecker()
    output = checker.process("สวัดดีคับ ม่ายรู้ว่าคุณสบายดีมั้ย")
    print(output)