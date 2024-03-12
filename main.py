import board
from digitalio import DigitalInOut, Direction, Pull
import adafruit_dotstar as dotstar
import time
import neopixel

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# NeoPixel strip of 12 LEDs on circular pcb
NUMPIXELS = 12
right_neopixels = neopixel.NeoPixel(board.D4, NUMPIXELS, brightness=1, auto_write=False)
left_neopixels = neopixel.NeoPixel(board.D2, NUMPIXELS, brightness=1, auto_write=False)

# Related to neopixel animations
dot_color_index = 0
j = 0

######################### HELPERS ##############################

# Helper to convert analog input to voltage
def getVoltage(pin):
    return (pin.value * 3.3) / 65536

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0) or (pos > 255):
        return (0, 0, 0)
    if pos < 85:
        return (int(255 - pos*3), int(pos*3), 0)
    elif pos < 170:
        pos -= 85
        return (0, int(255 - (pos*3)), int(pos*3))
    else:
        pos -= 170
        return (int(pos*3), 0, int(255 - pos*3))

def turn_off_neopixels(neopixels, numpixels):
    i = 0
    while i < numpixels:
       neopixels[i] = wheel(-1)
       i = i + 1
    neopixels.show()

def set_all_neopixels_to_color(neopixels, numpixels, color):
    i = 0
    while i < numpixels:
       neopixels[i] = color
       i = i + 1
    neopixels.show()

def set_neopixels_to_rainbow_swirl(neopixels, numpixels, seconds_between_pixel_sets=0.07):
    delta_between_pixels = 21
    i = 0
    j = 0
    while i < numpixels:
        neopixels[i] = wheel(j)
        i = i+1
        j = j+delta_between_pixels
        time.sleep(seconds_between_pixel_sets)
        neopixels.show()    


######################### RAINBOW SWIRL ANIMATION ##############################
def rainbow_swirl(right_neopixels, left_neopixels, numpixels, seconds=1.5):
    turn_off_neopixels(right_neopixels, numpixels)
    turn_off_neopixels(left_neopixels, numpixels)
    set_neopixels_to_rainbow_swirl(right_neopixels, numpixels)
    set_neopixels_to_rainbow_swirl(left_neopixels, numpixels)
    time.sleep(seconds)


######################### FLASH COLOR ANIMATION ##############################
def flash_through_colors(right_neopixels, left_neopixels, numpixels, target_iterations=5):
    i = 0
    current_iterations = 0

    while current_iterations < target_iterations:
        i = (i+10) % 256  # run from 0 to 255
        target_color = wheel(i)
        set_all_neopixels_to_color(right_neopixels, numpixels, target_color)
        set_all_neopixels_to_color(left_neopixels, numpixels, target_color)
        time.sleep(0.2)
        turn_off_neopixels(right_neopixels, numpixels)
        turn_off_neopixels(left_neopixels, numpixels)
        time.sleep(0.2)
        current_iterations = current_iterations + 1
        

######################### CLOCKWISE TO VIEWER ANIMATION ##############################
	
def both_clockwise_to_viewer_rotation(right_neopixels, left_neopixels, dot, numpixels, target_iterations=1000):
    i = 0
    j = 0
    current_iterations = 0
    
    while current_iterations < target_iterations:
        # spin internal LED around! autoshow is on
        dot[0] = wheel(i & 255)

        #disable previous led
        disable_previous_led_clockwise_to_viewer_rotation(right_neopixels, j, numpixels)
        disable_previous_led_clockwise_to_viewer_rotation(left_neopixels, j, numpixels)

        right_neopixels[j] = wheel(i)
        left_neopixels[j] = wheel(i)
        right_neopixels.show()
        left_neopixels.show()
    
        j = j+1

        i = (i+1) % 256  # run from 0 to 255
        # reset j back to first led in strip
        if(j == numpixels):
            j = 0
        current_iterations = current_iterations + 1
        
        time.sleep(0.03) # make bigger to slow down

def disable_previous_led_clockwise_to_viewer_rotation(neopixels, index, numpixels):
    if(index == 0):
        neopixels[numpixels-1] = wheel(-1)
    else:
        neopixels[index-1] = wheel(-1)

def disable_previous_led_counter_clockwise_to_viewer_rotation(neopixels, index, numpixels):
    if(index == numpixels-1):
        neopixels[0] = wheel(-1)
    else:
        neopixels[index+1] = wheel(-1)

######################### CLOCKWISE/COUNTER CLOCKWISE TO VIEWER ANIMATION ##############################
	
def clockwise_counter_clockwise_to_viewer_rotation(right_neopixels, left_neopixels, dot, numpixels, target_iterations=1000):
    i = 0
    j = 0
    k = numpixels-1
    current_iterations = 0
    
    while current_iterations < target_iterations:
        # spin internal LED around! autoshow is on
        dot[0] = wheel(i & 255)

        #disable previous led
        disable_previous_led_clockwise_to_viewer_rotation(right_neopixels, j, numpixels)
        disable_previous_led_counter_clockwise_to_viewer_rotation(left_neopixels, k, numpixels)

        right_neopixels[j] = wheel(i)
        left_neopixels[k] = wheel(i)
        right_neopixels.show()
        left_neopixels.show()
    
        j = j+1
        k = k-1

        i = (i+1) % 256  # run from 0 to 255
        # reset j back to first led in strip
        if(j == numpixels):
            j = 0
        # reset k back to last led in strip
        if(k < 0):
            k = numpixels-1

        current_iterations = current_iterations + 1
        
        time.sleep(0.03) # make bigger to slow down



######################### TURN ON ALL LIGHTS AND ITERATE THROUGH COLORS ANIMATION ##############################

def turn_on_all_lights_and_iterate_through_colors(right_neopixels, left_neopixels, dot, numpixels, target_iterations=1000):
    i = 0
    j = 0
    current_iterations = 0
    
    while current_iterations < target_iterations:
        # spin internal LED around! autoshow is on
        dot[0] = wheel(i & 255)

        right_neopixels[j] = wheel(i)
        left_neopixels[j] = wheel(i)
        right_neopixels.show()
        left_neopixels.show()
    
        j = j+1

        i = (i+1) % 256  # run from 0 to 255
        # reset j back to first led in strip
        if(j == numpixels):
            j = 0
        current_iterations = current_iterations + 1
        
        time.sleep(0.03) # make bigger to slow down
    turn_off_neopixels(right_neopixels, NUMPIXELS)
    turn_off_neopixels(left_neopixels, NUMPIXELS)



######################### MAIN LOOP ##############################

while True:
  rainbow_swirl(right_neopixels, left_neopixels, NUMPIXELS)
  flash_through_colors(right_neopixels, left_neopixels, NUMPIXELS)
  clockwise_counter_clockwise_to_viewer_rotation(right_neopixels, left_neopixels, dot, NUMPIXELS, 100)
  turn_on_all_lights_and_iterate_through_colors(right_neopixels, left_neopixels, dot, NUMPIXELS, 100)
  both_clockwise_to_viewer_rotation(right_neopixels, left_neopixels, dot, NUMPIXELS, 100)
  
  
