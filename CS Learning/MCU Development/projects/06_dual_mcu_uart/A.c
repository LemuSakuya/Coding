/**
 * Experiment 06: Dual-MCU Communication - Machine A (Receiver)
 * Receives two-byte string "00"~"04" from Machine B, displays ones digit on 7-segment.
 * Crystal: 11.0592MHz, Baud: 9600
 *
 * Hardware:
 *   P0   -> 7-segment segment (a b c d e f g dp) — needs pull-up resistors!
 *   P3.0 -> RXD, connect to Machine B TXD
 *   GND  -> common with Machine B
 *
 * Note: P0 is open-drain on standard 8051. For common-cathode 7-segment,
 *       add 10kΩ pull-up resistor network (e.g., 8x 10kΩ SIP) on P0.
 *       For common-anode, invert seg_table values: P0 = ~seg_table[idx].
 */

#include <reg51.h>

#define uint unsigned int
#define uchar unsigned char

/* Common-cathode 7-segment lookup table 0~F */
uchar code seg_table[] = {
    0x3f,  // 0
    0x06,  // 1
    0x5b,  // 2
    0x4f,  // 3
    0x66,  // 4
    0x6d,  // 5
    0x7d,  // 6
    0x07,  // 7
    0x7f,  // 8
    0x6f,  // 9
    0x77,  // A
    0x7c,  // B
    0x39,  // C
    0x5e,  // D
    0x79,  // E
    0x71   // F
};

uchar g_received_char = 0;   /* received char index (0~4), default 0 */
bit g_rx_done = 0;           /* flag: 1 = a complete 2-byte frame received */
bit g_rx_state = 0;          /* 0 = expecting tens digit, 1 = expecting ones digit */

/**
 * UART init: Mode 1 (8-bit), 9600 baud
 * TH1 = 256 - 11.0592MHz/(12*32*9600) = 253 = 0xFD
 */
void uart_init(void)
{
    SCON = 0x50;   /* Mode 1, REN=1 (enable receive) */
    TMOD &= 0x0f;  /* clear T1 bits */
    TMOD |= 0x20;  /* T1 Mode 2 (8-bit auto-reload) */
    TH1  = 0xfd;   /* 9600 baud @ 11.0592MHz */
    TL1  = 0xfd;
    TR1  = 1;      /* start T1 */
    ES   = 1;      /* enable serial interrupt */
    EA   = 1;      /* enable global interrupt */
}

/**
 * Serial ISR: receive two-byte frame "00"~"04" from Machine B
 * State machine synchronises on tens='0', then captures ones digit.
 */
void uart_isr(void) interrupt 4
{
    uchar tmp;
    if (RI) {
        RI = 0;                          /* clear RX flag */
        tmp = SBUF;                      /* read received byte */
        if (g_rx_state == 0) {
            /* expecting tens digit — must be '0' */
            if (tmp == '0') {
                g_rx_state = 1;          /* valid tens, wait for ones */
            }
            /* otherwise resync: stay in state 0, ignore byte */
        } else {
            /* expecting ones digit — '0'~'4' */
            g_rx_state = 0;              /* back to expecting tens */
            if (tmp >= '0' && tmp <= '4') {
                g_received_char = tmp - '0';
            } else {
                g_received_char = 0;     /* illegal → display 0 */
            }
            g_rx_done = 1;               /* notify main loop */
        }
    }
    /* Machine A does not send; TI is ignored */
}

void main(void)
{
    uart_init();

    P0 = seg_table[0];  /* default display '0' */

    while (1) {
        if (g_rx_done) {
            g_rx_done = 0;
            P0 = seg_table[g_received_char];  /* LUT output */
        }
    }
}
