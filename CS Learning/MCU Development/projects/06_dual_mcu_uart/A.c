/**
 * Experiment 06: Dual-MCU UART - Machine A
 *
 * Task:
 *   Machine A receives characters '0'~'4' from Machine B at 9600 bit/s,
 *   then displays the received number on the 7-segment display by table lookup.
 *
 * Crystal: 11.0592MHz
 *
 * Hardware:
 *   P0.0~P0.7 -> 7-segment a,b,c,d,e,f,g,dp through pull-up resistor pack
 *   P3.0/RXD  -> Machine B P3.1/TXD
 *   GND       -> common with Machine B
 */

#include <reg51.h>

#define uint unsigned int
#define uchar unsigned char

/* Common-cathode 7-segment code: bit0~bit7 = a,b,c,d,e,f,g,dp */
uchar code seg_table[] = {
    0x3f,  /* 0 */
    0x06,  /* 1 */
    0x5b,  /* 2 */
    0x4f,  /* 3 */
    0x66   /* 4 */
};

uchar g_display_num = 0;
bit g_display_update = 0;

void uart_init(void)
{
    SCON = 0x50;   /* serial mode 1, REN=1 */
    TMOD &= 0x0f;
    TMOD |= 0x20;  /* Timer1 mode 2, 8-bit auto reload */
    TH1 = 0xfd;    /* 9600 bit/s @ 11.0592MHz */
    TL1 = 0xfd;
    TR1 = 1;
    ES = 1;
    EA = 1;
}

void uart_isr(void) interrupt 4
{
    uchar dat;

    if (RI) {
        RI = 0;
        dat = SBUF;

        if (dat >= '0' && dat <= '4') {
            g_display_num = dat - '0';
            g_display_update = 1;
        }
    }

    if (TI) {
        TI = 0;
    }
}

void main(void)
{
    uart_init();
    P0 = seg_table[0];

    while (1) {
        if (g_display_update) {
            g_display_update = 0;
            P0 = seg_table[g_display_num];
        }
    }
}
