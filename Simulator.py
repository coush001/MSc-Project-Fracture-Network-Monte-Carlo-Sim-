import numpy as np
import matplotlib.pyplot as plt


def borehole(xmax, ymax):
    """
    Create a randomly orientated borehole given domain maxima
    
    Returns: LineString object
    """
    p1 = [np.random.ranf(1)* xmax, np.random.ranf(1)* ymax]
    p2 = [np.random.ranf(1)* xmax, np.random.ranf(1)* ymax]
    grad  = (p1[1]-p2[1]) / (p1[0]-p2[0])
    c = p1[1] - grad*p1[0]

    y0intercept = -c /grad
    ymaxintercept = (ymax - c) / grad
    xmaxintercept = grad * xmax + c
    x0intercept = c

    bp =[]
    if 0 <= y0intercept <= xmax:
        bp.append((y0intercept, 0))

    if 0 <= ymaxintercept <= xmax:
        bp.append((ymaxintercept, ymax))

    if 0 <= x0intercept <= ymax:
        bp.append((0, x0intercept))

    if 0 <= xmaxintercept <= ymax:
        bp.append((xmax, xmaxintercept))

    assert(len(bp)==2)
    x0 = bp[0][0]
    xf = bp[1][0]
    y0 = bp[0][1]
    yf = bp[1][1]
    length = np.sqrt((xf-x0)**2 + (yf-y0)**2)
    borehole = LineString([(x0, y0), (xf, yf)])
    ax.plot((x0, xf),(y0, yf), '--r', label='Boreholes')
    return borehole
    

#read file containing fracture start and end coordinates
file = open('FractureTips.txt', 'r')
lines = file.readlines()

# Initialise lists for storage
x0 = []
y0 = []
xf = []
yf = []

#Read lines and store values in respective lists
for line in lines:
    if line[0] != '#':
        line = line.rstrip('\n')
        line = line.split(',')
        assert(len(line) == 4)
        x0.append(float(line[0]))
        y0.append(float(line[1]))
        xf.append(float(line[2]))
        yf.append(float(line[3]))
        
# Max values of domain
ymax = max(max(y0),max(yf))
xmax = max(max(x0), max(xf))
        
# Create LineString objects of fractures        
frac_lines = [LineString([(x0[i],y0[i]),(xf[i], yf[i])]) for i in range(len(x0))] # linestring built correctly??
assert(len(frac_lines) == len(x0))

# Initilise Figure
fig = plt.figure(figsize=(16,8))
ax = plt.subplot(2,1,1)
for i in range(len(x0)):
    ax.plot((x0[i], xf[i]), (y0[i], yf[i]), '-b', linewidth=3)
    ax.set_title('Schematic Plot of fracture network and borehole samples')



# Number of Monte-Carlo Simulations
N = 50
# List to store the P10 Fracture density for each simulation (fracture isntances/length of borehole)
P10 = []
for n in range(N):
    #Define borehole    
    bh = borehole(xmax, ymax)
    bhlen = bh.length

    # Plot and compare borehole to fractures. Count crosses.
    count = 0
    for i in range(len(x0)):
        if frac_lines[i].crosses(bh):
                count += 1
                
    P10.append(count/bhlen)

ax2 = plt.subplot(2,1,2)
ax2.hist(P10, bins=20)
ax2.set_title('Distribution of P10 values for %i Simulations' % (N))
ax2.set_xlabel('P10 Value')
ax2.set_ylabel('Frequency')

plt.show()
