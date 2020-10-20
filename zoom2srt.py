import os, datetime, re
path_to_dir = (input("Enter the path to the recording: ") + '\\').replace("/", "\\")
if path_to_dir.count("\\") < 2:
    print("Path to the directory most likely not valid")
    exit(1)
yes = ["y", "Y", "yes", "YES", "Yes", "1"]
only_questions = input("Do you want to only include questions (messages that include '?') (y/yes/1): ").strip() in yes
ignore_list = []
if not only_questions:
    ignore_list = input("If you want, enter the messages you want to skip, separated by commas: ").split(',')
for index, element in enumerate(ignore_list):
    ignore_list[index] = ignore_list[index].strip()
path = os.path.dirname(path_to_dir)
beginning = path.split('\\')[-1].split(" ")[0]+" "+path.split(" ")[1].replace('.', ':')
beginning = re.compile("([: -])+").split(beginning)
beginning = datetime.datetime(int(beginning[0]), int(beginning[2]), int(beginning[4]), int(beginning[6]), int(beginning[8]), int(beginning[10]))

lines = 0
try:
    f_read = open(path_to_dir+"chat.txt", "r")
    f_write = open(path_to_dir+"zoom_0.srt", "w")
    for line in f_read:
        if len(line.split(':')) > 1:
            temp_text = line.split("From  ")[1]
            if temp_text.split(": ")[1].strip() in ignore_list:
                continue
            if "?" not in temp_text.split(": ")[1].strip() and only_questions:
                continue
            temp_out = ""
            temp_time = line.split("\t")[0].split(":")
            temp_time = datetime.datetime(beginning.year, beginning.month, beginning.day, int(temp_time[0]), int(temp_time[1]), int(temp_time[2]))
            temp_time = temp_time - beginning
            lines += 1
            temp_out += str(lines)
            temp_out += "\n"
            if len(str(temp_time).split(":")[0]) == 1:
                temp_out += '0'
            temp_out += str(temp_time) + ",000"
            temp_out += " --> "
            temp_time += datetime.timedelta(seconds=5)
            if len(str(temp_time).split(":")[0]) == 1:
                temp_out += '0'
            temp_out += str(temp_time) + ",000"
            temp_out += "\n"
            temp_out += temp_text + "\n"
            f_write.write(temp_out)

    print("The subtitles were created successfully!")
    f_read.close()
    f_write.close()
except IOError:
    print("An error occured when handling the files")
    exit(1)