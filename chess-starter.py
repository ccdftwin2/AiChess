"""import chess

board = chess.Board()
board.push_san("d4")
board.push_san("e5")
print(board.legal_moves.)"""
import asyncio
import chess
import chess.engine
import chess.svg
import cairosvg
import os

async def main() -> None:
    transport, engine = await chess.engine.popen_uci("/usr/local/Cellar/stockfish/12/bin/stockfish")

    board = chess.Board()
    while not board.is_game_over():
        result = await engine.play(board, chess.engine.Limit(time=0.5))
        print(result.move)
        board.push(result.move)
        svg = chess.svg.board(board, size=350)
        fh = open("board.svg","w")
        fh.write(svg)
        fh.close()
        os.system("cairosvg board.svg -o board.png")

    await engine.quit()

asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
asyncio.run(main())