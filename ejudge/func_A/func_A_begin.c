#include <stdio.h>
#define FUNC_SOLUTION
int func_A(float x, float y);
int taty_func_A(float x, float y)
{
    return y>=-2 && y<=x+3 && y<=-x+3; 
}
int main()
{
	float x, y;
    int res1, res2;
    scanf("%f%f", &x, &y);
#ifdef FUNC_SOLUTION
    res1 = taty_func_A(x,y);
    res2 = func_A(x,y);
    printf(res2 ? "YES\n" : "NO\n");
    
    if (res1 != res2)
        return 2;
#else    
    printf(taty_func_A(x,y) ? "YES\n" : "NO\n");
#endif    
	return 0;
}
