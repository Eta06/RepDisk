import os
import json
import random
import shutil

disk_list = []
new_list = []


# Color class for terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = "\033[31m"


# noinspection PyShadowingNames,PyBroadException
def trycopy(drive_letter, driver_id):
    try:
        driver_id = json.loads(driver_id)
        print(driver_id["driver-id"])
        path = os.getcwd()
        os.mkdir(path + "\\drivebackups\\" + driver_id["driver-id"])
    except FileExistsError:
        print(bcolors.WARNING + lang["folder_already_exists"] + bcolors.ENDC)
    except:
        try:
            path = os.getcwd()
            os.mkdir(path + "\\drivebackups")
            os.mkdir(path + "\\drivebackups\\" + driver_id["driver-id"])

        except:
            print(bcolors.RED + bcolors.BOLD + lang["unknown_error"])
            input(lang["press_any_key"])
            exit()
    # Copy files
    for root, dirs, files in os.walk(drive_letter):
        for file in files:
            source = os.path.join(root, file)
            # noinspection PyUnboundLocalVariable
            target = os.path.join(path + "\\drivebackups\\" + driver_id["driver-id"], file)
            shutil.copy(source, target)


# noinspection PyShadowingNames
def generate_driver_id():
    # This function generates a random driver id.
    ints = [random.randint(0, 9) for _ in range(10)]

    # Generate 10 random letters
    strs = [chr(random.randint(ord("a"), ord("z"))) for _ in range(10)]

    # Merge the lists
    return "".join([str(i) for i in ints] + strs)


# noinspection PyShadowingNames
def get_connected_disks():
    disk_list = []
    for i in range(65, 91):
        letter = chr(i)
        path = letter + ":"
        if os.path.isdir(path):
            disk_list.append(path)
    return disk_list


# noinspection PyShadowingNames
def show_newly_connected_disks(old_list, new_list):
    """
    This function shows newly connected disks.
    Args:
        old_list: The old disk list.
        new_list: The new disk list.
    Returns:
        The newly connected disks.
    """
    new_disks = [disk for disk in new_list if disk not in old_list]
    return new_disks


# noinspection PyAssignmentToLoopOrWithParameter,PyBroadException
def read_or_create_config_file(drive_letter):
    """
    This function reads or creates a config file on the drive.

    Args:
    drive_letter: The drive letter of the drive.

    Returns:
    The config file data.
    """

    file_path = f"{drive_letter}\\repdisk-drive.config"
    try:
        with open(file_path, "r") as f:
            data = f.read()
            if data is None or data is "":
                try:
                    data = {
                        "driver-id": generate_driver_id()
                    }
                    with open(file_path, "w") as f:
                        json.dump(data, f)
                except:
                    print(bcolors.RED+bcolors.BOLD+lang["cant_create_file_on_disk"])
                    print(lang["check_disk_permissions"])
                    input(lang["press_any_key"])
                    exit()
            return data
    except FileNotFoundError:
        try:
            data = {
                "driver-id": generate_driver_id()
            }
            with open(file_path, "w") as f:
                json.dump(data, f)
        except:
            print(bcolors.RED + bcolors.BOLD + lang["cant_create_file_on_disk"])
            print(lang["check_disk_permissions"])
            input(lang["press_any_key"])
            exit()
        return data
    except:
        print(bcolors.RED+bcolors.BOLD+lang["unknown_error"])
        input(lang["press_any_key"])
        exit()


# noinspection PyShadowingNames
def load_language(default_language):
    try:
        with open("appconfig.json", "r") as f:
            config = json.load(f)
        language = config.get("language", default_language)
        try:
            with open(f"lang/{language}.json", "r") as f:
                lang = json.load(f)
        except FileNotFoundError:
            print(lang["cant_load_lang"])
            input(lang["press_any_key"])
            exit()
    except FileNotFoundError:
        language = default_language
        try:
            with open(f"lang/{language}.json", "r") as f:
                lang = json.load(f)
        except FileNotFoundError:
            print(lang["cant_load_lang"])
            input(lang["press_any_key"])
            exit()
    return lang


if __name__ == "__main__":
    default_language = "en"
    lang = load_language(default_language)
    old_disk_list = get_connected_disks()
    print(bcolors.BOLD + bcolors.WARNING + "RepDisk")
    print(f"{bcolors.OKGREEN}{lang['connected_disks']}{bcolors.ENDC}")
    print(bcolors.RED+"--------------")
    print("")
    for i in range(65, 91):
        letter = chr(i)
        path = letter + ":"
        if os.path.isdir(path):
            print(path)
    print("")
    print(bcolors.RED + "--------------" + bcolors.ENDC)
    while True:
        new_disk_list = get_connected_disks()
        new_disks = show_newly_connected_disks(old_disk_list, new_disk_list)
        old_disk_list = new_disk_list
        if new_disks:
            print(bcolors.WARNING + lang["inserted_disk"] + str(new_disks[0]) + bcolors.ENDC)
            driver_id = read_or_create_config_file(new_disks[0])
            trycopy(new_disks[0], driver_id)
