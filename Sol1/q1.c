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
          "MOV EAX,0;"//set return value to 0
          "PUSH EBX;"
          "CMP EBX,2;"//if(i<2)return 0
          "JL _END;"//end program

          "MOV ECX,EBX;"//ECX=n
          "JMP _LOOP;"

          "_LOOP:"
            "POP EBX;"
            "PUSH EBX;"
            "MOV EAX,EBX;"//return value starts at n
            "MOV EDX,0;"//clear EDX=0
            "DIV ECX;"//EAX/ECX
            "CMP EDX,0;"//check if EAX%ECX=0
            "JNE _ENDLOOP;"//if(EAX$ECX=0) finish loop

            "MOV EDX,2;"//EDX=2
            "CMP ECX,EDX;"
            "JE _END;"

            "MOV EBX,2;"
            "_DIV:"
              "MOV EDX,0;"//clear EDX for DIV
              "MOV EAX,ECX;"//EAX=i (i is a var for loop)
              "DIV EBX;"//EAX/EBX
              "CMP EDX,0;"//EDX=EAX%EBX - check if MOD is 0
              "JE _ENDLOOP;"
              "INC EBX;"//i++
              "CMP EBX,ECX;"
              "JE _END;"//check if we checked all options for prime factor
              "JMP _DIV;"
            
            "_ENDLOOP:"
              "SUB ECX,1;"//i--
              "CMP ECX,1;"
              "JE _END;"//loop is done when i=1
              "JMP _LOOP;"

          "_END:"
            "POP EBX;"
            "MOV EAX,ECX;"//return value

    );

    asm ("MOV %0, EAX"
        : "=r"(output));

    printf("%d\n", output);
    
    return 0;
}
