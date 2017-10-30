#include <stdio.h>

int in_region(float x, float y)
{
    return y>=-2 && y <= x+3 && y <= -x+3;
}

int main()
{
    float x, y;
    scanf("%f%f", &x, &y);
    printf("%s\n", in_region(x,y) ? "YES" : "NO");
    return 0;
}
