#!/usr/bin/python
import sys, getopt, os
import subprocess

# Error = "CommandError: Cannot find a migration"
MAX_INSTANCES = 10
HELP = 'sqlmigrate.py -a <Django app>'
DJANGO_MANAGE = "manage.py"
DJANGO_PARAM = "sqlmigrate"

def main(argv):
    application = ''

    if not argv: #Manage no args
        print(HELP)
        sys.exit()

    try: #Manage opts & args 
        opts, args = getopt.getopt(argv,"ha:",["app="])
    except getopt.GetoptError:
        print(HELP)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' :
            print(HELP)
            sys.exit()
        elif opt in ("-a", "--app"):
            application = arg
            print('sqlmigrate statements for django app:%s', application)


    try: #Manage Django sqlmigrate statements 
        # while loop
        count = 0
        while (count < MAX_INSTANCES):   
            count = count + 1
            new_i = '%04d'%(int('0000')+count)
            #print("new_i: ", new_i)
            print("########################################## "+application+"/"+new_i+" ##########################################")
                 
            #python manage.py sqlmigrate oauth 0001
            command = './'+DJANGO_MANAGE+' '+DJANGO_PARAM+' '+str(application)+ ' ' + str(new_i)
            result = os.system(command)
            #result = os.popen(command).read()
            #print("result: ", len(result))

            #if (len(result) == 0):
            if (result > 0):
                raise AttributeError
            
    except AttributeError:
        #print ("No, this is normal.")
        print("End of statements.")
    except :
        print("Oops!", sys.exc_info()[0], "occurred.")

if __name__ == "__main__":
   main(sys.argv[1:])