from numpy.core.numeric import outer
import pygame as pg
import os
import time

if not pg.font:
    print("Warning: Font disabled. No text available!")
if not pg.mixer:
    print("Warning: Mixer disabled. No sound active!")


class DiceSprite:
    
    def __init__(self, tile_size):
        self.tile_size = tile_size
        pg.sprite.Sprite.__init__(self)
        self.image = load_image(os.path.join("images", "dice_sprites.png"), colorkey=None, width = 3*tile_size)

    def image_at(self, row=0, col=0):
        rect = pg.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
        image = pg.Surface(rect.size).convert()
        image.blit(self.image, (0, 0), rect)
        image.set_colorkey((10, 10, 10), pg.RLEACCEL)
        return image


class TableTopLayout:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1280, 800), pg.SCALED)
        pg.display.set_caption("Royal Game of UR")
        pg.mouse.set_visible(True)
        self.border = (40, 50)
        self.tile_size = (1280 - 2 * self.border[0]) / 12

        image_folder = "images"
        board_file = os.path.join(image_folder, "game_board.png")
        black_piece_file = os.path.join(image_folder, "black_piece.png")
        white_piece_file = os.path.join(image_folder, "white_piece.png")
        dice_sprite_file = os.path.join(image_folder, "dice_sprites.png")

        sound_folder = "sounds"
        roll_file = os.path.join(sound_folder, "roll.wav")
        drop_file = os.path.join(sound_folder, "drop.wav")
        throw_file = os.path.join(sound_folder, "throw.wav")
        simple_file = os.path.join(sound_folder, "simple.wav")

        self.roll_sound = load_sound(roll_file)
        self.drop_sound = load_sound(drop_file)
        self.throw_sound = load_sound(throw_file)
        self.simple_sound = load_sound(simple_file)

        self.board_img = load_image(board_file, colorkey=(10,10,10), width=8*self.tile_size)
        self.piece_W_img = load_image(white_piece_file, colorkey=(10,10,10), width=self.tile_size)
        self.piece_B_img = load_image(black_piece_file, colorkey=(10,10,10), width=self.tile_size)
        self.dice_sprite = DiceSprite(self.tile_size)


        self.home_W_rect = pg.Rect(self.border[0]+0.5*self.tile_size, self.border[1] + 0.5*self.tile_size, 7*self.tile_size, 1*self.tile_size)
        self.home_B_rect = pg.Rect(self.border[0]+0.5*self.tile_size, self.border[1] + 5.5*self.tile_size, 7*self.tile_size, 1*self.tile_size)
        self.board_rect = pg.Rect(self.border[0]+ 0*self.tile_size, self.border[1] + 2*self.tile_size, 8*self.tile_size, 3*self.tile_size)
        self.dice_rect = pg.Rect(self.border[0] + 9 * self.tile_size, self.border[0] + 2 * self.tile_size, 3*self.tile_size, 3*self.tile_size)

        self.clock = pg.time.Clock()




    def setup_table(self, game_string=None, dice_roll=0):
        ## Define UI setup
        full_board_rect = pg.Rect(self.border[0], self.border[1], self.screen.get_size()[0] - 2 * self.border[0], self.screen.get_size()[1] - 2* self.border[1])
        home_shape = (7 * self.tile_size, 1 * self.tile_size)


        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((85, 119, 94))

        play_area = pg.Surface(full_board_rect.size)
        play_area = play_area.convert()
        play_area.fill((85, 119, 94))

        home_W_area = pg.Surface(home_shape)
        home_W_area = home_W_area.convert()
        home_W_area.fill((10, 50, 10))

        board_area = pg.Surface(self.board_rect.size).convert()
        board_area.fill((10, 50, 10))
        board_area.blit(self.board_img, (0, 0))

        home_B_area = pg.Surface(home_shape)
        home_B_area = home_B_area.convert()
        home_B_area.fill((10, 50, 10))

        # Place pieces on board
        if game_string:

            # Place pieces in home area
            idx_start = game_string.find("0") + 1
            idx_end = game_string.find("1")
            pieces = game_string[idx_start:idx_end]
            black_home = 0
            white_home = 0
            for p in pieces:
                if p == "W":
                    home_W_area.blit(self.piece_W_img, (white_home * self.tile_size, 0))
                    white_home += 1
                elif p == "B":
                    home_B_area.blit(self.piece_B_img, (black_home * self.tile_size, 0))
                    black_home += 1
            
            # Count Score
            idx_start = game_string.find("f") + 1
            pieces = game_string[idx_start:]
            black_converted = 0
            white_converted = 0
            for p in pieces:
                if p == "W":
                    white_converted += 1
                elif p == "B":
                    black_converted += 1
            if pg.font:
                font = pg.font.Font(None, 64)
                w_text = font.render(f"{white_converted:01d}", True, (255, 255, 255))
                w_text_pos = w_text.get_rect(centerx=5.5*self.tile_size, centery=0.5*self.tile_size)
                b_text = font.render(f"{black_converted:01d}", True, (0, 0, 0))
                b_text_pos = b_text.get_rect(centerx=5.5*self.tile_size, centery=2.5*self.tile_size)
                board_area.blit(w_text, w_text_pos)
                board_area.blit(b_text, b_text_pos)

            for i in range(1, 15, 1):
                idx_start = game_string.find(f"{i:x}") + 1
                idx_end = game_string.find(f"{i+1:x}")
                pieces = game_string[idx_start:idx_end]
                if "W" in pieces:
                    indeces = board_tile_to_indeces(i, "W")
                    board_area.blit(self.piece_W_img, (indeces[0] * self.tile_size, indeces[1] * self.tile_size))
                if "B" in pieces:
                    indeces = board_tile_to_indeces(i, "B")
                    board_area.blit(self.piece_B_img, (indeces[0] * self.tile_size, indeces[1] * self.tile_size))

        player_W_indicator = pg.Surface((self.tile_size, self.tile_size)).convert()
        player_W_indicator.fill((255, 255, 255))
        player_B_indicator = pg.Surface((self.tile_size, self.tile_size)).convert()
        player_B_indicator.fill((0, 0, 0))

        dice_area = pg.Surface((3 * self.tile_size, 3 * self.tile_size))
        dice_area = dice_area.convert()
        dice_area.fill((10, 50, 10))
        if not dice_roll is None:
            dice_area.blit(self.dice_sprite.image_at(row=1 if dice_roll == 0 else 0, col=0), (0.3 * self.tile_size, 0.3 * self.tile_size))
            dice_area.blit(self.dice_sprite.image_at(row=1 if dice_roll <= 1 else 0, col=1), (1.6 * self.tile_size, 0.3 * self.tile_size))
            dice_area.blit(self.dice_sprite.image_at(row=1 if dice_roll <= 2 else 0, col=1), (0.3 * self.tile_size, 1.6 * self.tile_size))
            dice_area.blit(self.dice_sprite.image_at(row=1 if dice_roll <= 3 else 0, col=2), (1.6 * self.tile_size, 1.6 * self.tile_size))
        play_area.blit(home_W_area, (0.5 * self.tile_size, 0.5 * self.tile_size))
        play_area.blit(board_area, (0, 2*self.tile_size))
        play_area.blit(home_B_area, (0.5 * self.tile_size, 5.5 * self.tile_size))
        play_area.blit(dice_area, (9 * self.tile_size, 2 * self.tile_size))
        if game_string and game_string[0] == "W":
            play_area.blit(player_W_indicator, (10 * self.tile_size, 0.5 * self.tile_size))
        elif game_string and game_string[0] == "B":
            play_area.blit(player_B_indicator, (10 * self.tile_size, 5.5 * self.tile_size))
        background.blit(play_area, full_board_rect[:2])
        self.screen.blit(background, (0, 0))
        pg.display.flip()


    def get_clicked_tile_id(self, coords):
        coords = (coords[0], coords[1])
        value = -1
        if self.home_W_rect.collidepoint(coords[0], coords[1]):
            value = 0
        elif self.home_B_rect.collidepoint(coords[0], coords[1]):
            value = 0
        elif self.board_rect.collidepoint(coords[0], coords[1]):
            board_coords = (coords[0] - self.board_rect[0], coords[1] - self.board_rect[1])
            value = board_coords_to_tile(board_coords, self.tile_size)
        elif self.dice_rect.collidepoint(coords[0], coords[1]):
            value = 42
        return value

    def event_handler(self):
        going = True
        tile_value = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False, None
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return False, None
            elif event.type == pg.MOUSEBUTTONDOWN:
                tile_value = self.get_clicked_tile_id(pg.mouse.get_pos())
        return going, tile_value


def board_coords_to_tile(coords, tile_size):
    indeces = (int(coords[0] // tile_size), int(coords[1] // tile_size))
    if indeces[1] == 1:
        return indeces[0] + 5
    elif indeces[0] in [4, 5]:
        return -1
    else:
        return (20 - indeces[0]) % 16

def board_tile_to_indeces(tile, turn):
    if tile in range(5, 13, 1):
        return [tile-5, 1]
    elif tile in [1, 2, 3, 4]:
        return [20 - (tile + 16), 0 if turn == "W" else 2]
    elif tile in [13, 14]:
        return [20 - tile, 0 if turn == "W" else 2]

def test_image_files(imgs):
    import cv2
    for img_file in [board_file, black_piece_file, white_piece_file, dice_sprite_file]:
        img = cv2.imread(img_file)
        cv2.imshow("Image display", img)
        cv2.waitKey(0)


def load_image(name, colorkey=None, width=100):
    image = pg.image.load(name)
    size = image.get_size()
    scale = width / size[0]
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image


def load_sound(name):
    class NoneSound:
        def play(self):
            pass
    
    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    
    return pg.mixer.Sound(name)


if __name__ == "__main__":


    tabletop = TableTopLayout()
    going = True

    tabletop.setup_table(game_string="W0WWWWWWWBBBBBBB123456789abcdef", dice_roll=None)

    while going:
        tabletop.clock.tick(60)

        # Handle Input events
        going, coords = tabletop.event_handler()
            
        



