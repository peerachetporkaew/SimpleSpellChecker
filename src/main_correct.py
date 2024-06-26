from syllacut import tokenize
from FST import MultipleOutputFST

class LSTSpellChecker(object):

    def __init__(self,correct_list="./dict/royin_wordlist.txt",incorrect_list="./dict/lst_incorrect.txt"):
        root = MultipleOutputFST("ROOT")
        fp = open(correct_list,"r").read().splitlines()
        
        for line in fp:
            r = line.strip()
            root.addRule(tokenize(r),str(len(r)) + "|<")
        
        self.rule = root
        
        root = MultipleOutputFST("ROOT")
        fp = open(incorrect_list,"r").read().splitlines()

        for line in fp:
            r = line.split(" ||| ")
            root.addRule(tokenize(r[0]),str(len(r[0])) + "|" + r[1])
        
        self.incorrect_rule = root
        
    def process_correct(self,text):
        incorrectList = []
        tok = tokenize(text).split()
        #print(tok)
        i = 0
        while i < len(tok):
            match = self.rule.process(tok,i)
            #print(match)
            if len(match) > 0:
                longest_match = match[-1]
                incorrectList.append([i,longest_match])
                i = longest_match[0] + 1
            else:
                i += 1

        #Post-processing
        output = []
        for item in incorrectList:
            src = " ".join(tok[item[0]:item[1][0]+1])
            trg = int(item[1][1].split("|")[0])
            output.append([src,trg])

        return output
    
    def process_incorrect(self,text):
        incorrectList = []
        tok = tokenize(text).split()
        #print(tok)
        i = 0
        while i < len(tok):
            match = self.incorrect_rule.process(tok,i)
            #print(match)
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
    
    def _process(self,text):
        k = [0] * len(text)
        output = self.process_correct(text)
        incorrect_temp = text
        for item in output:
            x = item[0].replace(" ","")
            incorrect_temp = incorrect_temp.replace(x,"".join([" "]*len(x)))
        
        #print(incorrect_temp)
        
        correct = text
        output = self.process_incorrect(text)
        for item in output:
            x = item[0]
            correct = correct.replace(x,"".join([" "]*len(x)))
        #print(correct)
        items = correct.split()
        for item in items:
            text = text.replace(item," ")
        correct_list = text.split()
        incorrect_list = incorrect_temp.split()
        clean_list = []
        for il in incorrect_list:
            found = 0
            for item in correct_list:
                if il in item:
                    found = 1
                    break
            if found == 0:
                clean_list.append(il)
        
        return clean_list + correct_list
    
    def process(self,text):
        textL = text.split()
        out = []
        for item in textL:
            temp = self._process(item)
            out.extend(temp)
        return out
            

if __name__ == "__main__":
    checker = LSTSpellChecker()
    """
    output = checker.process_incorrect("สวัดดีคับ ม่ายรู้ว่าคุณสบายดีมั้ยกฎหมาย")
    print(output)
    
    output = checker.process_correct("สวัดดีคับ ม่ายรู้ว่าคุณสบายดีมั้ยกฎหมาย")
    print(output)
    """
    
    out = checker.process("สวัดดีคับ ม่ายรู้ว่าคุณสบายดีมั้ยกฏหมายดิจิตอล")
    print(out)