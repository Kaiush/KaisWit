#Upload 177

import datetime
import os
import random
import shutil
import sys

from graphviz import Digraph


def init():
    path_to_wit = os.path.join(os.getcwd(), '.wit')
    if not os.path.exists(path_to_wit):
        os.makedirs(path_to_wit)
    images = os.path.join(path_to_wit, 'images')
    staging = os.path.join(path_to_wit, "staging_area")
    if not os.path.exists(images):
        os.makedirs(images)
    if not os.path.exists(staging):
        os.makedirs(staging)
    with open(os.path.join(path_to_wit, 'references.txt'), 'w') as open_references:
        open_references.write('HEAD=None\nmaster=None')
    with open(os.path.join(path_to_wit, 'activated.txt'), 'w') as open_activated:
        open_activated.write('master')


def add():
    filename = sys.argv[2]
    path_to_cwd = os.getcwd()
    path_to_list = os.path.split(path_to_cwd)
    filename_list = os.path.split(filename)
    if filename_list[0] == '':
        filename_list = filename_list[1:]
    if filename_list[0].startswith('C:'):
        filename_list = filename_list[len(path_to_list):]
        filename = os.path.join(filename_list)
    dir_to_wit = find_nearest_wit(path_to_cwd)
    dir_to_staging = os.path.join(dir_to_wit, "staging_area")
    dir_to_father_file = os.path.dirname(dir_to_wit)
    gwd_list = (os.getcwd()).split(os.sep)
    list_father_file = dir_to_father_file.split(os.sep)
    if len(gwd_list) > len(list_father_file):
        for index in range(len(list_father_file), len(gwd_list)):
            dir_to_staging = os.path.join(dir_to_staging, gwd_list[index])
            if not os.path.isdir(dir_to_staging):
                os.makedirs(dir_to_staging)
    while len(filename_list) > 1:
        if filename_list[0] in os.listdir(path_to_cwd):
            if filename_list[0] not in os.listdir(dir_to_staging):
                dir_to_staging = os.path.join(dir_to_staging, filename_list[0])
                if not os.path.exists(dir_to_staging):
                    os.makedirs(dir_to_staging)
            else:
                dir_to_staging = os.path.join(dir_to_staging, filename_list[0])
            path_to_cwd += os.path.join(path_to_cwd, filename_list[0])
            filename_list = filename_list[1:]
    file_path = os.path.join(path_to_cwd, filename_list[0])
    print("-----------")
    print(file_path)
    print(os.path.join(dir_to_staging, os.path.split(file_path)[-1]))
    print("-----------")
    if os.path.isfile(file_path):
        if os.path.exists(os.path.join(dir_to_staging, os.path.split(file_path)[-1])):
            os.remove(os.path.join(dir_to_staging, file_path))
        shutil.copy2(file_path, dir_to_staging)
    elif os.path.isdir(file_path):
        if os.path.exists(os.path.join(dir_to_staging, os.path.split(file_path)[-1])):
            shutil.rmtree(os.path.join(dir_to_staging, os.path.split(file_path)[-1]))
        shutil.copytree(file_path, os.path.join(dir_to_staging, os.path.split(file_path)[-1]))


def find_nearest_wit(path):
    if isinstance(path, list):
        path = os.path.join(*path)
    foundWit = False
    while len(path) > 3 and not foundWit:
        if '.wit' in os.listdir(path):
            dir_to_wit = os.path.join(path, ".wit")
            foundWit = True
        path = os.path.dirname(path)
    if foundWit:
        return dir_to_wit
    else:
        raise FileNotFoundError("wit folder not found")   


def files_in_folder(file_path):
    files_list = []
    if os.path.exists(file_path):
        for folder_or_file in os.listdir(file_path):
            if os.path.isfile(os.path.join(file_path, folder_or_file)):
                files_list.append(os.path.join(file_path, folder_or_file))
            elif os.path.isdir(os.path.join(file_path, folder_or_file)):
                files_list.extend(files_in_folder(os.path.join(file_path, folder_or_file)))
    return files_list
    

def commit_id_generator():
    letters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    commit_id = ''.join(random.choices(letters, k=40))
    return commit_id


def get_previous_commit_id(path_to_references=None):
    if path_to_references is None:
        path_to_references = os.path.join(find_nearest_wit(os.getcwd()), 'references.txt')
    if os.path.isfile(path_to_references):
        with open(path_to_references, 'r') as open_references:
            return open_references.readlines()[0].split('=')[1].strip('\n').strip(' ')
    else:
        return None


def commit():
    path_to_wit = find_nearest_wit(os.getcwd())
    commit_id = commit_id_generator()
    path_to_images = os.path.join(path_to_wit, "images")
    path_to_references = os.path.join(path_to_wit, "references.txt")
    with open(os.path.join(path_to_wit, 'activated.txt')) as open_activated:
        active_branch = open_activated.read()
    os.makedirs(os.path.join(path_to_images, commit_id))
    previous_commit = get_previous_commit_id()
    if len(sys.argv) < 3:
        message = 'No message'
    else:
        message = sys.argv[2]
    with open(os.path.join(path_to_images, commit_id + ".txt"), "w") as open_file:
        open_file.write(f"parent={previous_commit}\ndate=" + str(datetime.datetime.now()) + "\nmessage=" + message)
    path_to_staging_area = os.path.join(path_to_wit, "staging_area")
    path_to_current_commit = os.path.join(path_to_images, commit_id)
    for afile in os.listdir(path_to_staging_area):
        path_to_afile = os.path.join(path_to_staging_area, afile)
        if os.path.isfile(path_to_afile):
            shutil.copy2(path_to_afile, path_to_current_commit)
        elif os.path.isdir(path_to_afile):
            shutil.copytree(path_to_afile, os.path.join(path_to_current_commit, afile))
    text_for_references = f'HEAD={commit_id}'
    with open(path_to_references, 'r+') as open_references:
        branches = open_references.readlines()[1:]
        open_references.seek(0)
        for index in range(len(branches)):
            if branches[index].split('=')[0] == active_branch:
                branches[index] = f"{active_branch}={commit_id}\n"
                print("UPDATED!")
        text_for_references += '\n' + ''.join(branches)
        open_references.write(text_for_references)


def finder_changes_to_be_commited(path_to_wit):
    changes_to_be_committed = []
    path_to_staging_area = os.path.join(path_to_wit, "staging_area")
    path_to_images = os.path.join(path_to_wit, 'images')
    previous_commit = get_previous_commit_id()
    if path_to_wit is None:
        raise OSError("No wit folder was found, please use init first.")
    previous_commit = get_previous_commit_id()
    files_in_staging = files_in_folder(path_to_staging_area)
    for afile in files_in_staging:
        files_name = os.path.split(afile)[1]
        afile_from_staging = afile.split('staging_area')[-1].strip('\\')
        path_to_backup_file = os.path.join(path_to_images, previous_commit, os.path.join(afile_from_staging))
        if os.path.exists(path_to_backup_file):
            if os.path.getmtime(afile) != os.path.getmtime(path_to_backup_file):
                changes_to_be_committed.append(files_name)
        else:
            changes_to_be_committed.append(files_name)
    return changes_to_be_committed


def status():
    path_to_wit = find_nearest_wit(os.getcwd())
    changes_to_be_committed = finder_changes_to_be_commited(path_to_wit)
    changes_not_staged_for_commit = finder_changes_not_staged_for_commit(path_to_wit)
    untracked_files = finder_untracked_files(path_to_wit)
    if path_to_wit is None:
        raise OSError("No wit folder was found, please use init first.")
    print(f"Changes_to_be_committed: {changes_to_be_committed}")
    print(f"Changes_not_staged_for_commit: {changes_not_staged_for_commit}")
    print(f"Untracked_files: {untracked_files}")


def finder_changes_not_staged_for_commit(path_to_wit):
    changes_not_staged_for_commit = []
    path_to_staging_area = os.path.join(path_to_wit, "staging_area")
    files_in_staging = files_in_folder(path_to_staging_area)
    for afile in files_in_staging:
        files_name = os.path.split(afile)[1]
        afile_from_staging = afile.split('staging_area')[-1].strip('\\')
        path_to_real_file = os.path.join(os.path.dirname(path_to_wit), afile_from_staging)
        if os.path.exists(path_to_real_file):
            if os.path.getmtime(afile) != os.path.getmtime(path_to_real_file):
                print("APPENDING!")
                changes_not_staged_for_commit.append(files_name)
    return changes_not_staged_for_commit


def finder_untracked_files(path_to_wit):
    untracked_files = []
    path_to_staging_area = os.path.join(path_to_wit, "staging_area")
    files_in_parent_folder = [afile for afile in files_in_folder(os.path.dirname(path_to_wit)) if '.wit' not in afile]
    partial_files_path = []
    len_of_parent_folder = len(os.path.dirname(path_to_wit).split(os.sep))
    for afile in files_in_parent_folder:
        partial_files_path.append(os.sep.join(afile.split(os.sep)[len_of_parent_folder:]))
    for apart in partial_files_path:
        files_path_in_staging = os.path.join(path_to_staging_area, apart)
        if not os.path.exists(files_path_in_staging):
            filename = os.path.split(apart)[1]
            untracked_files.append(filename)
    return untracked_files


def checkout():
    path_to_wit = find_nearest_wit(os.getcwd())
    if len(finder_changes_to_be_commited(path_to_wit)) > 0 or len(finder_changes_not_staged_for_commit(path_to_wit)):
        raise OSError('Folder is not ready for checkout!')
    commit_id_to_open, active_branch = sys.argv[2], sys.argv[2]
    path_to_activated = os.path.join(path_to_wit, 'activated.txt')
    if len(commit_id_to_open) > 30:
        active_branch = 'master'
    with open(os.path.join(path_to_wit, "references.txt"), 'r') as open_references:
        references_lines = open_references.readlines()
    for line in references_lines:
        if active_branch in line:
            commit_id_to_open = line.split('=')[1].strip('\n')
    with open(path_to_activated, 'w') as open_activated:
        print('CHANGING ACTIVE BRANCH!!')
        open_activated.write(active_branch)
    path_to_staging_area = os.path.join(path_to_wit, 'staging_area')
    if path_to_wit is None:
        raise OSError("No wit folder was found, please use init first.")
    path_to_commit = os.path.join(path_to_wit, "images", commit_id_to_open.strip('\n'))
    path_to_real_folder = os.path.dirname(path_to_wit)
    files_in_commit = files_in_folder(path_to_commit)
    paths_of_load_files = []
    for afile in files_in_commit:
        afile_from_commit = afile.split(commit_id_to_open)[-1].strip('\\')
        paths_of_load_files.append(os.path.join(path_to_real_folder, afile_from_commit))
    for index in range(len(paths_of_load_files)):
        if os.path.exists(paths_of_load_files[index]):
            os.remove(paths_of_load_files[index])
        paths_of_load_files[index] = os.path.dirname(paths_of_load_files[index])
        if not os.path.exists(paths_of_load_files[index]):
            os.makedirs(paths_of_load_files[index])
        print(f"----\n{files_in_commit[index]}\n{paths_of_load_files[index]}\n----")
        shutil.copy2(files_in_commit[index], paths_of_load_files[index])
    if os.path.exists(path_to_staging_area):
        print("DELETING!!")
        shutil.rmtree(path_to_staging_area)
    shutil.copytree(path_to_commit, path_to_staging_area)
    print("PASTING!")
    path_to_references = os.path.join(path_to_wit, 'references.txt')
    with open(path_to_references, 'r+') as open_references:
        branches = open_references.readlines()[1:]
        open_references.seek(0)
        for index in range(len(branches)):
            if branches[index].split('=')[0] == active_branch:
                branches[index] = f"{active_branch}={commit_id_to_open}\n"
        text_for_references = f"HEAD={commit_id_to_open}\n" + "".join(branches)
        open_references.write(text_for_references)


def graph():
    graph = Digraph(strict=True)
    get_commits(graph, get_previous_commit_id())
    graph.node('head', 'head', shape='plaintext')
    graph.edge('head', get_previous_commit_id())
    graph.view()


def get_commits(graph, commit_id):
    graph.node(commit_id, commit_id, shape='rectangle')
    for parent in get_parent_for_graph(commit_id):
        parent_node = get_commits(graph, parent)
        graph.edge(commit_id, parent_node)
    return commit_id


def get_parent_for_graph(commit_id):
    path_to_wit = find_nearest_wit(os.getcwd())
    with open(os.path.join(path_to_wit, 'images', commit_id + '.txt'), 'r') as open_commit:
        commit_lines = open_commit.readlines()
    parents = commit_lines[0].split('=')[1].strip()
    if parents == 'None':
        return []
    return parents.split(',')
        
    
def branch():
    path_to_wit = find_nearest_wit(os.getcwd())
    branch_name = sys.argv[2]
    path_to_references = os.path.join(path_to_wit, 'references.txt')
    with open(path_to_references, 'r') as open_references:
        current_commit = open_references.readlines()[0].split('=')[1].strip('\n')
    with open(path_to_references, 'a+') as open_references:
        open_references.write(f'{branch_name}={current_commit}\n')
    

def get_all_parents(commit_id):
    path_to_wit = find_nearest_wit(os.getcwd())
    path_to_images = os.path.join(path_to_wit, 'images')
    path_to_commitxt = os.path.join(path_to_images, commit_id + '.txt')
    commit_herritage_list = []
    reached_last_parent = False
    reached_merge = False
    while not reached_last_parent and not reached_merge:
        if ',' in path_to_commitxt:
            reached_merge = True
            two_parents = [path_to_commitxt.split(',')[0], path_to_commitxt.split(',')[1]]
        if commit_id.startswith('None') or not os.path.exists(path_to_commitxt):
            reached_last_parent = True
        else:
            commit_herritage_list.append(path_to_commitxt)
            with open(path_to_commitxt, 'r') as open_commitxt:
                list_commitxt = open_commitxt.readlines()
            commit_id = list_commitxt[0].split('=')[1].strip('\n')
            path_to_commitxt = os.path.join(path_to_images, commit_id + '.txt')
    if reached_merge:
        commit_herritage_list.extend(get_all_parents(two_parents[0])).extend(two_parents[1])
    else:
        return commit_herritage_list


def merge():
    if len(sys.argv) > 2:
        branch_to_merge = sys.argv[2]
    path_to_wit = find_nearest_wit(os.getcwd())
    first_commit = get_previous_commit_id()
    with open(os.path.join(path_to_wit, 'references.txt')) as open_references:
        lines_of_references = open_references.readlines()
    for line in lines_of_references:
        branch_name = line.split('=')[0]
        if branch_name == branch_to_merge:
            second_commit = line.split('=')[1].strip('\n')
    new_commit = commit_id_generator()
    path_to_new_commit = os.path.join(path_to_wit, 'images', new_commit)
    update_folder(first_commit, new_commit)
    update_folder(second_commit, new_commit)
    path_to_staging = os.path.join(path_to_wit, 'staging_area')
    shutil.rmtree(path_to_staging)
    shutil.copytree(path_to_new_commit, path_to_staging)
    text_to_commit = f"parent={first_commit},{second_commit}\ndate=" + str(datetime.datetime.now()) + "\nmessage=Merged"
    with open(path_to_new_commit + '.txt', 'w') as open_commitxt:
        open_commitxt.write(text_to_commit)
    with open(os.path.join(path_to_wit, 'activated.txt'), 'r+') as open_activated:
        active_branch = open_activated.read()
    with open(os.path.join(path_to_wit, 'references.txt'), 'r+') as open_references:
        references_lines = open_references.readlines()
        open_references.seek(0)
        for index in range(len(references_lines)):
            if references_lines[index].split('=')[0] == 'HEAD':
                print("UPDATING HEAD!")
                references_lines[index] = f'HEAD={new_commit}\n'
            elif references_lines[index].split('=')[0] == active_branch:
                print("UPDATING BRANCH!")
                references_lines[index] = f'{active_branch}={new_commit}\n'
        open_references.write(''.join(references_lines))               


def update_folder(commit_from, commit_to):
    path_to_wit = find_nearest_wit(os.getcwd())
    path_to_commit_from = os.path.join(path_to_wit, 'images', commit_from)
    files_in_commit_from = files_in_folder(path_to_commit_from)
    path_to_commit_to = os.path.join(path_to_wit, 'images', commit_to)
    partial_paths_in_commit_from = [apath.split(commit_from)[-1].strip('\\') for apath in files_in_commit_from]
    if not os.path.exists(path_to_commit_to):
        os.makedirs(path_to_commit_to)
    for index in range(len(files_in_commit_from)):
        print("COPYING")
        print(files_in_commit_from[index])
        file_in_new_dir = os.path.join(path_to_commit_to, partial_paths_in_commit_from[index])
        dir_to_copy_to = os.path.split(file_in_new_dir)[0]
        if not os.path.exists(dir_to_copy_to):
            os.makedirs(dir_to_copy_to)
        if not os.path.exists(file_in_new_dir):
            shutil.copy2(files_in_commit_from[index], dir_to_copy_to)


if len(sys.argv) > 1:
    if sys.argv[1] == 'init':
        init()
    elif sys.argv[1] == 'add':
        add()
    elif sys.argv[1] == 'commit':
        commit()
    elif sys.argv[1] == 'status':
        status()
    elif sys.argv[1] == 'checkout':
        checkout()
    elif sys.argv[1] == 'graph':
        graph()
    elif sys.argv[1] == 'branch':
        branch()
    elif sys.argv[1] == 'merge':
        merge()