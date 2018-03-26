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
        "CMP EBX,1;"
        "JL _ZERO_OR_LESS;"
        "CALL _FIB;"
        "JMP _END;"

        "_FIB:"
        	"CMP EBX,0;"//fib(0)=0
        	"JNZ _CONDTOSTOP;"//check if need to continue or not
        	"MOV EAX,0;"
        	"RET;"

        "_CONDTOSTOP:"//end of recursion call for current call
        	"CMP EBX,1;"
        	"JNZ _REC;"
        	"MOV EAX,1;"//set return value of the current call to 1
        	"RET;"//return value and continue to next instruction

        "_REC:"
        	"SUB EBX,1;"//get ready to calculate fib(n-1)
        	"PUSH EBX;"//store n-1 in stack
        	"CALL _FIB;"//calculate fib(n-1)
        	"POP EBX;"//restore n-1 to find out value of n-2
        	"SUB EBX,1;"//get ready to calculate fib(n-2)
        	"MOV ECX,EAX;"//ECX=fib(n-1)
        	"PUSH ECX;"//store in stack the value of fib(n-1)
        	"CALL _FIB;"//call to calculate fib(n-2)
        	"POP ECX;"//ECX=fib(n-2)
        	"ADD EAX,ECX;"//EAX=fib(n-1)+fib(n-2) - ready to return
        	"RET;"

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
