import chess
import chess.svg
import chess.polyglot
import time

# Creado tablero para que no me grite la función
board = chess.Board()
#movehistory = []

# Tablas usadas para la evaluación de posiciones
# Si la casilla es positiva, la pieza intentara moverse a esa casilla
# Si es negativa el motor tratara de evitar poner la pieza en esa casilla

pawntable = [  # La tabla esta hecha de tal manera que el motor se vea animado a avanzar los peones
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [  # Los caballos se ven animados a ocupar el centro y evitar los bordes a toda costa
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [  # Los alfiles deben evitar las esquinas y los bordes del tablero
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [  # Las torres deben evitar las columnas a y h a la vez que ocupar la fila 7
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [  # La dama debe evitar bordes y esquinas, y ocupar el centro
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [  # El rey debe mantenerse refugiado tras los peones
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


# Función que evaluará nuestro tablero
def evaluate_board():
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate() or board.is_insufficient_material():  # Rey ahogado o material insuficiente para dar mate resultan en tablas
        return 0

    # Obtenemos el numero de piezas que tienen ambos jugadores
    white_pawns = len(board.pieces(chess.PAWN, chess.WHITE))
    white_knights = len(board.pieces(chess.KNIGHT, chess.WHITE))
    white_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
    white_rooks = len(board.pieces(chess.ROOK, chess.WHITE))
    white_queen = len(board.pieces(chess.QUEEN, chess.WHITE))
    black_pawns = len(board.pieces(chess.PAWN, chess.BLACK))
    black_knights = len(board.pieces(chess.KNIGHT, chess.BLACK))
    black_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))
    black_rooks = len(board.pieces(chess.ROOK, chess.BLACK))
    black_queen = len(board.pieces(chess.QUEEN, chess.BLACK))

    # Calculamos la diferencia de material
    materialDiff = 100 * (white_pawns - black_pawns) + 320 * (white_knights - black_knights) + 330 * (
            white_bishops - black_bishops) \
                   + 500 * (white_rooks - black_rooks) + 900 * (white_queen - black_queen)

    # Calculamos la evaluacion segun las matrices definidas arriba
    # La primera linea ira sumando las piezas que tenemos en el tablero segun el valor dado en la tabla
    # La segunda linea flipea el tablero y evalua
    eval_pawns = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    eval_pawns = eval_pawns + sum(
        [-pawntable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.WHITE)])

    eval_knights = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    eval_knights = eval_knights + sum(
        [-knightstable[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.WHITE)])

    eval_bishops = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    eval_bishops = eval_bishops + sum(
        [-bishopstable[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.WHITE)])

    eval_rooks = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    eval_rooks = eval_rooks + sum(
        [-rookstable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.WHITE)])

    eval_queen = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    eval_queen = eval_queen + sum(
        [-queenstable[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.WHITE)])

    eval_king = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    eval_king = eval_king + sum(
        [-kingstable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.WHITE)])

    evaluation = materialDiff + eval_pawns + eval_knights + eval_bishops + eval_rooks + eval_queen + eval_king

    if board.turn:
        return evaluation
    else:
        return -evaluation


def alphabeta(alpha, beta, depth):
    best_score = -9999
    if depth == 0:
        return quiesce(alpha, beta)

    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depth - 1)
        board.pop()

        if score >= beta:
            return score
        if score > best_score:
            score = best_score
        if score > alpha:
            alpha = score

    return best_score


def quiesce(alpha, beta):
    stand_pat = evaluate_board()
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

    return alpha


def selectmove(depth):
    try:
        move = chess.polyglot.MemoryMappedReader("Perfect2017.bin").weighted_choice(board).move
        #movehistory.append(move)
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth-1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if boardValue > alpha:
                alpha = boardValue
            board.pop()

        #movehistory.append(bestMove)
        return bestMove


board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

print(board)
print(board.is_valid())
print(evaluate_board())

print(selectmove(3))

#board = chess.Board("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1")
board = chess.Board("2q1r1rk/3bbnnp/p2p1pp1/2pPp3/PpP1P1P1/1P2BNNP/2BQ1PRK/7R w - - 0 1")
print(board)
print(board.is_valid())
print(evaluate_board())
start_time = time.time()
print("Encontrando movimiento...")
move_found = selectmove(3)

print("Movimiento encontrado:")
print(move_found)
print("Ha tardado: " + time.time()-start_time + " segundos")

