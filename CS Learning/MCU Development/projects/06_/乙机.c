/**
 * Experiment 06: Dual-MCU Communication - Machine B (Sender)
 * Sends 0,1,2,3,4 cyclically on P1.7 button press.
 * Crystal: 11.0592MHz, Baud: 9600
 *
 * Hardware:
 *   P1.7 -> button (active low, external pull-up)
 *   P3.1 -> TXD, connect to Machine A RXD
 *   GND  -> common with Machine A
 */

#include <reg51.h>

#define uint unsigned int
#define uchar unsigned char

uchar g_send_index = 0;  /* current char index (0~4, wrap) */

/**
 * Rough millisecond delay
 */
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

/**
 * UART init: Mode 1 (8-bit), 9600 baud, TX only
 * TH1 = 256 - 11.0592MHz/(12*32*9600) = 253 = 0xFD
 */
void uart_init(void)
{
    SCON = 0x40;   /* Mode 1, REN=0 (no receive) */
    TMOD &= 0x0f;  /* clear T1 bits */
    TMOD |= 0x20;  /* T1 Mode 2 (8-bit auto-reload) */
    TH1  = 0xfd;   /* 9600 baud @ 11.0592MHz */
    TL1  = 0xfd;
    TR1  = 1;      /* start T1 */
    /* Machine B only sends; no serial interrupt needed */
}

/**
 * Send one byte
 */
void uart_send(uchar dat)
{
    SBUF = dat;
    while (!TI);    /* wait for TX complete */
    TI = 0;         /* clear TX flag */
}

void main(void)
{
    uart_init();

    while (1) {
        /* detect button press (P1.7 == 0, active low) */
        if ((P1 & 0x80) == 0x00) {
            delay_ms(10);  /* software debounce */
            if ((P1 & 0x80) == 0x00) {
                uart_send(g_send_index);  /* send current char */

                /* update index: 0->1->2->3->4->0 wrap */
                g_send_index++;
                if (g_send_index > 4) {
                    g_send_index = 0;
                }
            }
            /* wait for button release (prevent repeat) */
            while ((P1 & 0x80) == 0x00) {
                ;
            }
            delay_ms(10);  /* release debounce */
        }
    }
}
