def load_fake_platform_tiles(width, height, surface, TILE_SIZE, ground_image, platform_image):
    for x in range(width):
        for y in range(height):
            if x == 0:
                surface.blit(platform_image, (y*TILE_SIZE, x*TILE_SIZE))
            else:
                surface.blit(ground_image, (y*TILE_SIZE, x*TILE_SIZE))
    return surface
