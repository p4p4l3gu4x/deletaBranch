#!/usr/bin/python3

from subprocess import check_output
import sys, getopt
from distutils.util import strtobool
from six.moves import input

def listBranches(directory):
    raw_results = check_output('cd '+directory+'; git branch -r', shell=True).decode('utf-8')
    listOfBranches = []
    for b in raw_results.split('\n'):
        if(b != ""):
            branch_name = b.split("/")[1]
            listOfBranches.append(branch_name)
    return listOfBranches

def filter(customList, listOfBranches):
    listNonUsables = ['master']
    listNonUsables = listNonUsables + customList
    listFiltered = []
    for b in listOfBranches:
        if(b not in listNonUsables):
            listFiltered.append(b)
    return listFiltered

def confirmDelete(branchName):
    question = "Confirm delete branch '"+ branchName + "[y/n]': "
    user_input = input(question).lower()
    try:
        return bool(strtobool(user_input))
    except ValueError:
        print("Please use y/n.")
        confirmDelete(branchName)

def delete_branch(branch):
    print ("Deleting remote branch '" + branch+ "'")
    return check_output('git branch -D '+ branch, shell=True).strip()

def deleteBranches(listOfBranches):
    for branch in listOfBranches:
        if(confirmDelete(branch)):
            delete_branch(branch)
        else:
            print("Branch '", branch, "' not deleted")

def main(argv):
    gitRepoDirectory =  ""
    customList = []
    try:
      opts, args = getopt.getopt(argv,"d:b:")
    except getopt.GetoptError:
      print ('branch_delete -d <gitRepoDirectory> -b <listBranchesNotDelete>')
      sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d"):
            gitRepoDirectory = arg
        if opt in ("-b"):
            for item in arg.split(','):
                customList.append(item.strip())
            
    if(gitRepoDirectory == ""):
        print ('branch_delete -d <gitRepoDirectory> -b <listBranchesNotDelete>')
        sys.exit(2)

    listOfBranches = listBranches(gitRepoDirectory)
    listOfBranches = filter(customList, listOfBranches)
    listOfBranches.sort()
    print("Found '", len(listOfBranches), "' branches to delete")
    deleteBranches(listOfBranches)

if __name__ == '__main__':
    main(sys.argv[1:]);