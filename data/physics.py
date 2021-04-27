def collision_tile(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile[1]):
            hit_list.append(tile[1])
    return hit_list


def collision_not_tile(rect, object_list):
    hit_list = []
    for obj in object_list:
        if rect.colliderect(obj.rect):
            hit_list.append(obj)
    return hit_list


def move_with_collisions(entity, movement, tiles, platforms, sprites):
    # we can treat platforms and tiles as same collision type
    collision_types = {'top': False, 'bottom': False,
                       'right': False, 'left': False, 'bottom-platform': False}
    # check if desired movement is collision
    entity.rect.x += movement[0]

    # first we check X axis collisions
    # x collision with tile objects
    hit_list = collision_tile(entity.rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            entity.rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            entity.rect.left = tile.right
            collision_types['left'] = True
        if entity.entity_id == 1:
            entity.direction *= -1

    # x collision for platforms
    hit_list = collision_not_tile(entity.rect, platforms)
    for platform in hit_list:
        if movement[0] > 0:
            entity.rect.right = platform.rect.left
            collision_types['right'] = True
        elif movement[0] < 0:
            entity.rect.left = platform.rect.right
            collision_types['left'] = True
    # if entity is player
    if entity.entity_id == 0:
        # x collision with sprites
        hit_list = collision_not_tile(entity.rect, sprites)
        if len(hit_list):
            entity.hurt()

    # checking collisions for Y axis
    entity.rect.y += movement[1]

    # y collision with tile objects
    hit_list = collision_tile(entity.rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            entity.rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            entity.rect.top = tile.bottom
            collision_types['top'] = True

     # y collision with platforms
    hit_list = collision_not_tile(entity.rect, platforms)
    on_platform = None
    for platform in hit_list:
        if abs((entity.rect.bottom) - platform.rect.top) <= entity.collision_treshold:
            if platform.move_x:
                entity.rect.bottom = platform.rect.top
            else:
                entity.rect.bottom = platform.rect.top - 1
            collision_types['bottom-platform'] = True
            on_platform = platform
        elif abs((entity.rect.top) - platform.rect.bottom) <= entity.collision_treshold:
            entity.rect.top = platform.rect.bottom + platform.speed + 1
            collision_types['top'] = True

    # y collision with sprites
    hit_list = collision_not_tile(entity.rect, sprites)
    for sprite in hit_list:
        if abs((entity.rect.bottom) - sprite.rect.top) <= entity.collision_treshold:
            sprite.kill()
        elif abs((entity.rect.top) - sprite.rect.bottom) <= entity.collision_treshold:
            entity.hurt()

    return entity.rect, collision_types, on_platform
