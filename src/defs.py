# this file includes definitions, strings, help, etc for the weekly project

header = """
Weekly 
Ohad Eitam (oeitam@gmail.com)
Started May 2017
-------------------
this is the header
-------------------
"""

# columns definitions for the data bases
# megaprojects
dfm_columns = ['Name',
               'State',
               'PROJECTs_List',
               'Description',
               ]
# projects
dfp_columns = ['Name',
               'State',
               'MEGAPROJECT',
               'Description',
               ]
# tasks
dft_columns = ['State',
               'Description',
               'Creation_Date',
               'PROJECT',
               # optional from here
               'Due_Date',
               'Expiration_Date',
               'Location',
               'Context',
               'Reminders',
               'ACTIVITYs',
               'Sub_TASKs',
               'Parent_TASK',
               ]
# activities
dfa_columns = ['State',
               'Start_Time',
               'Description',
               'End_Time',
               'TASK',
               'PROJECT'
               ]

df_columns = { 'dfm': dfm_columns,
               'dfp': dfp_columns,
               'dft': dft_columns,
               'dfa': dfa_columns,
               }


# states definitions (all transitions are legel)
MEGAPROJ_states  = {'On' : 'The MEGAPROJECT is open',
                    'Off': 'The MEGAPROJECT is closed',
                    }

PROJECT_states   = {'Started' : 'The PROJECT started rolling',
                    'OnHold' : 'The PROJECT is not active - so nothin in it can change.',
                    'Ended'   : 'The project is concluded, done, finished.',
                    }

TASK_states      = {'Open'   : 'The TASK is created and may be on execution',
                    'OnHold': 'Execution on this TASK is stopped',
                    'Closed' : 'The TASK is completed',
                    }

ACTIVITY_states  = {'Started': 'The TASK is created and may be on execution',
                    'OnHold': 'Execution on this TASK is stopped',
                    'Ended'  : 'The TASK is completed',
                    }

###############

# keywords
keywords = {'create',
            'project',
            'task',
            'activity',
            'ACTIVITY',
            'attach',
            'set',
            'continue',
            'resume',
            'list',
            'clean',
            'search',
            'start',
            'delete',
            'context',
            'die',
            }


##########
MEGAPROJ = {
    'home': 'projects that belong to private life, home',
    'work': 'projects that belong to work'
}

# ====================================================

mlt = '''recieved 0082:create project project_one @Work1 | this is the first project I created #0002
sending data to the proc
the proc got this data: create project project_one @Work1 | this is the first project I created #0002
processing data from the client
--0059:Transaction: create project COMPLETED. New ID is: 1678--
server: Closing socket
server off
Press enter to finish the program'''


