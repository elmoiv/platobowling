import pyautogui as pg
import pygetwindow as pw
import PIL.ImageGrab, time, autopy

sleep = time.sleep

# (x, y, z)
# (x, y) of bright color on pin top
# (z) the corresponding x of the ball
#     for accurate shooting
PINS = [
        (890, 226, 764),
        (906, 229, 820),
        (923, 232, 890),
        (924, 226, 890),
        (939, 235, 939),
        (940, 229, 939),
        (958, 232, 991),
        (956, 225, 991),
        (974, 229, 1060),
        (990, 226, 1116)
    ]

# https://stackoverflow.com/a/55132370
# edited
def group_numbers(lst):
    substr = ""
    sub_list = []
    prev_digit = lst[0].isdigit()

    for char in lst:
        # if the character's digit-ness is different from the last one,
        #    then "tie off" the current substring and start a new one.
        this_digit = char.isdigit()
        if this_digit != prev_digit:
            sub_list.append(substr)
            substr = ""
            prev_digit = this_digit

        substr += char
    sub_list.append(substr)

    # Return filtered from '.' string
    return [i for i in sub_list if '.' not in i]

# Trying to hit those single pins
# if we have pins 0, 2, 4
# we manage to get the middle and shoot them all
# rather than shooting the outer right only
def single_targets(grps):
    grps = list(map(int, grps))
    dists = []
    
    for n, i in enumerate(grps):
        if n:
            a1, a2 = grps[n - 1], i
            dist = PINS[a2][2] - PINS[a1][2]
            if dist < 70:
                dists.append((a1, a2, dist))
    
    if len(dists) == 2:
        x, y = dists
        if x[1] == y[0]:
            return [x[0], x[1], y[1]], 3
    
    if len(dists) == 1:
        return [dists[0][0], dists[0][1]], 2
    
    return 0

def get_target(scr):
    print('------------------------------')
    existed = list('0123456789')

    # Detect pins
    for n, pin in enumerate(PINS):
        x, y, _ = pin
        
        # exist if bright color
        if not all(bit > 180 for bit in scr[x, y]):
            existed[n] = '.'

    # Get max pins together
    groups = group_numbers(existed)
    max_group = max(groups, key=len)
    max_len = len(max_group)

    print('Max group is: ', max_group, ':', max_len)
    
    # If single pins with space between then
    if max_len == 1 and len(groups) > 1:
        print('PINS: Single with spaces!')
        d = single_targets(groups)
        if d:
            print('Max group changed to: ', end='')
            max_group, max_len = d
    
    print(max_group, ':', max_len)
    
    # If no pins found
    if max_len == 0:
        return None

    # If all pins exist
    if max_len == 10:
        print('10 PINS')
        return 920

    p2 = int(max_group[max_len // 2])
    p1 = int(max_group[max_len // 2 - 1])
    
    # X cord if odd pins exist
    if max_len % 2:
        print('Odd PINS: ', max_len)
        return PINS[p2][2] + 6

    # If even, get the middle
    else:
        print('Even PINS: ', max_len)
        middle = PINS[p2][2] - PINS[p1][2]
        return PINS[p1][2] + middle // 2

def detect_window(name):
    if name in pw.getAllTitles():
        emulator = pw.getWindowsWithTitle(name)[0]
        emulator.maximize()

def drag_ball_to(x, y):
    pg.mouseDown()
    autopy.mouse.smooth_move(x, y)
    # Small cooldown to avoid ball slide away
    sleep(0.2)
    pg.mouseUp()

def main():
    while 1:

        # Detect LDPlayer and maximize
        detect_window('LDPlayer')
        sleep(2)

        # Read the screen colors
        screen = PIL.ImageGrab.grab().load()

        # When my turn and ball exists
        if screen[1060, 123] == (22, 135, 239) and \
           screen[875, 844] == (12, 11, 10):

            # Move pointer to ball position
            pg.moveTo(875, 843)

            # Decide where to shoot
            x_pos = get_target(screen)

            # Drag to detected x cord and shoot
            # 775
            drag_ball_to(x_pos, 775)
            sleep(1.5)
            drag_ball_to(x_pos, 735)

if __name__ == '__main__':
    main()