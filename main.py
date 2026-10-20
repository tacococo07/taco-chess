import raylib
import time

# window dimensions
screen_width = 800
screen_height = 800
board_size = 640
square_size = board_size // 8
offset_x = (screen_width - board_size) // 2
offset_y = (screen_height - board_size) // 2

# custom color scheme (dark mode aesthetic)
bg_color = (15, 15, 15, 255)
light_square = (238, 238, 210, 255)
dark_square = (118, 150, 86, 255)
white_piece = (255, 255, 255, 255)
black_piece = (30, 30, 30, 255)
selected_color = (245, 245, 66, 160)
valid_move_color = (100, 220, 100, 160)

piece_symbols = {
    "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
    "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙"
}

def create_board():
    return [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]

def is_white(piece):
    return piece != "." and piece.isupper()

def is_black(piece):
    return piece != "." and piece.islower()

def get_valid_moves(board, row, col, current_turn):
    piece = board[row][col]
    if piece == ".":
        return []
    
    if current_turn == "W" and not is_white(piece):
        return []
    if current_turn == "B" and not is_black(piece):
        return []

    moves = []
    p_type = piece.lower()

    if p_type == "p":
        direction = -1 if is_white(piece) else 1
        start_row = 6 if is_white(piece) else 1

        nr = row + direction
        if 0 <= nr < 8 and board[nr][col] == ".":
            moves.append((nr, col))
            nnr = row + 2 * direction
            if row == start_row and board[nnr][col] == ".":
                moves.append((nnr, col))

        for dc in [-1, 1]:
            nc = col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target != ".":
                    if is_white(piece) and is_black(target):
                        moves.append((nr, nc))
                    elif is_black(piece) and is_white(target):
                        moves.append((nr, nc))

    elif p_type == "n":
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in offsets:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target == "." or (is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target)):
                    moves.append((nr, nc))

    elif p_type == "k":
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),          (0, 1),
                   (1, -1),  (1, 0),  (1, 1)]
        for dr, dc in offsets:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target == "." or (is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target)):
                    moves.append((nr, nc))

    directions = []
    if p_type in ["r", "q"]:
        directions.extend([(-1, 0), (1, 0), (0, -1), (0, 1)])
    if p_type in ["b", "q"]:
        directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        while 0 <= nr < 8 and 0 <= nc < 8:
            target = board[nr][nc]
            if target == ".":
                moves.append((nr, nc))
            else:
                if (is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target)):
                    moves.append((nr, nc))
                break
            nr += dr
            nc += dc

    return moves

def main():
    raylib.InitWindow(screen_width, screen_height, b"taco chess - raylib")
    raylib.SetTargetFPS(60)
    
    # force window position and focus
    raylib.SetWindowPosition(200, 200)

    board = create_board()
    selected_sq = None
    valid_moves = []
    current_turn = "W"

    while not raylib.WindowShouldClose():
        # --- mouse input processing ---
        if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
            mouse_x = raylib.GetMouseX()
            mouse_y = raylib.GetMouseY()

            if offset_x <= mouse_x < offset_x + board_size and offset_y <= mouse_y < offset_y + board_size:
                col = (mouse_x - offset_x) // square_size
                row = (mouse_y - offset_y) // square_size

                if selected_sq is None:
                    if board[row][col] != ".":
                        moves = get_valid_moves(board, row, col, current_turn)
                        if moves:
                            selected_sq = (row, col)
                            valid_moves = moves
                else:
                    if (row, col) in valid_moves:
                        sr, sc = selected_sq
                        board[row][col] = board[sr][sc]
                        board[sr][sc] = "."
                        current_turn = "B" if current_turn == "W" else "W"
                    
                    selected_sq = None
                    valid_moves = []

        # --- draw loop ---
        raylib.BeginDrawing()
        raylib.ClearBackground(bg_color)

        for row in range(8):
            for col in range(8):
                is_light = (row + col) % 2 == 0
                color = light_square if is_light else dark_square
                x = offset_x + col * square_size
                y = offset_y + row * square_size
                raylib.DrawRectangle(x, y, square_size, square_size, color)

        if selected_sq:
            sr, sc = selected_sq
            sx = offset_x + sc * square_size
            sy = offset_y + sr * square_size
            raylib.DrawRectangle(sx, sy, square_size, square_size, selected_color)

        for vr, vc in valid_moves:
            vx = offset_x + vc * square_size
            vy = offset_y + vr * square_size
            raylib.DrawRectangle(vx, vy, square_size, square_size, valid_move_color)

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != ".":
                    symbol = piece_symbols.get(piece, "")
                    p_color = white_piece if is_white(piece) else black_piece
                    x = offset_x + col * square_size
                    y = offset_y + row * square_size
                    raylib.DrawText(symbol.encode('utf-8'), x + 18, y + 10, 48, p_color)

        raylib.DrawRectangleLines(offset_x, offset_y, board_size, board_size, raylib.RAYWHITE)
        turn_text = f"turn: {'white' if current_turn == 'W' else 'black'}"
        raylib.DrawText(turn_text.encode('utf-8'), 20, 20, 24, raylib.RAYWHITE)

        raylib.EndDrawing()

    raylib.CloseWindow()

if __name__ == "__main__":
    main()