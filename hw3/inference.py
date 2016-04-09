__author__ = 'Padma'
import sys
import re
from collections import deque
from copy import deepcopy
LOOP_CONTROL = 10

class ConstructSentence:

    def __init__(self, sents, sen_count):
        self.process(sents, sen_count)

    def __eq__(self, sent):
        if sent.__str__() == self.__str__():
            return True
        return False

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())

    def __copy__(self):
        return ConstructSentence(self.__str__(),"")

    def __ne__(self, sen):
        return not self.__eq__(sen)

    def of_index(self, sentence):
        for itr in range(self.no_arg):
            if sentence == self.pred_args[itr]:
                return itr

    def process(self,elem,sencount):

        elem = elem.strip()
        self.var_pred = re.match(r"\~?[A-Z][A-Z,a-z]*", elem).group()
        self.val_key = self.var_pred
        length = len(self.var_pred)
        temp = ""
        for itr in range(length,len(elem)):
            temp = temp + elem[itr]
        elem = temp
        elem = elem.replace("(", "")
        elem = elem.replace(")", "")
        num = elem.split(",")
        self.count = str(sencount)
        self.no_arg = len(num)
        self.pred_args = []

        for some in num:
            if some[0].islower():
                value = some + self.count
                self.pred_args.append(IdentifyVariable(value))
            else:
                self.pred_args.append(IdentifyVariable(some))

    def __str__(self):

        self.element = self.var_pred + "("
        self.element += ",".join(str(ags) for ags in self.pred_args) + ")"
        return self.element

    def clause_unify(self, query):

        if self.no_arg != query.no_arg or self.var_pred != query.var_pred:
            return None
        answer = []

        for i in range(self.no_arg):

            if self.pred_args[i].is_constant and query.pred_args[i].is_constant and \
                    self.pred_args[i] != query.pred_args[i]:
                return None
            elif self.pred_args[i].is_variable and query.pred_args[i].is_constant:
                answer.append([self.pred_args[i].exp, query.pred_args[i].exp])
            elif self.pred_args[i].is_variable and query.pred_args[i].is_variable:
                answer.append([self.pred_args[i].exp, query.pred_args[i].exp])

        return answer

class IdentifyVariable:

    def __init__(self, var):
        phrase = var.strip()
        self.is_variable = False
        self.is_constant = False
        self.exp = phrase
        if phrase[0].islower():
            self.is_variable = True
        else:
            self.is_constant = True

    def __str__(self):
        return self.exp

    def __hash__(self):
        return hash(self.exp + str(self.is_variable) + str(self.is_constant))

    def __eq__(self, other):
        if self.exp == other.exp and self.is_constant == other.is_constant and \
                self.is_variable == other.is_variable:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()


class SimplifiedSentence:

    def __init__(self,sentence,sen_count):
        self.simplify(sentence,sen_count)

    def simplify(self,sentence,sen_count):
        phrase = sentence.split("=>")
        self.lhs = []
        if phrase[0] != "":
            if "^" not in phrase[0]:
                self.lhs.append(ConstructSentence(phrase[0],sen_count))
            else:
                param_lhs = sorted(phrase[0].split("^"))
                for i in param_lhs:
                    self.lhs.append(ConstructSentence(i,sen_count))
        else:
            self.lhs = []
        self.rhs = ConstructSentence(phrase[1],sen_count)
        self.val_key = self.rhs.val_key

    @property
    def left(self):
        return self.lhs

    def __str__(self):
        self.element = "^".join(str(exp) for exp in self.lhs) + "=>" + \
                str(self.rhs)
        return self.element

    @property
    def right(self):
        return self.rhs

class KB:
    def __init__(self):
        self.elements = dict()
        self.total = -1
        self.KB = []

    def get_matching_rules(self, phrase):

        ans = []
        if phrase.val_key in self.elements:

            for j in self.elements[phrase.val_key]:

                if phrase.clause_unify(self.KB[j].right) or self.KB[j].right.clause_unify(phrase) or \
                        self.KB[j].right == phrase:
                    ans.append(self.KB[j])
        return ans

    def add(self, string, sen_count):
        sentence = SimplifiedSentence(string,sen_count)
        self.total += 1
        if sentence.val_key in self.elements:
            self.elements[sentence.val_key].append(self.total)
        else:
            self.elements[sentence.val_key] = [self.total]
        self.KB.append(sentence)

    def __str__(self):
        return "\n".join(str(exp) for exp in self.KB)

    def get_rules(self, itr):
        match = self.get_matching_rules(itr)
        return match

    def __repr__(self):
        return self.__str__()


def func_subs(passDic, other):

    copied = other.__copy__()
    for j in range(other.no_arg):
        if other.pred_args[j].is_variable and other.pred_args[j] in passDic:
            copied.pred_args[j] = passDic[other.pred_args[j]]
    return copied


def fol_bc_ask (KBase, querys, passtheta, num):

    matches = KBase.get_rules(querys)

    for match in matches:
        if match.right not in num.keys():
            num[match.right] = 1
        elif num[match.right] >= LOOP_CONTROL:
            return
        else:
            num[match.right] += 1
        for thetaOne in fol_bc_repeat(KBase, list(match.left), func_unify(match.right, querys, deepcopy(passtheta)), deepcopy(num)):
            yield thetaOne

def func_unify(valueOne, valueTwo, passedDic):

    if passedDic == None:
        return None

    elif valueOne == valueTwo:
        return passedDic

    elif isinstance(valueOne, IdentifyVariable) and valueOne.is_variable:
        return variale_unify(valueOne, valueTwo, passedDic)

    elif isinstance(valueTwo, IdentifyVariable) and valueTwo.is_variable:
        return variale_unify(valueTwo, valueOne, passedDic)

    elif isinstance(valueOne, ConstructSentence) and isinstance(valueTwo, ConstructSentence):
        return func_unify(valueOne.pred_args, valueTwo.pred_args, func_unify(valueOne.val_key, valueTwo.val_key, passedDic))

    elif isinstance(valueOne, list) and isinstance(valueTwo, list):
        return func_unify(valueOne[1:],valueTwo[1:],func_unify(valueOne[0], valueTwo[0], passedDic))

    else:
        return None

def fol_bc_repeat(KBase, query, pass_theta, num):

    if query:
        partOne = query[0]
        partTwo = None
        if len(query) > 1:
            partTwo = query[1:]

        if pass_theta:
            for thetaTwo in fol_bc_ask(KBase, func_subs(pass_theta, partOne),deepcopy(pass_theta), deepcopy(num)):
                for thetaThree in fol_bc_repeat(KBase, partTwo, deepcopy(thetaTwo), deepcopy(num)):
                    yield thetaThree
        else:
            for thetaTwo in fol_bc_ask(KBase, partOne, deepcopy(pass_theta), deepcopy(num)):
                for thetaThree in fol_bc_repeat(KBase, partTwo, deepcopy(thetaTwo), deepcopy(num)):
                    yield thetaThree
    else:
        yield pass_theta


def fol_get_straight(KBobj,goal):

    matches = KBobj.get_rules(goal)
    for match in matches:
        if len(list(match.left)) == 0 and goal == match.right:
            return True
    return False

def variale_unify(valueOne, valueTwo, passTheta):

    if valueOne in passTheta:
        return func_unify(passTheta[valueOne], valueTwo, passTheta)
    elif valueTwo in passTheta:
        return func_unify(valueOne, passTheta[valueTwo], passTheta)
    else:
        passTheta[valueOne] = valueTwo
    return passTheta

def main():

    inputFile = open(sys.argv[2],'r')
    outputFile = open("output.txt",'w')
    queryno = int(inputFile.readline().strip())
    query = []
    for i in range(0,int(queryno)):
        a = inputFile.readline().strip()
        query.append(a)

    clauseno = int(inputFile.readline().strip())
    KBobj = KB()

    sen_count = 1
    for i in range(0,int(clauseno)):
        element = inputFile.readline().strip()
        if "=>" not in element:
            element = "=>" + element
        KBobj.add(element,str(sen_count))
        sen_count += 1

    for i in range(len(query)):
        try:
            a = ""
            contructed_query = ConstructSentence(query[i],str(a))

            value = fol_get_straight(KBobj,contructed_query)

            if value == True:
                outputFile.write("TRUE"+"\n")
            else:
                result = dict()
                for j in fol_bc_ask(KBobj,contructed_query,dict(),dict()):
                    if j:
                        result = dict(result.items() + j.items())
                if result:
                    outputFile.write("TRUE"+"\n")
                else:
                    outputFile.write("FALSE"+"\n")

        except Exception, e:
            print("exception", e)
            outputFile.write("FALSE"+"\n")

    outputFile.close()

if __name__ == '__main__':
	main()
