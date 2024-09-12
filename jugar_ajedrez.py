import chess
import chess.engine
import pygame

# Inicializar pygame
pygame.init()

# Configurar pantalla
WIDTH, HEIGHT = 480, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess AI')

# Colores
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)

# Tablero
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Cargar imagenes
pieces = {}
for piece in ['p', 'n', 'b', 'r', 'q', 'k']:
    # BLANCAS
    pieces[piece.upper()] = pygame.image.load(f'images/w{piece}.png')
    # NEGRAS
    pieces[piece] = pygame.image.load(f'images/b{piece}.png')

# Dibujar tablero
def draw_board():
    colors = [WHITE, BLACK]
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Dibujar piezas
def draw_pieces(board):
    for i in range(BOARD_SIZE * BOARD_SIZE):
        piece = board.piece_at(i)
        if piece:
            row, col = divmod(i, BOARD_SIZE)
            # Invertir el orden de las filas para ver las blancas abajo
            screen.blit(pieces[piece.symbol()], (col * SQUARE_SIZE, (BOARD_SIZE - 1 - row) * SQUARE_SIZE))

# Iniciar tablero y motor
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-windows-x86-64-sse41-popcnt.exe")

# Establecer nivel de la IA (0 - 20)
skill_level = 5
engine.configure({"Skill Level": skill_level})

# Turno del jugador
player_turn = chess.WHITE

# Variables para controlar selección de movimientos
selected_square = None

# Función para que juegue la IA
def ai_move():
    result = engine.play(board, chess.engine.Limit(time=2.0))  # Tiempo de respuesta de la IA
    board.push(result.move)

# Función para detectar clics del jugador
def get_square_under_mouse(pos):
    col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
    row = BOARD_SIZE - 1 - row  # Invertir la fila para alinear el tablero
    return chess.square(col, row)

# Ciclo principal
running = True
while running:
    draw_board()
    draw_pieces(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_turn == chess.WHITE:
                # Lógica para que el jugador haga un movimiento
                pos = pygame.mouse.get_pos()
                # Aquí va la lógica para detectar clics y realizar movimientos.
                # Después de que el jugador haga un movimiento válido:
                square = get_square_under_mouse(pos)

                if selected_square is None:
                    # Seleccionar pieza
                    if board.piece_at(square) and board.color_at(square) == chess.WHITE:
                        selected_square = square
                else:
                    # Intentar mover la pieza seleccionada
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        player_turn = chess.BLACK
                    selected_square = None
    
    # Si es el turno de la IA
    if player_turn == chess.BLACK:
        ai_move()
        player_turn = chess.WHITE  # Cambiar el turno al jugador

    pygame.display.flip()

engine.quit()
pygame.quit()