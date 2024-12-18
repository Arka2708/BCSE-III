#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>

int main() {
    char folderPath[1000];
    printf("Enter the path: ");
    scanf("%s", folderPath);
    
    long long maxSize;
    printf("Enter the size: ");
    scanf("%lld", &maxSize);
    struct dirent *entry;
    struct stat fileStat;
    DIR *dir;

    dir = opendir(folderPath);
    if (dir == NULL) {
        perror("Unable to open the directory");
        return 1;
    }
    
    printf("FileName\t\tFileSize\t\t\t\n");
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) { 
            char filePath[256];
            snprintf(filePath, sizeof(filePath), "%s/%s", folderPath, entry->d_name);
            
            if (stat(filePath, &fileStat) == 0) {
                //totalSize += fileStat.st_size;
                if (maxSize <= (long long)fileStat.st_size) {
                    printf("%s\t\t%lld bytes\n", entry->d_name, (long long)fileStat.st_size);
                }
            }
        }
    }
    closedir(dir);
    return 0;
}
