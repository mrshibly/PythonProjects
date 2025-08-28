import pygame
from tkinter import messagebox, Tk

# Constants
WIDTH, HEIGHT = 600, 700  # Increased height for dashboard
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
HIGHLIGHT = (255, 255, 0)

# Piece Representation
GREEN_PAWN = 'P'
BLUE_PAWN = 'p'
EMPTY = '.'

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pawn Chess Multiplayer")
FONT = pygame.font.SysFont(None, 40)

# Score Tracking
score = {GREEN_PAWN: 0, BLUE_PAWN: 0}
selected_pawn = None
valid_moves = []

# Load pawn images
GREEN_PAWN_IMG = pygame.transform.smoothscale(pygame.image.load("green.png"), (SQUARE_SIZE, SQUARE_SIZE))
BLUE_PAWN_IMG = pygame.transform.smoothscale(pygame.image.load("blue.png"), (SQUARE_SIZE, SQUARE_SIZE))
# Load logo image
LOGO_IMG = pygame.transform.smoothscale(pygame.image.load("logo.png"), (180, 90))

def create_board():
    """Creates an 8x8 chessboard with pawns in their starting positions."""
    board = [[EMPTY] * COLS for _ in range(ROWS)]
    for i in range(COLS):
        board[1][i] = BLUE_PAWN
        board[6][i] = GREEN_PAWN
    return board

def draw_dashboard(board):
    dashboard_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)
    # Modern gradient background
    for i in range(100):
        color = (
            240 - i, 240 - i//2, 255 - i//4
        )
        pygame.draw.rect(WIN, color, (0, HEIGHT - 100 + i, WIDTH, 1))
    # Soft shadow
    shadow = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (60,60,90,60), shadow.get_rect(), border_radius=36)
    WIN.blit(shadow, (0, HEIGHT - 100))
    stack_font = pygame.font.SysFont("Segoe UI", 38, bold=True)
    score_text = stack_font.render(f"Green: {score[GREEN_PAWN]}  Blue: {score[BLUE_PAWN]}", True, (40, 40, 80))
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT - 80))
    pygame.draw.rect(WIN, (180, 180, 220), dashboard_rect, border_radius=30, width=4)
    pygame.draw.rect(WIN, (180, 180, 220), dashboard_rect, border_radius=30, width=4)

def draw_board(board):
    """Draws the chessboard and highlights valid moves with enhanced visuals."""
    # Subtle gradient background
    for y in range(ROWS):
        for x in range(COLS):
            square_rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            base = 220 if (x + y) % 2 == 0 else 80
            grad = int(20 * (y / ROWS))
            color = (base - grad, base - grad, base + grad)
            if selected_pawn and (y, x) in [m[1] for m in valid_moves]:
                color = (255, 255, 180)
            # Soft shadow for squares
            shadow = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (60,60,90,30), shadow.get_rect(), border_radius=12)
            WIN.blit(shadow, (x * SQUARE_SIZE, y * SQUARE_SIZE + 4))
            pygame.draw.rect(WIN, color, square_rect, border_radius=10)
            if selected_pawn and (y, x) == selected_pawn:
                neon_colors = [
                    (0, 255, 255, 60),
                    (0, 255, 128, 80),
                    (255, 0, 255, 90),
                    (255, 255, 0, 120),
                    (255, 255, 255, 200)
                ]
                for i, (r, g, b, a) in enumerate(reversed(neon_colors)):
                    s = pygame.Surface((SQUARE_SIZE - 2 + i*4, SQUARE_SIZE - 2 + i*4), pygame.SRCALPHA)
                    pygame.draw.ellipse(s, (r, g, b, a), s.get_rect(), 0)
                    WIN.blit(s, (x * SQUARE_SIZE + 1 - i*2, y * SQUARE_SIZE + 1 - i*2))
            # Draw pawns
            if board[y][x] == GREEN_PAWN:
                WIN.blit(GREEN_PAWN_IMG, (x * SQUARE_SIZE, y * SQUARE_SIZE))
            elif board[y][x] == BLUE_PAWN:
                WIN.blit(BLUE_PAWN_IMG, (x * SQUARE_SIZE, y * SQUARE_SIZE))
            # Move indicator
            if selected_pawn and (y, x) in [m[1] for m in valid_moves]:
                pygame.draw.circle(WIN, (255, 140, 0), (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 5)
                pygame.draw.circle(WIN, (255, 255, 0), (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 10)
    draw_dashboard(board)
    pygame.display.update()

def get_valid_moves(board, color):
    """Returns a list of valid moves for pawns of the given color with custom rules (including double-step and en passant)."""
    moves = []
    direction = -1 if color == GREEN_PAWN else 1
    start_row = 6 if color == GREEN_PAWN else 1
    enemy = BLUE_PAWN if color == GREEN_PAWN else GREEN_PAWN
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == color:
                new_row = row + direction
                # Single step
                if 0 <= new_row < ROWS and board[new_row][col] == EMPTY:
                    moves.append(((row, col), (new_row, col)))
                    # Double step from starting position
                    if row == start_row and board[row + direction][col] == EMPTY and board[row + 2 * direction][col] == EMPTY:
                        moves.append(((row, col), (row + 2 * direction, col)))
                # Captures
                for dcol in (-1, 1):
                    if 0 <= col + dcol < COLS and 0 <= new_row < ROWS:
                        if board[new_row][col + dcol] == enemy:
                            moves.append(((row, col), (new_row, col + dcol)))
                        # En passant
                        if row == (3 if color == GREEN_PAWN else 4):
                            if board[row][col + dcol] == enemy and board[new_row][col + dcol] == EMPTY:
                                moves.append(((row, col), (new_row, col + dcol)))
    return moves

def show_warning(message):
    """Displays a warning message in a popup."""
    root = Tk()
    root.withdraw()
    messagebox.showwarning("Invalid Move", message)
    root.destroy()

def make_move(board, move, turn):
    """Updates the board by executing the given move and updates the score. Handles en passant and double-step."""
    (r1, c1), (r2, c2) = move
    # En passant
    if abs(r2 - r1) == 1 and abs(c2 - c1) == 1 and board[r2][c2] == EMPTY:
        # Remove the captured pawn
        board[r1][c2] = EMPTY
    elif board[r2][c2] != EMPTY:
        score[turn] += 1
    board[r2][c2], board[r1][c1] = board[r1][c1], EMPTY
    return BLUE_PAWN if turn == GREEN_PAWN else GREEN_PAWN

def mode_selection_screen():
    selecting = True
    mode = None
    multiplayer_logo = pygame.transform.smoothscale(pygame.image.load("multiplayer.png"), (90, 90))
    ai_logo = pygame.transform.smoothscale(pygame.image.load("ai.png"), (90, 90))
    while selecting:
        for i in range(HEIGHT):
            color = (255 - i//4, 255 - i//8, 255)
            pygame.draw.rect(WIN, color, (0, i, WIDTH, 1))
        WIN.blit(LOGO_IMG, (WIDTH//2 - LOGO_IMG.get_width()//2, 20))
        title_font = pygame.font.SysFont("Segoe UI", 52, bold=True)
        title = title_font.render("Pawn Chess", True, (40, 40, 80))
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        mp_font = pygame.font.SysFont("Segoe UI", 40, bold=True)
        # Remove text buttons and use logos as buttons
        mp_rect = multiplayer_logo.get_rect(center=(WIDTH//2 - 100, 250))
        ai_rect = ai_logo.get_rect(center=(WIDTH//2 + 100, 350))
        # Draw logos with soft glow
        mp_logo_glow = pygame.Surface((110,110), pygame.SRCALPHA)
        pygame.draw.ellipse(mp_logo_glow, (0,255,0,120), mp_logo_glow.get_rect())
        WIN.blit(mp_logo_glow, mp_rect.topleft)
        WIN.blit(multiplayer_logo, mp_rect.topleft)
        ai_logo_glow = pygame.Surface((110,110), pygame.SRCALPHA)
        pygame.draw.ellipse(ai_logo_glow, (0,100,255,120), ai_logo_glow.get_rect())
        WIN.blit(ai_logo_glow, ai_rect.topleft)
        WIN.blit(ai_logo, ai_rect.topleft)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if mp_rect.inflate(60,28).collidepoint(pos):
                    mode = "multiplayer"
                    selecting = False
                elif ai_rect.inflate(60,28).collidepoint(pos):
                    mode = "ai"
                    selecting = False
                elif ai_rect.inflate(60,28).collidepoint(pos):
                    mode = "ai"
                    selecting = False
    return mode

import copy

def evaluate_board(board, ai_color):
    # Simple evaluation: material + advancement
    score_ai = 0
    score_human = 0
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ai_color:
                score_ai += 10
                # Encourage advancement
                score_ai += (6-row) if ai_color == GREEN_PAWN else (row-1)
            elif board[row][col] != EMPTY:
                score_human += 10
                score_human += (6-row) if board[row][col] == GREEN_PAWN else (row-1)
    return score_ai - score_human

def minimax(board, depth, alpha, beta, maximizing, ai_color):
    enemy = BLUE_PAWN if ai_color == GREEN_PAWN else GREEN_PAWN
    moves = get_valid_moves(board, ai_color if maximizing else enemy)
    if depth == 0 or not moves:
        return evaluate_board(board, ai_color), None
    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, move, ai_color)
            eval, _ = minimax(new_board, depth-1, alpha, beta, False, ai_color)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, move, enemy)
            eval, _ = minimax(new_board, depth-1, alpha, beta, True, ai_color)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def main():
    global selected_pawn, valid_moves, score
    mode = mode_selection_screen()
    board = create_board()
    run, turn = True, GREEN_PAWN
    winner = None
    rematch_rect = None
    ai_color = BLUE_PAWN if mode == "ai" else None
    while run:
        draw_board(board)
        if winner:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((30,30,60,200))
            WIN.blit(overlay, (0,0))
            win_font = pygame.font.SysFont("Segoe UI", 48, bold=True)
            win_text = win_font.render(f"{winner} Wins!", True, (255, 80, 80))
            WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 60))
            rematch_font = pygame.font.SysFont("Segoe UI", 40, bold=True)
            rematch_text = rematch_font.render("Rematch", True, (255,255,255))
            rematch_rect = rematch_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 10))
            pygame.draw.rect(WIN, (0, 100, 255), rematch_rect.inflate(60,28), border_radius=16)
            WIN.blit(rematch_text, rematch_rect)
            pygame.display.update()
        pygame.time.delay(100)
        if mode == "ai" and turn == ai_color and not winner:
            # AI move
            _, ai_move = minimax(board, 3, float('-inf'), float('inf'), True, ai_color)
            if ai_move:
                turn = make_move(board, ai_move, ai_color)
                if not get_valid_moves(board, turn):
                    winner = "Green" if turn == BLUE_PAWN else "Blue"
            else:
                winner = "Green" if ai_color == BLUE_PAWN else "Blue"
            selected_pawn = None
            valid_moves = []
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if winner:
                    if rematch_rect and rematch_rect.collidepoint(pos):
                        board = create_board()
                        score = {GREEN_PAWN: 0, BLUE_PAWN: 0}
                        turn = GREEN_PAWN
                        selected_pawn = None
                        valid_moves = []
                        winner = None
                        continue
                if pos[1] >= HEIGHT - 100 or winner:
                    continue
                col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                if selected_pawn is None:
                    if board[row][col] == turn and (mode == "multiplayer" or turn != ai_color):
                        selected_pawn = (row, col)
                        valid_moves = [move for move in get_valid_moves(board, turn) if move[0] == selected_pawn]
                else:
                    move = (selected_pawn, (row, col))
                    if move in valid_moves:
                        turn = make_move(board, move, turn)
                        if not get_valid_moves(board, turn):
                            winner = "Green" if turn == BLUE_PAWN else "Blue"
                    else:
                        show_warning("Invalid move! Try again.")
                    selected_pawn = None
                    valid_moves = []
    pygame.quit()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()

