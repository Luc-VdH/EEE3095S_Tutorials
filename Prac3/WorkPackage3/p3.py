# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import time

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
guess = 0
value = 0
guess_count = 0

# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()
pb = None
pled = None


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    global value
    global guess
    global guess_count
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        while not end_of_game:
            pass
        end_of_game = None
        if value == guess:
            print("Well done! You won the game with a guess count of", guess_count, "!")
            save_scores()
        else:
            print("You're final guess was incorrect.")
        guess_count = 0
        guess = 0
        value = 0

    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    if count != 0:
        print("There are {} scores. Here are the top 3!".format(count))
        # print out the scores in the required format
        names =[]
        scores=[]
        name = ""
        i = 0
        while i <len(raw_data):
            if((i+1)%4==0):
                scores.append(raw_data[i])
                i += 1
            else:
                for j in range(3):
                    name += str(raw_data[i+j])
                i += 3
                names.append(name)
                name = ""
        print(names)
        for i in range(3):
            print((i+1)," - {} took {} guesses".format(str(names[i]),str(scores[i])))
    else:
        print("There are {} scores.".format(count))
    


# Setup Pins
def setup():
    global pb
    global pled
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
    # Setup regular GPIO
    GPIO.setup(LED_value, GPIO.OUT)
    GPIO.output(LED_value, GPIO.LOW)
    GPIO.setup(btn_submit, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(btn_submit, GPIO.FALLING, callback=btn_guess_pressed, bouncetime=200)
    GPIO.setup(btn_increase, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(btn_increase, GPIO.RISING, callback=btn_increase_pressed, bouncetime=200)
    # Setup PWM channels
    GPIO.setup(LED_accuracy, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)

    pb = GPIO.PWM(buzzer, 1)
    pb.start(0)
    pled = GPIO.PWM(LED_accuracy, 1000)
    pled.start(0)

    # Setup debouncing and callbacks
    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = None
    score_count= int(eeprom.read_byte(0))
    # Get the scores
    scores = []
    if score_count != 0:
        scores= eeprom.read_block(1,4*score_count)
        
        # convert the codes back to ascii
        for i in range(len(scores)):
            if((i+1)%4==0):
                pass
            else:
                scores[i]= chr(scores[i])
    # return back the results
    return score_count, scores


# Save high scores
def save_scores():
    global guess_count

    # fetch scores
    score_count= int(eeprom.read_byte(0))
    fInfo= eeprom.read_block(1,4*score_count)

    # include new score
    user = input("Please enter three letters as your username: ")
    while len(user) != 3:
        user = input("Please enter three letters as your username: ")
    print(fInfo)

    # sort
    scores=[]
    count=0
    userScore=[]
    name=""
    for i in range(len(fInfo)):
        if count==3:
            userScore.append(name)
            userScore.append(fInfo[i])
            score.append(userScore)
            count=0
            name=""
        else:
            name += chr(fInfo[i])
            count += 1
    scores.sort(key=lambda x: x[1])
    data_to_write = []
    for i, score in enumerate(scores):
        # get the string
        for letter in score[0]:
            data_to_write.append(ord(letter))
        data_to_write.append(score[1])
        

    # update total amount of scores
    score_count += 1

    # write new scores
    print(score_count)
    print(fInfo)
    eeprom.write_block(0, [score_count])
    eeprom.write_block(1,data_to_write)
    


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
    global guess
    global LED_value
    if guess == 7:
        guess = 0
    else:
        guess += 1
    bits = "{:0>3b}".format(guess)
    if bits[0] == '1':
        GPIO.output(LED_value[2], GPIO.HIGH)
    else:
        GPIO.output(LED_value[2], GPIO.LOW)

    if bits[1] == '1':
        GPIO.output(LED_value[1], GPIO.HIGH)
    else:
        GPIO.output(LED_value[1], GPIO.LOW)

    if bits[2] == '1':
        GPIO.output(LED_value[0], GPIO.HIGH)
    else:
        GPIO.output(LED_value[0], GPIO.LOW)




# Guess button
def btn_guess_pressed(channel):
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    global pb
    global pled
    global guess_count
    global end_of_game

    start_time = time.time()
    while GPIO.input(channel) == 0:
        pass
    button_time = time.time() - start_time
    if button_time >= 3:
        end_of_game = True
        pb.stop()
        pled.stop()
        GPIO.output(LED_value, GPIO.LOW)
        
    elif button_time >= 0.1:
        guess_count += 1
        accuracy_leds()
        trigger_buzzer()
    

# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    global guess
    global value
    global pled
    dc = 0 
    dif = abs(guess - value)
    # if guess < value:
    #     dc = (guess/value)*100
    # elif guess > value:
    #     dc = ((8-guess)/(8-value))*100
    # else:
    #     dc = 100
    dc = ((7-dif)/7)*100
    print(dc)
    pled.ChangeDutyCycle(dc)

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    global guess
    global value
    global pb
    dif = abs(value - guess)
    if dif == 3:
        pb.ChangeDutyCycle(1)
        pb.ChangeFrequency(1)
    elif dif == 2:
        pb.ChangeDutyCycle(1)
        pb.ChangeFrequency(2)
    elif dif == 1:
        pb.ChangeDutyCycle(1)
        pb.ChangeFrequency(4)
    else:
        pb.ChangeDutyCycle(0)
        pb.ChangeFrequency(1)


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        guess = 0
        value = 0
        GPIO.output(LED_value, GPIO.LOW)
        pled.stop()
        pb.stop()
        GPIO.cleanup()
