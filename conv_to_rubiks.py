from rubik.cube import Cube
import copy
import random

cube_to_str= lambda c: ''.join(c._color_list())

MOVE_SET = ['L', 'Li', 'R', 'Ri',
            'U', 'Ui', 'D', 'Di',
            'F', 'Fi', 'B', 'Bi',
            'M', 'Mi', 'E', 'Ei',
            'S', 'Si', 'X', 'Xi',
            'Y', 'Yi', 'Z', 'Zi']
MAX_DEPTH = 100
START_STATE="WWWWWWWWWGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY" # TODO: check that this is solved



def extract_faces(c):
    c_str = c.flat_str()
    # Extract the faces from the cube string   
    top = c_str[0:9]
    left = c_str[9:12] + c_str[21:24] + c_str[33:36]
    front =  c_str[12:15] + c_str[24:27] + c_str[36:39]
    right = c_str[15:18] + c_str[27:30] + c_str[39:42]
    back = c_str[18:21] + c_str[30:33] + c_str[42:45]
    bot = c_str[45:-1] 
    return top, left, front, right, back, bot

def rot_face_str(face_str):
    new_order = [
        7,4,1,
        8,5,2,
        9,6,3
    ]
    new_face = [face_str[i-1] for i in new_order]
    return ''.join(new_face)

def is_sln(c,face):
    # loop through each face
    for f in extract_faces(c):
        for _ in range(4):
            if face == f:
                return True
            face = rot_face_str(face)
            
    return False
            
            
            
def do_move(c, move):
    # make copy since moves are mutable transformations
    _c=copy.copy(c)
    # Do move. EG: c.L()
    getattr(_c, move)()

    return cube_to_str(_c)


def adjacent_states(s):
    c=Cube(s)
    adj=[]
    for move in MOVE_SET:
        # make copy since moves are mutable transformations
        _c=copy.copy(c)
        # Do move. EG: c.L()
        getattr(_c, move)()
        # TODO: maybe not add if already explored?
        adj.append(cube_to_str(_c))

    return adj

def random_walk(c, ntimes=100):
    path=[]
    for _ in range(ntimes):
        move=random.choice(MOVE_SET)
        path.append(move)
        getattr(c, move)()
    return path
        
visited_nodes = set()

limit_2_depth=lambda limit: MAX_DEPTH - limit

def dls(node, path, limit, face, debug=False):  #function for dfs 
    visited_nodes.add(node.flat_str())         
    
    if debug: print("depth - {depth} - {path}".format(depth=limit_2_depth(limit), path=path))
    
    if is_sln(node,face):
        print("\tFound Target State: {goal} at moveset {path}".format(goal=node, path=path))
        return True, path
        
    if limit <= 0:
        return False, None
        
    #if node not in visited:
    # randomize the order of the moves
    move_order = MOVE_SET.copy()
    random.shuffle(move_order)
    for move in move_order:
        neighbour=Cube(do_move(node, move))
        
        if neighbour.flat_str() not in visited_nodes:
            
            #print(f"Visiting {neighbour.flat_str()} with move {move} at depth {limit}")
            solved, path_s = dls(neighbour, path+(move,), limit-1, face)
            if solved:
                return True, path_s
        #print(f"Skipping {neighbour.flat_str()} with move {move} at depth {limit}")
          
    return False, None


def iddfs(start_state, max_depth, face, debug=False): 
    for depth in range(1, max_depth+1):
        if debug:
            print("\tExec Depth of {depth}".format(depth=depth))
        # clear visited nodes
        visited_nodes.clear()
        solved, path = dls(start_state, tuple(), depth, face)
        if not solved:
            if debug:
                print(f"No Solution Found at Depth {depth}, {len(visited_nodes)} nodes visited")
        else:
            return True, path
    if debug:
        print('No Solution Found at All')
    
    return False, None


def main():
    iddfs(start_state=Cube(START_STATE), max_depth=MAX_DEPTH, face="WWWWWWWOO")
    
if __name__ == "__main__":
    main()
