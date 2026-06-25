#include <REGX52.H>

typedef unsigned char u8;
typedef unsigned int u16;

sbit K1 = P1 ^ 0;
sbit K2 = P1 ^ 1;
sbit K3 = P1 ^ 2;
sbit K4 = P1 ^ 3;
sbit K5 = P1 ^ 4;

static u8 mode = 0;

void delay_ms(u16 ms)
{
    u16 i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 123; j++) {
            ;
        }
    }
}

u8 key_scan(void)
{
    if (K1 == 0) {
        delay_ms(10);
        if (K1 == 0) {
            while (K1 == 0) { ; }
            return 1;
        }
    }

    if (K2 == 0) {
        delay_ms(10);
        if (K2 == 0) {
            while (K2 == 0) { ; }
            return 2;
        }
    }

    if (K3 == 0) {
        delay_ms(10);
        if (K3 == 0) {
            while (K3 == 0) { ; }
            return 3;
        }
    }

    if (K4 == 0) {
        delay_ms(10);
        if (K4 == 0) {
            while (K4 == 0) { ; }
            return 4;
        }
    }

    if (K5 == 0) {
        delay_ms(10);
        if (K5 == 0) {
            while (K5 == 0) { ; }
            return 5;
        }
    }

    return 0;
}

void update_mode(void)
{
    u8 key = key_scan();
    if (key != 0) {
        mode = key;
    }
}

void led_off(void)
{
    P3 = 0xFF;
}

void run_forward(void)
{
    u8 i;
    for (i = 0; i < 8; i++) {
        update_mode();
        if (mode != 1) {
            return;
        }
        P3 = ~(0x01 << i);
        delay_ms(120);
    }
}

void run_backward(void)
{
    signed char i;
    for (i = 7; i >= 0; i--) {
        update_mode();
        if (mode != 2) {
            return;
        }
        P3 = ~(0x01 << i);
        delay_ms(120);
    }
}

void run_high_low_blink(void)
{
    update_mode();
    if (mode != 3) {
        return;
    }
    P3 = 0x0F;
    delay_ms(250);

    update_mode();
    if (mode != 3) {
        return;
    }
    P3 = 0xF0;
    delay_ms(250);
}

void run_all_blink(void)
{
    update_mode();
    if (mode != 4) {
        return;
    }
    P3 = 0x00;
    delay_ms(250);

    update_mode();
    if (mode != 4) {
        return;
    }
    P3 = 0xFF;
    delay_ms(250);
}

void run_pair_inward(void)
{
    update_mode();
    if (mode != 5) {
        return;
    }
    P3 = 0x7E;
    delay_ms(500);

    update_mode();
    if (mode != 5) {
        return;
    }
    P3 = 0xBD;
    delay_ms(500);

    update_mode();
    if (mode != 5) {
        return;
    }
    P3 = 0xDB;
    delay_ms(500);

    update_mode();
    if (mode != 5) {
        return;
    }
    P3 = 0xE7;
    delay_ms(500);
}

void main(void)
{
    led_off();
    while (1) {
        update_mode();

        switch (mode) {
        case 1:
            run_forward();
            break;
        case 2:
            run_backward();
            break;
        case 3:
            run_high_low_blink();
            break;
        case 4:
            run_all_blink();
            break;
        case 5:
            run_pair_inward();
            break;
        default:
            led_off();
            break;
        }
    }
}
