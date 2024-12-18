#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>

int main() {
    char folderPath[1000];
    printf("Enter the path: ");
    scanf("%s", folderPath);
    
    struct dirent *entry;
    struct stat fileStat;
    DIR *dir;

    dir = opendir(folderPath);
    if (dir == NULL) {
        perror("Unable to open the directory");
        return 1;
    }

    long long totalSize = 0;

    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) {
            char filePath[256];
            snprintf(filePath, sizeof(filePath), "%s/%s", folderPath, entry->d_name);
            
            if (stat(filePath, &fileStat) == 0) {
                totalSize += fileStat.st_size;
            }
        }
    }

    printf("Total size of all files: %lld bytes\n", totalSize);

    closedir(dir);
    return 0;
}
