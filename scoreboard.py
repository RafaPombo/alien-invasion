import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_images()

    def prep_images(self):
        """Prepare the initial score images."""
        self.prep_level()
        self.prep_score()
        self.prep_high_score()
        self.prep_ships()
        self.prep_scoreboard()

    def prep_scoreboard(self):
        self.scoreboard_image = pygame.Surface((self.screen_rect.width, self.level_rect.bottom + 5))
        self.scoreboard_image.fill(self.settings.sb_color)

        self.scoreboard_rect = self.scoreboard_image.get_rect()

    def prep_level(self):
        """Turn the level into a rendered image."""

        self.level_title_image = self.font.render('LEVEL', True, self.text_color, self.settings.sb_color)

        self.level_title_rect = self.level_title_image.get_rect()
        self.level_title_rect.right = self.screen_rect.right - 5
        self.level_title_rect.top = 5

        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.sb_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.level_title_rect.right
        self.level_rect.top = self.level_title_rect.bottom + 5

    def prep_score(self):
        """Turn the score into a rendered image."""

        self.score_title_image = self.font.render('SCORE', True, self.text_color, self.settings.sb_color)

        self.score_title_rect = self.score_title_image.get_rect()
        self.score_title_rect.right = self.level_title_rect.left - 100
        self.score_title_rect.top = 5

        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.sb_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.score_title_rect.right
        self.score_rect.top = self.score_title_rect.bottom + 5

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.sb_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 5

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game, life=True)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw scores, level, and ships to the screen."""

        self.screen.blit(self.scoreboard_image, self.scoreboard_rect)

        self.screen.blit(self.level_title_image, self.level_title_rect)
        self.screen.blit(self.level_image, self.level_rect)

        self.screen.blit(self.score_title_image, self.score_title_rect)
        self.screen.blit(self.score_image, self.score_rect)

        self.screen.blit(self.high_score_image, self.high_score_rect)

        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
