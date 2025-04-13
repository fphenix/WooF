# =======================================================================================
# util module imported into fPhenix 2025 : Wheel Of Fortune
# A bunch of quality-of-life utils functions (static methods)
# =======================================================================================

# a bunch of small useful functions
import numpy

# ---------------------------------------------------------------------------------------
# return the word in str with its plural if nb > 1
# print(plural('horse', 1))                               # -> horse
# print(plural('horse', 3))                               # -> horses
# print(plural('Child', 1, 'Children', replace= True))    # -> Child
# print(plural('Child', 3, 'Children', replace= True))    # -> Children
# print(plural('sheep', 3, ''))                           # -> sheep
@staticmethod
def plural(str, nb, pl= 's', replace= False):
    if nb > 1:
        return pl if replace else str + pl
    else:
        return str

# ---------------------------------------------------------------------------------------
# return the value but clamped within and including min and max
@staticmethod
def clamp_between(val, minval, maxval):
    return max(minval, min(val, maxval))

# ---------------------------------------------------------------------------------------
# return the integer value but rotating it within and including min and max (integers)
# e.g.: min max = 0 9, if val = 10 return 0, if val = -1 return 9 else keep val
@staticmethod
def circulate(val, minval, maxval):
    if val > maxval:
        return minval
    if val < minval:
        return maxval
    else:
        return val 

# ---------------------------------------------------------------------------------------
# keep a float value between a min (including) and a max (excluping) like a modular operation % would do
# print(keepbetween(4.3, 2.2, 5.7))   #--->   4.3
# print(keepbetween(5.7, 2.2, 5.7))   #--->   2.2
# print(keepbetween(6.2, 2.2, 5.7))   #--->   2.7
# print(keepbetween(1.9, 2.2, 5.7))   #--->   5.4
# Note : rounding erros may occur (ex: print(keepbetween(5.9, 2.2, 5.7)) return 2.400...04 instead of 2.4)
@staticmethod
def keepbetween(val, minval, maxval):
    if val >= maxval:
        return minval + (val - maxval)
    elif val < minval:
        return maxval - (minval - val)
    else:
        return val

# ---------------------------------------------------------------------------------------
# remap the value val, currently ranging between boundary1 and boundary2
# to the new boundaries newbd1 and newbd2
@staticmethod
def remap(val, boundary1, boundary2, newbd1, nexbd2):
    return newbd1 + ((nexbd2 - newbd1) * ((val - boundary1) / (boundary2 - boundary1)) ) 


# ---------------------------------------------------------------------------------------
# Rotates a list to the right (direction -1 by default) or 
# to the left (if direction set to 1) by nb spots
@staticmethod
def rotate_list(lst, nb, direction= -1):
    return lst[direction*nb:] + lst[:direction*nb]


# ---------------------------------------------------------------------------------------
# replace the idx-th character (first has idx=0) from the string str with the charater char
# e.g.: print(char_replace('abcdef', 3, 'x')) return 'abcxef'
@staticmethod
def char_replace(str, idx, char):
    old_str = str
    new_str = old_str[:idx] + char + old_str[idx+1:]
    # Another algo could be :
    #          old_str = list(str)
    #          old_str[idx] = char
    #          new_str = ''.join(old_str)
    return new_str

# ---------------------------------------------------------------------------------------
# returns True if the color (r, g, b) is considered to be 
# 'light' or returns False if 'dark'
@staticmethod
def isColorLight(r, g, b):
    #Hue, Saturation, Perceived (square value)
    hsp_sq = (0.299 * r*r) + (0.587 * g*g) + (0.114 * b*b)
    #compare with central point at (255/2)²
    return hsp_sq > 16256.25