#include <reg52.h>

#define uint unsigned int
#define uchar unsigned char

#define MODE_STATIC_SINGLE_DIGIT 0
#define MODE_DYNAMIC_FOUR_DIGIT  1
#define EXPERIMENT_MODE MODE_DYNAMIC_FOUR_DIGIT
#define DYNAMIC_START_VALUE 5678u

#define SEG_ACTIVE_LEVEL   0

#define T0_RELOAD_H 0xFC
#define T0_RELOAD_L 0x18

uchar code seg_lut_raw[] = {
    0x3f, 0x06, 0x5b, 0x4f,
    0x66, 0x6d, 0x7d, 0x07,
    0x7f, 0x6f, 0x77, 0x7c,
    0x39, 0x5e, 0x79, 0x71
};

volatile uchar g_disp_buf[4] = {0, 0, 0, 0};
volatile uchar g_scan_idx = 0;
volatile uint g_ms_div = 0;
volatile uchar g_update_flag = 0;

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

uchar seg_encode(uchar value)
{
    uchar raw = seg_lut_raw[value & 0x0f];
#if SEG_ACTIVE_LEVEL
    return raw;
#else
    return (uchar)(~raw);
#endif
}

void seg_all_off(void)
{
#if SEG_ACTIVE_LEVEL
    P0 = 0x00;
#else
    P0 = 0xff;
#endif
}

void digit_all_off(void)
{
#if DIGIT_ACTIVE_LEVEL
    P2 = (P2 & 0xf0) | 0x00;
#else
    P2 = (P2 & 0xf0) | 0x0f;
#endif
}

void digit_on(uchar idx)
{
    uchar mask = (uchar)(1u << (idx & 0x03));
#if DIGIT_ACTIVE_LEVEL
    P2 = (P2 & 0xf0) | mask;
#else
    P2 = (P2 & 0xf0) | ((uchar)(~mask) & 0x0f);
#endif
}

void set_display_value(uint value)
{
    if (value > 9999u) {
        value = 0;
    }
    g_disp_buf[0] = (uchar)(value / 1000u);
    g_disp_buf[1] = (uchar)((value / 100u) % 10u);
    g_disp_buf[2] = (uchar)((value / 10u) % 10u);
    g_disp_buf[3] = (uchar)(value % 10u);
}

void timer0_init_1ms(void)
{
    TMOD &= 0xf0;
    TMOD |= 0x01;
    TH0 = T0_RELOAD_H;
    TL0 = T0_RELOAD_L;
    ET0 = 1;
    EA = 1;
    TR0 = 1;
}

void timer0_isr(void) interrupt 1
{
    TH0 = T0_RELOAD_H;
    TL0 = T0_RELOAD_L;

    digit_all_off();
    P0 = seg_encode(g_disp_buf[g_scan_idx]);
    digit_on(g_scan_idx);

    g_scan_idx++;
    if (g_scan_idx >= 4u) {
        g_scan_idx = 0;
    }

    g_ms_div++;
    if (g_ms_div >= 300u) {
        g_ms_div = 0;
        g_update_flag = 1u;
    }
}

void run_static_mode(void)
{
    uchar n;
    digit_all_off();
    digit_on(0);
    while (1) {
        for (n = 0; n < 10u; n++) {
            P0 = seg_encode(n);
            delay_ms(500);
        }
    }
}

void run_dynamic_mode(void)
{
    uint value = DYNAMIC_START_VALUE;
    set_display_value(value);
    timer0_init_1ms();
    while (1) {
        if (g_update_flag) {
            g_update_flag = 0;
            value++;
            if (value > 9999u) {
                value = 0;
            }
            set_display_value(value);
        }
    }
}

void main(void)
{
    digit_all_off();
    seg_all_off();

#if EXPERIMENT_MODE == MODE_STATIC_SINGLE_DIGIT
    run_static_mode();
#else
    run_dynamic_mode();
#endif
}