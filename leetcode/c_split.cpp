//
// Created by naruto on 11/25/19.
//

#include <iostream>
#include <string.h>
#include <vector>
#include "stdio.h"
using namespace std;

int main ()
    {
    string s;

    while(cin>>s){

        vector<int>nums;

        char *str = (char *)s.c_str();//string --> char
        const char *split = ",";
        char *p = strtok (str,split);//逗号分隔依次取出

        int a;
        while(p != NULL) {
            sscanf(p, "%d", &a);//char ---> int
            nums.push_back(a);
            p = strtok(NULL,split);
            }

        //printf
        for (int i=0; i<nums.size(); i++) {
            printf ("%d\n",nums[i]);
            }
        }


    return 0;
    }
