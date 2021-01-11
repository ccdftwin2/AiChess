import asyncio
import chess
import chess.engine
import chess.svg
import cairosvg
import os
import random
import re


async def main() -> None:
    # Stockfish engine
    transport, engine = await chess.engine.popen_uci("/usr/local/Cellar/stockfish/12/bin/stockfish")
    black = 0
    white = 0
    draws = 0
    board = chess.Board()

    for j in range(100):

        print("Game number: " + str(j+1))

        # Create the board
        board.reset()

        # Counter
        i = 0

        # Loop through the game
        while not board.is_game_over():
            # Get result from engine
            result = await engine.play(board, chess.engine.Limit(time=0.001))

            # Select random move
            num = random.randint(0, board.legal_moves.count() - 1)
            moves = str(board.legal_moves)[str(board.legal_moves).find(
                "(")+1:str(board.legal_moves).find(")")]
            move = moves.split(', ')[num]

            # Every other move is good- push to board
            if int(i/2) % 2 == 0:
                board.push_san(move)
                # Print each selected move
                print("Random: " + move + " (played)")
                print("Stockfish: " + str(result.move))
            else:
                board.push(result.move)
                # Print each selected move
                print("Random: " + move)
                print("Stockfish: " + str(result.move) + " (played)")

            # Push to image
            svg = chess.svg.board(board, size=350)
            fh = open("board.svg", "w")
            fh.write(svg)
            fh.close()

            # increment counter
            i += 1
            os.system("cairosvg board.svg -o board.png")

        # Update the number of wins
        if board.result == '1-0':
            white += 1
        elif board.result == '0-1':
            black += 1
        else:
            draws += 1

    await engine.quit()
    print("White: " + str(white) + ". Black: " +
          str(black) + ". Draws: " + str(draws) + ".")

asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
asyncio.run(main())
