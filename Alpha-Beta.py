import os, math

def GetWinner(board):
    """
    Returns the winner in the current board if there is one, otherwise it returns None.
    """

    # horizontal
    if board[0] == board[1] == board[2]:
        return board[0]
    elif board[3] == board[4] == board[5]:
        return board[3]
    elif board[6] == board[7] == board[8]:
        return board[6]

    # vertical
    elif board[0] == board[3] == board[6]:
        return board[0]
    elif board[1] == board[4] == board[7]:
        return board[1]
    elif board[2] == board[5] == board[8]:
        return board[2]

    # diagonal
    elif board[0] == board[4] == board[8]:
        return board[0]
    elif board[2] == board[4] == board[6]:
        return board[2]

    return None


def PrintBoard(board):
    """Clears the console and prints the current board."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'''
    {board[0]} | {board[1]} | {board[2]}
    {board[3]} | {board[4]} | {board[5]}
    {board[6]} | {board[7]} | {board[8]}
    ''')


def GetAvailableCells(board):
    """Returns a list of indices containing all available (empty) cells."""
    available = list()
    for cell in board:
        if cell != "X" and cell != "O":
            available.append(cell)
    return available


def minimax(position, depth, alpha, beta, isMaximizing):
    """
    Minimax algorithm with Alpha-Beta pruning.
    """

    winner = GetWinner(position)
    if winner != None:
        return (10 - depth) if winner == "X" else (-10 + depth)

    if len(GetAvailableCells(position)) == 0:
        return 0

    if isMaximizing:
        maxEval = -math.inf
        for cell in GetAvailableCells(position):
            position[cell - 1] = "X"
            Eval = minimax(position, depth + 1, alpha, beta, False)
            maxEval = max(maxEval, Eval)
            alpha = max(alpha, Eval)
            position[cell - 1] = cell

            if beta <= alpha:
                break

        return maxEval

    else:
        minEval = +math.inf
        for cell in GetAvailableCells(position):
            position[cell - 1] = "O"
            Eval = minimax(position, depth + 1, alpha, beta, True)
            minEval = min(minEval, Eval)
            beta = min(beta, Eval)
            position[cell - 1] = cell

            if beta <= alpha:
                break

        return minEval


def FindBestMove(currentPosition, AI):
    """
    Finds the best move for current AI player.
    """

    bestVal = -math.inf if AI == "X" else +math.inf
    bestMove = -1

    for cell in GetAvailableCells(currentPosition):

        currentPosition[cell - 1] = AI

        moveVal = minimax(
            currentPosition, 
            0, 
            -math.inf, 
            +math.inf, 
            False if AI == "X" else True
        )

        currentPosition[cell - 1] = cell

        if AI == "X" and moveVal > bestVal:
            bestVal = moveVal
            bestMove = cell

        elif AI == "O" and moveVal < bestVal:
            bestVal = moveVal
            bestMove = cell

    return bestMove


def main():
    player = input("Play as X or O? ").strip().upper()
    AI = "O" if player == "X" else "X"

    currentGame = [*range(1, 10)]

    currentTurn = "X"  # X always starts first.
    counter = 0

    while True:

        # AI turn
        if currentTurn == AI:
            cell = FindBestMove(currentGame, AI)
            currentGame[cell - 1] = AI
            currentTurn = player

        # Player turn
        elif currentTurn == player:
            PrintBoard(currentGame)
            while True:
                try:
                    humanInput = int(input("Enter Number: ").strip())
                except:
                    print("Invalid input. Enter a number 1-9.")
                    continue

                if humanInput in currentGame:
                    currentGame[humanInput - 1] = player
                    currentTurn = AI
                    break
                else:
                    PrintBoard(currentGame)
                    print("Cell Not Available.")

        # Check win
        if GetWinner(currentGame) is not None:
            PrintBoard(currentGame)
            print(f"{GetWinner(currentGame)} WON!!!")
            break

        counter += 1
        if counter == 9:
            PrintBoard(currentGame)
            print("Tie.")
            break


if __name__ == "__main__":
    main()
