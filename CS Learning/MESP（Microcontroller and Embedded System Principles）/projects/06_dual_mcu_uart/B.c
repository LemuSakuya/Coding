/**
 * Experiment 06: Dual-MCU UART - Machine B
 *
 * Task:
 *   Each time the button on P1.7 is pressed, Machine B sends one character
 *   from '0' to '4'. After '4', it returns to '0'.
 *
 * Crystal: 11.0592MHz, Baud: 9600 bit/s
 *
 * Hardware:
 *   P1.7      -> button, active low
 *   P3.1/TXD  -> Machine A P3.0/RXD
 *   GND       -> common with Machine A
 */

#include <reg51.h>

#define uint unsigned int
#define uchar unsigned char

sbit KEY_B = P1^7;

uchar g_send_num = 0;

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
    SCON = 0x40;   /* serial mode 1, transmit only */
    TMOD &= 0x0f;
    TMOD |= 0x20;  /* Timer1 mode 2, 8-bit auto reload */
    TH1 = 0xfd;    /* 9600 bit/s @ 11.0592MHz */
    TL1 = 0xfd;
    TR1 = 1;
}

void uart_send(uchar dat)
{
    TI = 0;
    SBUF = dat;
    while (!TI) {
        ;
    }
    TI = 0;
}

void main(void)
{
    uart_init();
    KEY_B = 1;     /* release P1.7 for input */

    while (1) {
        if (KEY_B == 0) {
            delay_ms(10);
            if (KEY_B == 0) {
                uart_send('0' + g_send_num);

                g_send_num++;
                if (g_send_num > 4) {
                    g_send_num = 0;
                }
            }

            while (KEY_B == 0) {
                ;
            }
            delay_ms(10);
        }
    }
}
