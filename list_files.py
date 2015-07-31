import os
import sys
import shutil

# basic information about a file
class music_file:
   def __init__(self, removal, fileloc):
        self.removal = removal
        self.fileloc = fileloc
        self.stripped = self.fileloc[len(removal)+1:]

# a bit more information for copying
class missing_music_file:
   def __init__(self, source_removal, destination_removal, source_fileloc, stripped):
       self.source_removal = source_removal
       self.destination_removal = destination_removal
       self.source_fileloc = source_fileloc
       self.stripped = stripped

# what lives in this directory
def walk_files(location):
    retval = []
    print('generating list of backup files in {0}....'.format(location))
    for path, dirs, files in os.walk(location):
        for file in files:
            f = music_file(location, os.path.join(path, file))
            retval.append(f)
    return retval

# what's in the first but not in the second?
def find_missing_files(first, second):
    print('generating list of files missing in {0}...'.format(second[0].removal))
    retval = []
    for f in first:
        found = False
        for g in second:
           if f.stripped == g.stripped:
               found = True
               break
        if not found:
            missing_file = missing_music_file(f.removal, second[0].removal, f.fileloc, f.stripped)
            retval.append(missing_file)
    return retval

def obtain_base_dir(file):
    subdivision = file.split('\\')[0]
    if subdivision == file:
       return ''
    return subdivision

def establish_directory_tree_to_file(directory, file):
    if os.path.exists(file):
        return True
    if not os.path.exists(directory):
        return False
    stripped_new_dir = obtain_base_dir(file)
    if stripped_new_dir == '':
        return True
    dir_to_create = os.path.join(directory, stripped_new_dir)
    if not os.path.exists(dir_to_create):
        print('Directory   {0} does not exist, creating'.format(dir_to_create))
	os.mkdir(dir_to_create)
    adjusted_file = file[len(stripped_new_dir)+1:]
    return establish_directory_tree_to_file(dir_to_create, adjusted_file);
    
def copy_missing_file(missing_file):
    if establish_directory_tree_to_file(missing_file.destination_removal, missing_file.stripped):
        dest_file = os.path.join(missing_file.destination_removal, missing_file.stripped)
	if not os.path.exists(dest_file):
	    print('  copying TO {0}'.format(dest_file))
	    shutil.copyfile(missing_file.source_fileloc, dest_file)

##################### MAIN PROGRAM CODE###################

print("\nGreetings. Welcome to a quick and dirty itunes library merger.\n")

# establish defaults
current_file_dir = "c:\music\itunes\music"
backup_file_dir = "f:\itunes-backup\itunes-backup"

# read command line parameters, or not
argcount = len(sys.argv)
if not argcount == 3:
    print("Unable to determine source directory and backup directory, using defaults:")
else:
    print("Using passed arguments:");
    current_file_dir = sys.argv[1]
    backup_file_dir = sys.argv[2]

# announce usage
print('    current_file_dir = {0}'.format(current_file_dir))
print('    backup_file_dir = {0}\n'.format(backup_file_dir))

# generate filelists
backup_filelist = walk_files(backup_file_dir)
current_filelist = walk_files(current_file_dir)

# see what is missing
files_missing_in_backup = find_missing_files(current_filelist, backup_filelist) 
missing_file_count = len(files_missing_in_backup)
print ('\nThere are {0} files missing in the backup.\n\n'.format(missing_file_count))

if missing_file_count:
  for file in files_missing_in_backup:
     print(file.stripped)
#    copy_missing_file(file)
#else:
#  print("THERE'S NOTHING TO DO, YOU LUNATIC!")
