# 14 Hours of Python Game Development - from Beginner to Advanced
# Instructor: Tech With Tim
# Followed along and coded by: Jose 'Joe' Ruiz
# Car Racing Game (Medium)
# Utils.py

import pygame


def scale_image(img, factor: float):
    """Scale an image by a given factor."""
    new_width  = round(img.get_width() * factor)
    new_height = round(img.get_height() * factor)
    return pygame.transform.scale(img, (new_width, new_height))
