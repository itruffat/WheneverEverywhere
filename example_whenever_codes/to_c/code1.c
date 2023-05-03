#include <stdio.h>
#include <malloc.h>

#ifndef True
typedef int bool ;
#define True 1
#define False 0
#endif

#define USING_WEIGHTED_RANDOM False

#ifndef TOTAL_LINES
#define TOTAL_LINES 1
#endif

#if USING_WEIGHTED_RANDOM
// This could really improve, code from here
// https://stackoverflow.com/questions/33010010/how-to-generate-random-64-bit-unsigned-integer-in-c
#ifndef RAND_MAX_WIDTH
#define IMAX_BITS(m) ((m)/((m)%255+1) / 255%255*8 + 7-86/((m)%255+12))
#define RAND_MAX_WIDTH IMAX_BITS(RAND_MAX)
_Static_assert((RAND_MAX & (RAND_MAX + 1u)) == 0, "RAND_MAX not a Mersenne number");

unsigned long long rand64() {
    unsigned long long r = 0;
    for (int i = 0; i < 64; i += RAND_MAX_WIDTH) {
        r <<= RAND_MAX_WIDTH;
        r ^= (unsigned) rand();
    }
    return r;
}
#endif
#endif

// GENERIC DEFINITIONS
//
typedef struct Line Line;
typedef struct StackCount StackCount;

struct Line {
    int line_number;
    void (*func) (void);
};

struct StackCount {
    int line_number;
    unsigned long long count;
};

Line lines [TOTAL_LINES];
StackCount executionStack [TOTAL_LINES];


#if USING_WEIGHTED_RANDOM
unsigned long long get_active_lines(){
    unsigned long long long_count = 0;
    for (unsigned int i = 0; i < TOTAL_LINES; i++) {
        long_count += executionStack[i].count;
    }
    return long_count;
}
#else
int get_active_lines(){
    int count = 0;
    for (unsigned int i = 0; i < TOTAL_LINES; i++) {
        if(executionStack[i].count > 0) count += 1;
    }
    return count;
}
#endif


#if USING_WEIGHTED_RANDOM
int get_position_of_active_line(unsigned long long active_line){
    int i = 0;
    while( (active_line > 0) && (i < TOTAL_LINES) ){
        active_line -= executionStack[i].count;
        if(active_line > 0) i += 1;
    };
    if(i == TOTAL_LINES) i = -1;
    return i;
}
#else
int get_position_of_active_line(int active_line){
    int i = 0;
    while( (active_line > 0) && (i < TOTAL_LINES) ){
        if(executionStack[i].count > 0) active_line -= 1;
        if(active_line > 0) i += 1;
    };
    if(i == TOTAL_LINES) i = -1;
    return i;
}
#endif

void change_pos_quantity(int position, long long quantity) {
    if (executionStack[position].count + quantity < 0) {
        executionStack[position].count = 0;
    } else {
        executionStack[position].count += quantity;
    }
}

int get_line_pos(int line_number){
    int i = 0;
    while( (lines[i].line_number != line_number) && i < TOTAL_LINES ) i += 1;
    if(i == TOTAL_LINES) i = -1;
    return i;
}

unsigned long long get_line_quantity(int line_number){
    return executionStack[get_line_pos(line_number)].count;
}

void change_lines_quantity(int line_number, long long quantity) {
    int position = get_line_pos(line_number);
    change_pos_quantity(position, quantity);
}


// LINES
//
void F0_for_line1(void) { 
    bool defer = False ;
    if(!defer){
        bool again = False || ( (executionStack[0].count) > (0));
        // Starting statements 
        printf("%c", READ);
        printf("\n");
        // Statements done
        if(!again) change_pos_quantity(0, -1);
    }
}

// MAIN
//
int main() {
    // Starting Lines definition
    lines[0]= (Line) {1, &F0_for_line1};
    executionStack[0] = (StackCount) {1,1};
    // Ending Lines definition

    #if USING_WEIGHTED_RANDOM
    printf("%llu", rand64());
    unsigned long long active_lines = TOTAL_LINES;
    #else
    int active_lines = TOTAL_LINES;
    #endif
    do{
        #if USING_WEIGHTED_RANDOM
        unsigned long long next_active_line = rand64()%(active_lines+1) ; // Not perfect but as good as it gets
        #else
        int next_active_line = rand()%(active_lines+1);
        #endif
        int position = get_position_of_active_line(next_active_line);
        lines[position].func();
        active_lines = get_active_lines();
    }while(active_lines > 0);

    return 0;
}
