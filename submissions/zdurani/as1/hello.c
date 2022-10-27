//ENSC 351 Assignent 1 - hello.c file
//Student Name: Zohra Khan Durani, Student Number: 301396012
//References: Utilized the code that was provided to us in the Assignment 1 document and Guides from Dr.Brian 
//Purpose: To run an LED and button game where a users reaction time is measured and displayed when LED3 is lit up.
//Initially Turns on LED0 (only if the button is already unpressed), when LED3 turn on, the program waits for 
//user to press the button and output measured results. If pressed too early, then the game restarts,
//if pressed too late, then the game exits.
//Note: 0 corresponds to button being pressed, 1 corresponds to being un-pressed

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include "hello.h"

#define BUTTON_GPIO_CONFIGURATION_COMMAND "config-pin p8.43 gpio"
#define USER_BUTTON_VALUE_PATH "/sys/class/gpio/gpio72/value"
#define BUTTON_GPIO_DIRECTION_PATH "/sys/class/gpio/gpio72/direction"
#define LED_PATH "/sys/class/leds/beaglebone:green:usr%d/trigger"
#define LED_PATH_BRIGHTNESS "/sys/class/leds/beaglebone:green:usr%d/brightness"
#define SIZE 100 

int main(int argc, char* args[])
{
    //some variables required during the main function execution
    int IndexForTimeArray = 0;
    long long TimeTakenToPressButton = 0;
    long long QuickestTimeToPressButton = 0;


    //The LEDs and USER button are configured
    initialConfigurationOfLightsAndButtons();


    //Hello World prompt with instructions
    printf("Hello Embedded World, from Zohra!\n\n");
    printf("When LED3 lights up, press the USER button!\n");


    while (1) {
        
        //Waits if the button is being pushed, if not, then this loops is skipped
        while(readFromFileToScreen(USER_BUTTON_VALUE_PATH) == '0') {
            //do nothing, contiuously loops
        }

        //Lights up only LED0
        turnOnLED0();

        //call to function that waits a random time, and returns a value that checks is the user attempts to
        //press the button early and cheat
        int cheating = waitSomeTimeAndCheckForCheating();

        if (cheating == 1) {

            //Default time of 5000ms is set, if cheating, then skips to trun LED on
            const int DEFAULT_TIMING_FOR_EARLY_BUTTON_PRESS = 5000;
            TimeTakenToPressButton = DEFAULT_TIMING_FOR_EARLY_BUTTON_PRESS; 
            cheating = 0;
        }
        else if (cheating == 0) {
            
            //LED3 turns on
            int LED_3 = 3;
            controlDaBrightness(LED_3,"1");

            //regular run of the game that returns the time it takes the user to press the USER button again
            TimeTakenToPressButton = normalRunOfTheGame();
            
            //Obtains the fastest time from among all the runs
            QuickestTimeToPressButton = searchForQuickestTime(TimeTakenToPressButton, IndexForTimeArray);
            IndexForTimeArray++;
        }

        //turns all LED's on, and then a summary is displayed of the results
        turnAllLEDsOnOrOff("1");
        summaryOfResponseTime(QuickestTimeToPressButton, TimeTakenToPressButton);
    }
    return 0;
}

long long normalRunOfTheGame(void)
{
    //obtains the start time for the timer
    long long StartTime = getTimeInMs();

    while (1) {
        //checks if time exceeds 5000ms, if yes all the LED's turn on and the program exits with a statement
        if(( getTimeInMs() - StartTime) > 5000) {
            printf("No input within 5000ms; quitting!\n");
            turnAllLEDsOnOrOff("0");
            exit(0);
        }
                    
        //continuosly checks when the user presses the button, and then breaks from the loop
        if (readFromFileToScreen(USER_BUTTON_VALUE_PATH) == '0')
            break;
    }
    
    //obtains the time when the button was pressed and calculates the difference to get the reaction time
    long long StoppedTime = getTimeInMs();
    long long TimeTakenToPressButton = StoppedTime - StartTime;

    return TimeTakenToPressButton;
}

void summaryOfResponseTime(long long QuickestTime, long long TimeTaken)
{
    //checks if the quickest time found and the current time are the same, if yes that means that theres a new best time
    if (QuickestTime == TimeTaken) 
            printf("New Best Time!\n");

    //prints the results           
    printf("Your reaction time is %lldms;",TimeTaken);
    printf(" best so far in the game is %lldms\n", QuickestTime);
}

void turnOnLED0 (void)
{
    //only turns on LED0
    int LED_0 = 0;
    controlDaBrightness(LED_0,"1");
    
    //loops to turn the rest off
    for (int i = 1; i < 4; i++) 
        controlDaBrightness(i, "0");
    
}

long long searchForQuickestTime(long long TimeTakenToPressButton, int IndexForTimeArray)
{
    //declares the array, then intializes it with the current time taken
    //initializes the array one index at a time
    long long ArrayBuffer[SIZE];
    ArrayBuffer[IndexForTimeArray] = TimeTakenToPressButton;

    //searches for the fastest time in the existing array buffer
    long long QuickestTimeToPressButton=ArrayBuffer[IndexForTimeArray];
    for (int i = 0; i < IndexForTimeArray; i++) {
        if (QuickestTimeToPressButton > ArrayBuffer[i])
                QuickestTimeToPressButton = ArrayBuffer[i];
    }

    return QuickestTimeToPressButton;        
}

void turnAllLEDsOnOrOff(char *OnOrOff)
{
    //loops to turn all LED's off
    for (int i = 0; i < 4; i++) {
        controlDaBrightness(i, OnOrOff);
    }
}

float randomTimeGenerator(void)
{
    int max = 3000;
    int min = 500;

    //uses seed random to generate a random time
    srand(time(0));

    //results in a random time within 0.5s and 3s
    int randomtimeInMS = rand()%(max-min+1) + min;
    
    return randomtimeInMS;
}

int waitSomeTimeAndCheckForCheating(void)
{
    //obtains a random time
    int RandTimeGenerated=randomTimeGenerator();
        
    //obtains start time
    long long BeginTime = getTimeInMs();
    int cheating;
        
    //loops through until the timer is complete, and continuosly checks if the button is pressed,
    //which will indicate if the user pressed the button too early
    while (getTimeInMs() < BeginTime + RandTimeGenerated) {
        if(readFromFileToScreen(USER_BUTTON_VALUE_PATH) == '0') {
            cheating = 1;
            break;
        }

        cheating = 0; 

        //sleeps continuosly for 10 ms in order to allow enough time to detect a change
        sleepForMs(10);  
    }

    return cheating;
}

void initialConfigurationOfLightsAndButtons(void)
{
    //calls controlDaTrigger function to set the triggers to none for each LED
    for (int i = 0; i < 4; i++) {
        controlDaTrigger(i);
    }

    //runs the command to configure the USER button
    runCommand(BUTTON_GPIO_CONFIGURATION_COMMAND);

    //opens and checks if file opens
    FILE *pFile = fopen(BUTTON_GPIO_DIRECTION_PATH, "w");
    if (pFile == NULL) {
        printf("ERROR: Unable to open export file.\n");
        exit(1);
    }
    
    // Write to data to the file using fprintf():
    fprintf(pFile, "in");
    // Close the file using fclose():
    fclose(pFile);
}

long long getTimeInMs(void)
{
    //creates a structure
    struct timespec spec;

    //obtains current time using clock() function
    clock_gettime(CLOCK_REALTIME, &spec);
    long long seconds = spec.tv_sec;
    long long nanoSeconds = spec.tv_nsec;

    //converts the time to milliseconds
    long long milliSeconds = seconds * 1000 + nanoSeconds / 1000000;
    return milliSeconds;
}

int sleepForMs(long long delayInMs)
{
    //takes the time in ms and converts in back to seconds and nanoseconds, and puts it into a struct
    const long long NS_PER_MS = 1000 * 1000;
    const long long NS_PER_SECOND = 1000000000;
    long long delayNs = delayInMs * NS_PER_MS;
    int seconds = delayNs / NS_PER_SECOND;
    int nanoseconds = delayNs % NS_PER_SECOND;
    struct timespec reqDelay = {seconds, nanoseconds};

    //calls nanosleep to pause the program
    int output = nanosleep(&reqDelay, (struct timespec *) NULL);
    return output;
    
}

void runCommand(char* command)
{
    // Execute the shell command (output into pipe)
    FILE *pipe = popen(command, "r");
    // Ignore output of the command; but consume it so we don't get an error when closing the pipe.
    char buffer[1024];
    while (!feof(pipe) && !ferror(pipe)) {
        if (fgets(buffer, sizeof(buffer), pipe) == NULL)
            break;
    }
    // Get the exit code from the pipe; non-zero is an error:
    int exitCode = WEXITSTATUS(pclose(pipe));
    if (exitCode != 0) {
        perror("Unable to execute command:");
        printf(" command: %s\n", command);
        printf(" exit code: %d\n", exitCode);
    }
}

void controlDaTrigger(int i)
{
    //obtains the path according to the specific LED
    char Path_complete[SIZE];
    snprintf(Path_complete, SIZE, LED_PATH,i);
    
    //opens the file for that specific LED
    FILE *pLedTriggerFile = fopen(Path_complete,"w");
    if (pLedTriggerFile == NULL) {
        printf("ERROR OPENING %s.", "/sys/class/leds/beaglebone:green:usr0/trigger");
        exit(1);
    }

    //sets trigger file to none
    int charWritten = fprintf(pLedTriggerFile, "none"); //turns trigger off
    if (charWritten <= 0) {
        printf("ERROR WRITING DATA");
        exit(1);
    }

    //closes the file
    fclose(pLedTriggerFile);
}

void controlDaBrightness(int LED, char *OnOrOff)
{
    //obtains the specific path according to the specified LED
    char Path_complete[SIZE];
    snprintf(Path_complete, SIZE, LED_PATH_BRIGHTNESS,LED);
    
    //opens the file for the specific LED, to do an error check
    FILE *pLedBrightnessFile = fopen(Path_complete,"w");
    if (pLedBrightnessFile == NULL) {
        printf("ERROR OPENING %s.", Path_complete);
        exit(1);
    }

    //turns the LED on or off
    int intWrittenBrightness = fprintf(pLedBrightnessFile, OnOrOff);
    if (intWrittenBrightness != 0 && intWrittenBrightness != 1) {
        printf("ERROR WRITING DATA");
        exit(1);
    }

    //closes the file
    fclose(pLedBrightnessFile);
}

char readFromFileToScreen(char *fileName)
{
    //opens the specific file to read from, and does an error check
    FILE *pFile = fopen(fileName, "r");
    if (pFile == NULL) {
        printf("ERROR: Unable to open file (%s) for read\n", fileName);
        exit(-1);
    }
    
    const int MAX_LENGTH = 1024;
    char buff[MAX_LENGTH];
    
    //reads from the file
    fgets(buff, MAX_LENGTH, pFile);
    
    //closes the file
    fclose(pFile);
    
    //removes the extra null characters and reads a single character of either 1 or 0
    buff[strlen(buff)-1] = '\0';
    buff[strlen(buff)-2] = '\0';
    buff[strlen(buff)-3] = '\0';
    return *buff;
}