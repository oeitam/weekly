# this file includes definitions, strings, help, etc for the weekly project

from ast import literal_eval

# read local definition file and evaluate it
f = open('C:\weekly.local\weekly.local.txt', 'r')
l = []
for line in f:
    line = line.rstrip()
    if (line[0] == '#'):
        continue
    l.append(literal_eval(line))

f.close()

location            = l[0]
data_loc            = l[1]
mode_sel            = l[2]
local_client_script = l[3]
data_loc_dropbox    = l[4]
dev_or_prod         = l[5]

data_loc = data_loc + '\\' + dev_or_prod

#         -0-        -1-      -2-
mode = ['socket', 'direct', 'prod' ][mode_sel]

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
db_names = {'dfm': 'Megaprojects DataFrame',
            'dfp': 'Projects DataFrame',
            'dft': 'Tasks DataFrame',
            'dfa' : 'Activities DataFrame',
            }

help_message = '''
==================================
1  ci
2  co
3  help
4  die
5  start @00000000 | two...
6  create megaproject Work2 | 2all ...
7  create project project_two @Work2 | th...
8  task @project_one | 1this ...
9  start @00000000 | two ...
10 start @0 | some ...
11 list search | ww26
12 list activity ww17
13 list task ww17
14 list megaproject columns
15 list project columns
16 list task columns
17 list activity columns
18 list megaproject states
19 list project states
20 list task states
21 list activity states
22 list megaproject for project project_one
23 list project for megaproject Work1
24 list task for project project_two
25 list activity for project project_one
26 list activity for task @2334
27 list activity col Start_Date drange 17ww17.Sun 17ww20.Mon
28 list activity col Start_Date drange 17ww17 17ww20.Mon
29 list activity col Start_Date drange 17ww17.Sun 17ww20
30 list activity col Start_Date drange 17ww17 17ww20
31 list activity col Start_Date drange bot 17ww20.Mon
32 list activity col Start_Date drange bot 17ww20
33 list activity col Start_Date drange 17ww17.Sun top
34 list activity col Start_Date drange 17ww17 top
35 list activity col Start_Date drange bot top
36 list megaproject col ID irange 2569 2631
37 list megaproject col ID irange 2569 top
38 list megaproject col ID irange bot 2631
39 list megaproject col ID irange bot top
40 halt @00000000
41 stop @00000000
42 cont @00000000
43 today | doing this something today
==================================
'''

# ====================================================



