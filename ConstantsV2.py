MAX_NUM_FREQ    = 6
TIME_WNDW_SIZE  = 5000       # Initial time window size
MAX_SLOT_SIZE   = 12.5
MAX_REQ_SIZE    = 200
STRT_WNDW_SIZE  = 0
STRT_WNDW_RANGE = STRT_WNDW_SIZE + 1

SMALL = True
LARGE = False
SMALL_OR_LARGE_WINDOW   = SMALL

AVAIL_SLOTS_INDEX   = 0     # Index of available slots is the last index in the array
TIME_WINDOW_INDEX   = 1     # index of actual implementation of time window

NumNodes        = 14
NumRes          = 10000
NumTrials       = 1
NumLambdas      = 1

guard_band      = 1
Mu              = 0.05

PROV            = 4
START           = 3
FULL            = 2
EMPTY           = 1

# First nineteen take roughly 1.36 hours
# total takes about 1.55 hours
# 7/26/17
LambdaList = [
    2.3, 2.5, 2.7, 2.9,
    3.1, 3.3, 3.5, 3.7, 3.9,
    4.1, 4.3, 4.5, 4.7, 4.9,
    5.1, 5.3, 5.5, 5.7, 5.9,
    6.1, 6.3, 6.5, 6.7, 6.9,
    7.1, 7.3, 7.5, 7.7, 7.9,
    8.1, 8.3, 8.5, 8.7, 8.9,
    9.1, 9.3, 9.5, 9.7
]

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

# R_NodesIndex        = 0
# R_ArrivIndex        = 1
# R_StartIndex        = 2
# R_HoldiIndex        = 3
# R_NumSlIndex        = 4

TestResList = [
    ['AB', 1, 1, 5, 2],
    ['AB', 2, 5, 3, 2],
    ['AB', 3, 3, 4, 2],
    ['AB', 4, 7, 4, 2],
    ['AB', 5, 6, 3, 2],
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

PRV_SSlotIndex      = 0
PRV_SDepthIndex     = 1
PRV_ESlotIndex      = 2
PRV_EDepthIndex     = 3

LINK_RAND_MIN       = 300
LINK_RAND_MAX       = 3000

LINK_DNE            = 9999 + LINK_RAND_MAX
LINK_SELF           = 10000 + LINK_RAND_MAX

TERMINATE_CHAR      = '1'

ERR_INSTR           = 0
DON_INSTR           = 1
PAS_INSTR           = 2
BLK_INSTR           = 3

MIN_INSTR           = ERR_INSTR
MAX_INSTR           = BLK_INSTR