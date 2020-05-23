//
// Created by naruto on 9/9/19.
//
#include <algorithm>
#include <iostream>
#include <array>
//#include <>
using namespace std;

template<class ForwardIterator>
inline size_t argmin(ForwardIterator first, ForwardIterator last)
    {
    return std::distance(first, std::min_element(first, last));
    }

template<class ForwardIterator>
inline size_t argmax(ForwardIterator first, ForwardIterator last)
    {
    return std::distance(first, std::max_element(first, last));
    }
int main() {
//    array <int, 7> numbers={2, 4, 8, 0, 6, -1, 3};
    vector <vector <float> > plate_arr={{12.5, 8.9, 100, 24.5, 30.0},{2, 4, 8, 1, 6, -1, 3}};
    float score=1;
    vector<float>labels;
    for (int i=0;i<plate_arr.size();i++)
        {
        size_t s=*max_element(plate_arr[i].begin(), plate_arr[i].end());
//        size_t max=plate_arr[i][m];//不是max
        size_t maxIndex = argmax(plate_arr[i].begin(), plate_arr[i].end());
        score*=s;
        labels.push_back(maxIndex);
        }
    labels.push_back(score);
    vector <float> ::iterator it=labels.begin();
    for (it;it!=labels.end();it++){
        cout<<*it<<endl;}
    return 0;
    }
//g++ -o demo -std=c++11  argmax.cpp
// g++ -o libpycallclass.so -shared -fPIC pycallclass.cpp。
//import ctypes
//so = ctypes.cdll.LoadLibrary
//lib = so("./libpycallclass.so")
//lib.display_int(100)


