#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    char ch;
    int counter = 0;
    char charset[] = "abcdefghijklmnopqrstuvwxyz";
    int charset_size = 26;
    char* filepath = "haystack/%c/%c/%c/%i";
    char output_file[18] = {0};

    FILE *fp = fopen("./needle", "r");

    if (fp == NULL) {
        exit(EXIT_FAILURE);
    }

    printf("The contents of needle file are:\n");

    while((ch = fgetc(fp)) != EOF) {
        printf("Writing character %i into haystack\n", counter);
        sprintf(output_file, filepath, charset[random() % 26], charset[random() % 26], charset[random() % 26], counter);

        FILE *outfile = fopen(output_file, "w");
        if (outfile == NULL) {
            exit(EXIT_FAILURE);
        }
        fputc(ch, outfile);
        fclose(outfile);

        counter++;
    }

    fclose(fp);
    return 0;
}
