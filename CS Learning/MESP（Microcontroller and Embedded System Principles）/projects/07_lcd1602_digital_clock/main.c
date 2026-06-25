#include <reg51.h>
#include <intrins.h>

#define uint unsigned int
#define uchar unsigned char

sbit LCD_RS = P2^0;
sbit LCD_RW = P2^1;
sbit LCD_EN = P2^2;

sbit KEY_HOUR  = P1^0;
sbit KEY_MIN   = P1^1;
sbit KEY_CLEAR = P1^2;

#define LCD_DATA P3

#define T0_RELOAD_H 0x3c
#define T0_RELOAD_L 0xb0

volatile uchar g_hour = 0;
volatile uchar g_min = 0;
volatile uchar g_sec = 0;
volatile uchar g_t0_count = 0;
volatile uchar g_display_flag = 1;

void delay_us(uint us);
void delay_ms(uint ms);
void lcd_write_cmd(uchar cmd);
void lcd_write_data(uchar dat);
void lcd_init(void);
void lcd_show_string(uchar row, uchar col, uchar *str);
void lcd_show_char(uchar row, uchar col, uchar ch);
void lcd_show_two_digits(uchar row, uchar col, uchar value);
void display_clock(void);
void timer0_init(void);
void timer0_load_50ms(void);
void scan_keys(void);

void delay_us(uint us)
{
    while (us--) {
        _nop_();
        _nop_();
        _nop_();
        _nop_();
    }
}

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

void lcd_write_cmd(uchar cmd)
{
    LCD_RS = 0;
    LCD_RW = 0;
    LCD_DATA = cmd;
    delay_us(5);
    LCD_EN = 1;
    delay_us(5);
    LCD_EN = 0;
    delay_us(5);
}

void lcd_write_data(uchar dat)
{
    LCD_RS = 1;
    LCD_RW = 0;
    LCD_DATA = dat;
    delay_us(5);
    LCD_EN = 1;
    delay_us(5);
    LCD_EN = 0;
    delay_us(5);
}

void lcd_init(void)
{
    delay_ms(15);
    lcd_write_cmd(0x38);
    delay_ms(5);
    lcd_write_cmd(0x0c);
    delay_ms(5);
    lcd_write_cmd(0x06);
    delay_ms(5);
    lcd_write_cmd(0x01);
    delay_ms(5);
}

void lcd_show_string(uchar row, uchar col, uchar *str)
{
    uchar addr;

    if (row == 1) {
        addr = 0x80 + col;
    } else {
        addr = 0xc0 + col;
    }

    lcd_write_cmd(addr);
    while (*str != '\0') {
        lcd_write_data(*str);
        str++;
    }
}

void lcd_show_char(uchar row, uchar col, uchar ch)
{
    if (row == 1) {
        lcd_write_cmd(0x80 + col);
    } else {
        lcd_write_cmd(0xc0 + col);
    }

    lcd_write_data(ch);
}

void lcd_show_two_digits(uchar row, uchar col, uchar value)
{
    lcd_show_char(row, col, value / 10 + '0');
    lcd_show_char(row, col + 1, value % 10 + '0');
}

void display_clock(void)
{
    lcd_show_two_digits(2, 6, g_hour);
    lcd_show_char(2, 8, ':');
    lcd_show_two_digits(2, 9, g_min);
    lcd_show_char(2, 11, ':');
    lcd_show_two_digits(2, 12, g_sec);
}

void timer0_load_50ms(void)
{
    TH0 = T0_RELOAD_H;
    TL0 = T0_RELOAD_L;
}

void timer0_init(void)
{
    TMOD &= 0xf0;
    TMOD |= 0x01;
    timer0_load_50ms();
    ET0 = 1;
    EA = 1;
    TR0 = 1;
}

void scan_keys(void)
{
    if (KEY_HOUR == 0) {
        delay_ms(10);
        if (KEY_HOUR == 0) {
            while (KEY_HOUR == 0) {
                ;
            }

            EA = 0;
            g_hour++;
            if (g_hour >= 24) {
                g_hour = 0;
            }
            g_display_flag = 1;
            EA = 1;
        }
    }

    if (KEY_MIN == 0) {
        delay_ms(10);
        if (KEY_MIN == 0) {
            while (KEY_MIN == 0) {
                ;
            }

            EA = 0;
            g_min++;
            if (g_min >= 60) {
                g_min = 0;
            }
            g_display_flag = 1;
            EA = 1;
        }
    }

    if (KEY_CLEAR == 0) {
        delay_ms(10);
        if (KEY_CLEAR == 0) {
            while (KEY_CLEAR == 0) {
                ;
            }

            EA = 0;
            g_hour = 0;
            g_min = 0;
            g_sec = 0;
            g_t0_count = 0;
            timer0_load_50ms();
            TR0 = 1;
            g_display_flag = 1;
            EA = 1;
        }
    }
}

void main(void)
{
    P1 = 0xff;
    LCD_DATA = 0x00;
    LCD_EN = 0;

    lcd_init();
    lcd_show_string(1, 2, "H.I.T. CHINA");
    lcd_show_string(2, 0, "TIME  00:00:00");

    timer0_init();

    while (1) {
        scan_keys();

        if (g_display_flag) {
            g_display_flag = 0;
            display_clock();
        }
    }
}

void timer0_isr(void) interrupt 1
{
    timer0_load_50ms();

    g_t0_count++;
    if (g_t0_count >= 20) {
        g_t0_count = 0;

        g_sec++;
        if (g_sec >= 60) {
            g_sec = 0;
            g_min++;
            if (g_min >= 60) {
                g_min = 0;
                g_hour++;
                if (g_hour >= 24) {
                    g_hour = 0;
                }
            }
        }

        g_display_flag = 1;
    }
}
