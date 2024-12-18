#include <stdio.h>

int main() {
    FILE *file;
    char *filename = "logfile.txt";
    char line[256]; 

    file = fopen(filename, "r"); 

    if (file == NULL) {
        perror("Unable to open the file");
        return 1;
    }

    while (fgets(line, sizeof(line), file)) {
        printf("%s", line);
    }

    fclose(file);
    return 0;
}
