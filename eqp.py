import csv
import sys

from itertools import permutations,product

#--------------------------------------------------------
class eqCandidate:
    def __init__(self,expression, result):
        self.expression = expression
        self.result = result
    
    def print_info(self):
        print(f"Expression: {self.expression}, Result: {self.result}")

#--------------------------------------------------------
class eqParams:
    def __init__(self,numbers, goal):
        self.numbers = numbers
        self.goal = goal

    def print_info(self):
        print(f"Numbers: {self.numbers}, Goal: {self.goal}")

#--------------------------------------------------------
# generate expressions for each number permutation against operation permutations
# and then all parenthesized orderings
# and then evaluate the expression to calculate the result
#--------------------------------------------------------
def evaluateExpression(expression, goal, opFamilyName, solutions):
    try:
        result = eval(expression)
    except ZeroDivisionError:
        print("You can't divide by zero!")
        result = -999
    finally:
        #print (expression + " == " + str(result))
        if result == goal:
            solution = eqCandidate(expression, result)
            solution.print_info()
            if opFamilyName not in solutions:
                solutions[opFamilyName] = []
            solutions[opFamilyName].append(solution)
            #solutions.append(solution)

#--------------------------------------------------------
def makeExprFamilyName(exprTokens):
    LookingForLHS = 1
    LookingForOp  = 2
    LookingForRHS = 3

    expr = []
    exprs = []

    eState = LookingForLHS

    for token in exprTokens:
        if eState == LookingForLHS:
            if type(token) == int:
                expr.append(token)
                eState = LookingForOp
            elif token == '(':
                continue
            elif token == ')':
                expr.append('X')
                eState = LookingForOp
            elif token in "+-*/":
                expr.append('X')
                expr.append(token)
                eState = LookingForRHS
            else:
                print("Error in makeExprFamilyName: LookingForLHS found: " + token)
        elif eState == LookingForOp:
            if token in "+-*/":
                expr.insert(token, 0)
                eState = LookingForRHS
            else:
                print("Error in makeExprFamilyName: LookingForOp found: " + token)
        elif eState == LookingForRHS:
            if type(token) == int:
                expr.append(token)
                exprCopy = expr.copy()
                exprs.append(exprCopy)
                expr = []
            elif token == '(':
                expr.append('X')
                exprCopy = expr.copy()
                exprs.append(exprCopy)
                expr = []
            else:
                print("Error in makeExprFamilyName: LookingForRHS found: " + token)
    exprFamilyName = getOpFamilyName(exprs)
    return exprFamilName

#--------------------------------------------------------

# evalExpression(  (o1, n1, n2),  (o2, x, n3),  (o3, x, n4) )
# construct expression
# eval the exxpression
# if meets goal then
#     get FamilyName and save in solutions
def evalExpression(exprTokens, goal, solutions):
    expression = ''.join(exprTokens)
    try:
        result = eval(expression)
    except ZeroDivisionError:
        print("You can't divide by zero!")
        result = -999
    finally:
        #print (expression + " == " + str(result))
        if result == goal:
            solution = eqCandidate(expression, result)
            solution.print_info()
            exprFamilyName = makeExprFamilyName(exprTokens)
            if exprFamilyName not in solutions:
                solutions[exprFamilyName] = []
            solutions[exprFamilyName].append(solution)
            #solutions.append(solution)

#--------------------------------------------------------
def getParamsFromCsv(csvFileName):
    with open(csvFileName, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
            return eqParams( [row[0], row[1], row[2], row[3]], int(row[4]))

#--------------------------------------------------------
def getParamsFromCmdLine():
# Check that 5 arguments were passed

    if len(sys.argv) != 6:
        print("Cmd Line params: ", len(sys.argv))
        return getParamsFromCsv("eqpuzzle.csv")

    # Assign the 5 arguments to variables

    n1 = sys.argv[1]
    n2 = sys.argv[2]
    n3 = sys.argv[3]
    n4 = sys.argv[4]
    goal = int(sys.argv[5])
    eqparams = eqParams([n1, n2, n3, n4], goal)

    # Print the variables
    print("Param 1: ", n1)
    print("Param 2: ", n2)
    print("Param 3: ", n3)
    print("Param 4: ", n4)
    print("Param 5: ", goal)
    return eqparams

msg = "Hello World"
print(msg)

#--------------------------------------------------------
def getOpFamilyName(ops):
    print("ops in getOpFamilyName: ")
    print(ops)
    opIds = []
    for i in range(3):
        if ops[i][0] == '*' or ops[i][0] == '/':
            opId = 'M'
        elif ops[i][0] == '+' or ops[i][0] == '-':
            opId = 'A'
        opNum = 1
        for j in range(1,3):
            if ops[i][j] != 'X':
                opNum = opNum * int(ops[i][j])
        opId = opId + str(opNum)
        opIds.append(opId)
    opFamilyName = ''.join(sorted(opIds, reverse=True))

    return opFamilyName

#--------------------------------------------------------
def algEqPuzzle(eqparams):
    numberPermutations = []
    uniqueNumberPermutations = []
    for numberPermutation in list(permutations(eqparams.numbers,4)):
        numberPermutations.append(numberPermutation)

        # Only keep isUnique permutations
        if numberPermutation not in uniqueNumberPermutations:
            uniqueNumberPermutations.append(numberPermutation)

    # print(numberPermutationList)
    # print(uniqueNumberPermutations)

    # Operations permutation generation

    operations = ["+", "-", "*", "/"]
    operationPermutations = product(operations, repeat=3)

    # for operationPermutation in operationPermutations:
    #     print(operationPermutation)

    # solutions is a dictionary of expression solutions keyed by familyname
    solutions = {}
    for np in uniqueNumberPermutations:
        # print(np)
        n1, n2, n3, n4 = np

        # find all permutations of 3 operations allowing repetition
        operationPermutations = product(operations, repeat=3)

        for op in operationPermutations:
            #print(op)
            o1, o2, o3 = op
            x = 'X'  # intermediate result

            # Order of operations = 1, 2, 3
            exprTokens = ["(", "(", n1, o1, n2, ")", o2, n3, ")", o3, n4]
            evalExpression(exprTokens, eqparams.goal, solutions)


            expression = str("((" + np[0] + op[0] + np[1] + ")" + op[1] + np[2] + ")" + op[2] + np[3])
            opFamilyName = getOpFamilyName( ((op[0],np[0],np[1]), (op[1],'X',np[2]), (op[2],'X',np[3])))  # pass this to evaluate expression
            evaluateExpression(expression, eqparams.goal, opFamilyName, solutions)

            # evalExpression(  (o1, n1, n2),  (o2, x, n3),  (o3, x, n4) )

            # convert operations and numbers to variables
            # make 'X' a variable
            # pass the 3 tuples to evaluate expression
            # ee will construct the expression, evaluate it, check the answer, generate family name, store result


            # Order of operations = 1, 3, 2
            # evalExpression(  (o1, n1, n2),  (o3, n3, n4),  (o2, x, x) )

            expression = str("(" + np[0] + op[0] + np[1] + ")" + op[1] + "(" + np[2] + op[2] + np[3] +")")
            opFamilyName = getOpFamilyName( ((op[0],np[0],np[1]), (op[2],np[2],np[3]), (op[1],'X','X')))
            evaluateExpression(expression, eqparams.goal, opFamilyName, solutions)

            # Order of operations = 2, 1, 3
            expression = str("(" + np[0] + op[0] + "(" + np[1] + op[1] + np[2] + "))" + op[2] + np[3])
            opFamilyName = getOpFamilyName( ((op[1],np[1],np[2]), (op[0],np[0],'X'), (op[2],'X',np[3])))
            evaluateExpression(expression, eqparams.goal, opFamilyName, solutions)

            # Order of operations = 2, 3, 1
            expression = str(np[0] + op[0] + "((" + np[1] + op[1] + np[2] + ")" + op[2] + np[3] +")")
            opFamilyName = getOpFamilyName( ((op[1],np[1],np[2]), (op[2],'X',np[3]), (op[0],np[0],'X')))
            evaluateExpression(expression, eqparams.goal, opFamilyName, solutions)

            # Order of operations = 3, 2, 1
            expression = str(np[0] + op[0] + "(" + np[1] + op[1] + "(" + np[2] + op[2] + np[3] +"))")
            opFamilyName = getOpFamilyName( ((op[2],np[2],np[3]), (op[1],np[1],'X'), (op[0],np[0],'X')))
            evaluateExpression(expression, eqparams.goal, opFamilyName, solutions)

    return solutions

    # for sol in solutions:
       #print("First solution expression is ", sol.expression)
       #return sol.expression

#--------------------------------------------------------
def serveEqPuzzle(n1, n2, n3, n4, goal):
    eqparams = eqParams([n1, n2, n3, n4], int(goal))
    return algEqPuzzle(eqparams)

#--------------------------------------------------------
if __name__ == "__main__":
    # app.run()
    eqparams = getParamsFromCmdLine()
    familiesOfExpressions = algEqPuzzle(eqparams)
    # Iterate through the dictionary using items()
    for familyName, solutions in familiesOfExpressions.items():
        print("FamilyName: " + familyName)
        for sol in solutions:
            print(sol.expression)


# called from flask ui
# result = serveEqPuzzle(n1, n2, n3, n4, goal)
