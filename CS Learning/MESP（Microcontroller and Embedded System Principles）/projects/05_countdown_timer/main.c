#include <reg51.h>

#define uint unsigned int
#define uchar unsigned char

uchar code discode_dot[] = {
    0xbf, 0x86, 0xdb, 0xcf, 0xe6,
    0xed, 0xfd, 0x87, 0xff, 0xef
};

uchar code discode_normal[] = {
    0x3f, 0x06, 0x5b, 0x4f, 0x66,
    0x6d, 0x7d, 0x07, 0x7f, 0x6f
};

uchar timer = 0;
uint second = 300;
uchar key = 0;

void display_time(void)
{
    P0 = discode_normal[second / 100];
    P2 = discode_dot[(second / 10) % 10];
    P1 = discode_normal[second % 10];
}

void timer0_load_50ms(void)
{
    TH0 = 0x3c;
    TL0 = 0xb0;
}

void main(void)
{
    TMOD = 0x01;
    ET0 = 1;
    EA = 1;

    display_time();

    while (1) {
        if ((P3 & 0x80) == 0x00) {
            key++;

            switch (key) {
            case 1:
                timer0_load_50ms();
                TR0 = 1;
                break;

            case 2:
                TR0 = 0;
                break;

            case 3:
                key = 0;
                second = 300;
                timer = 0;
                display_time();
                break;
            }

            while ((P3 & 0x80) == 0x00) {
                ;
            }
        }
    }
}

void int_T0(void) interrupt 1
{
    TR0 = 0;
    timer0_load_50ms();

    timer++;
    if (timer == 2) {
        timer = 0;
        second--;
        display_time();
    }

    if (second == 0) {
        TR0 = 0;
        second = 300;
        key = 2;
    } else {
        TR0 = 1;
    }
}
