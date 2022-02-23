//#include "deadbeef_rand.h"
#include <iostream>
#include <time.h>

using namespace std;

unsigned int deadbeef_seed = time(NULL);
unsigned int deadbeef_beef = 0xdeadbeef;

unsigned int deadbeef_rand() {
    deadbeef_seed = (deadbeef_seed << 7) ^ ((deadbeef_seed >> 25) + deadbeef_beef);
    deadbeef_beef = (deadbeef_beef << 7) ^ ((deadbeef_beef >> 25) + 0xdeadbeef);
    return deadbeef_seed;
}

void deadbeef_srand(unsigned int x) {
    deadbeef_seed = x;
    deadbeef_beef = 0xdeadbeef;
}

int main(int argc, char *argv[]) {

    int roll[5];
    bool match = false;
    int prev = 0;
    int count = 0;
    while (!match) {
        count++;
        match = true;
        for (int i = 0; i < 5; i++) {
            roll[i] = deadbeef_rand()%6+1;
            
            if (roll[i] != prev) {
                match = false;
            }
            prev = roll[i];
        }
        
    }
    
    
    for (int i = 0; i < 5; i++) {
        cout << roll[i] << endl;
    }
    
    cout << "It took " << count << " rolls to match all 5." << endl;
    
    return 0;
}











































////#include <iostream>
////#include <array>
////
////using namespace std;
////
////long fibonaci(long);
////
////
////int main() {
//////    long n;
//////    cout << "Enter an integer to compute it's Fibonaci result" << endl;
//////    cin >> n;
//////
//////    cout << fibonaci(n) << endl;
////
////
////
////}
//
//
//
//#include <iostream>
//#include <fstream>
//#include <cstdlib>
//#include <iomanip>
//#include <deque>
//
////#include "encodings.h"
//
//using namespace std;
//
//// This carves out 8k of memory for instructions
//#define RAM_INSTRUCTION_CNT (1 << 13)
//typedef struct block block;
//
//void process_code(deque<block>& tapeLine);
//
//bool flag = false;
//
//struct block {
//    char letter;
//    bool isBlank;
//};
//
//int main(int argc, char *argv[]) {
//    deque<block> tapeLine;
//      // Read the file
//
//    string line = "some letters";
//    block block;
//
//    for (int i = 0; i < line.size(); i++) {
//        block.letter = line[i];
//        tapeLine.push_back(block);
//    }
//
//
//    process_code(tapeLine);
//
//    for (int i = 0; i < tapeLine.size(); i++) {
//        cout << tapeLine[i].letter;
//    }
//    cout << endl;
//    cout << endl;
//    tapeLine.clear();
//    for (int i = 0; i < tapeLine.size(); i++) {
//        cout << tapeLine[i].letter;
//    }
//      return EXIT_SUCCESS;
//}
//
//void process_code(deque<block>& tapeLine) {
//    block block;
//    block.letter = 'j';
//    flag = true;
//    tapeLine.push_back(block);
//    block.letter = 'z';
//    tapeLine.push_front(block);
//
//}
//
//
//
//
//
//
//
//
//
//
//long fibonaci(long n){
//
//    long f[n];
//    f[0] = 0;
//    f[1] = 1;
//    for (long i = 2; i < n + 1; i++) {
//        f[i] = f[i-1] + f[i-2];
//    }
//    return f[n];
//}
