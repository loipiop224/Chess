from stockfish import Stockfish
import time
stockfish = Stockfish(path="/home/imnguyenhat213/Stockfish/src/stockfish",
                      depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})
stockfish.set_fen_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
moves = ['e2e4']
stockfish.set_position(moves)
print(stockfish.get_board_visual())
stockfish.set_elo_rating(1850)
stockfish.set_depth(16)


for i in range(0, 40):
    time.sleep(2.0)
    move = stockfish.get_best_move_time(1000)
    moves.append(move)
    stockfish.set_position(moves)
    print(stockfish.get_board_visual())
