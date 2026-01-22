class XiangqiRules:
    @staticmethod
    def is_valid_move(board, piece_type, color, start, end):
        start_row, start_col = start
        end_row, end_col = end
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Can't capture own pieces
        if board[end_row][end_col] and board[end_row][end_col][1] == color:
            return False

        # Check for flying general (direct confrontation)
        if piece_type == "general" and XiangqiRules._is_flying_general(board, start, end):
            return True

        # Different rules for each piece type
        if piece_type == "soldier":
            return XiangqiRules._valid_soldier_move(board, color, start, end)
        elif piece_type == "rook":
            return XiangqiRules._valid_rook_move(board, start, end)
        elif piece_type == "horse":
            return XiangqiRules._valid_horse_move(board, start, end)
        elif piece_type == "elephant":
            return XiangqiRules._valid_elephant_move(board, color, start, end)
        elif piece_type == "advisor":
            return XiangqiRules._valid_advisor_move(board, color, start, end)
        elif piece_type == "general":
            return XiangqiRules._valid_general_move(board, color, start, end)
        elif piece_type == "cannon":
            return XiangqiRules._valid_cannon_move(board, start, end)

        return False

    @staticmethod
    def _valid_soldier_move(board, color, start, end):
        start_row, start_col = start
        end_row, end_col = end
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Soldiers can only move forward before crossing river
        forward = 1 if color == "black" else -1

        # Check if soldier has crossed the river
        # River is between row 4 and 5
        crossed_river = (color == "black" and start_row >= 5) or (color == "red" and start_row <= 4)

        if crossed_river:
            # Can move forward or sideways, but only one step
            if (row_diff == forward and col_diff == 0) or (row_diff == 0 and abs(col_diff) == 1):
                return True
        else:
            # Can only move forward before crossing river
            if row_diff == forward and col_diff == 0:
                return True

        return False

    @staticmethod
    def _valid_rook_move(board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        # Rooks move in straight lines
        if start_row != end_row and start_col != end_col:
            return False

        return XiangqiRules._is_path_clear(board, start, end)

    @staticmethod
    def _valid_horse_move(board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Horse moves in L shape (2+1)
        if abs(row_diff) == 2 and abs(col_diff) == 1:
            block_row = start_row + row_diff // 2
            return board[block_row][start_col] is None
        elif abs(row_diff) == 1 and abs(col_diff) == 2:
            block_col = start_col + col_diff // 2
            return board[start_row][block_col] is None

        return False

    @staticmethod
    def _valid_elephant_move(board, color, start, end):
        start_row, start_col = start
        end_row, end_col = end
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Elephants can't cross the river
        # Black (top) 0-4, Red (bottom) 5-9
        if color == "black" and end_row > 4:
            return False
        if color == "red" and end_row < 5:
            return False

        # Elephants move diagonally 2 spaces
        if abs(row_diff) == 2 and abs(col_diff) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            return board[mid_row][mid_col] is None

        return False

    @staticmethod
    def _valid_advisor_move(board, color, start, end):
        start_row, start_col = start
        end_row, end_col = end
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Advisors must stay in the palace
        palace_rows = (0, 1, 2) if color == "black" else (7, 8, 9)
        palace_cols = (3, 4, 5)
        if end_row not in palace_rows or end_col not in palace_cols:
            return False

        # Advisors move diagonally 1 space
        return abs(row_diff) == 1 and abs(col_diff) == 1

    @staticmethod
    def _valid_general_move(board, color, start, end):
        start_row, start_col = start
        end_row, end_col = end
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Generals must stay in the palace
        palace_rows = (0, 1, 2) if color == "black" else (7, 8, 9)
        palace_cols = (3, 4, 5)
        if end_row not in palace_rows or end_col not in palace_cols:
            return False

        # Generals move orthogonally 1 space
        return (abs(row_diff) == 1 and col_diff == 0) or (row_diff == 0 and abs(col_diff) == 1)

    @staticmethod
    def _valid_cannon_move(board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        # Cannons move in straight lines
        if start_row != end_row and start_col != end_col:
            return False

        pieces_in_path = XiangqiRules._count_pieces_in_path(board, start, end)

        # If target is empty, path must be clear
        if board[end_row][end_col] is None:
            return pieces_in_path == 0
        else:
            # To capture, need exactly one piece to jump over
            return pieces_in_path == 1

    @staticmethod
    def _is_path_clear(board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col]:
                    return False
        else:
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col]:
                    return False

        return True

    @staticmethod
    def _count_pieces_in_path(board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        count = 0

        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col]:
                    count += 1
        else:
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col]:
                    count += 1

        return count

    @staticmethod
    def _is_flying_general(board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        # Only relevant for generals
        if start_col != end_col:
            return False

        # Check if there's a direct confrontation
        min_row = min(start_row, end_row)
        max_row = max(start_row, end_row)

        # Check if there are any pieces between the generals
        for row in range(min_row + 1, max_row):
            if board[row][start_col]:
                return False

        # Make sure the piece at the end is an enemy general
        if board[end_row][end_col] and board[end_row][end_col][0] == "general":
            return True

        return False

    @staticmethod
    def get_valid_moves(board, piece_type, color, start):
        valid_moves = []
        for row in range(10):
            for col in range(9):
                if XiangqiRules.is_valid_move(board, piece_type, color, start, (row, col)):
                    valid_moves.append((row, col))
        return valid_moves