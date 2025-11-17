from vpython import *

# TODO: Add line showing angle with no torque

# Window settings
scene.width = 640
scene.height = 480
scene.background = color.white
scene.title = "PHY 9C Midterm Problem Start 6 \n\n"
scene.align = "none"

# Display settings for shapes
axleRadius = 0.03
axleLength = 1.0
wireThickness = 0.05
wireLength = 0.80

# Axle object
axleShape = shapes.circle(radius = axleRadius, np = 64)
axlePath = [vec(0.0, 0.0, -axleLength / 2), vec(0.0, 0.0, axleLength / 2)]
axle = extrusion(shape = axleShape, path = axlePath, color = color.red)

# Wire loop object
wireShape = shapes.rectangle(width = wireThickness, height = wireThickness, roundness = 0.1)
wirePath = [vec(0.0, -axleRadius, -wireLength / 2), 
            vec(0.0, -axleRadius, wireLength / 2),
            vec(0.0, -axleRadius - wireLength, wireLength / 2), 
            vec(0.0, -axleRadius - wireLength, -wireLength / 2),  
            vec(0.0, -axleRadius + 0.01, -wireLength / 2)]
wireLoop = extrusion(shape = wireShape, path = wirePath, color = vec(0.75, 0.50, 0.25))

# Magnetic dipole moment vector
momentVec = arrow(pos = vec(0, -axleRadius - wireLength / 2, 0), axis = vec(-0.5, 0, 0), color = color.purple, 
                  opacity = 0.3, shaftwidth = 0.03, headwidth = 0.06, headlength = 0.09, visible = False)

system = compound([wireLoop, axle]) # Combine wire and axle

# Draw magnetic field
magneticField = []
for x in range(-4, 5):
    for z in range(-2, 3):
        xPos = x * 0.2
        zPos = z * 0.2
        arrow(pos = vec(xPos, -1, zPos), axis = vec(0, 2, 0), color = color.blue, opacity = 0.1, 
              shaftwidth = 0.02, headwidth = 0.04, headlength = 0.06)

# Animation
refreshRate = 30 # How many times the screen refreshes per second (Hz)
t = 0 # Total elapsed time
dt = 1 / refreshRate # Timestep (s)
g = 9.8 # Gravitational constant (N/kg)
a = 1 # Side length of square wire loop (m)
i = 1 # Current through wire loop (A)
l = 1 # Linear mass density of wire loop (kg/m)
B = 10 # Magnetic field strength (T)

I = (5.0/3.0)*l*a**3 # Moment of inertia
u = i*a**2 # Magnetic dipole moment magnitude

# Angles are measured clockwise from downward vertical, in radians
thetaCenter = atan(i*B/(2*l*g)) # Angle where there is no net torque on the system
thetaInitial = radians(60) # Initial angle of system
thetaDotInitial = 0 # Initial angular velocity of system
theta = thetaInitial # Current angle
theta0 = thetaInitial - thetaDotInitial * dt # Previous angle
thetaDotDotInitial = -(6*g/(5*a))*sin(theta) + (3*i*B/(5*l*a))*cos(theta) 

system.rotate(axis = vec(0, 0, -1), angle = theta, origin = vec(0, 0, 0)) # Align system with initial theta
momentVec.rotate(axis = vec(0, 0, -1), angle = theta, origin = vec(0, 0, 0)) # Align moment vector with initial theta

# Set up stats display on top of scene
scene.append_to_title("Angular displacement: ")
thetaText = wtext(text = '{:.3f}'.format(thetaInitial), pos = scene.title_anchor)
scene.append_to_title(" rad \n")
scene.append_to_title("Angular velocity: ")
thetaDotText = wtext(text = '{:.3f}'.format(thetaDotInitial), pos = scene.title_anchor)
scene.append_to_title(" rad/s \n")
scene.append_to_title("Angular acceleration: ")
thetaDotDotText = wtext(text = '{:.3f}'.format(thetaDotDotInitial), pos = scene.title_anchor)
scene.append_to_title(" rad/s<sup>2</sup> \n\n")

scene.append_to_title("Angle with no net torque:", '{:.3f}'.format(thetaCenter), "rad \n")
scene.append_to_title("Moment of inertia:", '{:.3f}'.format(I), "kg*m<sup>2</sup> \n")
scene.append_to_title("Magnitude of magnetic dipole moment: ", '{:.3f}'.format(u), "A*m<sup>2</sup> \n\n")

scene.append_to_title("Side length of wire loop: ", '{:.3f}'.format(a), "m \n")
scene.append_to_title("Current through wire loop: ", '{:.3f}'.format(i), "A \n")
scene.append_to_title("Linear mass density of wire loop: ", '{:.3f}'.format(l), "kg/m \n")
scene.append_to_title("Magnetic field strength: ", '{:.3f}'.format(B), "T \n\n")


# Set up energy graphs
g1 = graph(title = "Energy graphs", xtitle = "Time (s)", ytitle = "Energy (J)", scroll = True, xmin = 0, xmax = 5)
energy = gcurve(color = color.black, label = "E<sub>total</sub>")
kinetic = gcurve(color = color.red, label = "K<sub>total</sub>")
potentialGrav = gcurve(color = color.green, label = "U<sub>g</sub>")
potentialMag = gcurve(color = color.blue, label = "U<sub>B</sub>")

# Pause button, taken from double pendulum example on vpython web
run = False # Program starts paused
def pause(btn):
    global run
    run = not run # Toggle run
    # Update button text
    if run:
        btn.text = "Pause"
    else:
        btn.text = "Resume"
pauseBtn = button(text = "Resume", bind = pause, pos = scene.title_anchor) # Create pause button

# Reset button
def reset():
    global t, theta, theta0, energy, kinetic, potentialGrav, potentialMag, g1
    thetaOffset = thetaInitial - theta # Displacement from initial theta
    # Rotate system back to initial conditions
    system.rotate(axis = vec(0, 0, -1), angle = thetaOffset, origin = vec(0, 0, 0))
    momentVec.rotate(axis = vec(0, 0, -1), angle = thetaOffset, origin = vec(0, 0, 0)) 
    momentVec.visible = False
    t = 0
    theta = thetaInitial
    theta0 = thetaInitial - thetaDotInitial * dt
    energy.data = []
    kinetic.data = []
    potentialGrav.data = []
    potentialMag.data = []   
    g1.xmin = 0
    g1.xmax = 5
    thetaText.text = '{:.3f}'.format(thetaInitial)
    thetaDotText.text = '{:.3f}'.format(thetaDotInitial)
    thetaDotDotText.text = '{:.3f}'.format(thetaDotDotInitial)
resetBtn = button(text = "Reset", bind = reset, pos = scene.title_anchor) # Create pause button

# Button to toggle magnetic dipole moment display
def toggleMoment(btn):
    # Update button text
    if (momentVec.visible):
        btn.text = "Show moment"
    else:
        btn.text = "Hide moment"
    momentVec.visible = not momentVec.visible # Toggle visibility
toggleMomentBtn = button(text = "Show moment", bind = toggleMoment, pos = scene.title_anchor)

# Animation loop
while True:
    rate(refreshRate) # Needed for smooth animation
    if not run: continue # Skip updates if paused

    # Calculate angular acceleration, derived from midterm problem start
    thetaDotDot = -(6*g/(5*a))*sin(theta) + (3*i*B/(5*l*a))*cos(theta) 
    temp = theta
    theta = 2*theta - theta0 + thetaDotDot*dt**2 # Verlet integration
    theta0 = temp # Current theta becomes previous theta
    dtheta = theta - theta0 # Change in theta
    system.rotate(axis = vec(0, 0, -1), angle = dtheta, origin = vec(0, 0, 0)) # Rotate system by dtheta
    momentVec.rotate(axis = vec(0, 0, -1), angle = dtheta, origin = vec(0, 0, 0)) # Rotate moment vector by dtheta

    # Update energy graph
    thetaDot = (theta - theta0) / dt # Current angular velocity
    avgTheta = (theta + theta0) / 2 # Use average angle for accuracy
    K = 0.5*I*thetaDot**2 # Kinetic energy of system
    Ugrav = -2*g*l*(a ** 2)*cos(avgTheta) # Gravitational potential energy of system
    Umag = -i*(a**2)*B*sin(avgTheta) # Potential energy from magnetic dipole moment
    Etot = K + Ugrav + Umag
    energy.plot(t, Etot)
    kinetic.plot(t, K)
    potentialGrav.plot(t, Ugrav)
    potentialMag.plot(t, Umag)

    # Update stats
    thetaText.text = '{:.3f}'.format(avgTheta)
    thetaDotText.text = '{:.3f}'.format(thetaDot)
    thetaDotDotText.text = '{:.3f}'.format(thetaDotDot)

    t += dt # Update elapsed time