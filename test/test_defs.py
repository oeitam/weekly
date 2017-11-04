# oeitam

#print('test_defs.py !!')

from datetime import timedelta

debug_delta = timedelta(days=0)

test_commands = [
    #"ci",
    #"co",
    #"co",
    #"list activity state OnHold",
    #"list megaproject state On",
    #"list project state OnHold",
    #"list task state OnHold",
    #"list activity col Start_Date drange bot top",
    #"list activity ww 43",
    #"list activity ww 43 state OnHold",
    #"list activity state OnHold ww 43",
    #"list activity ww 43",
    #'list activity col Start_Date drange 17ww35.Sun 17ww39',
    #'today | help bla bla',
    #'sleep @11540 17ww50',
    #'sleep @11540 17ww50.Sun',
    #'die',
    #'cont @10673',
    #'sleep @10673 plus 99',
    #'list task state Dormant',
    #'list activity state Dormant',
    'sleep @10673 20201212',
    'list wakeup',
    #'die',
    'cont @11540',
    'cont @10687',
    'cont @10673',
    'sleep @11540 17ww50',
    'sleep @10687 20171205',
    'sleep @10673 plus 88',
    'sleep @10673',
    'list @11540',
    'list @10687',
    'list @10673',
    #'die',
    'help',
    #'list project',
    #'die',
    #'list activity state all col Start_Date drange 17ww35.Sun 17ww39.Mon',
    #'list activity col Start_Date drange 17ww35.Sun 17ww39.Mon state OnHold',
    #'list activity col Start_Date drange 17ww35.Sun 17ww39.Mon',
    #'list activity ww 43',
    #"die",
    #"start @00000000 | two this is some activity related to a taask",
    "create megaproject Work2 | 2all projects that relate to Work at Intel go here",
    "create megaproject Work2 | 2all projects that relate to Work at Intel go here",
    "create megaproject Work2 | 2all projects that relate to Work at Intel go here",
    "create project project_two @Work2 | this is the first project I created",
    "ci",
    "co",
    #"die",
    "create project project_three @Work1 | this is the first project I created",
    "create project project_four @Work2 | this is the first project I created",
    "create project project_five @Work1 | this is the first project I created",
    "task @project_one | 1this is what you need to do on project one",
    "task @project_one | 1another this is what you need to do on project one",
    "task @project_two | 1this is what you need to do on project two",
    "task @project_two1 | 1second this is what you need to do on project two",
    "task @project_two | 1third this is what you need to do on project two",
    #"die",
    "start @00000000 | two this is some activity related to a taask",
    "start @00000000 | three this is some activity related to a taask",
    "start @00000000 | four this is some activity related to a taask",
    "start @00000000 | five this is some activity related to a taask",
    "start @00000000 | six this is some activity related to a taask",
    "start @00000000 | seven this is some activity related to a taask",
    "start @0 | some activity, not project or task",
    #"die",
    "create megaproject Work2 | 2all projects that relate to Work at Intel go here",
    "create project project_two @Work2 | this is the first project I created",
    "create project project_three @Work1 | this is the first project I created",
    "create project project_four @Work2 | this is the first project I created",
    "create project project_five @Work1 | this is the first project I created",
    # "turn_on",
    "task @project_one | another this is what you need to do on project one",
    "task @project_two | this is what you need to do on project two",
    "task @project_two | second this is what you need to do on project two",
    "task @project_two | second this is what you need to do on project two",
    "start @00000000 | one this is some activity related to a taask",
    "stop @00000000",
    "cont @00000000",
    "list @00000000",
    "list @00000000",
    "list @00000000",
    "start @00000000 | two this is some activity related to a taask",
    "start @00000000 | three this is some activity related to a taask",
    "start @00000000 | four this is some activity related to a taask",
    "start @00000000 | five this is some activity related to a taask",
    "start @00000000 | six this is some activity related to a taask",
    "start @00000000 | seven this is some activity related to a taask",
    "create megaproject Work11 | 11all projects that relate to Work at Intel go here",
    "create project project_one1 @Work11 | this is the first project I created",
    "create megaproject Work21 | 21all projects that relate to Work at Intel go here",
    "create project project_two1 @Work21 | this is the first project I created",
    "create project project_three1 @Work11 | this is the first project I created",
    "create project project_four1 @Work21 | this is the first project I created",
    "list @00000000",
    "list @00000000",
    "list @00000000",
    "create project project_five1 @Work11 | this is the first project I created",
    # "turn_on",
    "task @project_one | 1this is what you need to do on project one",
    "task @project_one | 1another this is what you need to do on project one",
    "task @project_two | 1this is what you need to do on project two",
    "task @project_two1 | 1second this is what you need to do on project two",
    "task @project_two | 1third this is what you need to do on project two",
    "start @00000000 | one1 this is some activity related to a taask",
    "start @00000000 | two1 this is some activity related to a taask",
    "start @00000000 | three1 this is some activity related to a taask",
    # "list @00000000",
    "start @00000000 | four1 this is some activity related to a taask",
    "start @00000000 | five1 this is some activity related to a taask",
    "start @00000000 | six1 this is some activity related to a taask",
    "start @00000000 | seven1 this is some activity related to a taask",
    "list search | ww 26",
    "list activity ww 17",
    "list activity ww 18",
    "list activity ww 19",
    "list activity ww 20",
    "list task ww 17",
    "list task ww 18",
    "list task ww 19",
    "list task ww 20",
    #"die",
    "list megaproject columns",
    "list project columns",
    "list task columns",
    "list activity columns",
    "list megaproject states",
    "list project states",
    "list task states",
    "list activity states",
    #"die"
    "list megaproject for project project_one",
    "list project for megaproject Work1",
    "list task for project project_two",
    "list activity for project project_one",
    "list",
    "list activity for task @2334",
    #"die",
    "create megaproject Work1 | 1all projects that relate to Work at Intel go here",
    "list activity col Start_Date drange 17ww17.Sun 17ww20.Mon",
    "list activity col Start_Date drange 17ww17 17ww20.Mon",
    "list activity col Start_Date drange 17ww17.Sun 17ww20",
    "list activity col Start_Date drange 17ww17 17ww20",
    "list activity col Start_Date drange bot 17ww20.Mon",
    "list activity col Start_Date drange bot 17ww20",
    "list activity col Start_Date drange 17ww17.Sun top",
    "list activity col Start_Date drange 17ww17 top",
    "list activity col Start_Date drange bot top",
    #"die",
    "list megaproject col ID irange 2569 2631",
    "list megaproject col ID irange 2569 top",
    "list megaproject col ID irange bot 2631",
    "list megaproject col ID irange bot top",

    "halt @00000000",
    "stop @00000000",
    "cont @00000000",
    "list @00000000",
    #"die",
    #"turn on",
    "list megaproject",
    "list",
    "list",
    "list megaproject col Name is Work1",
    "list megaproject",
    "list",
    "list",
    "list",
    "list",
    "list megaproject limit 30",
    "list",
    "list",
    "list",
    "list",
    "list",
    "list project",
    "list",
    "list",
    "list project col Name is project_two",
    "list",
    "list",
    "list task",
    "list",
    "list",
    "list task col PROJECT is project_two",
    "list",
    "list",
    "list activity",
    "list",
    "list",
    "list activity col PROJECT is 1498",
    "list",
    "list activity col Description inc one",
    "list",
    "list activity col PROJECT not 1498",
    "list",
    "list activity col PROJECT ninc 1498",
    "list",
    "list",
    "list task",
    "list activity",
    #"die",
    "create project project_one @Work1 | this is the first project I created",
    "task @project_one | this is what you need to do on project one",
    "start @00000000 | one this is some activity related to a taask",
    "stop @00000000",
    "stop @00000000",
    "stop @00000000",
    "stop @00000000",
    "halt @00000000",
    "halt @00000000",
    "halt @00000000",
    "cont @00000000",
    "halt @00000000",
    "create megaproject Work2 | 2all projects that relate to Work at Intel go here",
    "create project project_two @Work2 | this is the first project I created",
    "create project project_three @Work1 | this is the first project I created",
    "create project project_four @Work2 | this is the first project I created",
    "create project project_five @Work1 | this is the first project I created",
    #"turn_on",
    "task @project_one | another this is what you need to do on project one",
    "task @project_two | this is what you need to do on project two",
    "task @project_two | second this is what you need to do on project two",
    "task @project_two | second this is what you need to do on project two",
    "start @00000000 | one this is some activity related to a taask",
    "stop @00000000",
    "cont @00000000",
    "list @00000000",
    "list @00000000",
    "list @00000000",
    "start @00000000 | two this is some activity related to a taask",
    "start @00000000 | three this is some activity related to a taask",
    "start @00000000 | four this is some activity related to a taask",
    "start @00000000 | five this is some activity related to a taask",
    "start @00000000 | six this is some activity related to a taask",
    "start @00000000 | seven this is some activity related to a taask",
    "create megaproject Work11 | 11all projects that relate to Work at Intel go here",
    "create project project_one1 @Work11 | this is the first project I created",
    "create megaproject Work21 | 21all projects that relate to Work at Intel go here",
    "create project project_two1 @Work21 | this is the first project I created",
    "create project project_three1 @Work11 | this is the first project I created",
    "create project project_four1 @Work21 | this is the first project I created",
    "list @00000000",
    "list @00000000",
    "list @00000000",
    "create project project_five1 @Work11 | this is the first project I created",
    #"turn_on",
    "task @project_one | 1this is what you need to do on project one",
    "task @project_one | 1another this is what you need to do on project one",
    "task @project_two | 1this is what you need to do on project two",
    "task @project_two1 | 1second this is what you need to do on project two",
    "task @project_two | 1third this is what you need to do on project two",
    "start @00000000 | one1 this is some activity related to a taask",
    "start @00000000 | two1 this is some activity related to a taask",
    "start @00000000 | three1 this is some activity related to a taask",
    # "list @00000000",
    "start @00000000 | four1 this is some activity related to a taask",
    "start @00000000 | five1 this is some activity related to a taask",
    "start @00000000 | six1 this is some activity related to a taask",
    "start @00000000 | seven1 this is some activity related to a taask",
    "stop @00000000",
    "stop @00000000",
    "stop @00000000",
    "list @00000000",
    "stop @00000000",
    "stop @00000000",
    "stop @00000000",
    "list @00000000",
    "cont @00000000",
    "cont @00000000",
    "cont @00000000",
    "halt @00000000",
    "halt @00000000",
    "halt @00000000",
    "online",
    "sleep @00000000",
    "sleep @00000000",
    "sleep @00000000",
    "sleep @00000000",
    "sleep @00000000",
    "sleep @00000000",
    #
    'die',
]


test_responses = []

