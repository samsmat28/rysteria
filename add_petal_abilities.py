with open("Server/System/PetalBehavior.c", "r", encoding="utf-8") as f:
    pb = f.read()

target = 'if (data->id == rr_petal_id_leaf)'
abilities = """if (data->id == rr_petal_id_tail)
            physical->acceleration_scale *= 1.15f;
        if (data->id == rr_petal_id_sail)
            to_rotate += 0.035f;
        if (data->id == rr_petal_id_plate || data->id == rr_petal_id_scale)
            health->damage_reduction_ratio += 0.08f;
        if (data->id == rr_petal_id_crown || data->id == rr_petal_id_relic)
        {
            player_info->modifiers.reload_speed *= 1.18f;
            player_info->modifiers.drop_pickup_radius += 40.0f;
            physical->acceleration_scale *= 1.10f;
        }
        """ + target

assert target in pb, "Не найден if (data->id == rr_petal_id_leaf) в PetalBehavior.c"
if "rr_petal_id_tail" not in pb:
    pb = pb.replace(target, abilities, 1)

cp_target = "player_info->client->checkpoint_y = flower_physical->y;"
cp_notify = cp_target + """
                if (simulation->animation_length < RR_MAX_ANIMATION_COUNT) {
                    struct rr_animation *anim = &simulation->animations[simulation->animation_length++];
                    memset(anim, 0, sizeof(*anim));
                    anim->type = rr_animation_type_chat;
                    strcpy(anim->name, "[Checkpoint]");
                    strcpy(anim->message, "New zone progress saved!");
                }"""

if "New zone progress saved!" not in pb and cp_target in pb:
    pb = pb.replace(cp_target, cp_notify, 1)

with open("Server/System/PetalBehavior.c", "w", encoding="utf-8") as f:
    f.write(pb)
print("Уникальные способности новых лепестков и уведомления о чекпоинте добавлены!")
