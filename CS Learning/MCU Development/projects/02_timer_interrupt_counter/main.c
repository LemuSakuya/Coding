#include <REGX52.H>

typedef unsigned int u16;

sbit LED0 = P3 ^ 0;

static u16 tick_ms = 0;

void timer0_init(void)
{
    TMOD &= 0xF0;
    TMOD |= 0x01;

    TH0 = 0xFC;
    TL0 = 0x18;

    ET0 = 1;
    EA = 1;
    TR0 = 1;
}

void timer0_isr(void) interrupt 1
{
    TH0 = 0xFC;
    TL0 = 0x18;

    tick_ms++;
    if (tick_ms >= 1000) {
        tick_ms = 0;
        LED0 = !LED0;
    }
}

void main(void)
{
    LED0 = 1;
    timer0_init();

    while (1) {
        ;
    }
}
