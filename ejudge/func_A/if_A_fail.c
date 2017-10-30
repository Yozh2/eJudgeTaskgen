#include <stdio.h>

int in_region(float x, float y)
{
    return y>=-2 && y <= x+3 && y <= -x+3;
}

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("%s\n", in_region(x,y) ? "YES" : "NO");
    return 0;
}
