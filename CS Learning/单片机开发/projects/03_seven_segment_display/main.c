#include <REGX52.H>

typedef unsigned char u8;
typedef unsigned int u16;

/*
 * 数码管实验（静态显示 + 动态扫描）
 * 端口约定：
 * - 段选：P0.0~P0.7 -> A B C D E F G DP
 * - 位选：P2.0~P2.3 -> DIG1 DIG2 DIG3 DIG4
 */

#define MODE_STATIC_SINGLE_DIGIT   0
#define MODE_DYNAMIC_FOUR_DIGIT    1

/* 选择实验模式：0=静态单个数码管，1=动态四位数码管 */
#define EXPERIMENT_MODE MODE_DYNAMIC_FOUR_DIGIT

/* 按你的 Proteus 器件类型调整电平极性 */
#define SEG_ACTIVE_LEVEL   0  /* 段选有效电平：0=低有效，1=高有效 */
#define DIGIT_ACTIVE_LEVEL 1  /* 位选有效电平：0=低有效，1=高有效 */

static const u8 seg_lut_raw[10] = {
    /* 共阴字形（高电平点亮）顺序 A B C D E F G DP */
    0x3F, /* 0 */
    0x06, /* 1 */
    0x5B, /* 2 */
    0x4F, /* 3 */
    0x66, /* 4 */
    0x6D, /* 5 */
    0x7D, /* 6 */
    0x07, /* 7 */
    0x7F, /* 8 */
    0x6F  /* 9 */
};

static u8 disp_buf[4] = {0, 0, 0, 0};
static u8 scan_idx = 0;
static u16 ms_counter = 0;

void delay_ms(u16 ms)
{
    u16 i;
    u16 j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 110; j++) {
            ;
        }
    }
}

u8 apply_seg_polarity(u8 raw)
{
    return (SEG_ACTIVE_LEVEL == 1) ? raw : (~raw);
}

void all_digits_off(void)
{
    if (DIGIT_ACTIVE_LEVEL == 1) {
        P2 &= 0xF0;
    } else {
        P2 |= 0x0F;
    }
}

void select_digit(u8 idx)
{
    u8 mask = (u8)(1u << idx);

    if (DIGIT_ACTIVE_LEVEL == 1) {
        P2 = (P2 & 0xF0) | mask;
    } else {
        P2 = (P2 & 0xF0) | ((~mask) & 0x0F);
    }
}

void seg_write_num(u8 num)
{
    if (num > 9) {
        num = 0;
    }

    P0 = apply_seg_polarity(seg_lut_raw[num]);
}

void display_scan_step(void)
{
    all_digits_off();
    seg_write_num(disp_buf[scan_idx]);
    select_digit(scan_idx);

    scan_idx++;
    if (scan_idx >= 4) {
        scan_idx = 0;
    }
}

void set_display_number(u16 n)
{
    disp_buf[0] = (u8)(n / 1000);
    disp_buf[1] = (u8)((n / 100) % 10);
    disp_buf[2] = (u8)((n / 10) % 10);
    disp_buf[3] = (u8)(n % 10);
}

void timer0_init_1ms(void)
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

    if (EXPERIMENT_MODE == MODE_DYNAMIC_FOUR_DIGIT) {
        display_scan_step();
        ms_counter++;
    }
}

void run_static_experiment(void)
{
    u8 d;

    all_digits_off();
    select_digit(0);

    while (1) {
        for (d = 0; d <= 9; d++) {
            seg_write_num(d);
            delay_ms(500);
        }
    }
}

void run_dynamic_experiment(void)
{
    u16 number = 0;

    set_display_number(number);

    while (1) {
        if (ms_counter >= 300) {
            ms_counter = 0;

            number++;
            if (number > 9999) {
                number = 0;
            }
            set_display_number(number);
        }
    }
}

void main(void)
{
    P0 = apply_seg_polarity(0x00);
    all_digits_off();

    if (EXPERIMENT_MODE == MODE_STATIC_SINGLE_DIGIT) {
        run_static_experiment();
    } else {
        timer0_init_1ms();
        run_dynamic_experiment();
    }
}
