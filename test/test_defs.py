# oeitam

from datetime import timedelta

debug_delta = timedelta(days=0)

test_commands = [
    "start @0 | some activity, not project or task",
    "die",
    "list search | ww26",
    "list activity ww17",
    "list activity ww18",
    "list activity ww19",
    "list activity ww20",
    "list task ww17",
    "list task ww18",
    "list task ww19",
    "list task ww20",
    "die",
    "list megaproject columns",
    "list project columns",
    "list task columns",
    "list activity columns",
    "list megaproject states",
    "list project states",
    "list task states",
    "list activity states",
    "die"
    "list megaproject for project project_one",
    "list project for megaproject Work1",
    "list task for project project_two",
    "list activity for project project_one",
    "list",
    "list activity for task @2334",
    "die",
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
    "die",
    "list megaproject col ID irange 2569 2631",
    "list megaproject col ID irange 2569 top",
    "list megaproject col ID irange bot 2631",
    "list megaproject col ID irange bot top",
    "halt @0000",
    "stop @0000",
    "cont @0000",
    "list @0000",
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
    # #"die",
    "create project project_one @Work1 | this is the first project I created",
    "task @project_one | this is what you need to do on project one",
    "start @0000 | one this is some activity related to a taask",
    "stop @0000",
    "stop @0000",
    "stop @0000",
    "stop @0000",
    "halt @0000",
    "halt @0000",
    "halt @0000",
    "cont @0000",
    "halt @0000",
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
    "start @0000 | one this is some activity related to a taask",
    "stop @0000",
    "cont @0000",
    "list @0000",
    "list @0000",
    "list @0000",
    "start @0000 | two this is some activity related to a taask",
    "start @0000 | three this is some activity related to a taask",
    "start @0000 | four this is some activity related to a taask",
    "start @0000 | five this is some activity related to a taask",
    "start @0000 | six this is some activity related to a taask",
    "start @0000 | seven this is some activity related to a taask",
    "create megaproject Work11 | 11all projects that relate to Work at Intel go here",
    "create project project_one1 @Work11 | this is the first project I created",
    "create megaproject Work21 | 21all projects that relate to Work at Intel go here",
    "create project project_two1 @Work21 | this is the first project I created",
    "create project project_three1 @Work11 | this is the first project I created",
    "create project project_four1 @Work21 | this is the first project I created",
    "list @0000",
    "list @0000",
    "list @0000",
    "create project project_five1 @Work11 | this is the first project I created",
    #"turn_on",
    "task @project_one | 1this is what you need to do on project one",
    "task @project_one | 1another this is what you need to do on project one",
    "task @project_two | 1this is what you need to do on project two",
    "task @project_two1 | 1second this is what you need to do on project two",
    "task @project_two | 1third this is what you need to do on project two",
    "start @0000 | one1 this is some activity related to a taask",
    "start @0000 | two1 this is some activity related to a taask",
    "start @0000 | three1 this is some activity related to a taask",
    # "list @0000",
    "start @0000 | four1 this is some activity related to a taask",
    "start @0000 | five1 this is some activity related to a taask",
    "start @0000 | six1 this is some activity related to a taask",
    "start @0000 | seven1 this is some activity related to a taask",
    "stop @0000",
    "stop @0000",
    "stop @0000",
    "list @0000",
    "stop @0000",
    "stop @0000",
    "stop @0000",
    "list @0000",
    "cont @0000",
    "cont @0000",
    "cont @0000",
    "halt @0000",
    "halt @0000",
    "halt @0000",
    #
    'die',
]


test_responses = []

