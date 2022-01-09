from os import path
# ======================================================================================================================
# root =================================================================================================================
root = path.dirname(__file__)
# ======================================================================================================================
# Uygulama Bilgileri ===================================================================================================
app_name = "Sahra - Sanal Asistan"
app_version = "0.33.25.6"
app_version_type = "Dizüstü Sürüm"
app_author = "Onur Erikçi"
app_author_contact = "onurerikci@yaani.com"
app_logo = path.join(root, 'assets\\visuals\\128\\Sahra.ico')
tray_logo = path.join(root, 'assets\\visuals\\32\\Sahra.ico')
app_release_notes_location = path.join(root, 'assets\\release_notes\\release_notes.shr')
# ======================================================================================================================
# İkonlar ==============================================================================================================
command_sahara_icon = path.join(root, 'assets\\visuals\\16\\command_sahara.ico')
show_functions_icon = path.join(root, 'assets\\visuals\\16\\show_functions.ico')
edit_commands_icon = path.join(root, 'assets\\visuals\\16\\edit_commands.ico')
application_usage_tracker_icon = path.join(root, 'assets\\visuals\\16\\application_usage_tracker.ico')
release_notes_icon = path.join(root, 'assets\\visuals\\16\\release_notes.ico')
about_icon = path.join(root, 'assets\\visuals\\16\\about.ico')
exit_icon = path.join(root, 'assets\\visuals\\16\\exit.ico')
screenshot_icon = path.join(root, 'assets\\visuals\\16\\screenshot.ico')
brightness_icon = path.join(root, 'assets\\visuals\\16\\brightness.ico')
power_icon = path.join(root, 'assets\\visuals\\16\\power.ico')
confirmation_icon = path.join(root, 'assets\\visuals\\16\\confirmation.ico')
volume_icon = path.join(root, 'assets\\visuals\\16\\volume.ico')
application_usage_watch_icon = path.join(root, 'assets\\visuals\\16\\application_usage_watch.ico')
application_usage_show_icon = path.join(root, 'assets\\visuals\\16\\application_usage_show.ico')
take_a_screenshot_icon = path.join(root, 'assets\\visuals\\16\\take_a_screenshot.ico')
screenshot_folder_icon = path.join(root, 'assets\\visuals\\16\\screenshot_folder.ico')
brightness_hundred_icon = path.join(root, 'assets\\visuals\\16\\brightness_hundred.ico')
brightness_zero_icon = path.join(root, 'assets\\visuals\\16\\brightness_zero.ico')
shutdown_self_icon = path.join(root, 'assets\\visuals\\16\\shutdown_self.ico')
restart_icon = path.join(root, 'assets\\visuals\\16\\restart.ico')
suspend_icon = path.join(root, 'assets\\visuals\\16\\suspend.ico')
lock_icon = path.join(root, 'assets\\visuals\\16\\lock.ico')
accept_icon = path.join(root, 'assets\\visuals\\16\\accept.ico')
deny_icon = path.join(root, 'assets\\visuals\\16\\deny.ico')
volume_fifty_icon = path.join(root, 'assets\\visuals\\16\\volume_fifty.ico')
volume_zero_icon = path.join(root, 'assets\\visuals\\16\\volume_zero.ico')
volume_mute_icon = path.join(root, 'assets\\visuals\\16\\volume_mute.ico')
backup_icon = path.join(root, 'assets\\visuals\\16\\backup.ico')
command_sahara_icon64 = path.join(root, 'assets\\visuals\\64\\command_sahara.ico')
listening_start_icon64 = path.join(root, 'assets\\visuals\\64\\listening_start.ico')
listening_stop_icon64 = path.join(root, 'assets\\visuals\\64\\listening_stop.ico')
i_dont_understand_icon64 = path.join(root, 'assets\\visuals\\64\\i_dont_understand.ico')
unknown_command_icon_64 = path.join(root, 'assets\\visuals\\64\\unknown_command.ico')
connection_lost_icon64 = path.join(root, 'assets\\visuals\\64\\connection_lost.ico')
edit_save_icon64 = path.join(root, 'assets\\visuals\\64\\edit_save.ico')
edit_cancel_icon64 = path.join(root, 'assets\\visuals\\64\\edit_cancel.ico')
accept_icon64 = path.join(root, 'assets\\visuals\\64\\accept.ico')
deny_icon64 = path.join(root, 'assets\\visuals\\64\\deny.ico')
take_a_screenshot_icon64 = path.join(root, 'assets\\visuals\\64\\take_a_screenshot.ico')
screenshot_folder_icon64 = path.join(root, 'assets\\visuals\\64\\screenshot_folder.ico')
are_you_confirm_icon64 = path.join(root, 'assets\\visuals\\64\\are_you_confirm.ico')
brightness_hundred_icon64 = path.join(root, 'assets\\visuals\\64\\brightness_hundred.ico')
brightness_icon64 = path.join(root, 'assets\\visuals\\64\\brightness.ico')
brightness_zero_icon64 = path.join(root, 'assets\\visuals\\64\\brightness_zero.ico')
volume_icon64 = path.join(root, 'assets\\visuals\\64\\volume.ico')
volume_fifty_icon64 = path.join(root, 'assets\\visuals\\64\\volume_fifty.ico')
volume_zero_icon64 = path.join(root, 'assets\\visuals\\64\\volume_zero.ico')
volume_mute_icon64 = path.join(root, 'assets\\visuals\\64\\volume_mute.ico')
walk_icon64 = path.join(root, 'assets\\visuals\\64\\walk.ico')
no_data_icon64 = path.join(root, 'assets\\visuals\\64\\no_data.ico')
# ======================================================================================================================
# Fonksiyon Açıklamaları ===============================================================================================
brightness_functions_location = path.join(root, 'assets\\functions\\brightness_functions\\brightness_functions.shr')
confirmation_functions_location = path.join(root, 'assets\\functions\\confirmation_functions\\confirmation_functions.shr')
power_functions_location = path.join(root, 'assets\\functions\\power_functions\\power_functions.shr')
screenshot_functions_location = path.join(root, 'assets\\functions\\screenshot_functions\\screenshot_functions.shr')
volume_functions_location = path.join(root, 'assets\\functions\\volume_functions\\volume_functions.shr')
# ======================================================================================================================
# Ekran Alıntısı Komutları =============================================================================================
screenshot_location = path.join(root, "assets\\screenshots\\")
take_a_screenshot_location = path.join(root, 'assets\\commands\\screenshot_commands\\take_a_screenshot.shr')
open_screenshots_folder_location = path.join(root, 'assets\\commands\\screenshot_commands\\open_screenshots_folder.shr')
# ======================================================================================================================
# Ekran Parlaklığı Komutları ===========================================================================================
brightness_hundred_location = path.join(root, 'assets\\commands\\brightness_commands\\brightness_hundred.shr')
brightness_fifty_location = path.join(root, 'assets\\commands\\brightness_commands\\brightness_fifty.shr')
brightness_zero_location = path.join(root, 'assets\\commands\\brightness_commands\\brightness_zero.shr')
brightness_up_location = path.join(root, 'assets\\commands\\brightness_commands\\brightness_up.shr')
brightness_down_location = path.join(root, 'assets\\commands\\brightness_commands\\brightness_down.shr')
# ======================================================================================================================
# Güç Komutları ========================================================================================================
lock_windows_location = path.join(root, 'assets\\commands\\power_commands\\lock_windows.shr')
reboot_windows_location = path.join(root, 'assets\\commands\\power_commands\\reboot_windows.shr')
shutdown_windows_location = path.join(root, 'assets\\commands\\power_commands\\shutdown_windows.shr')
suspend_windows_location = path.join(root, 'assets\\commands\\power_commands\\suspend_windows.shr')
shutdown_self_location = path.join(root, 'assets\\commands\\power_commands\\shutdown_self.shr')
# ======================================================================================================================
# Onay Komutları =======================================================================================================
yes_location = path.join(root, 'assets\\commands\\confirmation_commands\\yes.shr')
no_location = path.join(root, 'assets\\commands\\confirmation_commands\\no.shr')
# ======================================================================================================================
# Ses Komutları ========================================================================================================
volume_on_location = path.join(root, 'assets\\commands\\volume_commands\\volume_on.shr')
volume_off_location = path.join(root, 'assets\\commands\\volume_commands\\volume_off.shr')
volume_hundred_location = path.join(root, 'assets\\commands\\volume_commands\\volume_hundred.shr')
volume_fifty_location = path.join(root, 'assets\\commands\\volume_commands\\volume_fifty.shr')
volume_zero_location = path.join(root, 'assets\\commands\\volume_commands\\volume_zero.shr')
volume_up_location = path.join(root, 'assets\\commands\\volume_commands\\volume_up.shr')
volume_down_location = path.join(root, 'assets\\commands\\volume_commands\\volume_down.shr')
# ======================================================================================================================
# Uygulama Kullanımı İzleyici ==========================================================================================
application_usage_tracker_configurations_location = "assets\\configurations\\application_usage_tracker_configurations\\application_usage_tracker.cfg"
application_usage_tracker_databases_location = "assets\\application_usages\\"
# ======================================================================================================================
# ======================================================================================================================