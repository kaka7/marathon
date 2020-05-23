
#include <iostream>
#include <stdio.h>
using namespace std;

int main(int argc, char const *argv[])
{
    FILE* fin;
    fin = fopen(argv[1],"rb");
    float x=0;
    fread(&x,4,1,fin);
    cout<<x<<endl;
    return 0;
}
