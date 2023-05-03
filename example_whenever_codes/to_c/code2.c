#include <stdio.h>
#include <malloc.h>

#ifndef True
typedef int bool ;
#define True 1
#define False 0
#endif

#define USING_WEIGHTED_RANDOM False

#ifndef TOTAL_LINES
#define TOTAL_LINES 9
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
    bool defer = False  || ( (((executionStack[2].count) > (0)) || ((executionStack[0].count) <= (executionStack[1].count))) || ((executionStack[6].count) > (99)));
    if(!defer){
        bool again = False || ( (executionStack[0].count) > (0));
        // Starting statements 
        change_pos_quantity(1,executionStack[0].count);
        change_pos_quantity(2,1);
        change_pos_quantity(6,1);
        // Statements done
        if(!again) change_pos_quantity(0, -1);
    }
}
void F1_for_line2(void) { 
    bool defer = False  || ( (((executionStack[2].count) > (0)) || ((executionStack[1].count) <= (executionStack[0].count))) || ((executionStack[6].count) > (99)));
    if(!defer){
        bool again = False || ( (executionStack[1].count) > (0));
        // Starting statements 
        change_pos_quantity(0,executionStack[1].count);
        change_pos_quantity(2,1);
        change_pos_quantity(6,1);
        // Statements done
        if(!again) change_pos_quantity(1, -1);
    }
}
void F2_for_line3(void) { 
    bool defer = False  || ( (executionStack[4].count) > (0));
    if(!defer){
        bool again = False;
        // Starting statements 
        printf("%llu", (executionStack[0].count) + (executionStack[1].count));
        printf("\n");
        // Statements done
        if(!again) change_pos_quantity(2, -1);
    }
}
void F3_for_line4(void) { 
    bool defer = False  || ( (executionStack[4].count) > (0));
    if(!defer){
        bool again = False;
        // Starting statements 
        printf("%s", "1");
        printf("\n");
        // Statements done
        if(!again) change_pos_quantity(3, -1);
    }
}
void F4_for_line5(void) { 
    bool defer = False ;
    if(!defer){
        bool again = False;
        // Starting statements 
        change_pos_quantity(3,1);
        change_lines_quantity((-1) * (3),1);
        change_pos_quantity(6,1);
        // Statements done
        if(!again) change_pos_quantity(4, -1);
    }
}
void F5_for_line6(void) { 
    bool defer = False  || ( (executionStack[3].count) > (0));
    if(!defer){
        bool again = False;
        // Starting statements 
        change_pos_quantity(2,1);
        // Statements done
        if(!again) change_pos_quantity(5, -1);
    }
}
void F6_for_line7(void) { 
    bool defer = False ;
    if(!defer){
        bool again = False;
        // Starting statements 
        change_pos_quantity(6,1);
        // Statements done
        if(!again) change_pos_quantity(6, -1);
    }
}
void F7_for_line8(void) { 
    bool defer = False  || ( (executionStack[6].count) < (100));
    if(!defer){
        bool again = False;
        // Starting statements 
        change_lines_quantity((-1) * (1),executionStack[0].count);
        change_lines_quantity((-1) * (2),executionStack[1].count);
        change_lines_quantity((-1) * (7),100);
        change_lines_quantity((-1) * (3),1);
        // Statements done
        if(!again) change_pos_quantity(7, -1);
    }
}
void F8_for_line9(void) { 
    bool defer = False  || ( ((executionStack[2].count) > (0)) || ((executionStack[5].count) > (0)));
    if(!defer){
        bool again = False;
        // Starting statements 
        change_pos_quantity(0,1);
        change_pos_quantity(2,1);
        // Statements done
        if(!again) change_pos_quantity(8, -1);
    }
}

// MAIN
//
int main() {
    // Starting Lines definition
    lines[0]= (Line) {1, &F0_for_line1};
    executionStack[0] = (StackCount) {1,1};
    lines[1]= (Line) {2, &F1_for_line2};
    executionStack[1] = (StackCount) {2,1};
    lines[2]= (Line) {3, &F2_for_line3};
    executionStack[2] = (StackCount) {3,1};
    lines[3]= (Line) {4, &F3_for_line4};
    executionStack[3] = (StackCount) {4,1};
    lines[4]= (Line) {5, &F4_for_line5};
    executionStack[4] = (StackCount) {5,1};
    lines[5]= (Line) {6, &F5_for_line6};
    executionStack[5] = (StackCount) {6,1};
    lines[6]= (Line) {7, &F6_for_line7};
    executionStack[6] = (StackCount) {7,1};
    lines[7]= (Line) {8, &F7_for_line8};
    executionStack[7] = (StackCount) {8,1};
    lines[8]= (Line) {9, &F8_for_line9};
    executionStack[8] = (StackCount) {9,1};
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