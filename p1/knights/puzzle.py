from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is a knight if and only if A is both a knave and a knight
    Biconditional(AKnight, And(AKnave, AKnight)),
    # A is a knave if and only if A is not both a knight and a knave
    Biconditional(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # A is a knave if an only if A and B are not both knaves.
    Biconditional(AKnave, Not(And(AKnave, BKnave))),
    # A is a knight if and only if A and B are knaves.
    Biconditional(AKnight, And(AKnave, BKnave)),
    # A being a knave implies that one of them is a knight.
    Implication(AKnave, Or(AKnight,BKnight))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    
    # A is either a knight or knave, B is either knight or knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    
    # A is a knight if and only if A is not a knave
    Biconditional(AKnight, Not(AKnave)),
    # B is a knight of and only if B is not a knave
    Biconditional(BKnight,Not(BKnave)),
 
    # If A is knight --> "Same kind"
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If B is knight --> "Different kind"
    Biconditional(BKnight, Or(And(AKnight,BKnave),And(AKnave, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    Or(AKnave,AKnight),
    Or(BKnave,BKnight),
    Or(CKnave,CKnight),

    # A is a knight if and only if A is not a knave
    Biconditional(AKnight, Not(AKnave)),
    # B is a knight if and only if B is not a knave
    Biconditional(BKnight,Not(BKnave)),
    # C is a knight if and only if C is not a knave
    Biconditional(CKnight, Not(CKnave)),
 
    # A is knight iff "I am a knight" or "I am a knave" is true
    Biconditional(Or(AKnight, AKnight), Or(AKnight, AKnave)),
    # B is a knight iff "A said 'I am a knave' 
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    # B is a knight iff C is a knave
    Biconditional(BKnight, CKnave),
    # C is a knight iff A is a knight
    Biconditional(CKnight, AKnight)

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()


