#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    int input, output;

    if (argc != 2) {
        printf("USAGE: %s <number>\n", argv[0]);
        return -1;
    }

    input = atoi(argv[1]);

    asm ("MOV EBX, %0"
        :
        : "r"(input));

    asm (
        "_FIB:"
        	"CMP EBX,1;"
        	"JL _ZERO_OR_LESS;"
        	"MOV EAX,0;"//set EAX to FIB(0)
        	"MOV ECX,1;"//set ECX to FIB(1)
        	//finished to init registers
        	"_LOOP:"
        		"MOV EDX,EAX;"
        		"ADD EAX,ECX;"//calculate next value
        		"SUB EBX,1;"//decrease the value of input
        		"MOV ECX,EDX;"//set ECX to the previous value
        		//now ready for checking conditions
        		"CMP EBX,0;"//check if need to continue to next iteration
        		"JZ _END;"//finshed - go to end of program
        		"JMP _LOOP;"//next iteration - go back to the loop

        	"_ZERO_OR_LESS:"//if the input is zero or less
        		"MOV EAX,0;"//need to return zero at this case
        		"JMP _END;"//finish and return 0

        "_END:"//end of program
    );

    asm ("MOV %0, EAX"
        : "=r"(output));

    printf("%d\n", output);
    
    return 0;
}
