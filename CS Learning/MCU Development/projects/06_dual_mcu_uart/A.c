/**
 * Experiment 06: Dual-MCU UART - Machine A
 *
 * Function according to the schematic:
 *   1. K1 on Machine A sends a command to Machine B.
 *   2. Machine A receives a digit from Machine B and displays it on the
 *      common-cathode 7-segment display connected to P0.
 *
 * Crystal: 11.0592MHz, Baud: 9600
 *
 * Hardware:
 *   P0.0~P0.7 -> 7-segment a,b,c,d,e,f,g,dp through pull-up resistor pack
 *   P1.7      -> K1 button, active low
 *   P3.0/RXD  -> Machine B P3.1/TXD
 *   P3.1/TXD  -> Machine B P3.0/RXD
 *   GND       -> common with Machine B
 */

#include <reg51.h>

#define uint unsigned int
#define uchar unsigned char

#define CMD_BLINK 'L'

sbit KEY_A = P1^7;

/* Common-cathode 7-segment code: bit0~bit7 = a,b,c,d,e,f,g,dp */
uchar code seg_table[] = {
    0x3f,  /* 0 */
    0x06,  /* 1 */
    0x5b,  /* 2 */
    0x4f,  /* 3 */
    0x66,  /* 4 */
    0x6d,  /* 5 */
    0x7d,  /* 6 */
    0x07,  /* 7 */
    0x7f,  /* 8 */
    0x6f   /* 9 */
};

uchar g_display_num = 0;
bit g_display_update = 0;

void delay_ms(uint ms)
{
    uint i;
    uchar j;

    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++) {
            ;
        }
    }
}

void uart_init(void)
{
    SCON = 0x50;   /* mode 1, REN=1 */
    TMOD &= 0x0f;
    TMOD |= 0x20;  /* Timer1 mode 2 */
    TH1 = 0xfd;    /* 9600bps @ 11.0592MHz */
    TL1 = 0xfd;
    TR1 = 1;
    ES = 1;
    EA = 1;
}

void uart_send(uchar dat)
{
    ES = 0;        /* avoid TI causing a serial interrupt while polling */
    TI = 0;
    SBUF = dat;
    while (!TI) {
        ;
    }
    TI = 0;
    ES = 1;
}

void uart_isr(void) interrupt 4
{
    uchar dat;

    if (RI) {
        RI = 0;
        dat = SBUF;

        if (dat >= '0' && dat <= '9') {
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
    KEY_A = 1;             /* release P1.7 for input */
    P0 = seg_table[0];     /* default display 0 */

    while (1) {
        if (g_display_update) {
            g_display_update = 0;
            P0 = seg_table[g_display_num];
        }

        if (KEY_A == 0) {
            delay_ms(10);
            if (KEY_A == 0) {
                uart_send(CMD_BLINK);
            }

            while (KEY_A == 0) {
                ;
            }
            delay_ms(10);
        }
    }
}
