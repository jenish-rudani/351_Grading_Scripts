#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pthread.h>
#include <stdbool.h>

#define USER "/sys/class/gpio/gpio72/value"

//define trigger access files for all leds
#define TRIGGER_0 "/sys/class/leds/beaglebone:green:usr0/trigger"
#define TRIGGER_1 "/sys/class/leds/beaglebone:green:usr1/trigger"
#define TRIGGER_2 "/sys/class/leds/beaglebone:green:usr2/trigger"
#define TRIGGER_3 "/sys/class/leds/beaglebone:green:usr3/trigger"

//define brightness access files for all leds
#define BRIGTH_0 "/sys/class/leds/beaglebone:green:usr0/brightness"
#define BRIGTH_1 "/sys/class/leds/beaglebone:green:usr1/brightness"
#define BRIGTH_2 "/sys/class/leds/beaglebone:green:usr2/brightness"
#define BRIGTH_3 "/sys/class/leds/beaglebone:green:usr3/brightness"

// change trigger of brigthness with a value given
void writeToLED(char file[], char value[])
{
   FILE *pLedTriggerFile = fopen(file, "w");
   if (pLedTriggerFile == NULL)
   {
      printf("ERROR OPENING %s.", file);
      exit(1);
   }
   int charWritten = fprintf(pLedTriggerFile, value);
   if (charWritten <= 0)
   {
      printf("ERROR WRITING DATA");
      exit(1);
   }
   else
   {
      fclose(pLedTriggerFile);
   }
}

// control LEDs 1,2,3 (not 0)
void turnAll(char value[])
{
   writeToLED(BRIGTH_1, value);
   writeToLED(BRIGTH_2, value);
   writeToLED(BRIGTH_3, value);
}

static void runCommand(char *command)
{
   // Execute the shell command (output into pipe)
   FILE *pipe = popen(command, "r");
   // Ignore output of the command; but consume it
   // so we don't get an error when closing the pipe.
   char buffer[1024];
   while (!feof(pipe) && !ferror(pipe))
   {
      if (fgets(buffer, sizeof(buffer), pipe) == NULL)
         break;
   }
   // Get the exit code from the pipe; non-zero is an error:
   int exitCode = WEXITSTATUS(pclose(pipe));
   if (exitCode != 0)
   {
      perror("Unable to execute command:");
      printf(" command: %s\n", command);
      printf(" exit code: %d\n", exitCode);
   }
}

//initialize leds before game starts
void setLEDs()
{
   writeToLED(TRIGGER_0, "none");
   writeToLED(TRIGGER_1, "none");
   writeToLED(TRIGGER_2, "none");
   writeToLED(TRIGGER_3, "none");
   turnAll("0");
}

//generates a random number between 0.5 and a
float generateRandom(float a)
{
   float x = (float)rand() / (float)(RAND_MAX / a) + 0.5;
   return x;
}

//read a value of USER button (return 1 when pressed)
int readUser()
{
   int button = 0;
   FILE *pFile = fopen(USER, "r");
   if (pFile == NULL)
   {
      printf("ERROR: Unable to open file (%s) for read\n", USER);
      exit(-1);
   }
   else
   {
      char buff[2];
      fgets(buff, 2, pFile);
      if (buff[0] == '0') // inverse the bits (by default 0 means pressed)
      {
         button = 1;
      }
      fclose(pFile);
   }
   return button;
}

// static void sleepForMs(long long delayInMs)
// {
//    const long long NS_PER_MS = 1000 * 1000;
//    const long long NS_PER_SECOND = 1000000000;
//    long long delayNs = delayInMs * NS_PER_MS;
//    int seconds = delayNs / NS_PER_SECOND;
//    int nanoseconds = delayNs % NS_PER_SECOND;
//    struct timespec reqDelay = {seconds, nanoseconds};
//    nanosleep(&reqDelay, (struct timespec *)NULL);
// }

static long long getTimeInMs(void)
{
   struct timespec spec;
   clock_gettime(CLOCK_REALTIME, &spec);
   long long seconds = spec.tv_sec;
   long long nanoSeconds = spec.tv_nsec;
   long long milliSeconds = seconds * 1000 + nanoSeconds / 1000000;
   return milliSeconds;
}

//times the user reaction after LED3 lights up
int waitForResponse()
{
   long long start_time = getTimeInMs();
   while (1)
   {
      int pressed = readUser();
      if (pressed == 1)
      {
         break;
      }
     
      if(getTimeInMs() - start_time > 5000){
         break;
      }
   }
   long long total_time = getTimeInMs() - start_time;
   return (int)total_time;
}

//checks for early user reaction (before LED 3 lights up)
bool checkEarly()
{

   int time = 1000 * generateRandom(3.0);
   bool flag = 0;
   long long start_time = getTimeInMs();
   while (1)
   {
      int pressed = readUser();
      if (pressed == 1)
      {
         flag = 1;
         break;
      }
      if(getTimeInMs() - start_time >= time){
         break;
      }
   }
   //printf("Out of loop\n");
   return flag;
}


void startGame()
{
   printf("When LED3 lights up, press the USER button!\n");
   int best = 5000;
   writeToLED(BRIGTH_0, "1");

   while (1)
   {
      while (1)
      {
         int pressed = readUser();
         if (pressed == 0){
            break;}
      }

      turnAll("0");
      
      bool flag = checkEarly();

      if(flag==1){
         printf("Too soon. Be careful!\n");
         turnAll("1");
         continue;
      }

      writeToLED(BRIGTH_3, "1");
      int time = waitForResponse();
      if(time>5000){
         printf("No input within 5000ms; quitting!\n");
         break;}
      if (time < best)
      {
         best = time;
         printf("New best time!\n");
      }
      printf("Your reaction time was %d ms; best so far in game is %d ms.\n", time, best);
      turnAll("1");
   }
   turnAll("0");
   writeToLED(BRIGTH_0, "0");
   return;
}

int main()
{
   printf("Hello embedded world, from Alex!\n");

   runCommand("config-pin p8.43 gpio");

   setLEDs();
   startGame();

   return 0;
}