from personclass import *
from relationclass import *

def FamTreeLoad(familyName):
    with open(familyName+".ft", "r") as file:
        line = file.readline()
        while line:
            lineSplit = line.split()
            if lineSplit[0] == "family":
                famName(lineSplit[1])
            elif lineSplit[0] == "count":
                numPerson(int(lineSplit[1]))
            elif lineSplit[0] == "links":
                numLinks(int(lineSplit[1]))
            elif lineSplit[0] == "name":
                name = lineSplit[1]
                age = int(file.readline().split()[1])
                n = file.readline().split()
                if n[1] == "true":
                    sex = True
                else:
                    sex = False
                addtoPersonArray(name, age, sex)
            elif lineSplit[0] == "child":
                linkIn(str(line).rstrip('\n'))
            line = file.readline()

def makeTree():
    habalnk = len(getLinkIn())
    while habalnk > 0:
        for i in returnPerson():
            bilang = 0
            while bilang < len(getLinkIn()):
                if i.name == links[bilang].split()[1]:
                    if i.left == None:
                        leftchild = str(links[bilang].split()[2])
                        i.left = findPerson(leftchild)
                        findPerson(leftchild).parent = i
                        findPerson(leftchild).gen = i.gen + 1
                    elif i.right == None:
                        rightchild = str(links[bilang].split()[2])
                        i.right = findPerson(rightchild)
                        findPerson(rightchild).parent = i
                        findPerson(rightchild).gen = i.gen + 1

                bilang += 1
        habalnk -= 1

def leastCommonAncestor(n1, n2):
    g1 = findPerson(n1).gen
    g2 = findPerson(n2).gen
    p1 = findPerson(n1)
    p2 = findPerson(n2)
    while True:
        if p1.parent == None:
            return p1
            break
        elif p2.parent == None:
            return p2
            break
        elif g1 == g2:
            if p1.parent == p2.parent:
                return p1.parent
                break
            else:
                p1 = p1.parent
                p2 = p2.parent
                g1 = p1.gen
                g2 = p2.gen
                while True:
                    if p1.parent == p2.parent:
                        return p1.parent
                        break
                    else:
                        p1 = p1.parent
                        p2 = p2.parent
                        g1 = p1.gen
                        g2 = p2.gen
        elif g1 > g2:
            while g1 != g2:
                p1 = p1.parent
                g1 = p1.gen
            if p1 == p2:
                return p2
            elif p1.parent == p2.parent:
                return p1.parent
                break
            else:
                p1 = p1.parent
                p2 = p2.parent
                g1 = p1.gen
                g2 = p2.gen
                while True:
                    if p1.parent == p2.parent:
                        return p1.parent
                        break
                    else:
                        p1 = p1.parent
                        p2 = p2.parent
                        g1 = p1.gen
                        g2 = p2.gen
        elif g2 > g1:
            while g2 != g1:
                p2 = p2.parent
                g2 = p2.gen
            if p2 == p1:
                return p1
            elif p1.parent == p2.parent:
                return p1.parent
                break
            else:
                p1 = p1.parent
                p2 = p2.parent
                g1 = p1.gen
                g2 = p2.gen
                while True:
                    if p1.parent == p2.parent:
                        return p1.parent
                        break
                    else:
                        p1 = p1.parent
                        p2 = p2.parent
                        g1 = p1.gen
                        g2 = p2.gen

def listAncestors(name):
    list = []
    p1 = findPerson(name)
    while p1.gen > 1:
        p1 = p1.parent
        list.append(p1.name)
    list.sort()
    for i in list:
        print(i)

def listDescendants(name, traversal):
    p = findPerson(name)
    if p:
        traversal += (str(p.name) + "-")
        traversal = listDescendants(p.left, traversal)
        traversal = listDescendants(p.right, traversal)
    return traversal


def relationship(ppp1,ppp2):
    Ordinal = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    Times = ["once", "twice", "thrice", "four times", "five times", "six times", "seven times", "eight times", "nine times", "ten times"]
    Great = ["", "", "", "great-", "great-great-", "great-great-great-","great-great-great-great-", "great-great-great-great-great-", "great-great-great-great-great-great-", "great-great-great-great-great-great-great-", "great-great-great-great-great-great-great-great-", "great-great-great-great-great-great-great-great-great-"]
    p1 = findPerson(ppp1)
    p2 = findPerson(ppp2)
    l = leastCommonAncestor(ppp1,ppp2)
    l1 = l.gen
    d1 = (p1.gen - l1)
    d2 = (p2.gen - l1)

    nearest = min(d1, d2)
    furthest = max(d1, d2)

    if nearest >= 2:
        degree = (nearest - 1)
        removal = abs(d1 -d2)
        if removal == 0:
            return str(Ordinal[degree] + " cousin")
        else:
            return str(Ordinal[degree] + " cousin, " + Times[removal] + " removed")
    elif nearest == 1:
        if furthest == 1:
            if p2.sex == True:
                return "brother"
            else:
                return "sister"
        elif furthest == 2:
            return Term("nibling", d1, d2, p2.sex)
        else:
            return str(Great[furthest] + "grand" + Term("nibling", d1, d2, p2.sex))
    elif nearest == 0:
        if furthest == 1:
            return Term("child", d1, d2, p2.sex)
        else:
            return str(Great[furthest] + "grand" + Term("child", d1, d2, p2.sex))


def Term(kind, d1, d2, sex):
    if d1 < d2:
        if kind == "child":
            if sex == True:
                return "son"
            else:
                return "daughter"
        else:
            if sex == True:
                return "nephew"
            else:
                return "niece"
    elif d1 > d2:
        if kind == "child":
            if sex == True:
                return "father"
            else:
                return "mother"
        else:
            if sex == True:
                return "uncle"
            else:
                return "aunt"


fam = input()
if fam.split()[0] == "load":
    FamTreeLoad(fam.split()[1])
    makeTree()
#print(leastCommonAncestor("Patricia", "Robert").name)
print(relationship("Joyce", "Alma"))
