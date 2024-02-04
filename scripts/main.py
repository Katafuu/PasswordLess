import random
import string
import itertools



def genPass(*args):
        p=''
        try:
          pwdLength = args[0]
        except:
          pwdLength = 14
        for x in range(pwdLength):
            n = random.choice(string.printable.strip())
            p += n
        return p

def randomizePass(self):
        self.loadPass()
        for x in range(self.passWrds):
            self.passWrds[x] == self.genPass()
        self.savePass()


