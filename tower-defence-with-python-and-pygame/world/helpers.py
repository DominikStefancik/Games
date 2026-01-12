def draw_text(surface, text, font, text_column, x, y):
    # First we have to turn a text into an image
    image = font.render(text, True, text_column)
    surface.blit(image, (x, y))
