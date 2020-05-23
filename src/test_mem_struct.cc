//
// Created by naruto on 10/16/19.
//

#include <stdio.h>
#include <string.h>
#include <cstdlib>

//打印整形数组
void printfarr(unsigned long *arr, size_t size){
    for (size_t i = 0; i < size; i++)
        {
        printf("%x ", arr[i]);
        }
    printf("\n");
    }

//根据传入的数组arr，比较大小，在out上对应标上其大小的顺序值
//总觉得这个算顺序的办法好笨，谁有更好的麻烦贡献出来
void sx(unsigned long* arr, unsigned long *out, size_t size){
    memset(out, -1, size*sizeof(unsigned long));

    for (size_t i = 0; i < size; i++)
        {
        int min;
        for (size_t j = 0; j < size; j++)
            {
            if (out[j]==-1)
                {
                out[j] = i + 1;
                min = j;
                break;
                }
            }

        for (size_t k = min + 1; k < size; k++)
            {
            if((out[k]==-1) && (arr[k] < arr[min])){
                out[min] = -1;
                out[k] = i + 1;
                min = k;
                }
            }
        }
    }

//全局区()
int global1 = 1;
int global2 = 1;
int global3 = 1;
int static global4 = 1;


//文字常量区
const char *str1 = "abc";
const char *str2 = "abc";
const char *str3 = "abcd";
const char *str4 = "abcde";

//程序代码区
void testadd1(int* b){ int a=0;}
void testadd2(){ int b; }
void testadd(){
    //栈区
    int stack1 = 1;
    int stack2 = 1;
    int stack3 = 1;
    //堆区地址
    int *heap1 = (int *)malloc(sizeof(int));
    int *heap2 = (int *)malloc(sizeof(int));
    int *heap3 = (int *)malloc(sizeof(int));

    printf("栈区 变量的地址\n");
    printf("&stack1=%x\n", &stack1);
    printf("&stack2=%x\n", &stack2);
    printf("&stack3=%x\n", &stack3);
    printf("\n");

    printf("堆区 空间的地址\n");
    printf("heap1=%x\n", heap1);
    printf("heap2=%x\n", heap2);
    printf("heap3=%x\n", heap3);

    printf("\n");
    printf("全局区(global)变量的地址\n");
    printf("&global1=%x\n", &global1);
    printf("&global2=%x\n", &global2);
    printf("&global3=%x\n", &global3);
    printf("&global4=%x\n", &global4);

    printf("\n");
    printf("文字常量区 常量的地址\n");
    printf("str1=%x\n", str1);
    printf("str2=%x\n", str2);
    printf("str3=%x\n", str3);
    printf("str4=%x\n", str4);

    printf("\n");
    printf("程序代码区(函数)的地址\n");
    printf("testadd1=%x\n", testadd1);
    printf("testadd2=%x\n", testadd2);
    printf("testadd=%x\n", testadd);
    printf("\n");

    unsigned long a[5] = { (unsigned long)testadd1, (unsigned long)str1, (unsigned long)&global1,(unsigned long)heap1 , (unsigned long)&stack1 };
    unsigned long a1[5];
    sx(a, a1, 5);
    printfarr(a, 5);
    printfarr(a1, 5);
    printf("\n");
    }

int main()
    {
    static int m = 0;
    int a = 0;
    printf("main=%x\n", main);
    printf("主函数static变量%x\n",&a);
    printf("主函数变量%x\n",&m);
    printf("\n");

    char *s1 = "Hellow Word";
    char s2[] = "Hellow Word";
    printf("栈:主函数s1变量%x\n",&s1);
    printf("栈:主函数s2变量%x\n",&s2);


    testadd();
    return 0;
    }
