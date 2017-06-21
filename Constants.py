MAX_NUM_FREQ    = 128
TIME_WNDW_SIZE  = 320       # Maximum theoretical holding time is around 320

NumNodes        = 14
NumRes          = 500

guard_band  = 1
Lambda      = 1
Mu          = 0.05

FULL        = True
EMPTY       = False

NodeList        = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LinkList        = [
    ['AB', 1100], ['AC', 1600], ['AH', 2800],
    ['BC', 600], ['BD', 1000],
    ['CF', 2000],
    ['DE', 600], ['DK', 2400],
    ['EF', 1100], ['EG', 800],
    ['FJ', 1200], ['FM', 2000],
    ['GH', 700],
    ['HI', 700],
    ['IJ', 900], ['IL', 500], ['IN', 500],
    ['KL', 800], ['KN', 800],
    ['LM', 300],
    ['MN', 300]
    ]
TestLinkList    = [
    ['AB', 1100], ['AD', 10],
    ['BC', 5], ['BD', 500],
    ['AC', 2000]
    ]

TestResList = [
    ['AK', 0, 2, 10, 5]
]

N_NameIndex         = 0
N_CostIndex         = 1

L_NodePrIndex       = 0
L_LengthIndex       = 1

P_PathIndex         = 0
P_CostIndex         = 1

FWD_EndIndex        = 0
FWD_ResIndex        = 1

R_NodesIndex        = 0
R_ArrivIndex        = 1
R_StartIndex        = 2
R_HoldiIndex        = 3
R_NumSlIndex        = 4

LINK_RAND_MIN       = 300
LINK_RAND_MAX       = 3000

LINK_DNE            = 9999 + LINK_RAND_MAX
LINK_SELF           = 10000 + LINK_RAND_MAX

TERMINATE_CHAR      = '1'

ERR_INSTR           = 0
DON_INSTR           = 1
PAS_INSTR           = 2