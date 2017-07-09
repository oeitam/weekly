# this file includes definitions, strings, help, etc for the weekly project


sel = 2
#         -0-        -1-      -2-
mode = ['socket', 'direct', 'prod' ][sel]

days_of_week = {'Sun': '-0',
                'Mon': '-1',
                'Tue': '-2',
                'Wed': '-3',
                'Thu': '-4',
                'Fri': '-5',
                'Sat': '-6',
                }


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
               'Start_Date',
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
               'Start_Date',
               'Description',
               'End_Date',
               'TASK',
               'PROJECT'
               ]

all_col = { 'megaproject' : dfm_columns ,
            'project'     : dfp_columns ,
            'task'        : dft_columns ,
            'activity'    : dfa_columns ,
            }

# columns to print
dfm_columns_to_print = ['Name',
                        'State',
                        #'PROJECTs_List',
                        'Description',
                        ]
# projects
dfp_columns_to_print = ['Name',
                        'State',
                        'MEGAPROJECT',
                        'Description',
                        ]
# tasks
dft_columns_to_print = ['State',
                        'Description',
                        'Start_Date',
                        'PROJECT',
                        # optional from here
                        'Due_Date',
                        'Expiration_Date',
                        #'Location',
                        #'Context',
                        #'Reminders',
                        #'ACTIVITYs',
                        #'Sub_TASKs',
                        #'Parent_TASK',
                         ]

dfa_columns_to_print = ['State',
                        'Start_Date',
                        'Description',
                        'End_Date',
                        #'TASK',
                        #'PROJECT'
                        ]

columns_to_print_table = { 'dfm' : dfm_columns_to_print ,
                           'dfp' : dfp_columns_to_print,
                           'dft' : dft_columns_to_print,
                           'dfa' : dfa_columns_to_print,
                           }
# activities



df_columns = { 'dfm': dfm_columns,
               'dfp': dfp_columns,
               'dft': dft_columns,
               'dfa': dfa_columns,
               }


# states definitions (all transitions are legel)
megaproject_states  = {'On' : 'The MEGAPROJECT is open',
                       'Off': 'The MEGAPROJECT is closed',
                       }

project_states   = {'Started' : 'The PROJECT started rolling',
                    'OnHold' : 'The PROJECT is not active - so nothin in it can change.',
                    'Ended'   : 'The project is concluded, done, finished.',
                    }

task_states      = {'Open'   : 'The TASK is created and may be on execution',
                    'OnHold': 'Execution on this TASK is stopped',
                    'Closed' : 'The TASK is completed',
                    }

activity_states  = {'Started': 'The TASK is created and may be on execution',
                    'OnHold': 'Execution on this TASK is stopped',
                    'Ended'  : 'The TASK is completed',
                    }

all_stat = { 'megaproject' : megaproject_states,
             'project'     : project_states,
             'task'        : task_states,
             'activity'    : activity_states,
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

# databases name
db_names = {'dfm' : 'Megaprojects DataFrame',
            'dfp' : 'Projects DataFrame',
            'dft' : 'Tasks DataFrame',
            'dfa' : 'Activities DataFrame',
            }
# ====================================================



