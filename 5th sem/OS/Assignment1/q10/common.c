#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char **argv) {
    FILE *file;
    char *filename = "logfile.txt";

    file = fopen(filename, "a"); // Open the file in append mode

    if (file == NULL) {
        perror("Unable to open the file");
        return 1;
    }
    
    time_t currentTime;
    struct tm *localTime;

    time(&currentTime); // Get the current time
    localTime = localtime(&currentTime); // Convert to local time
     
    char* stringList[] = {
        "",
        "Display Greetings",
        "List Large Files",
        "Disk Usage\t\t",
        "View Log File\t"
    };
    // Append content to the file
    fprintf(file, "%s\t%s\t%s", "Arkajyoti", stringList[atoi(argv[1])], asctime(localTime));

    fclose(file); // Close the file
    return 0;
}