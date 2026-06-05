/**
 * Experiment 06: Dual-MCU UART - Machine B
 *
 * Function according to the schematic:
 *   1. K2 on Machine B sends one digit to Machine A, then Machine A displays it.
 *   2. Machine B receives a command from Machine A and blinks its LEDs.
 *
 * Crystal: 11.0592MHz, Baud: 9600
 *
 * Hardware:
 *   P1.0/P1.3 -> LEDs through 220R to VCC, active low
 *   P1.7      -> K2 button, active low
 *   P3.0/RXD  -> Machine A P3.1/TXD
 *   P3.1/TXD  -> Machine A P3.0/RXD
 *   GND       -> common with Machine A
 */

#include <reg51.h>

#define uint unsigned int
#define uchar unsigned char

#define CMD_BLINK 'L'

sbit LED1 = P1^0;
sbit LED2 = P1^3;
sbit KEY_B = P1^7;

uchar g_send_num = 0;
bit g_blink_request = 0;

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

void blink_leds(void)
{
    uchar i;

    for (i = 0; i < 3; i++) {
        LED1 = 0;
        LED2 = 0;
        delay_ms(200);
        LED1 = 1;
        LED2 = 1;
        delay_ms(200);
    }
}

void uart_isr(void) interrupt 4
{
    uchar dat;

    if (RI) {
        RI = 0;
        dat = SBUF;

        if (dat == CMD_BLINK) {
            g_blink_request = 1;
        }
    }

    if (TI) {
        TI = 0;
    }
}

void main(void)
{
    uart_init();
    LED1 = 1;      /* LED off, active low */
    LED2 = 1;
    KEY_B = 1;     /* release P1.7 for input */

    while (1) {
        if (g_blink_request) {
            g_blink_request = 0;
            blink_leds();
        }

        if (KEY_B == 0) {
            delay_ms(10);
            if (KEY_B == 0) {
                uart_send('0' + g_send_num);

                g_send_num++;
                if (g_send_num > 9) {
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
