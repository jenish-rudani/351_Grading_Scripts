#include <stdio.h>
#include <sys/wait.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>

#define LED0_Path "/sys/class/leds/beaglebone:green:usr0"
#define LED1_Path "/sys/class/leds/beaglebone:green:usr1"
#define LED2_Path "/sys/class/leds/beaglebone:green:usr2"
#define LED3_Path "/sys/class/leds/beaglebone:green:usr3"
#define UserButton_Path "/sys/class/gpio/gpio72"
#define lightOn 1
#define lightOff 0
#define allowInputUserButton "config-pin p8.43 gpio"
//function given by Dr fraser on canvas to run a linux command
static void runCommand(char* command)
{
// Execute the shell command (output into pipe)
FILE *pipe = popen(command, "r");
// Ignore output of the command; but consume it
// so we don't get an error when closing the pipe.
char buffer[1024];
while (!feof(pipe) && !ferror(pipe)) {
if (fgets(buffer, sizeof(buffer), pipe) == NULL)
break;
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


//function given by Dr fraser on canvas to wait a specified number of ms
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


//function given by Dr fraser on canvas to read from file
void readFromFileToScreen(char *fileName)
{
FILE *pFile = fopen(fileName, "r");
if (pFile == NULL) {
printf("ERROR: Unable to open file (%s) for read\n", fileName);
exit(-1);
}
// Read string (line)
const int MAX_LENGTH = 1024;
char buff[MAX_LENGTH];
fgets(buff, MAX_LENGTH, pFile);
// Close
fclose(pFile);
printf("Read: '%s'\n", buff);
}

//function given by Dr fraser on canvas to read from file
char getDataFromFile(char *fileName)
{
FILE *pFile = fopen(fileName, "r");
if (pFile == NULL) {
printf("ERROR: Unable to open file (%s) for read\n", fileName);
exit(-1);
}
// Read string (line)
const int MAX_LENGTH = 1024;
char buff[MAX_LENGTH];
fgets(buff, MAX_LENGTH, pFile);
// Close
fclose(pFile);
return buff[0];
}

//code given by Dr fraser on canvas to read from file adapted to be a function
void writeIntToFile(char *fileName, int input)
{
    sleepForMs(300);
FILE *pFile = fopen(fileName, "w");
if (pFile == NULL) {
printf("ERROR: Unable to open export file.\n");
exit(1);
}
// Write to data to the file using fprintf():
fprintf(pFile, "%d", input);
// Close the file using fclose():
fclose(pFile);
// Call nanosleep() to sleep for ~300ms before use.
}


//code given by Dr fraser on canvas to read from file adapted to be a function
void writeStringToFile(char *fileName, char* input)
{
    sleepForMs(300);
FILE *pFile = fopen(fileName, "w");
if (pFile == NULL) {
printf("ERROR: Unable to open export file.\n");
exit(1);
}
// Write to data to the file using fprintf():
fprintf(pFile, "%s", input);
// Close the file using fclose():
fclose(pFile);
// Call nanosleep() to sleep for ~300ms before use.
}
//function given by Dr fraser on canvas to get current time
static long long getTimeInMs(void)
{
struct timespec spec;
clock_gettime(CLOCK_REALTIME, &spec);
long long seconds = spec.tv_sec;
long long nanoSeconds = spec.tv_nsec;
long long milliSeconds = seconds * 1000
+ nanoSeconds / 1000000;
return milliSeconds;
}


int main()
{
    printf("Hello embedded world, from Andrew Speers \n");
    
    runCommand(allowInputUserButton);
    
    //allow direct control of LED's
    writeStringToFile(LED0_Path "/trigger", "none");
    writeStringToFile(LED1_Path "/trigger", "none");
    writeStringToFile(LED2_Path "/trigger", "none");
    writeStringToFile(LED3_Path "/trigger", "none");
    
    //best time store outside of loop
    long long bestTime = 5000;
    //always loop
    while(true)
    {
    
    //turn all lights off to start
    writeIntToFile(LED0_Path "/brightness",lightOff);
    writeIntToFile(LED1_Path "/brightness",lightOff);
    writeIntToFile(LED2_Path "/brightness",lightOff);
    writeIntToFile(LED3_Path "/brightness",lightOff);

    int Button_Value=getDataFromFile(UserButton_Path "/value");
    //while button is pressed do nothing and wait (zero when pressed) ASCII value of charcter 0 is int 48
    while(Button_Value==48)
    {
        //do nothing but update button
        Button_Value=getDataFromFile(UserButton_Path "/value");
    }
    //light up LED0
    writeIntToFile(LED0_Path "/brightness",lightOn);
    
    //seed random number 
    srand(time(0));
    
    int lowerLimit=1;
    int upperLimit=6;
    //generate random number between 1 and 6
    int randNum = (rand() % (upperLimit-lowerLimit+1))+lowerLimit;
    //create a number between 500 and 3000 to wait 0.5 to 3 seconds
    long long waitTimeInms = randNum*1000;

    printf("\n when light lights up pres USER button \n");
    //wait random ammount of time 
    sleepForMs(waitTimeInms);
    
    Button_Value=getDataFromFile(UserButton_Path "/value");
    long long timeElapsed;
    if (Button_Value != 48){
        //light up light 3 to react to
        writeIntToFile(LED3_Path "/brightness",lightOn);
        long long timeStart;
        long long timeEnd;
        timeStart = getTimeInMs();
        Button_Value=getDataFromFile(UserButton_Path "/value");
        while(Button_Value!=48)
            {
                //do nothing but wait for input
                Button_Value=getDataFromFile(UserButton_Path "/value");
                timeEnd = getTimeInMs();
                timeElapsed = timeEnd-timeStart;
                //if more than 5s then exit program
                if(timeElapsed>5000){
                    printf(" No input with 5 seconds; Terminating program! \n");
                    return 0;
                }
                
            }
        //record how long the reaction took
        
        

    }
    else{
        // press too early set time to max
        printf(" You pressed the button too early! \n");
        timeElapsed = 5000; 
    }
    //set best time to max time of 5s
    

    if(bestTime>timeElapsed){
        bestTime=timeElapsed;
    }

    //light up all LED's
    writeIntToFile(LED0_Path "/brightness",lightOn);
    writeIntToFile(LED1_Path "/brightness",lightOn);
    writeIntToFile(LED2_Path "/brightness",lightOn);
    writeIntToFile(LED3_Path "/brightness",lightOn);

    printf("\n Your reaction time was  ");
    printf("%lld", timeElapsed);
    printf(";  The best time so far is  ");
    printf("%lld", bestTime);
    } 
    
    //should never reach here
    return 1;
    }
    //////////////////////////////////////////////////////////////////
    