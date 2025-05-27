New Updates:
		
1) Few underlying bugs that slowed the script were found and cleared.
2) The control keys were minimized from 4 to 2. Previously, we had s, p, c and t for stop(mute), pause, continue and terminate respectively. In this version, muting the alarm , pausing the detection and resuming the detection are controlled by a single key 'p'. Termination is done by pressing 'Esc' key.
3) The low hanging cable detection performed at the immediate emergenace of the cable in the frame is skipped. Instead the alarm is only turned ON when the low hanging cable crosses a particular pixel in the x-direction. This eases the user to understand the location of the cable in the frame for accurately. Also, errors occured due to wrong detection of the black edges of the skid as cables are rectified.

