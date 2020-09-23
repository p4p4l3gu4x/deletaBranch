#!/usr/bin/python3

from subprocess import check_output
from distutils.util import strtobool
from six.moves import input
import sys, getopt
import re


def listBranches(directory):
    raw_results = check_output('cd '+directory+'; git fetch --all -p', shell=True).decode('utf-8')
    raw_results = check_output('cd '+directory+'; git branch -r --merged', shell=True).decode('utf-8')
    listOfBranches = []
    for b in raw_results.split('\n'):
        if(b != ""):
            branch_name = b.split("/")[1]
            listOfBranches.append(branch_name)
    return listOfBranches

def filterBranches(customList, listOfBranches):
    listNonUsables = ['master']
    listNonUsables = listNonUsables + customList
    listFiltered = []
    for b in listOfBranches:
        if(b not in listNonUsables):
            listFiltered.append(b)
    return listFiltered

def confirmDelete(itemName, type):
    question = "Confirm delete " + type + " '"+ itemName + "'[y/n]: "
    user_input = input(question).lower()
    try:
        return bool(strtobool(user_input))
    except ValueError:
        print("Please use y/n.")
        confirmDelete(itemName, type)

def deleteBranch(branch):
    print ("Deleting remote branch '" + branch+ "'")
    try:
        response = check_output('git push origin --delete '+ branch, shell=True).strip()
        print ("Remote branch '" + branch+ "' deleted.")
        return response
    except ValueError:
        print ("Error to delete remote branch '" + branch+ "'.")
        return False;
    
def deleteBranches(listOfBranches):
    for branch in listOfBranches:
        if(confirmDelete(branch, "branch")):
            deleteBranch(branch)
        else:
            print("Branch '" +  branch + "' not deleted.")

def listTags(directory):
    print('List of tags')
    raw_results = check_output('cd '+directory+'; git fetch --tags -p', shell=True).decode('utf-8')
    raw_results = check_output('cd '+directory+'; git ls-remote --tags origin', shell=True).decode('utf-8')
    listOfTags = []
    for l in raw_results.split("\n"):
        if(l != ""):
            t = l.split("/")
            listOfTags.append(t[2])
    return listOfTags

def filterTags(filter, listOfTags):
    print('Filter Tags - ' + filter )
    p = re.compile('^' + filter + '$')
    listOfTagsFiltered = []
    if(filter == ""):
        listOfTagsFiltered = listOfTags
    else:
        for tag in listOfTags:
            if p.match(tag):
                listOfTagsFiltered.append(tag)
                
    return listOfTagsFiltered

def deleteTag(tagName):
    print ("Deleting remote tag '" + tagName+ "'")
    try:
        response = check_output('git push origin --delete '+ tagName, shell=True).strip()
        print ("Remote tag '" + tagName+ "' deleted.")
        return response
    except ValueError:
        print ("Error to delete remote tag '" + tagName+ "'.")
        return False;

def deleteTags(listOfTags):
    for tag in listOfTags:
        if(confirmDelete(tag, "tag")):
            deleteTag(tag)
        else:
            print("Tag '" +  tag + "' not deleted.")

def main(argv):
    gitRepoDirectory =  ""
    customList = []
    tags = False
    tagFilter = ""
    try:
      opts, args = getopt.getopt(argv, "d:b:", ["tags="])
    except getopt.GetoptError:
      print ('branch_delete -d <gitRepoDirectory> -b <listBranchesNotDelete> --tags=<regexFilter>')
      sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d"):
            gitRepoDirectory = arg
        if opt in ("-b"):
            for item in arg.split(','):
                customList.append(item.strip())
        if opt in ("--tags"):
            tags = True
            if(arg != ""):
                tagFilter = arg
    if(gitRepoDirectory == ""):
        print ('branch_delete -d <gitRepoDirectory> -b <listBranchesNotDelete> --tags=<regexFilter>')
        sys.exit(2)
    listOfBranches = listBranches(gitRepoDirectory)
    listOfBranches = filterBranches(customList, listOfBranches)
    listOfBranches.sort()
    print("Found '", len(listOfBranches), "' branches to delete")
    deleteBranches(listOfBranches)
    if tags:
        listOfTags = listTags(gitRepoDirectory)
        listOfTags = filterTags(tagFilter, listOfTags)
        listOfTags.sort()
        print("Found '", len(listOfTags), "' Tags to delete.")
        deleteTags(listOfTags)

if __name__ == '__main__':
    main(sys.argv[1:]);