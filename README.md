
[images_path]: images/

<img src="images/md_title.png" width="750"/>
<img src="images/front_panel_cropped.png" width="1000"/>

# <a href="https://nelson-n.github.io/Mark1.github.io/">Mark 1 Resin 3d Printer</a>

**Mark 1** is an open-source resin 3d printer capable of printing at variable print size and resolution.
* Maximum Print Size: 230mm by 130mm at 120 micron resolution with 500mm focal length lens.
* Medium Print Size: 190mm by 110mm at 100 micron resolution with 300mm focal length lens.
* Minimum Print Size: 150mm by 80mm at 80 micron resolution with 200mm focal length lens.
* Max Print Height: 220mm.
* Sub 3 second layer cure times.
* Variable move speed, lift speed, and cure time.
* Quick detach build plate, internal heater with automatic temperature control, automatic lens shutter.

## Directory

* [Notes](#Notes)
    * [Troubleshooting](#Troubleshooting)
    * [G-code](#G-code)
    * [Movement](#Movement)
    * [Resin Profile Settings](#Resin-Profile-Settings)
    * [General Notes](#General-Notes)
    * [Dimensions](#Dimensions)
* [Parts](#Parts)
    * [Electronics](#Electronics)
    * [Motors](#Motors)
    * [Projector](#Projector)
    * [Resin Vat](#Resin-Vat)
    * [Linear Movement](#Linear-Movement)
    * [Frame](#Frame)
    * [Exterior Cover](#Exterior-Cover)
    * [Bolts](#Bolts)
* [Software Setup](#Software-Setup)
    * [Raspberry Pi Setup](#Raspberry-Pi-Setup)
    * [Arduino and RAMPS Board Setup](#Arduino-and-RAMPS-Board-Setup)
    * [Stepper Motor Setup](#Stepper-Motor-Setup)
    * [Servo Motor Setup](#Servo-Motor-Setup)
    * [Arduino and RAMPS Software Install](#Arduino-and-RAMPS-Software-Install)
    * [Verify RAMPS Functionality](#Verify-RAMPS-Functionality)
    * [Install and Launch NanoDLP](#Install-and-Launch-NanoDLP)
    * [NanoDLP Settings](#NanoDLP-Settings)
    * [Projector Setup](#Projector-Setup)
    * [Controlling Projector Power via Pi](#Controlling-Projector-Power-via-Pi)
    * [Controlling Heater via Pi](#Controlling-Heater-via-Pi)
    * [Mark 1 Software Setup](#Mark1-Software-Setup)
* [Manufacturing](#Manufacturing)
    * [General Manufacturing Notes](#General-Manufacturing-Notes)
    * [Linear Rail Manufacturing](#Linear-Rail-Manufacturing)
    * [Resin Vat Manufacturing](#Resin-Vat-Manufacturing)
    * [Build Plate Angle Mount Manufacturing](#Build-Plate-Angle-Mount-Manufacturing)
    * [Build Plate Strut Manufacturing](#Build-Plate-Strut-Manufacturing)
    * [Build Plate Manufacturing](#Build-Plate-Manufacturing)
    * [Motor Mount Plate Manufacturing](#Motor-Mount-Plate-Manufacturing)
    * [Projector Backplate Manufacturing](#Projector-Backplate-Manufacturing)
    * [Stabilizer Mount Manufacturing](#Stabilizer-Mount-Manufacturing)
    * [Endstop Mount Manufacturing](#Endstop-Mount-Manufacturing)
    * [Lens Holder Manufacturing](#Lens-Holder-Manufacturing)
    * [Shutter Manufacturing](#Shutter-Manufacturing)
    * [Hinge Jig Manufacturing](#Hinge-Jig-Manufacturing)
    * [Back Panel Manufacturing](#Back-Panel-Manufacturing)
    * [Side Panel 1 Manufacturing](#Side-Panel-1-Manufacturing)
    * [Side Panel 2 Manufacturing](#Side-Panel-2-Manufacturing)
    * [Side Window Manufacturing](#Side-Window-Manufacturing)
    * [Lower Front Panel Manufacturing](#Lower-Front-Panel-Manufacturing)
    * [Upper Front Panel Manufacturing](#Upper-Front-Panel-Manufacturing)
    * [Top Panel Manufacturing](#Top-Panel-Manufacturing)
    * [Bottom Panel Manufacturing](#Bottom-Panel-Manufacturing)
    * [Decal Manufacturing](#Decal-Manufacturing)
* [Construction](#Construction)
    * [Resin Vat Construction](#Resin-Vat-Construction)
    * [Frame Construction](#Frame-Construction)
    * [Internals Construction](#Internals-Construction)
    * [Panel Construction](#Panel-Construction)
* [Assembly](#Assembly)
    * [Projector Backplate Assembly](#Projector-Backplate-Assembly)
    * [Projector Backplate Electronics Assembly](#Projector-Backplate-Electronics-Assembly)
    * [Bottom Panel Assembly](#Bottom-Panel-Assembly)
    * [Full Frame Printer Assembly](#Full-Frame-Printer--Assembly)
* [Calibration](#Calibration)
    * [Lens Calibration](#Lens-Calibration)
    * [Quality Checks](#Quality-Checks)

## Notes<a name="Notes"></a>

### Troubleshooting<a name="Troubleshooting"></a>
* **If wifi and ssh connection to Raspberry Pi is not working.**
    * Occasionally the Raspberry Pi boots and is unable to connect to the wifi. 
    * Resolve this issue by turning the Pi off, resetting the wifi router, then rebooting the Pi.
    * If connection problems persist, connect the Raspberry Pi a wifi router via ethernet cable and then try connecting.
    * Note that the connection to the Raspberry Pi can be monitored with a simple `ping` command from a terminal/shell.
* **If wifi and ssh connection to Raspberry Pi is not working.**
    * The wifi router may re-assign the Raspberry Pi to a new IP address. Use the tool https://www.nanodlp.com/dashboard to find the newly assigned IP address and change your connection/ssh accordingly.
* **Printed object is positioned in the middle of the build plate despite manually moving the object in CAD.**
    * In order to move the location of the print, when slicing the object select: Advanced Options -> Auto Center: Disable.
* **When manually moving the stepper motors in NanoDLP, the motor moves up or down at full speed ad-infinitum.**
    * This occurs because the motor thinks that it is from far from Z position 0, and the motor tries to quickly zero itself.
    * Resolve this issue by arbitrarily setting the current motor position to 0 with the G-code command: **G92 Z0**
    * All Z movement will now be relative to this 0 point. For example, moving up 1mm either with the NanoDLP raise 1mm button or with the G-code command **G1 Z1 F200** will move the motors up 1mm relative to the 0 point.
* **Need to change a setting on the Raspberry Pi, but NanoDLP turns Pi display into a blank screen.**
    * To terminate NanoDLP ssh into the pi and run:
    * **sudo systemctl disable nanodlp**
    * **sudo systemctl stop nanodlp**
* **Motor is not making any sound nor responding to any move commands.**
    * This may occur because the Vref is set too low and the stepper motors are not receiving sufficient voltage.
    * Resolve this issue by turning the screw on the A4988 (DRV8825)  motor driver clockwise.
* **Z-axis movement is strange. Motor is stalling, distance moved is incorrect, number of pulses per mm is incorrect, etc.**
    * This may be caused by incorrect settings in the marlin configuration.h file that is sourced when NanoDLP boots.
    * To check these default settings, open the RAMPS terminal after launching NanoDLP to check the default G-code that is sourced from configuration.h.
* **Z-axis movement is strange. 1mm movement button raises the build plate by more than 1mm. 100 pulse button turns the stepper motor too much or too little.**
    * This may be caused by an incorrect steps per unit setting.
    * Resolve this issue by running the G-code command **M92 Z400**, for details see the *Calibrating Z Axis* section.
    * Note that to make this change permanent, the G-code start up code box and G-code print start box must be altered to include **M92 Z400**.
* **Z-axis movement is double what is should be. The build plate moves 2mm for a 1mm move command.**
    * The stepper motor pulsing or microstepping is randomly thrown off. Measure the movement of the build plate in response to a 1mm move command to confirm that the movement is inaccurate.
    * If movement is double, fix this by running the G-code command **M92 Z200** to reduce the number of pulses per 1mm of movement.
    * Note that to make this change permanent, the G-code Bootup Code box and G-code print start box must be altered to include **M92 Z200**.
    * Both of these boxes can be find in System -> Machine Settings -> Code / Gcode.
* **NanoDLP commands are not running in the correct order.**
    * For example, the projector begins displaying the first burn in layer before the built plate has finished descending into the resin vat.
    * Resolve this issue by assuring that the command **[[WaitForDoneMessage]]** is placed after every move command such as **G28** and **G1** in the G-code.
    * For aditional information on this issue see the **Start of Print Code** documentation.
* **First layer of print sticks to resin vat instead of build plate.**
    * Resin may now be warm enough, wait for built-in heater to raise the ambient temperature to the required level.
* **You want to adjust the Z-lift height or other esoteric settings of a resin profile.**
    * A number of resin profile settings including Z-lift height and after layer wait time cannot be adjusted using the NanoDLP web interface. The only way to adjust these settings is to manually alter the resin profile .json file.
    * In general, it is better to edit the .json file of a resin profile than to edit the profile using the NanoDLP web interface as the layout is clearer and offers more control over the settings. 

<div style="page-break-after: always;"></div>

### G-code<a name="G-code"></a>

* For a list of G-codes: https://marlinfw.org/docs/gcode/G028.html  

#### Positioning
* Find current position: **M114**
* Set the Z-axis 0 position to the current position: **G92 Z0**
* Home the Z-axis: **G28 Z0**
    * This moves the motors up until the endstop is triggered, from here it will move to point 0.
* Move stepper motor to the floor (position 0): **G1 Z0**
* Move stepper motor up to 100mm (position 100): **G1 Z100**

#### Movement
* Move stepper motor, controlling for speed: **G1 Z90 F200**
    * **F** controls the movement rate of the stepper motor, **Z90** moves to 90mm above the floor.
* Change default stepper motor speed: **G1 F100**
    * Changes all subsequent move commands such as **G1 Z20** to the speed 100.
* Set motor acceleration: **M201**
    * Alters how quickly the motor accelerates to the top speed specified by **F**.
    * **M201 Z1** is a slow acceleration and **M201 Z25** is an immediate acceleration.
    * Current set by default to **M201 Z4**.
* Set steps per unit: **M92 Z400**.
    * Sets how many steps (pulses) should be set to the stepper motor per mm of movement.
    * For details see the *Calibrating Z Axis* section.
* Dwell in the same position for a set period of time: **G4 P500**
    * Pauses the command queue and waits for a set period of time.
    * **G4 P1000** dwells for 1 second, **G4 P500** dwells for a half second.

#### Endstops and Servo Motors
* Test endstop activation: **M119**
* Trigger servo: **M280 P0 S255**
    * P0 sends the command goes to pin 0 (D11 on RAMPS 1.4 board).
    * S255 sets the servo position, use **M280 P0 S0** to close the servo.

#### Random
* Set units to mm: **G21**
    * By default **G21** is run an units are set to mm.
* Set max feedrate: **M203**
    * Does not seem to alter motor movement at all, currently set by default to **M203 Z20**.
* Set units to absolute positioning: **G90**
    * Sets units so that they are in absolute terms relative to a 0 point. Thus a command like **G1 Z10** moves to the absolute point of 10mm above 0, no matter the current Z location of the build plate.
    * The opposite of this is relative positioning, where a command like **G1 Z10** moves the motors up 10mm relative to the last position. Relative positioning can be set with the command **G91**.
* Display all stepper motor movement settings: **M503**
    * Displays movement settings such as M201 acceleration setting and M205 jerk setting.

<div style="page-break-after: always;"></div>

### Movement<a name="Movement"></a>

#### Z-Axis Steps per mm Setting

* Nema 17 stepper motors have a 1.8 degree step angle, for each step (pulse) the motor turns 1.8 degrees.
* The A4988 motor driver is set to utilize 1/16 microstepping by connecting all pins under the motor driver. Each step (pulse) is split into 16 steps (pulses).
* The leadscrews have an 8mm pitch, thus each 360 degree rotation of the stepper motor moves the build plate up 8mm.

* 360 degrees / 1.8 degree step angle = 200 steps to make a full rotation.
* 200 steps (pulses) * 16 microstepping = 3200 pulses to make a full rotation.
* 8mm leadscrew pitch means that 1/8 of a rotation must be made to raise the build plate 1mm.
* 1mm raise of build plate = 3200 steps * 1/8 = 400 steps (pulses).

* It takes 400 pulses to raise the build plate 1mm, this is set with the G-code command **M92 Z400**.
    * Microstepping Sixteenth Step: **M92 Z400**
    * Microstepping Half Step: **M92 Z50**
    * Microstepping Full Step: **M92 Z25**
* This steps per unit value is set by default in configuration.h. It should also be manually set in NanoDLP in the Bootup Code box.
* Set the default steps per unit value by changing the G-code in the Bootup Code G-code code box and in the Start of Print G-code code box.
    * Both of these boxes can be find in System -> Machine Settings -> Code / Gcode.

#### Endstop Calibration
* Endstop calibration setting are inputted into the Start of Print code box.
    * NanoDLP -> System -> Machine Settings -> Axis / Movement -> Start of Print
* The chunk of G-code in this box raises the build plate to the endstop to identify the build plate position, and then moves the build plate to the bottom of the resin vat to begin the print.
* In the Start of Print G-code box the command **G28 Z0 F400** moves the build plate upwards until the endstop is triggered, the command **G92 Z"Max Height"** is then run to identify the current position of the build plate.
    * Set **"Max Height"** to the distance between the bottom of the resin vat and the endstop, for example **G92 Z218.8**.
* To measure this distance move the build plate to its desires lowest point a few microns above the resin vat bottom, zero the Z position with the command **G92 Z0**, manually raise the build plate until the endstop has just been triggered, run the command **M114** to find the current Z location, plug in this value as "Max Height". 

#### Start of Print Code
* The following code is run as the first set of commands at the beginning of any print.
* This code is designed to identify the build plate position by triggering the endstop and then move the build plate into its starting position at Z = 0.

**M92 Z200** Set steps (pulses) per mm to 200. Alternatively 400 should be used depending on the microstepping of the motor. <br>
**G28 Z0 F400** Auto home, moves the motor up at a speed of 400 until it hits the Z-axis endstop. <br>
**[[WaitForDoneMessage]]** Wait for Z-axis movement completion message from RAMPS before continuing with subsequent commands. <br>
**G90** Set positioning to absolute mode. <br>
**G92 Z218.8** Set current Z position to 218.8, this is the distance from the resin vat floor to the endstop that has been previously measured. <br>
**G4 P500** Dwell for half a second at the endstop before beginning downward movement towards the resin vat floor. <br>
**G1 Z25 F400** Move from endstop to 25mm above resin vat floor at a speed of 400. <br>
**[[WaitForDoneMessage]]** Wait for Z-axis movement completion message from RAMPS before continuing with subsequent commands. <br>
**G4 P100** Dwell for a tenth of a second. <br>
**G1 Z10 F100** Move from 25mm to 10mm above the resin vat at a slower speed of 100. This is where the build plate begins to dip into the resin. <br>
**[[WaitForDoneMessage]]** Wait for Z-axis movement completion message from RAMPS before continuing with subsequent commands. <br>
**G4 P100** Dwell for a tenth of a second. <br>
**G1 Z0 F50** Move to bottom of the resin vat at a slower speed of 50. <br>
**[[WaitForDoneMessage]]** Wait for Z-axis movement completion message from RAMPS before continuing with subsequent commands. <br>
**G4 P500** Dwell for half a second before print begins. <br>
**[[WaitForDoneMessage]]** Wait for Z-axis movement completion message from RAMPS before continuing with subsequent commands. <br>
**[[PositionSet0]]** Now that the build plate is at the bottom of the resin, set to Z position to 0. <br>
**M106** Turn fan on. <br>

* The command **[[WaitForDoneMessage]]** is necessary after any movement command such as **G28** or **G1**. In the marlin firmware file
*Configuration_adv.h* there is a setting enabled that causes marlin to send the message "Z\_move\_comp" to the Raspberry Pi after every 
completed Z-axis movement. With the command **[[WaitForDoneMessage]]** NanoDLP listens for the "Z\_move\_comp" message and performs the next
action after seeing this message. However, because there is a lag between the message being sent from marlin on the RAMPS 1.4 board and the
message arriving to NanoDLP on the Raspberry Pi, if multiple movement are run in quick succession NanoDLP interprets all actions as being completed
after the first "Z\_move\_comp" message arrives. This causes NanoDLP to get ahead of itself and continue with the next print steps before the
Z-axis movement is completed. An example of this is the first burn in layer image being displayed before the build plate is fully lowered
into the resin vat. Additionally, short dwell commands such as **G4 P100** are added after the **[[WaitForDoneMessage]]** command to ensure that
all commands are processed correctly

#### Resume Print Code
**G90**
**G92 Z[[CurrentPosition]]** Set Z position to the current position. <br>
**G1 Z[[LayerPosition]]** Move to the current layer being printed. <br>
**[[WaitForDoneMessage]]** <br>
**[[PositionSet[[LayerPosition]]]]** Set Z position to the layer position that was just moved to. <br>
**M106** <br>

#### Print Stop Code
**G1 Z200 F300** Move to 200mm above the bottom of the resin vat after finishing print. <br>
**[[WaitForDoneMessage]]** <br>
**[[PositionSet[[StopPosition]]]]** <br>
**M107** Turn fan off. <br>

<div style="page-break-after: always;"></div>

### Resin Profile Settings<a name="Resin-Profile-Settings"></a>

Demo resin profiles may be found in `/resin_profiles`. These .json files contain resin profiles for working with Siraya Tech Blu Tough Emerald Blue resin. An example .json file with printer machine settings is also available in `/resin_profiles`.

#### Code Before Each Layer
**G1 Z[[LayerPosition]] F[[ZSpeed]]** Move to next print layer at the speed set in Dynamic Speed. <br>
**[[WaitForDoneMessage]]** <br>
**G4 P100** <br>
**[[PositionSet[[LayerPosition]]]]** Update current Z position. <br>
**[[WaitForDoneMessage]]** <br>

#### Code After Each Layer
**G4 P100** <br>
**G1 Z{[[LayerPosition]] + [[ZLiftDistance]]} F[[ZSpeed]]** Lift the build plate by the height set in Dynamic Lift at the speed set in Dynamic Speed. <br>
**[[WaitForDoneMessage]]** <br>
**G4 P100** <br>
**[[PositionChange[[ZLiftDistance]]]]** Update current Z position. <br>
**[[WaitForDoneMessage]]** <br>

#### Dynamic Settings
* Dynamic setting boxes allow print variables to alter throughout the print.
* Boolean conditions evaluate to 1 if met or else 0.
* For an additional explanation of how dynamics settings may be set: https://docs.google.com/document/d/1ySVb57AXCVfBFSr9KF7B7k3M130pJvRXXfEoh6pJP_4/edit#
* For a list of variables that may be used in dynamic settings: https://docs.nanodlp.com/manual/code/

#### Dynamic Speed
* For the first two layers, sets movement speed to 50. For subsequent layers lift speed is a function of the total area being printed. The larger the area being printed to slower the layer lifts, with movement speed values ranging from 80 to 150. <br>
**{(([[LayerNumber]]<=2)*50) + ([[LayerNumber]]>2) * (150-80*(0.087*(log([[TotalSolidArea]]))))}**

#### Dynamic Cure Time
* The first two layers (burn in layers) cure for 5x the normal cure time. Subsequent layers cure for between 2.5 to 3.5 seconds depending on the size of the layer that is being printed. Smaller layers cure for more time. <br>
**{((([[LayerNumber]]<=2)*4)+1)*(3.5-2.5*(0.087*(log([[TotalSolidArea]]))))}**

#### Dynamic Lift
* The first two layers lift 6mm, subsequent layers lift 2mm to 4mm as a function of the largest object in the layer. Layers with larger objects lift higher.
* The logic behind using LargestArea is that large objects will require more time for resin to flow in after each layer is lifted. <br>
**{(([[LayerNumber]]<=2)*6)+([[LayerNumber]]>2)*(2+4*(0.087*(log([[LargestArea]]))))}**

#### Dynamic Wait After Lift
* The first two layers wait for 1 seconds after lift. Subsequent layers wait for 0.05 to 0.25 seconds depending on the size of the total area being printed. Larger layers wait longer. <br>
**{(([[LayerNumber]]<=2)*1) + ([[LayerNumber]]>2) * (0.25-0.05*(0.087*(log([[TotalSolidArea]]))))}**

<div style="page-break-after: always;"></div>


### General Notes<a name="General-Notes"></a>
* The smaller the focal length, the more barrel factor that you need to compensate for image warping.
    * This occurs because smaller focal length -> thicker lens -> more light bending -> more magnification.
* Optimal barrel factor changes by lens focal length.
* If there are still air bubbles between the build plate and resin vat on the initial burn in layer, you can make the delay before displaying burn in layers arbitrarily long in the resin profile to allow these air bubbles to escape from under the build plate.

<div style="page-break-after: always;"></div>

### Dimensions<a name="Dimensions"></a>
* Projector is mounted 273mm from the bottom of the resin vat.
    * Note that this measurement is from the top of the projector (not the lens) to the bottom of the resin vat.
* The travel of the build plate / maximum print size in the Z dimension is ~220mm.

<div style="page-break-after: always;"></div>

## Parts<a name="Parts"></a>

### Electronics<a name="Electronics"></a>
* **Raspberry Pi 3 Model 3B+**
    * 5V/2.5A DC power input.
* **Raspberry Pi power cord**
    * 5.25V/3A.
    * 3.3ft. cable.
* **16gb Memory Card**
    * NOOBS pre-installed.
* **RAMPS 1.4 Controller Board**
    * 12V/5A power input.
* **A4988 Stepper Motor Driver**
* **DRV8825 Stepper Motor Driver**
    * Note, the DRV8825 stepper motor driver is an alternative to the A4988 that provides more amps to the stepper motors and is thus preferred.
* **MEGA 2560 R3 Microcontroller**
    * USB connector cable necessary for interaction with Pi.
* **Mechanical Endstop**
    * 2A current rating.
    * 3.3ft cable length. 
    * 3 wire input.
* **60W/12V/5A Power Supply**
    * 3ft. cable to 3-prong plug, 1ft. cable to power output.
    * 90-265V AC input to 12V 5A output.
    * Case size is X: 7.48in., Y: 1.92in., Z: 1.34in.   
* **HDMI Cord**
    * 1.6ft. length.
    * Thin cable, slim connectors to fit projector backplate size constraint.
* **Power Strip**
    * 5 AC outlets, 3 USB ports, 5 ft. cord, power switch, 4 wall mounts.
    * Dimensions: X: 6.77in., Y: 3.54in., Z: 1.1in.
    * Max power: 1875W (125V~15A), AC 100-250V.
* **DHT 11 Temperature Humidity Sensor**
    * 3.3-5V DC working voltage.
* **2 Channel Relay Module**
    * 5V control voltage.
    * High current relay 250V/10A AC to 30V/10A DC. 
* **500W Electric Space Heater**

### Motors<a name="Motors"></a>
* **(2x) Nema 17 Stepper Motor**
    * Rated 2A/1.4ohms resistance.
    * 1.8 degree step angle.
    * 4 wire input.
* **20Kg Servo Motor**
    * 4.8-6.8V DC input.
    * 270 degree control angle.

### Projector<a name="Projector"></a>
* **ViewSonic PX703HD**
    * 1920 x 1080 pixel resolution.
    * 115200 Baud Rate.
    * 1.3x optical zoom.
    * 1.13 - 1.47 throw ratio.
* **200mm Focal Length Convex Lens**
    * 75mm diameter.
* **300mm Focal Length Convex Lens**
    * 75mm diameter.
* **500mm Focal Length Convex Lens**
    * 75mm diameter.
* **Aluminum Sheet for Shutter**
    * Aluminum Sheet 0.16in x 4in x 10in.

### Resin Vat<a name="Resin-Vat"></a>
* **6063 Aluminum Angle for Vat Walls**
    * 1in. x 1in. x 0.125in.
    * 1200mm (47.24in.) necessary. 
* **Borosilicate Glass**
    * 12in x 8in x 1/8in thick.
* **FEP Film**
    * 250mm (9.84in.) x 140mm (5.51in.) minimum necessary.
    * 11.75in x 12in, 5mil thick.
* **Bolt and Gasket for Vat Drain.**
* **3M Marine Adhesive Sealant**
    * Fast Cure 5200.

### Linear Movement<a name="Linear-Movement"></a>
* **(4x) 350mm Linear Guide and Slide Block**
    * Stainless steel, ball bearings.
    * MGN 12H with H-type carriage.
* **(2x) 400mm Lead Screw, Pillow Bearing Blocks, and Copper Nut**
    * Stainless steel lead screw, copper nut. 
    * Lead screw diameter is 8mm.
* **(2x) Stepper Motor Mounting Brackets**
    * Alloy steel.
    * Fits 42mm Nema 17 Stepper Motor.
* **6061 Aluminum Angle Mounted to Linear Guide Slide Blocks and Lead Screw.**
    * 1.5in. x 1.5in. x 0.125in.
    * 816mm (32.12in.) necessary.
* **6063 Aluminum Angle Struts for Suspending Build Plate**
    * 1in. x 1.5in. x 0.125in.
    * 540mm (21.26in.) necessary.
* **6061 Aluminum Sheet for Build Plate**
    * 0.25in. thickness.
    * 270mm x 150mm necessary.

### Frame <a name="Frame"></a>
* **(6x) 300mm Linear Rail for Horizontal Struts**
    * Aluminum.
    * 20mm x 20mm diameter, 6mm T-slot.
    * Size: 2020V-B.
* **(6x) 400mm Linear Rail for Horizontal Struts**
    * 20mm x 20mm diameter, 6mm T-slot.
    * Size: 2020V-B.
* **(4x) 600mm Linear Rail for Vertical Base Struts**
    * 20mm x 20mm diameter, 6mm T-slot.
    * Size: 2020V-B.
* **(4x) 400mm 2040 Double Linear Rail for Vertical Top Struts**
    * 20mm x 40mm diameter, 6mm T-slot.
    * Will be cut down to 350mm during construction process.
    * Size: 2040V.
* **(32x) Gussets / Corner Brackets for Connecting Linear Rail**
    * Dimensions: X: 20mm, Y: 28mm, Z: 28mm.
    * 6mm hole for mounting gussets.
* **(40x) M5 T-nuts for Mounting Object to Linear Rail**
    * Part Number: TL-M5-40pcs.
* **(50x) M5 T-nuts for Mounting Object to Linear Rail**
    * Part Number: BR-TN-0015 
* **5052 Aluminum Sheet for Mounting Projector to Frame**
    * 0.125in. thickness.
    * 440mm x 200mm needed.
* **(2x) 5052 Aluminum Sheet for Mounting Stepper Motors to Frame**
    * 0.125in. thickness.
    * 440mm x 50mm needed.
* **(4x) Threaded Feet for Frame**
    * Nickel-plated steel with cushion. Swivel level mounting.
    * 1" Long, 10-32 threaded stud.

### Exterior Cover <a name="Exterior-Cover"></a>
* **(9x) Type 1 PVC Plastic Sheets**
    * Polyvinyl Chloride.
    * 3mm thickness.
    * (1x) Back Panel: 446mm x 956mm.
    * (2x) Top and Bottom Panel: 340mm x 446mm.
    * (1x) Front Bottom Panel: 446mm x 593mm.
    * (1x) Front Top Panel: 446mm x 363mm.
    * (2x) Side Bottom Panels: 340mm x 590mm.
    * (2x) Opaque Side Top Panels: 340mm x 360mm. 
* **(8x) Hinges**
    * Steel mortise mount hinges with holes, nonremovable pin.
    * Hinge size is X: 2.5", Y: 1.25".
* **(8x) Magnetic Latches**
    * Black Zinc-Plated Steel latches and strike plates.
    * Dimensions X: 5/16", Y: 1", Z: 15/16".

### Bolts <a name="Bolts"></a>
* **(4x) M6 x 60mm Countersunk Bolts for Connecting Build Plate to Build Plate Struts**
    * (8x) M6 nuts.
    * (4x) M6 wing nuts.
* **(8x) M5 x 35mm Bolts for Mounting Stabilizer Mounts to Linear Rail.**
* **(2x) M5 x 15mm Bolts for Mounting Lens Holder to Projector Backplate.**
    * (2x) M5 nuts.
* **(8x) M5 x 10mm Bolts for Connecting Build Plate Struts to Build Plate Angle Mounts**
    * (8x) M5 nuts.
* **(16x) M5 x 10mm Countersunk Bolts for Connecting Hinges to Linear Rail through PVC Plates.**
    * (16x) M5 nuts. 
* **(34x) M5 x 8mm Bolts for Connecting Exterior Panels to Linear Rail**
    * (16x) M5 Linear Rail T-nuts.
* **(16x) M5 x 8mm Bolts for Connecting Aluminum Sheet and Angle to Frame**
    * (16x) M5 Linear Rail T-nuts.
* **(64x) M5 Linear Rail T-nuts for Connecting Gussets to Linear Rail.**
    * Replaces weak T-nuts that come with the gussets.
* **(8x) M4 x 16mm Bolts for Connecting Stepper Motor Mounts to Aluminum Motor Mount Plates**
    * (8x) M4 nuts.
    * Optional (8x) additional M4 nuts for correctly spacing motor mount away from aluminum sheet.
* **(4x) M4 x 20mm Bolts for Mounting Electric Heater to Floor Plate.**
    * (12x) M4 nuts.
* **(3x) M4 x 12mm Bolts for Connecting Projector to Projector Backplate**
    * (3x) M4 nuts.
* **(8x) M4 x 12mm Bolts for Connecting Magnets to Linear Rail.**
    * (8x) M4 Linear Rail T-nuts.
* **(2x) M4 x 8mm Bolts for Mounting Power Supply Brick to Floor Plate.**
    * (2x) M4 nuts.
* **(3x) M3 x 25mm Bolts for Mounting RAMPS 1.4 Board to Projector Backplate.**
    * (9x) M3 nuts for mounting RAMPS with space between RAMPS 1.4 and backplate.
* **(2x) M3 x 16mm Countersunk Bolts for Mounting Lens Holder Ring to Lens Holder Arms.**
    * (2x) M3 nuts.
* **(2x) M3 x 16mm Bolts for Mounting Endstop to Endstop Mount.**
    * (6x) M3 nuts for mounting endstop with space between the endstop and endstop mount.
* **(8x) M3 x 10mm Bolts for Mounting Copper Nuts to Build Plate Angle Mounts.**
    * (8x) M3 nuts.
* **(4x) M3 x 10mm Bolts for Mounting Power Relay to Projector Backplate.**
    * (12x) M3 nuts for mounting relay with space between the relay and backplate.
* **(1x) M3 x 10mm Bolts for Mounting DHT11 Temperature Sensor to Projector Backplate.**
    * (3x) M3 nuts for mounting the temperature sensor with space between the sensor and backplate.
* **(4x) M3 x 10mm Bolts for Mounting Power Strip to Floor Plate.**
    * (4x) M3 nuts.
* **(16x) M3 x 6mm Bolts for Mounting Build Plate Angle Mounts to Linear Rail.**
* **(16x) M3 x 6mm Bolts for Mounting Linear Guides to Linear Rail.**
    * (16x) M3 Linear Rail T-nuts.
* **(4x) M2 x 20mm Bolts for Mounting Raspberry Pi 3B+ to Projector Backplate.**
    * (12x) M2 nuts for mounting Pi with space between Pi and backplate.
* **(2x) 10-24in. x 3/8in. Bolts for Resin Vat Drain Plugs.**
    * (2x) 10-24in. nuts and gaskets for sealing drain plugs.

* **Totals**
    * (4x) M6 x 60mm Countersunk Bolts.
    * (8x) M6 Nuts.
    * (4x) M6 Wing Nuts.
    * (8x) M4 x 35mm Bolts.
    * (2x) M5 x 15mm Bolts.
    * (8x) M5 x 8mm Bolts.
    * (34x) M5 x 8mm Bolts.
    * (112x) M5 Linear Rail T-nuts.
    * (26x) M5 Nuts.
    * (4x) M4 x 20mm Bolts.
    * (8x) M4 x 16mm Bolts.
    * (8x) M4 x 12mm Bolts.
    * (6x) M4 x 8mm Bolts.
    * (8x) M4 Linear Rail T-nuts.
    * (22x) M4 Nuts.
    * (2x) M3 x 16mm Bolts.
    * (2x) M3 x 16mm Countersunk Bolts.
    * (26x) M3 x 10mm Bolts.
    * (32x) M3 x 6mm Bolts.
    * (16x) M3 x T-nuts.
    * (35x) M3 Nuts.
    * (2x) 10-24in. x 3/8in. Bolts.
    * (2x) 10-24in. Nuts.

## Software Setup <a name="Software-Setup"></a>

### Raspberry Pi Setup <a name="Raspberry-Pi-Setup"></a>
* If SD card does not come with NOOBS OS pre-installed, connect SD card to 
external computer and write Raspberry Pi OS to the SD card using the
Raspberry Pi imager software.
* If SD card comes with NOOBS pre-installed, power on Raspberry Pi with monitor,
keyboard, and mouse attached. Select Raspberry Pi OS Full 32-bit to install.
* Proceed through Raspberry Pi setup after boot. 
* Update Raspberry Pi: **sudo apt-get update**
* Install vim: **sudo apt-get install vim**
* Add terminal shortcuts for convenience:
    * **vim ~/.bashrc**
    * **alias c='clear'**
    * **source ~/.bashrc**
* Change computer name.
    * **sudo vim /etc/hostname**
    * Change name to mark1-0 where 01 is the printer model and 0 is the
serial number of the particular printer.
    * **sudo vim /etc/hosts**
    * Change all instances of the original computer name to the name added to
/etc/hostname. 
    * To put changes into effect: **sudo reboot**
* Set static IP address.
    * Open DHCP config file: **sudo vim /etc/dhcpcd.conf**
    * At the bottom of the file add the following to set a static IP address
for both a wired and wireless connection (eth0 = wired, wlan0 = wireless).
    * In the code below replace XXX.XXX with your local IP address.

        `interface eth0` <br>
        `static ip_address=XXX.XXX.12.10/24` <br>
        `static routers=XXX.XXX.12.1` <br>
        `static domain_name_servers=XXX.XXX.12.1`

        `interface wlan0` <br>
        `static ip_address=XXX.XXX.12.200/24` <br>
        `static routers=XXX.XXX.12.1` <br>
        `static domain_name_servers=XXX.XXX.12.1`

* This statically assigns the IP addresses XXX.XXX.12.10 if connected via wifi and XXX.XXX.12.200 if connected via ethernet. 
    * Make sure XXX.XXX.12 matches the IP addresses of the desired internet source.
    * Increment 10 and 200 in the IP addresses above by one with each new printer
to avoid conflict if multiple printers are running on the same internet.
    * Reboot for IP changes to take effect: **sudo reboot**
* Install ufw, open port 22 for ssh, open port 80 to display the NanoDLP interface to the web.
    * **sudo apt-get install ufw**
    * **sudo ufw enable**
    * **sudo ufw allow 22**
    * **sudo ufw allow 80**
    * Allow ssh via port 22 and ssh password login: **sudo vim /etc/ssh/sshd_config**
* Install openssh-server to support ssh connections from the server (pi) side.
    * **sudo apt install openssh-server**
    * **sudo systemctl enable ssh**
* From personal computer, copy public key to the remote server.
    * ssh-copy-id -p 22 pi@XXX.XXX.12.200
* On personal computer, add ssh profile to ~/.ssh/config.

### Arduino and RAMPS Board Setup <a name="Arduino-and-RAMPS-Board-Setup"></a>
* Attach RAMPS 1.4 to Arduino 2560.
* Attach heat sink to the processor on the A4988 stepper driver.
* Attach three microstepper jumpers to the pins under where the Z-axis stepper
is attached.
    * For A4988 motor driver three jumpers sets the microstepping to 1/16.
    * One jumper sets halfstepping. Jumper should be placed on the MS1 jumper (the jumper farthest from the VREF screw).
* Attach stepper driver to Z-axis location with current adjustment screw facing
away from the USB cord.
* Attach stepper motor to Z-axis location with black wire facing away from the
USB cord.
* Attach end stop wire to Z-max location with red wire closest to the stepper
motor.
    * Note, the Z-max location is the 3 pins farthest from the power supply (closest to the 4 pins).
    * Note, if the endstop wires are incorrectly attached to the RAMPS board
(i.e. the GND goes to the power source), this will result in a burning plastic smell.
* Connect power supply to the 5A power supply terminals.
    * These are the two terminal farthest from the USB plug.
    * Red (+) in left terminal, Black (-) in right terminal.
* Connect RAMPS and Arduino board to pi via USB in lower right USB slot.

### Stepper Motor Setup <a name="Stepper-Motor-Setup"></a>
* The voltage sent to the stepper motors must be set correctly.
    * This voltage (Vref) is set by turning the screw on the A4988 motor driver clockwise to increase voltage.
* The equation for setting this voltage varies based on the stepper motor driver.
* The equation for an A4988 driver is: Vref = 8 * I * R
    * Where: 8 is a constant specific to the A4988 driver, I is the maximum current capacity of the stepper motor, and R is the resistance of the stepper motor driver.
    * These Nema 17 stepper motors have a maximum current rating of 2.0A, for safety we multiply this by 90% to get I = 1.8A.
    * The resistance of A4988 drivers varies by manufacturer, these have a resistance of 0.1 ohms so R = 0.1.
* Vref = 8 * 1.8 * 0.1 = 1.44
* Use a volt meter with the positive end on the Vref screw to set the correct Vref.
* On Mark 1, Vref is current set to ~1V as this supplies enough power and is quieter than running the motors at 1.4V.

### Servo Motor Setup <a name="Servo-Motor-Setup"></a>
* Attach servo motor to servo motor pins.
    * Note, connect to the set of 3 pins that is closest to the power supply. This is the D11 slot which corresponds to Pin 0.
    * Note, the black wire (ground) goes closest to the edge of the board.
    * It is possible to supply power to the servo motor by shorting the VCC and 5V pins that are to the left of the reset button by connecting these pins via a jumper. 
    * Doing this supplies power to the servo motor from the Arduino, however, running the servo motor like this will overpower the Arduino and cause it to shut off.
    * Thus, the 5V pin must be given its own 5V power supply. Use LM7805 voltage regulator to step the 12V power input down to 5V. Note that the LM7805 outputs 1.5A which is not enough to turn the servo motor. Use two LM7805 regulators to provide 3A to the servo motor.
    * A servo motor in the 3 pin slot closest to the power supply (D11 slot, Pin 0) is controlled via the G-Code command: **M280 P0 S0** / **M280 P0 S255**.

### Arduino and RAMPS Software Install <a name="Arduino-and-RAMPS-Software-Install"></a>
* Connect Raspberry Pi to monitor, keyboard, and mouse.
* If NanoDLP has already been set up, terminate NanoDLP and access the desktop.
* To terminate NanoDLP ssh into the pi and run:
    * **sudo systemctl disable nanodlp**
    * **sudo systemctl stop nanodlp**
* Navigate to Marlin install page and install Marlin 2.0.x.
    * marlinfw.org/docs/basics/install.html
    * Right click .zip downloaded file and extract to: /home/pi
* Navigate to Arduino install page and install Arduino IDE.
    * arduino.cc/en/Main/Software_
    * Download Linux ARM 32 bit version.
    * Extract the downloaded files to: /home/pi
    * Inside the arduino files run **sudo bash install.sh**
* On local computer (not Raspberry Pi) navigate to the directory where firmware configurations are stored.
    * /marlin\_local/Marlin
    * Copy configuration files from local computer to Raspberry Pi.
    * **scp Configuration.h Configuration_adv.h pi@XXX.XXX.12.201:/home/pi/Marlin-2.0.x/Marlin** 
* On Raspberry Pi navigate to /home/pi/Marlin-2.0.x/Marlin and double click Marlin.ino.
    * Inside Arduino IDE:
    * Tools -> Port -> /dev/ttyUSB0
    * Board -> Arduino Mega or Mega 2560
    * Click arrow in the upper left to compile and upload configuration files to RAMPS board.
    * These configuration files are used whenever NanoDLP boots.

### Verify RAMPS Functionality <a name="Verify-RAMPS-Functionality"></a>
* Download pronterface.
    * **sudo apt update**
    * **sudo apt install printrun**
* Launch pronterface and verify RAMPS functionality.
    * Run pronterface with the command: **pronterface**
    * Check in the upper left of the GUI that the Port is correct and set the 
Baud Rate to 115200.
    * Run the Gcode command M119 to verify endstop functionality.
    * Endstop statuses should read: x_min: open, y_min: open, z_min: open, z_max: open.
    * If M119 is ran while the endstop is triggered, z_max should read z_max: triggered.
    * Move Z-axis position and check that it is spinning in the correct direction.
    * When Z-axis is set to move up, the stepper motor should spin clockwise (to the left).
    * Check Z-axis homing capability. Click the Z home button and then press and hold the endstop to set the Z home.
    * After homing, move down 2mm in the Z direction and then move 10mm up. On the 10mm up command, the stepper motor should only move 2mm up.

* If NanoDLP was previously set up, enable NanoDLP so that it runs on launch.
    * **sudo systemctl enable nanodlp**
    * **sudo systemctl start nanodlp**

### Install and Launch NanoDLP <a name="Install-and-Launch-NanoDLP"></a>
* From pi, download NanoDLP with wget.
    * **(wget https://www.nanodlp.com/download/nanodlp.linux.arm.rpi.stable.tar.gz --no-check-certificate -O - | tar -C /home/pi -xz --warning=no-timestamp)**
    * **cd /home/pi/printer**
* Before running **setup.sh**, manually install pigpio.
    * **sudo apt-get install pigpio**
    * If this fails with a locked dpk error, run the following commands.
    * **sudo rm /var/lib/apt/lists/lock**
    * **sudo rm /var/cache/apt/archives/lock**
    * **sudo rm /var/lib/dpkg/lock**
    * **sudo dpkg --configure -a**
    * **sudo apt update**
    * **sudo apt-get install pigpio**
* Run **sudo ./setup.sh**
    * Are you using shutter and is it wired to Raspberry Pi: Y
    * This apt installs pigpio, but it should already be installed above.
    * Do you want to optimize Raspberry Pi settings for NanoDLP automatically: Y
    * Do you want to enable i2c to enable... : Y
    * To expand file system, enable SSH server and camera module.. : Y
    * 5 Interfacing Options -> P2 SSH -> Yes
    * 5 Interfacing Options -> I2C -> Yes
    * 5 Interfacing Options -> Remote GPIO -> Yes
    * 7 Advances Options -> A1 Expand Filesystem
* Note: The first time connecting to NanoDLP, you may have to do it via 
ethernet. After connecting via ethernet the first time, NanoDLP can be accessed
over wifi via the static ethernet IP address: XXX.XXX.12.200
* After the pi reboots and NanoDLP begins running (note the black screen), 
go to https://www.nanodlp.com/dashboard on your personal computer to find the IP
address assigned to the pi. The NanoDLP dashboard can be accessed at this IP
address. This IP address should be equivalent to the eth0 address: XXX.XXX.12.10
* Connect to NanoDLP through the browser with this IP address, click the wifi 
button and connect to wifi within the NanoDLP browser.
* After disconnecting the pi from ethernet and restarting, you should be able
to access the NanoDLP interface on wifi via: XXX.XXX.12.200

### NanoDLP Settings <a name="NanoDLP-Settings"></a>
* System -> Machine Settings -> Axis / Movement
* Start of Print Code
    * Change **G28** command to **G28 Z0**. If homing is done with the **G28** command than triggering the endstop will kill the printer. The **G28 Z0** command must be used so that homing is done with respect to the Z axis.
* Manual Movement Code Template
    * Change the line: output = **"G1 Z"+pos+"\r\n";** to: **output = "G1 Z"+pos+"\r F200\n";**
    * Adding F200 controls the speed with which the motor moves when using manual Z Axis Control. If it is not set to a specific value, the motor will use maximum speed which will over-pulse the motor and cause it to fail.

### Projector Setup <a name="Projector-Setup"></a>
* Remove UV dissipation lens from projector lamp.
    * Unscrew the two screws that are on the sides of the projector next to the lens and the projector fan.
    * Use a small edged tool to pry up around the edges of the top casing and slide it forward, sufficient force must be applied unattach the plastic connectors that connect the top casing to the projector.
    * Loosen the single screw that connects the lamp to the projector, unplug the lamp power wire, and remove the lamp from the projector.
    * Pry off small aluminum case that holds UV dissipation glass in front of the lamp, remove UV dissipation glass.
    * Re-install lamp into projector and tighten the single screw until it is very tight.
* First power on projector without HDMI attached to change projector settings.
    * Basic -> Splash Screen -> Black
    * Power Management -> Auto Power On -> Signal HDMI 
    * Power Management -> Auto Power On -> Signal HDMI 
    * Power Management -> Auto Power On -> Signal HDMI 
* Change lens shift so that the projection image is in the middle of the resin vat and not offset.
    * Menu -> Lens Shift -> 20
* Projector brightness is set to 50 (default).
    * For resolution calibration, brightness may be turned down so that calibration grids are easier to look at. Make sure to reset brightness to 50 before printing.

### Controlling Projector Power via Pi <a name="Controlling-Projector-Power-via-Pi"></a>
* In projector settings enable CEC for control via HDMI cable.
* SSH into pi and run: **sudo apt install cec-utils**
* Scan for CEC capable devices: **echo 'scan' | cec-client -s -d 1**
* Example turn on device at address 0.0.0.0: **echo 'on 0.0.0.0' | cec-client -s -d 1**
* Example turning off device at address 0.0.0.0: **echo 'standby 0.0.0.0 | cec-client -s -d 1**
* Note, the current HDMI cord does not support CEC, thus this feature cannot currently be used.

<div style="page-break-after: always;"></div>

### Controlling Heater via Pi <a name="Controlling-Heater-via-Pi"></a>

#### DHT11 Temperature Sensor Setup
* Wire DHT11 sensor to Raspberry Pi, on the Raspberry Pi pinout:
    * Power to Pin 2 (5V power).
    * Ground to Pin 6 (GND).
    * Input to Pin 7 (GPIO 4).
* SSH to the Pi and install the following modules:
    * **pip3 install adafruit-circuitpython-dht**
    * **sudo apt-get install libgpiod2**
* Navigate to **/home/pi/** and create a directory for temperature control scripts called **temp_ctrl**.
    * Copy temp_ctrl python scripts from repository into the **temp_ctrl** directory.

#### Electric Heater Setup
* Cut power cord in half.
* Seperate and strip wires, connect two of the wires via solder and cover soldered wire with electrical tape.
    * Note that because it is AC there are only two wires and it does not matter which two are connected and which two go into the relay.
* Solder extension wires to the two remaining exposed wires, cover the soldered connections with electral tape.
    * Connect the remaining two wires to the Common and Normally Open terminals on the relay.
    * Use terminal 1, the terminal below the yellow jumper.
    * The Common terminal is in the middle, and the Normally Open is the right terminal if the blue relay boxes are pointed towards you.
* Connect jumper cables from relay to Pi.
    * Connect ground wire from Gnd on the relay to Pin 9 (GND) on the Pi.
    * Connect control wire from In1 on the relay to Pin 11 (GPIO 17) on the Pi.
    * Connect power wire from Vcc on the relay to Pin 4 (5V power) on the Pi.
* SSH to the Pi and install the following modules:
    * **pip3 install RPi.GPIO**

<div style="page-break-after: always;"></div>

### Mark 1 Software Setup <a name="Mark1-Software-Setup"></a>
* Navigate to Mark 1 software directory on local computer.
    * **/Mark1/software**
* Update **~/.vimrc** and **~/.bashrc**.
    * **scp vimrc.txt bashrc.txt pi@XXX.XXX.12.201:/home/pi/Marlin-2.0.x/Marlin**
    * Copy the text in **vimrc.txt** into **~/.vimrc**.
    * Then, from within vim run: **:source ~/.vimrc**.
    * Copy the text in **bashrc.txt** into **~/.bashrc**.
    * Then run: **source .bashrc**
* Copy heater control scripts to pi.
    * **scp -r temp_ctrl pi@XXX.XXX.12.201:/home/pi/Marlin-2.0.x/Marlin**

* Install pip packages on pi.
    * **pip install [...]**
    * **time**
    * **board**
    * **adafruit_dht**

## Manufacturing <a name="Manufacturing"></a>

### General Manufacturing Notes <a name="General-Manufacturing-Notes"></a>

#### Drill Bits
* 1/8in. or .128in. drill bit for M3 holes.
* 5/32in. drill bit for M4 holes.
    * 11/64in. drill bit if conservative.
* 13/64in. drill bit for M5 holes.
* .242in. for M6 holes.
* 3/32in. or 1/8in. drill bit to prep hole before drilling if using a handheld drill.

#### Tapping 
* When tapping, always check what the correct hole size to drill is first.
* When tapping, set the tap to max speed and tap using short bursts of power.
    * Consider greasing or lubricating the tap before if working with stiffer materials.

<div style="page-break-after: always;"></div>

### Linear Rail Manufacturing<a name="Linear-Rail-Manufacturing"></a>
* (2x) 400mm Linear Rail for top horizontal struts are cut from 400mm to 360mm.
* (2x) 400mm 2040 Double Linear Rail for top vertical struts are cut from 400mm to 350mm.
* Use masking tape to fix linear rail together and cut the linear rail while taped together. This ensures uniform length.

<img src="images/linear_extrusion_manufacturing.jpg" width="1000"/>

<img src="images/upper_frame_2.jpg" width="700"/>

<div style="page-break-after: always;"></div>

### Resin Vat Manufacturing<a name="Resin-Vat-Manufacturing"></a>
* (2x) 1in. x 1in. x 0.125in. angle cut to 440mm length.
* (2x) 1in. x 1in. x 0.125in. angle cut to 160mm length.
* Drill 4 M5 holes for mounting resin vat to frame.
* On left side 160mm angle piece, drill and tap hole for drainage bolt.
    * Close to one corner, drill holes with 5/32 in. drill bit.
    * Tap hole with 10-24 tap bit. 

<img src="images/resin_vat_manufacturing.jpg" width="1200"/>

<img src="images/resin_vat_1.jpg" width="1200"/>

<img src="images/resin_vat_2.jpg" width="1200"/>

<img src="images/resin_vat_3.jpg" width="1200"/>

<div style="page-break-after: always;"></div>

### Build Plate Angle Mount Manufacturing<a name="Build-Plate-Angle-Mount-Manufacturing"></a>
* (2x) 1.5in. x 1.5in. x 0.125in. angle cut to 410mm length.
* On vertical angle side:
    * (2x) Drill 8 M3 holes for mounting angle to linear guide carriages.
* On horizontal angle side:
    * (2x) Drill 4 M5 holes for mounting build plate strut to build plate angle mount.
    * (2x) Drill 4 M3 holes for mounting copper nut to build plate angle mount.
    * (2x) Drill 10.2mm hole for copper nut to go through.

<img src="images/build_plate_angle_mount_manufacturing_vertical.jpg" width="1200"/>

<img src="images/build_plate_angle_mount_manufacturing_horizontal.jpg" width="1200"/>

<div style="page-break-after: always;"></div>

### Build Plate Strut Manufacturing <a name="Build-Plate-Strut-Manufacturing"></a>
* (2x) 1.5in. x 1in. x 0.125in. angle cut to 270mm length.
* (2x) Drill 4 M5 holes on 1.5in. side for mounting build plate strut to build plate angle mount.
* (2x) Drill 2 M6 holes on 1.5in. side for attaching build plate strut to build plate.
    * Drill M6 holes with 17/64in. or similar drill bit. This larger hole makes it easier to insert and remove build plate after prints.

<img src="images/build_plate_strut_manufacturing.jpg" width="1200"/>

<img src="images/build_plate_struts.jpg" width="1200"/>

<div style="page-break-after: always;"></div>

### Build Plate Manufacturing <a name="Build-Plate-Manufacturing"></a>
* Cut 0.25in. aluminum sheet to 270mm by 150mm.
* Drill 4 M6 holes for mounting build plate to build plate strut.
* Drill M3 holes around build plate border for resin drainage.

<img src="images/build_plate_manufacturing.jpg" width="1200"/>

<img src="images/build_plate_1.jpg" width="1200"/>

<img src="images/build_plate_2.jpg" width="1200"/>

<img src="images/build_plate_3.jpg" width="1200"/>

<div style="page-break-after: always;"></div>

### (2x) Motor Mount Plate Manufacturing <a name="Motor-Mount-Plate-Manufacturing"></a>
* (2x) Cut 0.125in. aluminum sheet to 440mm by 50mm.
* (2x) Drill 4 M5 holes for mounting motor mount plate to frame.
* (2x) Drill 4 M4 holes for mounting stepper motor mount to motor mount plate.

<img src="images/motor_mount_plate_manufacturing.jpg" width="1200"/>

<div style="page-break-after: always;"></div>

### Projector Backplate Manufacturing <a name="Projector-Backplate-Manufacturing"></a>
* Cut 0.125in. aluminum sheet to 440mm by 200mm.
* Drill 4 M5 holes for mounting projector backplate to frame.
* Drill 3 M4 holes for mounting projector to projector backplate.
* Drill 4 2.75mm holes for mounting Raspberry Pi 3B+. 
* Drill 3 3.50mm holes for mounting RAMPS 1.4.
* Drill 4 3.50mm holes for mounting relay.
* Drill 1 3.50mm hole for mounting DHT11 temperature sensor.
* Cut 2 M5 slots for magnifying lens mount.

<img src="images/projector_backplate_manufacturing.jpg" width="1200"/>

<img src="images/projector_backplate.jpg" width="1200"/>

<div style="page-break-after: always;"></div>

### (4x) Stabilizer Mount Manufacturing <a name="Stabilizer-Mount-Manufacturing"></a>
* (4x) Mill 55mm x 20mm x 20mm block out of aluminum or plastic.
* (4x) Drill 2 M5 holes through the 55mm x 20mm face for bolts to pass through.

<img src="images/stabilizer_mount_manufacturing_horizontal.jpg" width="600"/> <img src="images/stabilizer_mount_manufacturing_vertical.jpg" width="600"/>

<img src="images/stabilizer_mounts_1.jpg" width="1200"/>

<img src="images/stabilizer_mounts_2.jpg" width="1200"/>

<div style="page-break-after: always;"></div>

### Endstop Mount Manufacturing <a name="Endstop-Mount-Manufacturing"></a>
* Endstop must be positioned slightly below the top of the frame so that it is triggered when the build plate is at its maximum height.
* Measure distance from top of build plate angle mount to top of the frame, cut 0.125in. aluminum sheet to roughly 25mm x the measured height.
* Drill two 13/64in. holes roughly 10mm from one edge of the aluminum mount, these holes will be used to connect the mount to the top of the printer frame via M5 bolts.
* Measure correct position for endstop and mark this level as a straight line on the aluminum mount. Across this line drill two 9/64in. holes that are 20mm apart. These holes are used to connect the endstop to the endstop mount.

<div style="page-break-after: always;"></div>

### Lens Holder Manufacturing <a name="Lens-Holder-Manufacturing"></a>
* 3d printed lens holder. If holes are not big enough for an M5 bolt to pass through, expand the holes with a 13/64in. drill bit. 
* Center of lens is 80mm from the projector backplate. At this distance the projector light passes through the middle of the lens which distorts the light rays the least.
* Mounting holes are 80 mm apart.

<img src="images/lens_holder_ring_manufacturing.jpg" width="700"/>
<img src="images/lens_holder_arms_manufacturing.jpg" width="700"/>

<img src="images/lens_holder_base_manufacturing.jpg" width="1400"/>

<div style="page-break-after: always;"></div>

### Shutter Manufacturing <a name="Shutter-Manufacturing"></a>
* Aluminum Sheet 0.16in x 4in x 10in used.
* Place lens holder on copper sheet and trace outline of lens holder size.
* Draw full shutter outline on copper sheet, account for the distance from the servo motor arm to the projector lens.
* Cut copper sheet around the outline with scissors.
* Drill holes to connect shutter to the servo motor.
* Sand shutter edges and surfaces, clean with isopropyl alcohol (IPA).

<div style="page-break-after: always;"></div>

### Hinge Jig Manufacturing <a name="Hinge-Jig-Manufacturing"></a>
* 1in. x 1in. x 0.125in. angle is cut to 100mm length.
* Drill 6 M5 holes for 3 different hinge spaces (10mm, 13mm, 13.6mm).
* Note that because angle has 3.175mm wall, holes must be offset by 3.175mm.
    * When using jig, the wall of the angle will be pressed against the edge of the PVC sheet.

<img src="images/hinge_jig_manufacturing.jpg" width="800"/>

<div style="page-break-after: always;"></div>


### Back Panel Manufacturing <a name="Back-Panel-Manufacturing"></a>
* 0.125in. PVC sheet is cut to 956mm by 446mm.
* Drill 12 M5 for 6 hinges.
* Drill 2 M5 holes to mount lower right side to frame.

<img src="images/back_panel_manufacturing.jpg" width="1000"/>

<img src="images/back_panel.jpg" width="1000"/>

<div style="page-break-after: always;"></div>

### Side Panel 1 Manufacturing <a name="Side-Panel-1-Manufacturing"></a>
* 0.125in. PVC sheet is cut to 590mm by 340mm.
* Drill 4 M5 for 2 hinges.
* Drill 2 M5 holes to mount left side to frame.

<img src="images/side_panel_1_manufacturing.jpg" width="1000"/>

<img src="images/side_panel_1.jpg" width="1000"/>

<div style="page-break-after: always;"></div>

### Side Panel 2 Manufacturing <a name="Side-Panel-2-Manufacturing"></a>
* 0.125in. PVC sheet is cut to 590mm by 340mm.
* Drill 4 M5 holes for 2 hinges.

<img src="images/side_panel_2_manufacturing.jpg" width="1000"/>

<img src="images/side_panel_2.jpg" width="1000"/>

<div style="page-break-after: always;"></div>

### (2x) Side Window Manufacturing <a name="Side-Window-Manufacturing"></a>
* 0.125in. acrylic sheet is cut to 360mm by 340mm.
* (2x) Drill 4 M5 holes for 2 hinges.

<img src="images/side_window_manufacturing.jpg" width="1000"/>

<img src="images/side_window_1.jpg" width="1000"/>

<img src="images/side_window_2.jpg" width="1000"/>

<div style="page-break-after: always;"></div>

### Lower Front Panel Manufacturing <a name="Lower-Front-Panel-Manufacturing"></a>
* 0.125in. PVC sheet is cut to 593mm by 446mm.
* Drill 4 M5 holes for 2 hinges.

<img src="images/lower_front_panel_manufacturing.jpg" width="1000"/>

<img src="images/lower_front_panel.jpg" width="1000"/>

<div style="page-break-after: always;"></div>

### Upper Front Panel Manufacturing <a name="Upper-Front-Panel-Manufacturing"></a>
* 0.125in. PVC sheet is cut to 446mm by 363mm.
* Drill 4 M5 holes to mount sheet to frame.

<img src="images/upper_front_panel_manufacturing.jpg" width="1000"/>

<img src="images/upper_front_panel.jpg" width="1000"/>

<div style="page-break-after: always;"></div>

### Top Panel Manufacturing <a name="Top-Panel-Manufacturing"></a>
* Note that on the first build of the Mark 1, the corner holes that the projector feet pass through did not align correctly. Holes needed to be closer than 13mm from the panel edge.
* 0.125in. PVC sheet is cut to 446mm by 340mm.
* Drill 4 M5 holes to mount sheet to tapped holes in the top of the frame.

<img src="images/top_panel_manufacturing.jpg" width="1000"/>

<img src="images/top_panel.jpg" width="1000"/>

<div style="page-break-after: always;"></div>

### Bottom Panel Manufacturing <a name="Bottom-Panel-Manufacturing"></a>
* Note that on the first build of the Mark 1, the corner holes that the projector feet pass through did not align correctly. Holes needed to be closer than 13mm from the panel edge.
* 0.125in. PVC sheet is cut to 446mm by 340mm.
* Drill 4 M4 (10-32 threaded bolt) holes for projector feet to pass through. On first build used 13/64in. drill bit for these holes.
* Drill 4 M5 holes to mount sheet to frame.

<img src="images/bottom_panel_manufacturing.jpg" width="1000"/>

<img src="images/bottom_panel.jpg" width="1000"/>

<div style="page-break-after: always;"></div>

### Decal Manufacturing <a name="Decal-Manufacturing"></a>
* Design decals in figma.
    * Select any overlapping lines in figma -> right click -> Outline Stroke
    * This turns any line with thickness into outlines instead of a single thin line.
    * Export decals as SVG files.
* In Fusion create a new component.
    * Create an outline of the correct extrusion shape and extrude this shape 1mm.
    * Insert -> Insert SVG, then cancel the operation before running the same commands again.
    * Due to a bug, the second time that the SVG is inserted in Fusion you will have the ability to scale and move the SVG file.
    * Scale and move SVG so that it fits over the decal size, extrude away decal sections.
    * Right click on the component -> Save as Mesh -> Export as STL.
* On 3D printer, shine the decal layer on the bottom of the resin vat with the build plate retracted.
    * Shine layer for 10 seconds.
    * After decals have been cleaned, place under a flat weighted surface so that they do not curl when drying.
* After decals have dried, apply clear epoxy to the back of the decal and adhere decals to the build plate and motor mount plates.
    * The layer of epoxy should evenly cover the entire back of the decal or else the transparent decal will end up with spotty coloring.

<img src="images/motor_mount_decal_manufacturing.jpg" width="800"/>

<div style="page-break-after: always;"></div>

## Construction <a name="Construction"></a>

### Resin Vat Construction <a name="Resin-Vat-Construction"></a>

#### Adhere FEP Film to Glass
* 12in. x 8in. borosilicate glass is already the correct dimension so it does not need to be cut.
* Cut FEP film to 270mm x 150mm.
* Position resin vat over glass and mark where the corners of the vat are, orient the FEP film within the corners appropriately and lay it on the glass.
    * Mark slightly outside the corners of the FEP film. These markers serve as guides when applying the FEP film.
* Make sure that glass it thoroughly cleaned before applying FEP film.
* On the edge of the FEP film, one side of the edge is slightly rough. This side is the adhesive side (release liner) side of the film.
* Use knife or razor blade then tweezers to slightly peel one corner. Note that all parts of the adhesive that are touched will be compromised so touch as little of the corner as possible.
* Align exposed corner of the FEP film with the top left corner marker and begin FEP application process.
    * Peel away a small corner of the release liner from under the FEP, then press down evenly across the FEP film with a tissue from the top to adhere it to the glass.
    * Always peel the FEP film away at the same angle (roughly 45 degrees).
    * Peel small amounts of the adhesive backing at a time to avoid the creation of air bubbles.
    * After a small amount of FEP has been peeled, begin gently pressing down over a region that is already been adhered to the glass before slowly working the pressure towards the newly exposed FEP film.
    * Always keep tension on the non-adhered portion of the FEP film.
    * Air bubbles form when exposed FEP that is not immediately to the right of the already adhered portion makes contact with the glass. The above two steps are meant to prevent this.

#### Construct Resin Vat
* Mark areas where angle intersect, then apply adhesive sealant to all surfaces that will make contact.
* Press angle together and orient correctly so that the vat forms 90 degree angles and angle pieces are even.
    * Make sure that the shorter walls are vertically aligned and not tilting inwards.
* Use a flat end stick to press sealent into corners.
* Set curing position by pressing all four sides of the vat with heavy objects. Make sure that the curing position is correct.
* Use isopropyl alcohol to clean excessive adhesive that may have accidentally rubbed on the vat.
* Leave to cure for at least 12 hours.

<img src="images/resin_vat_construction.jpg" width="1200"/>

#### Adhere Glass to Resin Vat
* Lay glass on resin vat and draw outline of glass to mark the boundary of where adhesive sealant goes.
* Between outline and inside of resin vat, lay a thick bead of adhesive sealant.
    * Adhesive bead must be thick and continuous to create a full seal.
    * Do not lay the bead close to the resin vat inside edge to avoid covering FEP film or blocking the build plate when bead is compressed.
* Align glass with outline and gently lay it on the adhesive sealant bead. Let gravity begin the sealing process. Gently press out any air bubbles after. 
* Leave to cure for at least 12 hours.
* Adhesive sealant that is stuck to the glass can be removed with isopropyl alcohol (IPA). IPA will leave a smudge on the glass that can be rubbed out by rubbing on it with a paper towel or tissue paper for an extended period of time.

<div style="page-break-after: always;"></div>

### Frame Construction <a name="Frame-Construction"></a>

#### Lower Frame Section
* Tap 600mm linear rail pieces and attach threaded feet.
    * Use 10-32 tap. To prevent bit from getting stuck while tapping, drill in short bursts.
* Build lower frame rectangles made of 600mm and 400mm linear rail.
    * Use M4 x 16mm bolts for connecting stepper motor mounts to motor mount plates.
    * Optionally place M4 nuts and washers between the motor mount and motor mount plates to align the stepper motor with the linear drive rod.
    * Note that both linear drive rods must be perfectly vertical. Nuts and washers provide slight adjustments to the stepper motor position.
    * Use clear epoxy to adhere motor mount decal to motor mount plate.
    * Attach stepper motors to stepper motor mounts, make sure that wires are facing the correct direction.
    * Use M5 x 8mm bolts to connect motor mount plates to frame.
    * Attach magnets to the lower frame section before constructing frame.
* Attach 300mm linear rail to lower frame rectangle to construct lower frame.
    * Before attaching 300mm linear rail, put in T-nuts for holding gussets, the resin vat, and a magnet.
* Attach lower stabilizer mounts to linear rail using M4 x 30mm bolts.

<img src="images/stepper_motors_1.jpg" width="1000"/>

<img src="images/stepper_motors_2.jpg" width="1000"/>

#### Upper Frame Section
* Attach linear guides to 400mm double linear rail. 
* Attach 400mm double linear rail vertically.
* Attach upper stabilizer mounts to linear rail using M4 x 30mm bolts.
* Tap outer corner holes in the double linear rail for mounting the top panel.
    * Tap with a M5 tap bit.

<div style="page-break-after: always;"></div>

### Internals Construction <a name="Internals-Construction"></a>

#### Build Plate, Strut, and Angle Mount Construction
* Use M3 x 10mm bolts and nuts to attach copper nuts to build plate angle mounts.
* Use M3 x 6mm bolts to mount build plate angle mounts to linear guide carriages.
* Feed linear guide rods through stabilizer mounts and copper nut, connect to stepper motor.
* Use M5 x 8mm bolts to connect build plate struts to build plate angle mounts.

#### Build Plate Construction
* Sand build plate with 80 grit sandpaper. Sand in one direction.

<div style="page-break-after: always;"></div>

### Panel Construction <a name="Panel-Construction"></a>
* When drilling holes in the panel with the use of the hinge jig, first drill through the PVC with a small drill bit after pounding the desired hole location.
    * This ensures that larger M5 holes do not deviate from the location that was pounded into the PVC.
    * Use a 3/32 in. bit or similar.

#### Bottom Panel Construction
* Once the bottom panel has been manufactured, attach it to the bottom of the frame with M5 bolts and the projector feet.
* Place Power Strip and Power Supply in their desired locations on the bottom panel, use marker to mark the position of the bolts that will mount these parts to the bottom panel.
* Measure and drill triangular bolt pattern on the electric heater side.
    * Bolt pattern is a triangle with side lengths 100mm and 40mm.
* Draw bolt pattern on the bottom panel.
* Drill M3 holes to mount the Power Strip, M4 holes to mount the Power Supply, and M4 holes to mount electric heater

#### Rest of Panels Construction
* Measure and mark hole locations on the back panel first. The marks on this panel will serve as a guide for hole locations on all adjacent panels.
    * Note, for M5 holes you can use a 7/32in. drill bit instead of a 13/64in. drill bit to increase the margin for error.
    * Note, connect the panels to the frame using thicker T-nuts instead of thin T-nuts that can be placed in linear rail track.
    * Mark and drill 0.365in. hole for power strip. 25/64in. drill bit used for drilling hole.
* Next mark the hole positions on side panel two. Afterwards align the panel with the back panel to verify that hinge hole placement lines up.
* Repeat the same steps for the side window panels and then side panel one. Finish with the front panels.
* After marking hole locations, pound hole locations using jig.
* Drill holes in the back panel, side panel two, and one of the side windows. Assemble these three panels to the frame to confirm correct manufacturing and construction.
* Afterwards, drill holes in all other panels and assemble all panels to the frame to verify correct construction.
    * Note that hinges are attached with the hinge bearing facing inwards.
* After confirming that panels fit, remove panels for post-processing.
    * De-burr holes, bevel hole openings, sand rough edges, and clean panels.

<div style="page-break-after: always;"></div>

## Assembly <a name="Assembly"></a>

### Projector Backplate Assembly <a name="Projector-Backplate-Assembly"></a>
* Use clear epoxy to adhere backplate decal to the projector backplate.
* Mount projector to backplate with M4 x 12mm bolts.
* Mount Raspberry Pi 3B+ to backplate with M2 x 20mm bolts. 
    * Pi must be mounted as far as possible from the backplate for cords to fit.
* Mount RAMPS 1.4 to backplate with M3 x 25mm bolts.
    * RAMPS 1.4 must be mounted as close as possible to backplate for cords to fit.
* Make sure that no pins on either board touch the backplate or the bolts that connect the board to the backplate.
* Attach lens holder to backplate with M5 x 15mm bolts.
* Adhere servo motor to backplate with double sided adhesive foam. 
    * Note that the servo motor should be mounted reverse of how it is mounted in the picture below. The servo motor arm should be close to the backplate decal, not close to the lens holder as it is pictured.
    * Because the servo motor only has a movement range of 270 degrees, the arm must be close to the backplate decal for the shutter to be able to fully unblock the projector lens.
* Construct 12V to 5V LM7805 step down mechanism.
    * For each LM7805 voltage regulator (2x) solder a red wire to the positive pin, a black wire to the negative pin, and a white wire to the output pin.
    * Solder the two white wires to an additional white wire that has a female connector. This connector is plugged into the 5V pin on the RAMPS 1.4 board.
* Perform cable management.

<img src="images/assembled_backplate_front.jpg" width="1000"/>

<img src="images/assembled_backplate_electronics.jpg" width="1000"/>

<img src="images/assembled_backplate_side.jpg" width="1000"/>

### Projector Backplate Electronics Assembly <a name="Projector-Backplate-Electronics-Assembly"></a>
* Raspberry Pi Model 3B+.
    * 5V/2.5A black power cable connects to Raspberry Pi Model 3B+.
    * Black HDMI cable connects Raspberry Pi to projector.
    * Blue USB cable connect Raspberry Pi to RAMPS 1.4 board. Note that this USB cable plugs into the bottom right USB port on the Raspberry Pi. 
    * DHT11 temperature sensor wires connect to Raspberry Pi GPIO pins. Red wire (5V power) to Pin 2. Brown wire (control) to Pin 7 (GPIO 4). Black wire (ground) to Pin 6.
* RAMPS 1.4 Board.
    * Solder two wires to the 12V/5A power supply cords to extend them if necessary. Cover soldered wire with electrical tape.
    * 12V/5A power supply (not pictured) connects to green RAMPS 1.4 terminal blocks. 
    * Red and black wires connect 12V RAMPS power supply to (2x) LM7805 12V to 5V voltage step downs. The white wire 5V output is connects to the 5V middle pin on the RAMPS 1.4 board.
    * Servo motor wires connect stepper motor 1 slot (stepper motor pins closest to the green terminal blocks) to the servo motor. Black wire is closest to the outside of the RAMPS 1.4 board and white wire is closest to the stepper motor driver. Note that this is reversed in the pictures. These pictures are incorrect and the servo motor connector should be the reverse of what it is in the photos. 
    * (2x) stepper motor wires connect to stepper motor pins located next to the A4988 stepper motor driver. Blue wires are closest to the RAMPS 1.4 terminal blocks.
    * Endstop wires connect to Z-max endstop pins which are the 3 pins farthest from the RAMPS 1.4 terminal blocks (just below the 4 pin connector). Red wire is closest to the stepper motor pins and white wire is closest to the edge of the RAMPS 1.4 board.
* Relay Module.
    * Connect two exposed wires from the heater to the Common and Normally Open terminals on the relay.
    * Connect wires to terminal 1, the blue terminal below the yellow jumper.
    * The Common terminal is in the middle, and the Normally Open is the right terminal if the blue relay boxes are pointed towards you.
    * Power relay wires connect to Raspberry Pi GPIO pins. Red wire (5V power) from VCC to Pin 4. Brown wire (control) from ln1 to Pin 11 (GPIO 17). Black wire (ground) to Pin 9.

<img src="images/backplate_electronics_1.jpg" width="500"/> <img src="images/backplate_electronics_2.jpg" width="500"/> <img src="images/backplate_electronics_4.jpg" width="500"/> <img src="images/backplate_electronics_3.jpg" width="500"/>

### Bottom Panel Assembly <a name="Bottom-Panel-Assembly"></a>
* Mount power supply to panel with (2x) M4 x 8mm bolts and (2x) M4 nuts.
* Mount power strip to panel with (4x) M3 x 10mm bolts and (4x) M3 nuts.
* Mount electric heater to panel with (4x) M4 x 20mm bolts and (12x) M4 nuts.
    * Use nuts to position electric heater off the ground so that it is not touching the bottom panel.

<img src="images/assembled_bottom_panel.jpg" width="1200"/>

### Full Frame Printer Assembly <a name="Full-Frame-Printer-Assembly"></a>

**Assembly order:**

* Attach linear guides and slide block to linear rail.
* Attach build plate angle mount to linear guides.
* Attach stepper motors to motor mount plates.
    * Care that all washers, bolts, and nuts are secure. Check that motor aligns with mount plate.
* Loosely attach motor mount plates and stabilizer mounts to frame.
* Lay frame on one side and pass linear guide rod through stabilizer mounts, copper nut, and into stepper motor.
* Align all linear guide rod components so that the linear guide rod is perfectly straight before securing stabilizer mounts and motor mount plate to frame.
    * Move build plate angle mount up and down to verify that linear guide rod is straight throughout the whole movement without any bending.
* Attach projector backplate to frame.
* Attach bottom panel to frame.
* Connect electronics between projector backplate and bottom panel, perform wire management.
* Attach build plate struts and build plate to linear movement components.
* Attach resin vat to frame.

## Calibration <a name="Calibration"></a>

### Lens Calibration <a name="Lens-Calibration"></a>
* Even after measuring build area and calculating resolution, parts are still incorrectly scaled (parts are slightly bigger than designed in CAD, i.e. a 20mm x 20mm square will print as 21mm x 21mm).
* This is addressed by scaling the resolution settings.
    * Bigger Resolution -> Smaller Projection Image
    * For example, the ideal scaling for the 300mm lens on maximum zoom is 103.5% of the measured resolution.
* Optimal scaling may vary by lens focal length and projector zoom. To find the ideal scaling:
    * Create a test part with specific dimensions.
    * Cover bottom side of the resin vat with cover, project the test part onto the cover.
    * Measure the size of the projected image, adjust resolution measurements by the appropriate scaling factor until the projected image is the correct size.

**300mm lens**
* Barrel Factor = 0.50
* Barrel Center X = 960
* Barrel Center Y = 750 

* Maximum Zoom
    * Optimal scaling factor is 103.5%
    * 6.62in x 3.75in
    * 168.15mm x 95.25mm (1.765 ratio)
    * X res: 168.15mm x 1000 / 1920 = 87.58 micron * 1.035 scaling factor = 90.65 micron
    * Y res: 95.25mm x 1000 / 1080 = 88.19 micron * 1.035 scaling factor = 91.28 micron

* Zoom scroll in middle.
    * 7.52in x 4.19in
    * 191.01mm x 106.43mm (1.794 ratio)
    * X res: 191.01mm x 1000 / 1920 = 99.48 micron
    * Y res: 106.43mm x 1000 / 1080 = 98.55 micron

* Minimum Zoom
	* 8.50in x 4.75in
	* 215.90mm x 120.65mm (1.789 ratio)
	* X res: 215.90mm x 1000 / 1920 = 112.45 micron
	* Y res: 120.65mm x 1000 / 1080 = 111.71 micron	

**200mm lens**
* Barrel Factor = 0.40
* Barrel Center X = 960
* Barrel Center Y = 750 

* Maximum Zoom
	* 5.85in x 3.28in
	* 148.59mm x 83.31mm (1.784 ratio)
	* X res: 148.59mm x 1000 / 1920 = 77.39 micron
	* Y res: 83.31mm x 1000 / 1080 = 77.14 micron

**500mm lens**
* Barrel Factor = 0.05
* Barrel Center X = 960
* Barrel Center Y = 750 

* Minimum Zoom
	* 9.03in x 5.14in
	* 229.36mm x 130.56mm (1.756 ratio)
	* X res: 229.36mm x 1000 / 1920 = 119.46 micron
	* Y res: 130.56mm x 1000 / 1080 = 120.89 micron

### Quality Checks <a name="Quality-Checks"></a>

#### Vertical Alignment of Linear Drive Rods
* Both linear drive rods must be perfectly vertical. 
* Use calipers to measure the distance between the linear drive rod and the frame in all four sections where the linear guide rod passes in front of the frame.
* Place nuts and washers between the stepper motor mounts and motor mount plates to nudge the stepper motor to the correct distance.

<div style="page-break-after: always;"></div>

## Specs <a name="Specs"></a>

#### Print Size and Resolution
* Max Z Height: 218.8mm
* Max Print Size: 230mm x 130mm @ 120 micron resolution.
* Middle Print Size: 191mm x 107mm @ 99 micron resolution.
    * 300mm lens with zoom scroll in middle.
* Minimum Print Size: 150mm x 80mm @ 77 micron resolution.

* Max Print Volume = ~ 230mm x 130mm x 220mm.

* Lens is mounted 273mm from resin vat.

<div style="page-break-after: always;"></div>

