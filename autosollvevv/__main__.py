import sys


#!/bin/python3
import os
import sys
import json
import collections
import argparse

json_directive_names_path = os.path.join("/sw/crusher/ums/ums012/SOLLVE/autosollvevv/json_data/directive_names.json")
json_directive_names_file= open(json_directive_names_path)
dir_names=json.load(json_directive_names_file)

json_env_names_path = os.path.join("/sw/crusher/ums/ums012/SOLLVE/autosollvevv/json_data/runtime_library_names.json")
json_env_names_file= open(json_env_names_path)
env_names=json.load(json_env_names_file)

#print(json_directive_files)
#print()
#print(json_clause_files)
#print()
#print(json_clause_group_files)


#print(len(entiredirlist))
#print(len(json_directive_files))
#print(dir_names[0]["4.5"])
def get_dirlist(omp_ver, dir_names):
    entiredirlist=[]
    for b in range(len(dir_names)):
        if dir_names[b][omp_ver] == 1:
            entiredirlist.append(dir_names[b]["Directive"])
    return(entiredirlist)

def get_envlist(omp_ver, env_names):
    entireenvlist=[]
    for b in range(len(env_names)):
        if env_names[b][omp_ver] == 1:
            entireenvlist.append(env_names[b]["Runtime Library"])
    return(entireenvlist)

def split_prag(prag):
    pragarr= prag.split()
    i=0
    j=0
    sp1=-1
    sp2=-1
    sp3=-1
    sp4=-1
    skp=0
    word=''
    splitprag=[]
    #split pragma into desired parts
    for a in pragarr:
        #check for "("
        if pragarr[i].find('(')>= 0:
            sp1 = pragarr[i].find('(')
            #print("found (")
        #check for ")"
        if pragarr[i].find(')') >= 0:
            sp2 = pragarr[i].find(')')
            #print("found )")
        #check for ":"
        if pragarr[i].find(':') >= 0:
            sp3 = pragarr[i].find(':')
            #print("found :")
        #check for ","
        if pragarr[i].find(',') >= 0:
            sp3 = pragarr[i].find(',')
            #print("found ,")

        stri=pragarr[i]
        #print (stri[-1])
        if sp1 !=-1 or sp2!=-1 or sp3!=-1 or sp4!=-1:
    #        print("in")
            #print ("working string:"+stri)
            # split and add into new array by iterating through each char
            for b in stri:
                if b == '(':
                    if word != '':
                        splitprag.append(word)
                    splitprag.append('(')
                    word=''
                    skp=1
                if b == ')':
                    if word != '':
                        splitprag.append(word)
                    splitprag.append(')')
                    word=''
                    skp=1
                if b == ':':
                    if word != '':
                        splitprag.append(word)
                    splitprag.append(':')
                    word=''
                    skp=1
                if b == ',':
                    if word != '':
                        splitprag.append(word)
                    splitprag.append(',')
                    word=''
                    skp=1
                # skp makes sure chars arent repeated
                if skp == 0:
                    word = word + b
                else:
                    skp=0
                if j == len(stri)-1:
                    if word != '':
                        splitprag.append(word)
                    #print("appended "+word)
                    word=''
                    j=0
                    break

                j+=1
            skip=1
        else:
            skip=0

        #reset variables
        sp1=-1
        sp2=-1
        sp3=-1
        sp4=-1
        #print(pragarr[i]+ "skip:"+ str(skip))
        if skip == 0:
            splitprag.append(pragarr[i])
            skip = 0
        i+=1
    return splitprag

def pragtype(splitprag):
    #pragtypeindicator= splitprag[0]+splitprag[1]+splitprag[2]
    pragtypechecker = ''
    pragtypeindicator=3
    for b in splitprag:
        pragtypechecker=pragtypechecker+b
        #print(pragtypechecker)
        if pragtypechecker == "#pragma omp" or pragtypechecker == "# pragma omp" or pragtypechecker == "!$omp" or pragtypechecker == "!$ omp" or pragtypechecker == "! $omp"or pragtypechecker == "! $ omp":
            pragtypeindicator = 1
            #print("in")
            break
        else:
            pragtypeindicator = 2
        pragtypechecker=pragtypechecker+' '
    return(pragtypeindicator)





def envchecker(entireenvlist,splitprag):
    envused=''
    for b in range(len(entireenvlist)):
        for a in splitprag:
            if entireenvlist[b] == a:
                envused= a
            #elif a == splitprag[-1]:
                #print("not found")
    return(envused)

def dirchecker(entiredirlist,splitprag):
    dirfound=''
    for b in range(len(entiredirlist)):
        k=0
        for a in splitprag:
            lengthb=len(entiredirlist[b].split()) #number of words in the directive
            dirc= splitprag[k]
    #        print (lengthb)

            # Go through each word in array till it equals the length of the directive and add to string
            for c in range(lengthb-1):
                if k+c+1<=len(splitprag)-1:
                    dirc = dirc + ' ' + splitprag[k+c+1]
                    #print (k+c+1)

            #print("-->"+dirc)
            #print (dirdb[b]["directive"])
            #Compare the two
            if dirc == entiredirlist[b]:
                #print ("found")
                #To check if a smaller subset of the directive was already considered
                if len(dirc) > len(dirfound):
                    if dirc.find(dirfound) >= 0:
                        dirfound = dirc
                        dirid=b
                        #print (dirfound)
                # to check if a larger superset of the directive is already found
                if dirfound.find(dirc) == -1:
                    dirfound = dirc
                    dirid=b
                    #print (dirfound)
                else:
                    n=0#print("its a subset")
                dirp=1
            k+=1
    return(dirfound)

def clausechecker(splitprag, dirfound):
    split_dir=dirfound.split()
    #print(split_dir)
    dir_index=splitprag.index(split_dir[-1])
    parentheses_checker=0
    reeclauselist=[]
    #print(len(splitprag))
    for b in range(dir_index+1,len(splitprag)):
        #print(splitprag[b])
        if parentheses_checker == 0 and splitprag[b] != '(' and splitprag[b] != ')':
            #print (splitprag[b])
            reeclauselist.append(splitprag[b])
        if splitprag[b] == '(':
            parentheses_checker=1
        elif splitprag[b] == ')':
            parentheses_checker=0
    return(reeclauselist)



def conditionerchecker(clauselist,splitprag):
    arrconditionerlist=[[-1 for x in range(20)]for y in range(20)]
    for b in range(len(clauselist)):
        optionn=0
        conditionern=0
        #print(clauselist[b])
        clausestrindex = splitprag.index(clauselist[b])
        #print("clausestrindex "+str(splitprag[clausestrindex]))
        if clausestrindex == len(splitprag):
            break
        try:
            if splitprag[clausestrindex + 1] == "(":
                optstart= clausestrindex + 1 #Start of optoin string
                for  a in range (optstart, len(splitprag)):
                    #print(a)
                    if splitprag[a] == ")":
                        optend = a #end of option string
                        break
                #print("start " +str(optstart)+" end "+str(optend))
                init_val=optstart+1
                #print(splitprag[optend])
                for a in range (optstart+1, optend+1):
                    #print("in"+splitprag[a])
                #throws exception when clauses are empoty
                    temp_val=''
                    if splitprag[a] == ',' or splitprag[a] == ')':
                        for c in range (init_val , a):
                            temp_val = temp_val + splitprag[c]
                        arrconditionerlist[b][conditionern] = temp_val
                        conditionern+=1
                        init_val = a + 1
            else:
                arrconditionerlist[b][conditionern]=-2
                #optionlist[b][optionn]= -2
            #print(arrconditionerlist[b])
        except:
            arrconditionerlist[b][conditionern]=-2
            break
    return(arrconditionerlist)

def get_test_names(envused, dirfound, clauselist, conditionerlist, omp_version,pragtypeindicator):
    test_names_list=[]
    testnames = open('/sw/crusher/ums/ums012/SOLLVE/autosollvevv/json_data/test_names_new.json')
    testnamesdb = json.load(testnames)
    if omp_version== "4.5":
        entiredirlist=get_dirlist("4.5", dir_names)
        entireenvlist=get_envlist("4.5", env_names)
    elif omp_version== "5.0":
        entiredirlist=get_dirlist("5.0", dir_names)
        entireenvlist=get_envlist("5.0", env_names)
    elif omp_version== "5.1":
        entiredirlist=get_dirlist("5.1", dir_names)
        entireenvlist=get_envlist("5.1", env_names)
    for b in range(len(testnamesdb)):
    #for b in range(20,21):
        #testconditionerlist=[[-1 for x in range(20)]for y in range(20)]
        if testnamesdb[b]["Pragma"] != "":
            if str(testnamesdb[b]["OMP Version"]) == omp_version:
                splittestname=split_prag(testnamesdb[b]["Pragma"])
                #print(splittestname)
                if pragtype(splittestname) ==  pragtypeindicator:
                    if pragtypeindicator == 2:
                        test_envused=envchecker(entireenvlist,splittestname)
                        if envused == test_envused and envused != '':
                            test_names_list.append(testnamesdb[b]["Test Name"])
                            continue
                        else:
                            continue
                    elif pragtypeindicator == 1:
                        test_dirfound=dirchecker(entiredirlist,splittestname)
                        if dirfound == test_dirfound:
                            test_clauselist=clausechecker(splittestname, test_dirfound)
                            #print(clauselist)
                            #print(test_clauselist)
                            testconditionerlist=conditionerchecker(test_clauselist,splittestname)
                            #print(testconditionerlist)
                            #print(splittestname)
                        else:
                            continue
                else:
                    continue
            else:
                continue
        else:
            continue
        if len(test_clauselist) == 1:
            for c in range(len(clauselist)):
                #print(conditionerlist[c])
                if test_clauselist[0] == clauselist[c]:
                    temp_conditioner_val = testconditionerlist[0][0]
                    if temp_conditioner_val != -2:
                        #print(testconditionerlist[0])
                        for d in conditionerlist[c]:
                            #print(d, c)
                            #print(testconditionerlist[0][0])
                            if testconditionerlist[0][0] in str(d):
                                test_names_list.append(testnamesdb[b]["Test Name"])
                    elif temp_conditioner_val == -2:
                        test_names_list.append(testnamesdb[b]["Test Name"])
        if len(test_clauselist) != 1:
            if len(clauselist) == len(test_clauselist):
                if sorted(clauselist) == sorted(test_clauselist):
                    test_names_list.append(testnamesdb[b]["Test Name"])
    return(test_names_list)

def result_display(test_names_list, omp_version, filelang):
    #print("in")
    result = open ('/sw/crusher/ums/ums012/SOLLVE/autosollvevv/json_data/crusher.json')
    resultdb = json.load(result)
    testnames = open('/sw/crusher/ums/ums012/SOLLVE/autosollvevv/json_data/test_names_new.json')
    testnamesdb = json.load(testnames)
    printed=0
    for c in test_names_list:
        #print(c)
        for b in range(len(resultdb)):
            if resultdb[b]["Test name"] == c and resultdb[b]["OMP version"] == omp_version:
                if filelang in resultdb[b]["Test name"]:
                    if printed==0:
                        print("Test Name: "+resultdb[b]["Test name"]+" OpenMP Version: "+resultdb[b]["OMP version"])
                        for d in range(len(testnamesdb)):
                            if testnamesdb[d]["Test Name"]==resultdb[b]["Test name"]:
                                print("Related Pragma: "+testnamesdb[d]["Pragma"])
                        printed=1
                    print("Compiler Name: " +resultdb[b]["Compiler name"]+" Result: "+resultdb[b]["Compiler result"])
        printed =0
        print()

def result_display_comp(test_names_list, omp_version, compver, filelang):
    #print("in")
    result = open ('/sw/crusher/ums/ums012/SOLLVE/autosollvevv/json_data/crusher.json')
    resultdb = json.load(result)
    testnames = open('/sw/crusher/ums/ums012/SOLLVE/autosollvevv/json_data/test_names_new.json')
    testnamesdb = json.load(testnames)
    printed=0
    for c in test_names_list:
        #print(c)
        for b in range(len(resultdb)):

            if resultdb[b]["Test name"] == c and resultdb[b]["OMP version"] == omp_version and resultdb[b]["Compiler name"] == compver:
                if filelang in resultdb[b]["Test name"]:
                    if printed==0:
                        print("Test Name: "+resultdb[b]["Test name"]+" OpenMP Version: "+resultdb[b]["OMP version"])
                        for d in range(len(testnamesdb)):
                            if testnamesdb[d]["Test Name"]==resultdb[b]["Test name"]:
                                print("Related Pragma: "+testnamesdb[d]["Pragma"])
                        printed=1
                    print("Compiler Name: " +resultdb[b]["Compiler name"]+" Compiler Result: "+resultdb[b]["Compiler result"]+" Runtime Result: "+resultdb[b]["Runtime result"])
        printed =0
        print()


def result_display_complist(test_names_list, omp_version, complist, filelang):
    #print("in")
    result = open ('/sw/crusher/ums/ums012/SOLLVE/autosollvevv/json_data/crusher.json')
    resultdb = json.load(result)
    testnames = open('/sw/crusher/ums/ums012/SOLLVE/autosollvevv/json_data/test_names_new.json')
    testnamesdb = json.load(testnames)
    printed=0
    for c in test_names_list:
        #print(c)
        for b in range(len(resultdb)):
            for h in complist:
                if resultdb[b]["Test name"] == c and resultdb[b]["OMP version"] == omp_version and resultdb[b]["Compiler name"] == h:
                    if filelang in resultdb[b]["Test name"]:
                        if printed==0:
                            print("Test Name: "+resultdb[b]["Test name"]+" OpenMP Version: "+resultdb[b]["OMP version"])
                            for d in range(len(testnamesdb)):
                                if testnamesdb[d]["Test Name"]==resultdb[b]["Test name"]:
                                    print("Related Pragma: "+testnamesdb[d]["Pragma"])
                            printed=1
                        print("Compiler Name: " +resultdb[b]["Compiler name"]+" Compiler Result: "+resultdb[b]["Compiler result"]+" Runtime Result: "+resultdb[b]["Runtime result"])
        printed =0
        print()



#print(entireenvlist)
def ext_check(expected_extensionlist, openner):
    err=1
    def extension(filename):
        for a in expected_extensionlist:
            if a in str(filename):
                err=0
        if err!=1:
            return openner(filename)
        else:
            raise argparse.ArgumentTypeError('File must have a .c or .cpp or .F90 extension')
    return extension

def main():
    const1= ''
    word=''
    splitprag=[]
    skip=0
    lineskp=0
    envused_45=''
    envused_50=''
    envused_51=''
    dirid=''
    clausen=0
    dirfound_45=''
    dirfound_50=''
    dirfound_51=''
    clauselist_45=[]
    clauselist_50=[]
    clauselist_51=[]
    optionlist=[[-1 for x in range(20)]for y in range(20)]
    conditionerlist_45=[[-1 for x in range(20)]for y in range(20)]
    conditionerlist_50=[[-1 for x in range(20)]for y in range(20)]
    conditionerlist_51=[[-1 for x in range(20)]for y in range(20)]


    prag= "#pragma omp target map(tofrom:errors) defaultmap (present:scalar)"
    #prag= "atomic compare"
    #prag= "#pragma omp target update to"
    #prag="#pragma omp begin declare variant"
    #prag="#pragma omp tile"
    #prag = input("Enter your pragma statement:")


    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=ext_check([".cpp",".c",".F90"], argparse.FileType('r')), help="This is to input the program file")
    parser.add_argument('-c','--compiler', type=str, choices=['llvm','rocm','cce'], help="This is to specify the compiler to show all versions")
    parser.add_argument('-cv','--compilerversion', choices=['llvm_14','llvm_15','llvm_16','rocm_4.5','rocm_5.0','rocm_5.2','cce_14.0.0','cce_14.0.1'], type=str, help="This is to specify the compiler with it's version")
    parser.add_argument('-omp','--openmp', type=str, choices=["4.5","5.0","5.1","5.2"], help="This is to specify the OpenMP Version")
    args = parser.parse_args()
    file_loc= args.file
    if ".c" in file_loc.name:
        filelang="c"
    elif ".cpp" in file_loc.name:
        filelang="cpp"
    elif ".F90" in file_loc.name:
        filelang=".F90"
    #print(filelang)
    #print(args.compiler)
    #print(args.compilerversion)
    #print(args.openmp)
    #file_loc=input("Enter file name: ")
    print()
    print("----------------------------------------------------------------------")
    #file = open(file_loc, 'r')
    if args.compilerversion == 'llvm_14':
        compilerver='llvm_14_0_0'
    elif args.compilerversion == 'llvm_15':
        compilerver='llvm_15_0_0'
    elif args.compilerversion == 'llvm_16':
        compilerver='llvm_16_0_0'
    elif args.compilerversion == 'rocm_4.5':
        compilerver='rocm_4_5_2'
    elif args.compilerversion == 'rocm_5.0':
        compilerver='rocm_5_0_2'
    elif args.compilerversion == 'rocm_5.2':
        compilerver='rocm_5_2_0'
    elif args.compilerversion == 'cce_14.0.0':
        compilerver='cce_14_0_0'
    elif args.compilerversion == 'cce_14.0.1':
        compilerver='cce_14_0_1'
    elif args.compiler == "llvm":
        compilerverlist=['llvm_14_0_0','llvm_15_0_0','llvm_16_0_0']
    elif args.compiler == "rocm":
        compilerverlist=['rocm_4_5_2','rocm_5_0_2','rocm_5_2_0']
    elif args.compiler == "cce":
        compilerverlist=['cce_14_0_0','cce_14_0_1']
    file_lines = file_loc.readlines()
    line_count=0
    entiredirlist_45=get_dirlist("4.5", dir_names)
    entireenvlist_45=get_envlist("4.5", env_names)
    entiredirlist_50=get_dirlist("5.0", dir_names)
    entireenvlist_50=get_envlist("5.0", env_names)
    entiredirlist_51=get_dirlist("5.1", dir_names)
    entireenvlist_51=get_envlist("5.1", env_names)
    for line_n in range(len(file_lines)):

        if lineskp != 0:
            lineskp=lineskp-1
            continue
        line=file_lines[line_n]
        #print(line_n)
        line_count=line_count+1
        #print(line.strip())
        splitprag=split_prag(line.strip())
        #print(len(splitprag))
        if len(splitprag)!= 0 or len(splitprag)!= 1:
            try:
                temp_line_n=line_n
                for temp_line_ittr in range(len(file_lines)):
                    if splitprag[len(splitprag)-1]=="\\":
                        #print(temp_line_n)
                        lineskp=lineskp+1
                        next_line=file_lines[temp_line_n+temp_line_ittr+1]
                        next_splitprag=split_prag(next_line.strip())
                        splitprag.pop()
                        splitprag=splitprag+next_splitprag
                    else:
                        break
            except:
                x=1

        pragtypeindicator=pragtype(splitprag)
        if pragtypeindicator == 2:
            envused_45=envchecker(entireenvlist_45,splitprag)
            envused_50=envchecker(entireenvlist_50,splitprag)
            envused_51=envchecker(entireenvlist_51,splitprag)
        elif pragtypeindicator == 1:
            #print(splitprag,line_count)
            dirfound_45=dirchecker(entiredirlist_45,splitprag)
            dirfound_50=dirchecker(entiredirlist_50,splitprag)
            dirfound_51=dirchecker(entiredirlist_51,splitprag)
            #print(dirfound_45)
            #print(dirfound_50)
            #print(dirfound_51)

            if dirfound_45 == '':
                continue
            #print ("consturct:"+dirfound)
            else:
                clauselist_45=clausechecker(splitprag, dirfound_45)
                conditionerlist_45=conditionerchecker(clauselist_45,splitprag)

            if dirfound_50 == '':
                continue
            else:
                clauselist_50=clausechecker(splitprag, dirfound_50)
                conditionerlist_50=conditionerchecker(clauselist_50,splitprag)

            if dirfound_51 == '':
                continue
            else:
                clauselist_51=clausechecker(splitprag, dirfound_51)
                conditionerlist_51=conditionerchecker(clauselist_51,splitprag)

        elif pragtypeindicator == 3:
            continue
        #print(clauselist)


        test_names_list_45=get_test_names(envused_45, dirfound_45, clauselist_45, conditionerlist_45, "4.5",pragtypeindicator)
        test_names_list_50=get_test_names(envused_50, dirfound_50, clauselist_50, conditionerlist_50, "5.0",pragtypeindicator)
        test_names_list_51=get_test_names(envused_51, dirfound_51, clauselist_51, conditionerlist_51, "5.1",pragtypeindicator)

        if args.openmp:
            if args.openmp == "4.5":
                if args.compilerversion:
                    if len(test_names_list_45) != 0:
                        print("Line number: "+str(line_count))
                        print("Line: "+line.strip())
                        print()
                        if len(test_names_list_45) !=0:
                            print("OMP 4.5 tests")
                            result_display_comp(test_names_list_45,"4.5",compilerver, filelang)
                        print("----------------------------------------------------------------------")
                elif args.compiler:
                    for h in compilerverlist:
                        if len(test_names_list_45) != 0:
                            print("Line number: "+str(line_count))
                            print("Line: "+line.strip())
                            print()
                            if len(test_names_list_45) !=0:
                                print("OMP 4.5 tests")
                                result_display_comp(test_names_list_45,"4.5",h, filelang)
                            print("----------------------------------------------------------------------")
                else:
                    if len(test_names_list_45) != 0:
                        print("Line number: "+str(line_count))
                        print("Line: "+line.strip())
                        print()
                        if len(test_names_list_45) !=0:
                            print("OMP 4.5 tests")
                            result_display(test_names_list_45,"4.5", filelang)
                        print("----------------------------------------------------------------------")
            elif args.openmp == "5.0":
                if args.compilerversion:
                    if len(test_names_list_50) != 0:
                        print("Line number: "+str(line_count))
                        print("Line: "+line.strip())
                        print()
                        if len(test_names_list_50) !=0:
                            print("OMP 5.0 tests")
                            result_display_comp(test_names_list_50,"5.0",compilerver, filelang)
                        print("----------------------------------------------------------------------")
                elif args.compiler:
                    for h in compilerverlist:
                        if len(test_names_list_45) != 0:
                            print("Line number: "+str(line_count))
                            print("Line: "+line.strip())
                            print()
                            if len(test_names_list_50) !=0:
                                print("OMP 5.0 tests")
                                result_display_comp(test_names_list_50,"5.0",h, filelang)
                            print("----------------------------------------------------------------------")
                else:
                    if len(test_names_list_50) != 0:
                        print("Line number: "+str(line_count))
                        print("Line: "+line.strip())
                        print()
                        if len(test_names_list_50) !=0:
                            print("OMP 5.0 tests")
                            result_display(test_names_list_50,"5.0", filelang)
                        print("----------------------------------------------------------------------")
            elif args.openmp == "5.1":
                if args.compilerversion:
                    if len(test_names_list_51) != 0:
                        print("Line number: "+str(line_count))
                        print("Line: "+line.strip())
                        print()
                        if len(test_names_list_51) !=0:
                            print("OMP 5.1 tests")
                            result_display_comp(test_names_list_51,"5.1",compilerver, filelang)
                        print("----------------------------------------------------------------------")
                elif args.compiler:
                    for h in compilerverlist:
                        if len(test_names_list_45) != 0:
                            print("Line number: "+str(line_count))
                            print("Line: "+line.strip())
                            print()
                            if len(test_names_list_51) !=0:
                                print("OMP 5.1 tests")
                                result_display_comp(test_names_list_51,"5.1",h, filelang)
                            print("----------------------------------------------------------------------")
                else:
                    if len(test_names_list_51) != 0:
                        print("Line number: "+str(line_count))
                        print("Line: "+line.strip())
                        print()
                        if len(test_names_list_51) !=0:
                            print("OMP 5.1 tests")
                            result_display(test_names_list_51,"5.1", filelang)
                        print("----------------------------------------------------------------------")
        elif args.compilerversion:
            test_names_list= test_names_list_45

            for a in test_names_list_50:
                if a not in test_names_list:
                    test_names_list.append(a)

            for a in test_names_list_51:
                if a not in test_names_list:
                    test_names_list.append(a)

            if len(test_names_list) != 0:
                print("Line number: "+str(line_count))
                print("Line: "+line.strip())
                print()
                if len(test_names_list_45) !=0:
                    print("OMP 4.5 tests")
                    result_display_comp(test_names_list_45,"4.5",compilerver, filelang)
                if len(test_names_list_50) !=0:
                    print("OMP 5.0 tests")
                    result_display_comp(test_names_list_50,"5.0",compilerver, filelang)
                if len(test_names_list_51) !=0:
                    print("OMP 5.1 tests")
                    result_display_comp(test_names_list_51,"5.1",compilerver, filelang)
                print("----------------------------------------------------------------------")
        elif args.compiler:
            test_names_list= test_names_list_45

            for a in test_names_list_50:
                if a not in test_names_list:
                    test_names_list.append(a)

            for a in test_names_list_51:
                if a not in test_names_list:
                    test_names_list.append(a)

            if len(test_names_list) != 0:
                print("Line number: "+str(line_count))
                print("Line: "+line.strip())
                print()
                if len(test_names_list_45) !=0:
                    print("OMP 4.5 tests")
                    result_display_complist(test_names_list_45,"4.5",compilerverlist, filelang)
                if len(test_names_list_50) !=0:
                    print("OMP 5.0 tests")
                    result_display_complist(test_names_list_50,"5.0",compilerverlist, filelang)
                if len(test_names_list_51) !=0:
                    print("OMP 5.1 tests")
                    result_display_complist(test_names_list_51,"5.1",compilerverlist, filelang)
                print("----------------------------------------------------------------------")
        else:
            test_names_list= test_names_list_45

            for a in test_names_list_50:
                if a not in test_names_list:
                    test_names_list.append(a)

            for a in test_names_list_51:
                if a not in test_names_list:
                    test_names_list.append(a)

            if len(test_names_list) != 0:
                print("Line number: "+str(line_count))
                print("Line: "+line.strip())
                print()
                if len(test_names_list_45) !=0:
                    print("OMP 4.5 tests")
                    result_display(test_names_list_45,"4.5", filelang)
                if len(test_names_list_50) !=0:
                    print("OMP 5.0 tests")
                    result_display(test_names_list_50,"5.0", filelang)
                if len(test_names_list_51) !=0:
                    print("OMP 5.1 tests")
                    result_display(test_names_list_51,"5.1", filelang)
                print("----------------------------------------------------------------------")

if __name__ == '__main__':
    main()
