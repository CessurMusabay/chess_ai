import os
import pygame


class ChessPiece:
    img_width = 64

    def __init__(self, is_white):
        self.cb_state = []
        root_path = os.path.dirname(os.path.abspath(__file__))
        class_name = self.__class__.__name__.lower()
        self.is_white = is_white
        self.img_path = os.path.join(root_path, f"images/{'white' if self.is_white else 'black'}/{class_name}.png")
        self.img = pygame.transform.scale(pygame.image.load(self.img_path), (self.img_width, self.img_width))

    def is_valid_pos(self, i, j):
        # return is_valid_pos, has_ate
        try:
            piece = self.cb_state[i][j]
            if piece is None:
                return True, False
            elif self.is_white != piece.is_white:
                return True, True
        except:
            pass
        return False, True


class Pawn(ChessPiece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.point = 1

    def next_steps(self, pos, cb_state):
        steps = []
        i, j = pos

        if self.is_white:
            if i == 6 and cb_state[i - 2][j] is None and cb_state[i - 1][j] is None:
                steps.append((i - 2, j))
            if cb_state[i - 1][j] is None and i > 0:
                steps.append((i - 1, j))

            if i > 0 and j < 7:
                right = cb_state[i - 1][j + 1]
                if (right is not None) and (not right.is_white):
                    steps.append((i - 1, j + 1))
            if i > 0 and j > 0:
                left = cb_state[i - 1][j - 1]
                if (left is not None) and (not left.is_white):
                    steps.append((i - 1, j - 1))

        if not self.is_white:
            if i == 1 and cb_state[i + 2][j] is None and cb_state[i + 1][j] is None:
                steps.append((i + 2, j))
            if cb_state[i + 1][j] is None and i < 7:
                steps.append((i + 1, j))

            if i < 7 and j < 7:
                right = cb_state[i + 1][j + 1]
                if (right is not None) and (right.is_white):
                    steps.append((i + 1, j + 1))
            if i < 7 and j > 0:
                left = cb_state[i + 1][j - 1]
                if (left is not None) and (left.is_white):
                    steps.append((i + 1, j - 1))

        return steps


class Rook(ChessPiece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.point = 5

    def next_steps(self, pos, cb_state):
        self.cb_state = cb_state
        steps = []
        i, j = pos

        # top
        for k in range(i - 1, -1, -1):
            is_valid, has_ate = self.is_valid_pos(k, j)
            if is_valid: steps.append((k, j))
            if has_ate: break

        # bottom
        for k in range(i + 1, 8, 1):
            is_valid, has_ate = self.is_valid_pos(k, j)
            if is_valid: steps.append((k, j))
            if has_ate: break

        # right
        for k in range(j + 1, 8, 1):
            is_valid, has_ate = self.is_valid_pos(i, k)
            if is_valid: steps.append((i, k))
            if has_ate: break

        # left
        for k in range(j - 1, -1, -1):
            is_valid, has_ate = self.is_valid_pos(i, k)
            if is_valid: steps.append((i, k))
            if has_ate: break

        return steps


class Knight(ChessPiece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.point = 3

    def next_steps(self, pos, cb_state):
        self.cb_state = cb_state
        steps = []
        i, j = pos
        max_step = 3

        for k in range(2, -3, -1):
            if k == 0: continue

            pos = (i + k, j + abs(max_step - abs(k)))
            print(pos)
            is_valid, has_ate = self.is_valid_pos(pos[0], pos[1])
            if is_valid: steps.append(pos)

            pos = (i + k, j - abs(max_step - abs(k)))
            print(pos)
            is_valid, has_ate = self.is_valid_pos(pos[0], pos[1])
            if is_valid: steps.append(pos)

        return steps


class Bishop(ChessPiece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.point = 3

    def next_steps(self, pos, cb_state):
        self.cb_state = cb_state
        steps = []
        i, j = pos

        # top right
        l = 1
        for k in range(i - 1, -1, -1):
            is_valid, has_ate = self.is_valid_pos(k, j + l)
            if is_valid: steps.append((k, j + l))
            if has_ate: break
            l += 1

        # bottom right
        l = 1
        for k in range(i + 1, 8, 1):
            is_valid, has_ate = self.is_valid_pos(k, j + l)
            if is_valid: steps.append((k, j + l))
            if has_ate: break
            l += 1

        # top left
        l = 1
        for k in range(i - 1, -1, -1):
            is_valid, has_ate = self.is_valid_pos(k, j - l)
            if is_valid: steps.append((k, j - l))
            if has_ate: break
            l += 1

        # bottom left
        l = 1
        for k in range(i + 1, 8, 1):
            is_valid, has_ate = self.is_valid_pos(k, j - l)
            if is_valid: steps.append((k, j - l))
            if has_ate: break
            l += 1

        return steps


class Queen(ChessPiece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.__bishop = Bishop(is_white=is_white)
        self.__rook = Rook(is_white=is_white)
        self.point = 9

    def next_steps(self, pos, cb_state):
        self.cb_state = cb_state
        steps = self.__bishop.next_steps(pos, cb_state) + self.__rook.next_steps(pos, cb_state)
        return steps


class King(ChessPiece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.point = 1000

    def next_steps(self, pos, cb_state):
        self.cb_state = cb_state
        steps = []
        i, j = pos

        for k in [-1, 0, 1]:
            for l in [-1, 0, 1]:
                if k == l == 0: continue
                new_i, new_j = k + i, j + l
                is_valid, has_ate = self.is_valid_pos(new_i, new_j)
                if is_valid: steps.append((new_i, new_j))

        return steps
