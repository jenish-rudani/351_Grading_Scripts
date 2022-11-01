#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define LED0 "/sys/class/leds/beaglebone:green:usr0/brightness"
#define LED1 "/sys/class/leds/beaglebone:green:usr1/brightness"
#define LED2 "/sys/class/leds/beaglebone:green:usr2/brightness"
#define LED3 "/sys/class/leds/beaglebone:green:usr3/brightness"
#define USERBUTTON "/sys/class/gpio/gpio72/value"

static void sleepForMs(long long delayInMs);
static long long getTimeInMs(void);
static void lightLED(int index);
static void shutoffLED(int index);
static long long getReactionTime(long long timeStart);
static void runCommand(char* command);
static char getButtonStatus(void);

int main(){
    srand(time(0));

    //initialize the LEDs and GPIO
    shutoffLED(4);
    //runCommand("cd /sys/class/gpio/gpio72");
    runCommand("config-pin p8.43 gpio");

    printf("Hello embedded world, from Alon!\n\n");

    //wait while user holds done USER button
    printf("When LED3 lights up, press the USER button as fast as you can!\n");
    long bestTime = 5000;

    for(;;){
        //lights up LED0
        lightLED(0);

        sleepForMs(500 + rand()%2500);

        //light up LED3
        lightLED(3);

        long long timeStart = getTimeInMs();
        long long timeFinish;

        //check if the user is already pressing down the button
        if(getButtonStatus() == '0'){
            timeFinish = timeStart + 5000;
        }
        else{

            //waits for the USER button to be pressed 
            //and exits the program if user takes longer than 5000
            timeFinish = getReactionTime(timeStart);
        }

        //lights up all LEDs
        lightLED(4);

        //checks results against the record, and prints the summary
        long reactionTime = timeFinish - timeStart;
        if(reactionTime < bestTime){
            bestTime = reactionTime;
            printf("New best time!\n");
        }
        printf("Your reaction time is %ldms; best so far in game is %ldms\n", reactionTime, bestTime);
        
        //shuts off all LEDs
        sleepForMs(3000);
        shutoffLED(4);
    }
}

//Template is from the assignment document
static void runCommand(char* command)
{
    // Execute the shell command (output into pipe)
    FILE *pipe = popen(command, "r");
    // Ignore output of the command; but consume it 
    // so we don't get an error when closing the pipe.
    char buffer[1024];
    while (!feof(pipe) && !ferror(pipe)) {
        if (fgets(buffer, sizeof(buffer), pipe) == NULL){
        break;
        }
        // printf("--> %s", buffer); // Uncomment for debugging
    }
    // Get the exit code from the pipe; non-zero is an error:
    int exitCode = WEXITSTATUS(pclose(pipe));
    if (exitCode != 0) {
        perror("Unable to execute command:");
        printf(" command: %s\n", command);
        printf(" exit code: %d\n", exitCode);
    }
}

static char getButtonStatus(void)
{
    FILE *buttonValue = fopen(USERBUTTON, "r");
    if(buttonValue == NULL){
        printf("Error reading %s.\n", USERBUTTON);
        exit(-1);
    }

    int buttonState = fgetc(buttonValue);
    fclose(buttonValue);
    return buttonState;
}

static long long getReactionTime(long long timeStart)
{
    while((getTimeInMs() - timeStart) < 5000){
        int buttonState = getButtonStatus();
        if(buttonState == '0'){
            int result = getTimeInMs();
            return result;
        }
    }

    printf("Taking a nap? Try again.\n");
    shutoffLED(4);
    exit(1);
}

//Taken from the assignment document
static void sleepForMs(long long delayInMs)
{
    const long long NS_PER_MS = 1000 * 1000;
    const long long NS_PER_SECOND = 1000000000;

    long long delayNs = delayInMs * NS_PER_MS;
    int seconds = delayNs / NS_PER_SECOND;
    int nanoseconds = delayNs % NS_PER_SECOND;

    struct timespec reqDelay = {seconds, nanoseconds};
    nanosleep(&reqDelay, (struct timespec *) NULL);
}

//Taken from the assignment document
static long long getTimeInMs(void) 
{
    struct timespec spec;
    clock_gettime(CLOCK_REALTIME, &spec);
    long long seconds = spec.tv_sec;
    long long nanoSeconds = spec.tv_nsec;
    long long milliSeconds = seconds * 1000 + nanoSeconds / 1000000;

    return milliSeconds;
}

static void lightLED(int index)
{
    FILE *brightnessLED;
    switch (index){
    case 0:
        brightnessLED = fopen(LED0, "w");
        if(brightnessLED == NULL){
            printf("Error opening %s.\n", LED0);
            exit(1);
        }

        int writeChar = fprintf(brightnessLED, "1");
        if(writeChar <= 0){
            printf("Error writing data.\n");
            exit(1);
        }

        fclose(brightnessLED);
        break;
    case 1:
        brightnessLED = fopen(LED1, "w");
        if(brightnessLED == NULL){
            printf("Error opening %s.\n", LED1);
            exit(1);
        }

        writeChar = fprintf(brightnessLED, "1");
        if(writeChar <= 0){
            printf("Error writing data.\n");
            exit(1);
        }
        fclose(brightnessLED);
        break;
    case 2:
        brightnessLED = fopen(LED2, "w");
        if(brightnessLED == NULL){
            printf("Error opening %s.\n", LED2);
            exit(1);
        }

        writeChar = fprintf(brightnessLED, "1");
        if(writeChar <= 0){
            printf("Error writing data.\n");
            exit(1);
        }
        fclose(brightnessLED);
        break;
    case 3:
        brightnessLED = fopen(LED3, "w");
        if(brightnessLED == NULL){
            printf("Error opening %s.\n", LED3);
            exit(1);
        }

        writeChar = fprintf(brightnessLED, "1");
        if(writeChar <= 0){
            printf("Error writing data.\n");
            exit(1);
        }
        fclose(brightnessLED);
        break;
    case 4:
        lightLED(0);
        lightLED(1);
        lightLED(2);
        lightLED(3);
        break;
    default:
        break;
    }
}

static void shutoffLED(int index)
{
    FILE *brightnessLED;
    switch (index){
    case 0:
        brightnessLED = fopen(LED0, "w");
        if(brightnessLED == NULL){
            printf("Error opening %s.\n", LED0);
            exit(1);
        }

        int writeChar = fprintf(brightnessLED, "0");
        if(writeChar <= 0){
            printf("Error writing data.\n");
            exit(1);
        }
        fclose(brightnessLED);
        break;
    case 1:
        brightnessLED = fopen(LED1, "w");
        if(brightnessLED == NULL){
            printf("Error opening %s.\n", LED1);
            exit(1);
        }

        writeChar = fprintf(brightnessLED, "0");
        if(writeChar <= 0){
            printf("Error writing data.\n");
            exit(1);
        }
        fclose(brightnessLED);
        break;
    case 2:
        brightnessLED = fopen(LED2, "w");
        if(brightnessLED == NULL){
            printf("Error opening %s.\n", LED2);
            exit(1);
        }

        writeChar = fprintf(brightnessLED, "0");
        if(writeChar <= 0){
            printf("Error writing data.\n");
            exit(1);
        }
        fclose(brightnessLED);
        break;
    case 3:
        brightnessLED = fopen(LED3, "w");
        if(brightnessLED == NULL){
            printf("Error opening %s.\n", LED3);
            exit(1);
        }

        writeChar = fprintf(brightnessLED, "0");
        if(writeChar <= 0){
            printf("Error writing data.\n");
            exit(1);
        }
        fclose(brightnessLED); 
        break;
    case 4:
        shutoffLED(0);
        shutoffLED(1);
        shutoffLED(2);
        shutoffLED(3);
        break;
    default:
        break;
    }
}
