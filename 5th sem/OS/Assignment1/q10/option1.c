#include <stdio.h>
#include <time.h>

int main(int argc, char **argv) {
    time_t currentTime;
    struct tm *timeInfo;
    int hour;

    time(&currentTime); 
    timeInfo = localtime(&currentTime);
    hour = timeInfo->tm_hour;

    if (hour >= 6 && hour < 12)
    {
        printf("Good Morning.\n");
    }
    else if (hour >= 12 && hour < 16)
    {
        printf("Good afternoon.\n");
    }
    else if (hour >= 16 && hour < 20)
    {
        printf("Good evening.\n");
    }
    else
    {
        printf("Good night.\n");
    }
    
}