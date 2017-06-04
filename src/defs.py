# this file includes definitions, strings, help, etc for the weekly project

header =
'''
Weekly 
Ohad Eitam (oeitam@gmail.com)
Started May 2017
-------------------
this is the header
-------------------
'''

# columns definitions for the data bases
# megaprojects
dfm_columns = ['ID',
               'State',
               'PROJECTs List',
               ]
# projects
dfp_columns = ['ID,'
               'State',
               'MEGAPROJECT',
               ]
# tasks
dft_columns = ['ID',
               'State',
               'Due Date',
               'Creation Date',
               'Expiration Date'
               'PROJECT',
               'Location',
               'Context',
               'Reminders',
               'ACTIVITY',
               'Sub TASK',
               'Parent TASK',
               ]
# activities
dfa_columns = ['ID',
               'State',
               'Start Time',
               'End Time',
               'TASK',
               ]

# states definitions (all transitions are legel)
MEGAPROJ_states  = {'On' : 'The MEGAPROJECT is open',
                    'Off': 'The MEGAPROJECT is closed',
                    }

PROJECT_states   = {'Started' : 'The PROJECT started rolling',
                    'On Hold' : 'The PROJECT is not active - so nothin in it can change.',
                    'Ended'   : 'The project is concluded, done, finished.',
                    }

TASK_states      = {'Open'   : 'The TASK is created and may be on execution',
                    'On Hold': 'Execution on this TASK is stopped',
                    'Closed' : 'The TASK is completed',
                    }

ACTIVITY_states  = {'Started': 'The TASK is created and may be on execution',
                    'On Hold': 'Execution on this TASK is stopped',
                    'Ended'  : 'The TASK is completed',
                    }

###############

MEGAPROJ = {
    'home': 'projects that belong to private life, home',
    'work': 'projects that belong to work'
}

