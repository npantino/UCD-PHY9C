from vpython import *

# TODO: Add dielectric option

# Window settings
scene.width = 640
scene.height = 480
scene.background = color.white
scene.title = "PHY 9C Midterm Problem Start 8 \n\n"
scene.align = "none"
scene.camera.pos = vec(0, 0, 4) # Move camera backward

# Battery object
battery = cylinder(pos = vec(-3, 0, 2), axis = vec(0, 0, 1), radius = 0.2, color = color.orange)

# Resistor object
resistor = curve(pos = [vec(-3, 0, 1), vec(-2.8, 0, 0.9), vec(-3.2, 0, 0.8), 
                        vec(-2.8, 0, 0.7), vec(-3.2, 0, 0.6), vec(-2.8, 0, 0.5), vec(-3.2, 0, 0.4), vec(-3, 0, 0.3)],
                          radius = 0.05, color = color.red) 

# Switch object
switch1 = cylinder(pos = vec(0, 0, 0), axis = vec(0, 0, -1.414), radius = 0.1, color = vec(0.5, 0.5, 0.5))

# Inductor object
inductor = helix(pos = vec(0.3, 0, 1), axis = vec(0, 0, 1), radius = 0.3, thickness = 0.05, color = color.purple)

# Capacitor object
capTop = box(pos = vec(3, 0, 1.25), axis = vec(0.5, 0, 0), length = 0.5, height = 0.5, width = 0.1, color = color.yellow)
capTop = box(pos = vec(3, 0, 1.75), axis = vec(0.5, 0, 0), length = 0.5, height = 0.5, width = 0.1, color = color.yellow)

# Dielectric object
dielectric = box(pos = vec(3.5, 0, 1.5), axis = vec(0.5, 0, 0), length = 0.5, height = 0.5, width = 0.3, color = color.black)

# Connecting wires
wire1 = curve(pos = [vec(-3, 0, 2), vec(-3, 0, 1)], radius = 0.05, color = color.black) # Battery to resistor
wire2 = curve(pos = [vec(-3, 0, 0.3), vec(-3, 0, -1), vec (-1, 0, -1)], radius = 0.05, color = color.black) # Resistor to switch
wire3 = curve(pos = [vec(-3, 0, 3), vec(-3, 0, 4), vec(3, 0, 4)], radius = 0.05, color = color.black) # Switch to bottom
wire4 = curve(pos = [vec(0, 0, 0), vec(0, 0, 1)], radius = 0.05, color = color.black) # Switch to inductor
wire5 = curve(pos = [vec(0, 0, 2), vec(0, 0, 4)], radius = 0.05, color = color.black) # Inductor to bottom
wire6 = curve(pos = [vec(1, 0, -1), vec(3, 0, -1), vec(3, 0, 1.25)], radius = 0.05, color = color.black) # Switch to capacitor
wire7 = curve(pos = [vec(3, 0, 1.75), vec(3, 0, 4)], radius = 0.05, color = color.black) # Capacitor to bottom

# Calcs
refreshRate = 60
dt = 1.0 / refreshRate # Timestep
t = 0 # Total elapsed time
switchState = 1 # Switch starts in middle
iL = 0 # Inductor current downward
vL = 0 # Inductor voltage downward
vC = 0 # Capacitor voltage downward
vR = 0 # Resistor voltage upward

# System parameters
emf = 12 # Voltage of emf source
R = 1 # Resistance of resistor in ohms
L = 1 # Inductance of inductor in henries
C0 = 1 # Capacitance of capacitor in farads, in vacuum
C = C0 # Current capacitance of capacitor
K = 2 # Dielectric constant of dielectric

# Display stats on top of scene
scene.append_to_title("Elapsed time: ")
tText = wtext(text = '{:.3f}'.format(0), pos = scene.title_anchor)
scene.append_to_title(" s \n")
scene.append_to_title("Inductor current downward: ")
iLText = wtext(text = '{:.3f}'.format(0), pos = scene.title_anchor)
scene.append_to_title(" A \n")
scene.append_to_title("Inductor voltage downward: ")
vLText = wtext(text = '{:.3f}'.format(0), pos = scene.title_anchor)
scene.append_to_title(" V \n")
scene.append_to_title("Capacitor voltage downward: ")
vCText = wtext(text = '{:.3f}'.format(0), pos = scene.title_anchor)
scene.append_to_title(" V \n")
scene.append_to_title("Resistor voltage upward: ")
vRText = wtext(text = '{:.3f}'.format(0), pos = scene.title_anchor)
scene.append_to_title(" V \n")

# Method to move dielectric
scene.append_to_title("Fraction of dielectric in capacitor: ")
dieText = wtext(text = '{:.3f}'.format(0), pos = scene.title_anchor)
scene.append_to_title("\n\n")
def moveDielectric(evt):
    if (evt.id == "die"):
        dielectric.pos = vec(3.5 - evt.value, 0, 1.5)
        dieText.text = evt.value * 2

dielectricSlider = slider(bind = moveDielectric, min = 0, max = 0.5, step = 0.005, value = 3.5 - dielectric.pos.x, id = "die", pos = scene.title_anchor)
scene.append_to_title("\n\n")


# TODO: Add resistor voltage
g1 = graph(title="Current graph", xtitle="Time (s)", ytitle="Current (A)", scroll=True, xmin=0, xmax=5)
current = gcurve(color=color.black, label="I<sub>L</sub>")

g2 = graph(title="Voltage graph", xtitle="Time (s)", ytitle="Voltage (V)", scroll=True, xmin=0, xmax=5)
inductorVoltage = gcurve(color=color.purple, label="V<sub>L</sub>")
capacitorVoltage = gcurve(color=color.yellow, label="V<sub>C</sub>")
resistorVoltage = gcurve(color=color.red, label="V<sub>R</sub>")

# Pause button, taken from double pendulum example on vpython web
run = True # Program starts running
def pause(btn):
    global run
    run = not run # Toggle run
    # Update button text
    if run:
        btn.text = "Pause"
    else:
        btn.text = "Resume"
pauseBtn = button(text = "Pause", bind = pause, pos = scene.title_anchor) # Create pause button

# Button to toggle switch
# Three states, left (0), middle (1), right (2)
def toggleSwitchLeft(btn):
    global switchState
    if (switchState == 1):
        switch1.rotate(axis = vec(0, 1, 0), angle = pi/4, origin = vec(0, 0, 0))
    if (switchState == 2):
        switch1.rotate(axis = vec(0, 1, 0), angle = pi/2, origin = vec(0, 0, 0))
    switchState = 0
toggleSwitchLeftBtn = button(text = "Switch left", bind = toggleSwitchLeft, pos = scene.title_anchor)
def toggleSwitchMiddle(btn):
    global switchState
    if (switchState == 0):
        switch1.rotate(axis = vec(0, 1, 0), angle = -pi/4, origin = vec(0, 0, 0))
    if (switchState == 2):
        switch1.rotate(axis = vec(0, 1, 0), angle = pi/4, origin = vec(0, 0, 0))
    switchState = 1
toggleSwitchLeftBtn = button(text = "Switch middle", bind = toggleSwitchMiddle, pos = scene.title_anchor)
def toggleSwitchRight(btn):
    global switchState
    if (switchState == 0):
        switch1.rotate(axis = vec(0, 1, 0), angle = -pi/2, origin = vec(0, 0, 0))
    if (switchState == 1):
        switch1.rotate(axis = vec(0, 1, 0), angle = -pi/4, origin = vec(0, 0, 0))
    switchState = 2
toggleSwitchLeftBtn = button(text = "Switch right", bind = toggleSwitchRight, pos = scene.title_anchor)

# Reset function
def reset():
    global t, iL, vL, vC, vR, C, C0, dielectricSlider, dielectric, switchState
    
    # Reset switch to middle
    if (switchState == 0):
        switch1.rotate(axis = vec(0, 1, 0), angle = -pi/4, origin = vec(0, 0, 0))
    if (switchState == 2):
        switch1.rotate(axis = vec(0, 1, 0), angle = pi/4, origin = vec(0, 0, 0))
    switchState = 1

    # Reset other variables
    t = 0
    iL = 0
    vL = 0
    vC = 0
    vR = 0

    # Reset dielectric
    C = C0
    dielectricSlider.value = 0
    dielectric.pos = vec(3.5, 0, 1.5)

    # Reset graphs
    g1.xmin = 0
    g1.xmax = 5
    g2.xmin = 0
    g2.xmax = 5

    current.data = []
    inductorVoltage.data = []
    capacitorVoltage.data = []
    resistorVoltage.data = []

    # Reset stats display
    tText.text = '{:.3f}'.format(0)
    iLText.text = '{:.3f}'.format(0)
    vLText.text = '{:.3f}'.format(0)
    vCText.text = '{:.3f}'.format(0)
    vRText.text = '{:.3f}'.format(0)

resetBtn = button(text = "Reset", bind = reset, pos = scene.title_anchor)
# Animation loop
while True:
    rate(refreshRate) # Needed for smooth animation
    if not run: continue # Skip animation when paused

    # Update dielectric of capacitor
    Cprev = C # Store previous die const
    fracDie = dielectricSlider.value * 2 # Actual fraction of dielectric inside cap, updated
    k = 1 - fracDie + K*fracDie # New dielectric constant of cap
    C = k*C0 # New capacitance
    vC /= C/Cprev # Update capacitor voltage (more dielectric, weaker electric field, less voltage)

    # Case 0: Switch left, charging RL circuit
    # 1st order ODE, Euler integration
    if (switchState == 0):
        diL = dt*(emf - R*iL)/L
        iL += diL
        vL = emf - R*iL
        vR = iL * R

    # Case 1: Switch middle, constant inductor current, no inductor voltage or resistor voltage
    if (switchState == 1):
        vL = 0
        vR = 0
    
    # Case 2: Switch right, oscillating LC circuit
    # Velocity Verlet Integration
    if (switchState == 2):
        vn = vC/L
        an = -iL/(L*C)
        iL += vn*dt + 0.5*an*dt**2
        an1 = -iL/(L*C)
        vn += 0.5*(an + an1)*dt
        vC = vn*L
        vL = vC
        vR = 0

    # Update graphs
    current.plot(t, iL)
    inductorVoltage.plot(t, vL)
    capacitorVoltage.plot(t, vC)
    resistorVoltage.plot(t, vR)

    # Update text
    tText.text = '{:.3f}'.format(t)
    iLText.text = '{:.3f}'.format(iL)
    vLText.text = '{:.3f}'.format(vL)
    vCText.text = '{:.3f}'.format(vC)
    vRText.text = '{:.3f}'.format(vR)

    t += dt # Update elapsed time



