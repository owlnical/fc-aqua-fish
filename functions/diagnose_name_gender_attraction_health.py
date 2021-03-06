
import arcade


def diagnose_name_gender_attraction_health(fish_list, info_list):
    # Funtions som skriver ut fiskarnas status
    # Informationen ligger lagrad i "info_list"
    if len(info_list) < len(fish_list):
        list_length = len(info_list)
    else:
        list_length = len(fish_list)
    for i in range(list_length):
        x = fish_list[i].center_x
        y = fish_list[i].center_y
        arcade.draw_text(str(info_list[i][0]) + " " + str(info_list[i][1]), x, y + 24, arcade.color.BLACK, 18)
        arcade.draw_text(str(info_list[i][2]), x, y, arcade.color.BLACK, 18)
        arcade.draw_text(str(info_list[i][3]), x, y, arcade.color.BLACK, 18, anchor_x="left", anchor_y="top")
