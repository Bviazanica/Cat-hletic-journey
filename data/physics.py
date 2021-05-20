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

def apply_gravitation(current_vel, GRAVITY, tick, GRAVITY_FORCE_LIMIT):
    current_vel += GRAVITY * tick
    if current_vel > GRAVITY_FORCE_LIMIT:
        current_vel = GRAVITY_FORCE_LIMIT
    return current_vel

def move_with_collisions(entity, movement, tiles, platforms, sprites, invisible_blocks, item_boxes):
    # we can treat platforms and tiles as same collision type
    collision_types = {'top': False, 'bottom': False, 
                       'right': False, 'left': False, 'bottom-platform': False, 'invisible-block-top': False ,'item-box-top': False}
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

    hit_list = collision_not_tile(entity.rect, item_boxes)
    for box in hit_list:
        if movement[0] > 0:
            entity.rect.right = box.rect.left
            collision_types['right'] = True
        elif movement[0] < 0:
            entity.rect.left = box.rect.right
            collision_types['left'] = True

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
        for sprite in hit_list:
            if sprite.alive and not sprite.in_death_animation and not entity.invulnerability:
                entity.hurt(False, 'sprite')

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

    # y collision with invisible blocks
    hit_list = collision_not_tile(entity.rect, invisible_blocks)
    for block in hit_list:
        if movement[1] < 0:
            entity.rect.top = block.rect.bottom
            block.visible = True
            collision_types['invisible-block-top'] = True

    hit_list = collision_not_tile(entity.rect, item_boxes)
    for box in hit_list:
        if movement[1] < 0:
            entity.rect.top = box.rect.bottom
            if entity.entity_id == 0:
                box.hits_to_break -= 1
                box.new_state = True
            collision_types['item-box-top'] = True
            
        elif movement[1] > 0:
            entity.rect.bottom = box.rect.top
            collision_types['bottom'] = True
    # y collision with platforms
    hit_list = collision_not_tile(entity.rect, platforms)
    for platform in hit_list:
        if abs((entity.rect.bottom) - platform.rect.top) <= entity.collision_treshold:
            if platform.move_x or (platform.move_x == False and platform.move_y == False):
                entity.rect.bottom = platform.rect.top
            elif platform.move_y:
                entity.rect.bottom = platform.rect.top - 1
            collision_types['bottom-platform'] = True
        elif abs((entity.rect.top) - platform.rect.bottom) <= entity.collision_treshold:
            entity.rect.top = platform.rect.bottom  + 1
            collision_types['top'] = True

    # y collision with sprites
    if entity.entity_id == 0:
        hit_list = collision_not_tile(entity.rect, sprites)
        for sprite in hit_list:
            if sprite.in_death_animation == False and sprite.alive:
                if abs((entity.rect.bottom) - sprite.rect.top) <= entity.collision_treshold:
                    if sprite.entity_id == 2:
                        entity.hurt(False)
                    else:
                        sprite.in_death_animation = True
                elif abs((entity.rect.top) - sprite.rect.bottom) <= entity.collision_treshold and not entity.invulnerability:
                    entity.hurt(False)

       


    return entity.rect, collision_types
