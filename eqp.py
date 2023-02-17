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
def evaluateExpression(expression, goal, solutions):
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
            solutions.append(solution)

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

    operations = ["+", "-", "*","/"]
    operationPermutations = product(operations, repeat=3)

    # for operationPermutation in operationPermutations:
    #     print(operationPermutation)

    solutions = []
    for np in uniqueNumberPermutations:
        print(np)
        operationPermutations = product(operations, repeat=3)

        for op in operationPermutations:
            #print(op)

            # Order of operations = 1, 2, 3
            expression = str("((" + np[0] + op[0] + np[1] + ")" + op[1] + np[2] + ")" + op[2] + np[3])
            evaluateExpression(expression, eqparams.goal, solutions)

            # Order of operations = 1, 3, 2
            expression = str("(" + np[0] + op[0] + np[1] + ")" + op[1] + "(" + np[2] + op[2] + np[3] +")")
            evaluateExpression(expression, eqparams.goal, solutions)

            # Order of operations = 2, 1, 3
            expression = str("(" + np[0] + op[0] + "(" + np[1] + op[1] + np[2] + "))" + op[2] + np[3])
            evaluateExpression(expression, eqparams.goal, solutions)

            # Order of operations = 2, 3, 1
            expression = str(np[0] + op[0] + "((" + np[1] + op[1] + np[2] + ")" + op[2] + np[3] +")")
            evaluateExpression(expression, eqparams.goal, solutions)

            # Order of operations = 3, 2, 1
            expression = str(np[0] + op[0] + "(" + np[1] + op[1] + "(" + np[2] + op[2] + np[3] +"))")
            evaluateExpression(expression, eqparams.goal, solutions)



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
    algEqPuzzle(eqparams)


# called from flask ui
# result = serveEqPuzzle(n1, n2, n3, n4, goal)
