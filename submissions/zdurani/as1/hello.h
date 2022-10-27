//ENSC 351 Assignent 1 - hello.h file
//Student Name: Zohra Khan Durani, Student Number: 301396012
//References: Utilized the code that was provided to us in the Assignment 1 document and Guides from Dr.Brian 
//Purpose: To run an LED and button game where a users reaction time is measured and displayed when LED3 is lit up.
//Initially Turns on LED0 (only if the button is already unpressed), when LED3 turn on, the program waits for 
//user to press the button and output measured results. If pressed too early, then the game restarts,
//if pressed too late, then the game exits.

#ifndef HELLO_H
#define HELLO_H

//Gets the current time in milliseconds
long long getTimeInMs(void);

//Waits a number of millseconds
int sleepForMs(long long delayInMs);

//Runs a linux command 
void runCommand(char* command);

//Generates a random time between 0.5s and 3s
float randomTimeGenerator(void);

//Sets the trigger files for an LED to none
void controlDaTrigger(int i);

//Turns a specific LED on or off, depending on parameters
void controlDaBrightness(int LED, char *OnOrOff);

//Reads the contents from a file to the screen
char readFromFileToScreen(char *fileName);

//Runs the intial code that sets up the LED triggers, and the GPIO for the button
void initialConfigurationOfLightsAndButtons(void);

//waits some random time using the random generator function, and check if the user tries to press the button early and cheat
int waitSomeTimeAndCheckForCheating(void);

//turns all LED's either on or off
void turnAllLEDsOnOrOff(char *LEDnumber);

//conducts a search through the array with all the times to find the dastest time
long long searchForQuickestTime(long long timetaken, int counter);

//turns on LED0 only
void turnOnLED0(void);

//Displays a summary of the surrent time taken and the quicket time takes
void summaryOfResponseTime(long long quickesttime, long long timetaken);

//checks a normal round of the game when the user does not try to cheat. It runs and obtains the time
//taken to press the button
long long normalRunOfTheGame(void);

#endif