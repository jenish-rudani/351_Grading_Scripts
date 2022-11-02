#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// buttons
void readButtonValue(char button[], char *output, int size);
// LEDs
void writeLEDSetting(char ledNum[], char ledFile[], char newSetting[]);
// command
void writeFile(char filePath[], char data[]);
void readFile(char filePath[], char *output, int size);
static void runCommand(char* command);
void sleepForMs(long milliseconds);
long long getTime();

// reads the value of a pin, pin must be initialized
// button : string "/gpio72" etc
#define GPIO_PATH "/sys/class/gpio"
void readButtonValue(char button[], char *output, int size){
    char filePath[1024] = GPIO_PATH;
    strcat(filePath, button);
    strcat(filePath, "/value");
    readFile(filePath, output, size);
}

// writes a new setting to a specified LED file, failure 
// to specify a valid LED file will terminate the program
// ledNum[] : string 0-3 specifying LED
// ledFile[] : string "/trigger" "/brightness" etc
// newSetting : string specifying the new setting
#define LED_PATH "/sys/class/leds/beaglebone:green:usr"
void writeLEDSetting(char ledNum[], char ledFile[], char newSetting[]){
    char filePath[1024] = LED_PATH;
    strcat(filePath, ledNum);
    strcat(filePath, ledFile);
    writeFile(filePath, newSetting);
}

// writes data to filePath
// filePath : string, path to file
// data : string data written to file
void writeFile(char filePath[], char data[]){
    FILE *fp;
    //printf("OPENING: %s\n",filePath);
    fp = fopen(filePath, "w+");
    if(fp == NULL) {
        printf("ERROR OPENING FILE");
        exit(1);
    }
    int charWritten = fprintf(fp, data);
    //printf("WRITING NEW DATA: %s\n",data);
    if(charWritten <= 0){
        printf("ERROR WRITING NEW DATA");
        exit(1);
    }
    fclose(fp);
}

// reads data from filePath as a string
// filePath : string, path to file
// output : pointer, output string
// size : integer, number of characters to read
void readFile(char filePath[], char* output, int size){
    FILE *fp;
    //printf("OPENING: %s\n",filePath);
    fp = fopen(filePath, "r");
    if(fp == NULL) {
        printf("ERROR OPENING FILE");
        exit(1);
    }
    fgets(output, size, fp);
    fclose(fp);
}

// run a linux command
static void runCommand(char command[]){
    FILE *pipe = popen(command, "r");
    char buffer[1024];
    while(!feof(pipe) && !ferror(pipe)){
        if(fgets(buffer, sizeof(buffer), pipe) == NULL){
            break;
        }
    }
    int exitCode = WEXITSTATUS(pclose(pipe));
    if(exitCode !=0){
        perror("Unable to execute command:");
        printf(" command: %s\n", command);
        printf(" exit code: %d\n", exitCode);
    }
}

// sleep program
void sleepForMs(long milliseconds){
    int seconds = milliseconds/1000;
    int nanoseconds = (milliseconds - seconds*1000)*1000000;
    struct timespec remaining, request = {seconds, nanoseconds};
    nanosleep(&request, &remaining);
}

// get current time in ms
long long getTime(){
    struct timespec spec;
    clock_gettime(CLOCK_REALTIME, &spec);
    long long s = spec.tv_sec;
    long long ms = s*1000 + spec.tv_nsec / 1000000;
    return ms;
}

// driver
long long bestReactionTime = 9999;
int main(){
    // init USER button
    writeFile("/sys/class/gpio/export", "72");
    runCommand("config-pin p8.43 gpio");
    runCommand("config-pin p8.43 in");
    const int BtnValSize = 16;
    char USERBtnVal[BtnValSize]; // define string for reading button value
    // init LEDs
    writeLEDSetting("0", "/trigger", "none");
    writeLEDSetting("1", "/trigger", "none");
    writeLEDSetting("2", "/trigger", "none");
    writeLEDSetting("3", "/trigger", "none");
    writeLEDSetting("0", "/brightness", "0");
    writeLEDSetting("1", "/brightness", "0");
    writeLEDSetting("2", "/brightness", "0");
    writeLEDSetting("3", "/brightness", "0");
    // technically you can just use writeFile:
    // writeFile(LED_PATH "0/trigger", "none");
    // but it makes less sense than writeLEDSetting
    printf("Hello embedded world, from Eric!\n"); // initialized

    // initialize game
    while(1){
        // wait while user holds down USER button
        while(1){
            readButtonValue("/gpio72", USERBtnVal, BtnValSize);
            if(atoi(USERBtnVal) == 1) break;
        }
        // light up only LED 0
        writeLEDSetting("0", "/brightness", "1");
        writeLEDSetting("1", "/brightness", "0");
        writeLEDSetting("2", "/brightness", "0");
        writeLEDSetting("3", "/brightness", "0");
        // wait a random time between 0.5s and 0.3s
        srand(time(NULL)); // randomize seed
        int waitTime = rand()%201 + 300;
        printf("When LED3 lights up, press the USER button!\n");
        sleepForMs(waitTime);
        // if user is pressing USER button already
        // - record response time as 5.0s
        // - Skip to "Light up all LEDs"
        // Light up LED 3 and start timer
        long long currTime = getTime();
        long long reactionTime = 0;
        writeLEDSetting("3", "/brightness", "1");
        // When user presses USER button, stop timer
        // - if timer >5s, exit with message
        int stopGame = 0;
        do{
            readButtonValue("/gpio72", USERBtnVal, BtnValSize);
            reactionTime = getTime() - currTime;
            if(reactionTime > 5000){
                printf("No input within 5000ms; quitting!\n");
                stopGame = 1;
                break;
            }
        }while(atoi(USERBtnVal) == 1);
        if(stopGame) break;
        // Light up all LEDs
        writeLEDSetting("0", "/brightness", "1");
        writeLEDSetting("1", "/brightness", "1");
        writeLEDSetting("2", "/brightness", "1");
        writeLEDSetting("3", "/brightness", "1");
        // Display summary:
        if(reactionTime < bestReactionTime) {
            printf("New best time!\n");
            bestReactionTime = reactionTime;
        }
        printf("Your reaction time was %4lldms; best so far in game is %4lldms.\n", reactionTime, bestReactionTime);
        // -How many ms was the current response time?
        // -How many ms is the best response time so far this game?
    }
    // turn off LEDs
    writeLEDSetting("0", "/trigger", "none");
    writeLEDSetting("1", "/trigger", "none");
    writeLEDSetting("2", "/trigger", "none");
    writeLEDSetting("3", "/trigger", "none");
    writeLEDSetting("0", "/brightness", "0");
    writeLEDSetting("1", "/brightness", "0");
    writeLEDSetting("2", "/brightness", "0");
    writeLEDSetting("3", "/brightness", "0");
}