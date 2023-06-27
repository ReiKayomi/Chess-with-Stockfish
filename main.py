import pygame
import chess
import stockfish
import os

pygame.init()

WIDTH, HEIGHT = 800, 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION

pygame.display.set_caption("Chess")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

board = chess.Board()

engine = stockfish.Stockfish("stockfish (EXTRACT ME)\stockfish\stockfish-windows-2022-x86-64-modern.exe")

piece_images = {}

def load_piece_images():
    piece_directory = "piece_images"
    for color in ["white", "black"]:
        for piece_type in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
            file_name = f"{color}_{piece_type}.png"
            file_path = os.path.join(piece_directory, color, file_name)
            image = pygame.image.load(file_path)
            piece_images[(color, piece_type)] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

load_piece_images()

def draw_board():
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if (row + col) % 2 == 0:
                color = pygame.Color("white")
            else:
                color = pygame.Color("gray")
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            square = chess.square(col, DIMENSION - 1 - row)
            piece = board.piece_at(square)
            if piece:
                piece_name = piece.symbol()
                piece_color = "white" if piece.color == chess.WHITE else "black"
                piece_type = chess.piece_name(piece.piece_type).lower()
                piece_image = piece_images[(piece_color, piece_type)]
                screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def make_ai_move():
    engine.set_fen_position(board.fen())
    best_move = engine.get_best_move_time(1000)
    board.push_san(best_move)

def screen_to_chess_pos(screen_pos):
    row = screen_pos[1] // SQUARE_SIZE
    col = screen_pos[0] // SQUARE_SIZE
    return chess.square(col, DIMENSION - 1 - row)

running = True
selected_square = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()
                square = screen_to_chess_pos(pos)
                piece = board.piece_at(square)
                if selected_square is None and piece is not None and piece.color == board.turn:
                    selected_square = square
                elif selected_square is not None and selected_square == square:
                    selected_square = None
                elif selected_square is not None:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        if move.promotion is not None:
                            promotion_piece = None
                            while promotion_piece not in ["q", "r", "b", "n"]:
                                promotion_piece = input("Enter promotion piece (q, r, b, n): ")
                            move.promotion = chess.Piece.from_symbol(promotion_piece.upper())
                        board.push(move)
                        make_ai_move()
                        selected_square = None

    screen.fill(pygame.Color("white"))

    draw_board()

    if selected_square is not None:
        pygame.draw.rect(screen, (0, 255, 0, 100), (chess.square_file(selected_square) * SQUARE_SIZE,
                                                    (DIMENSION - 1 - chess.square_rank(selected_square)) * SQUARE_SIZE,
                                                    SQUARE_SIZE, SQUARE_SIZE), 3)

    pygame.display.flip()

pygame.quit()