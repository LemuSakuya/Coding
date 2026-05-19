#include <reg51.h>
#include <intrins.h>

//================== 引脚定义 ==================
sbit RS = P2^0;     // LCD寄存器选择，P2.0 为 RS
sbit RW = P2^1;     // LCD读写控制，P2.1 为 RW
sbit E  = P2^2;     // LCD使能引脚，P2.2 为 E
sbit K1 = P3^0;     // 按键K1 接 P3.0，低电平有效

//================== 函数声明 ==================
void delay_ms(unsigned int ms);
void delay_us(unsigned int us);
void lcd_write_cmd(unsigned char cmd);
void lcd_write_data(unsigned char dat);
void lcd_init(void);
void lcd_show_string(unsigned char row, unsigned char col, unsigned char *str);
void lcd_show_char(unsigned char row, unsigned char col, unsigned char ch);
void lcd_show_num(unsigned char row, unsigned char col, unsigned int num);



//================== 延时函数 ==================
void delay_ms(unsigned int ms)
{
    unsigned int i, j;
    for(i = 0; i < ms; i++)
        for(j = 0; j < 120; j++);
}

void delay_us(unsigned int us)
{
    while(us--)
    {
        _nop_(); _nop_(); _nop_(); _nop_();
    }
}

//================== LCD1602写入函数 ==================
void lcd_write_cmd(unsigned char cmd)
{
    RS = 0;
    RW = 0;
    P0 = cmd;
    delay_us(5);
    E = 1;
    delay_us(5);
    E = 0;
    delay_us(5);
}

//================== LCD1602初始化 ==================
void lcd_init(void)
{
    delay_ms(15);
    lcd_write_cmd(0x38);    // 8位数据，2行显示，5x7字体
    delay_ms(5);
    lcd_write_cmd(0x0C);    // 显示开，光标关
    delay_ms(5);
    lcd_write_cmd(0x06);    // 地址指针自动+1
    delay_ms(5);
    lcd_write_cmd(0x01);    // 清屏
    delay_ms(5);
}

//================== LCD显示函数 ==================
void lcd_show_string(unsigned char row, unsigned char col, unsigned char *str)
{
    unsigned char addr;
    if(row == 1)
        addr = 0x80 + col;      // 第一行起始地址0x80
    else
        addr = 0xC0 + col;      // 第二行起始地址0xC0
    
    lcd_write_cmd(addr);
    
    while(*str != '\0')
    {
        lcd_write_data(*str);
        str++;
    }
}

void lcd_show_char(unsigned char row, unsigned char col, unsigned char ch)
{
    unsigned char addr;
    if(row == 1)
        addr = 0x80 + col;
    else
        addr = 0xC0 + col;
    
    lcd_write_cmd(addr);
    lcd_write_data(ch);
}

void lcd_write_data(unsigned char dat)
{
    RS = 1;
    RW = 0;
    P0 = dat;
    delay_us(5);
    E = 1;
    delay_us(5);
    E = 0;
    delay_us(5);
}

//================== 主函数 ==================
void main(void)
{
    unsigned char count = 0;        // 计数值，范围 0-99
    unsigned char key_flag = 0;     // 按键标志

    K1 = 1;                         // K1 置 1，启用上拉

    lcd_init();                     // 初始化 LCD1602

    // 在第一行第6列显示 "zyh"
    lcd_show_string(1, 6, "zyh");

    // 在第二行第2列显示学号 "202430227039"
    lcd_show_string(2, 2, "202430227039");

    while(1)
    {
        // ----- K1按键检测：按一次计数加一并显示 0-99 -----
        if(K1 == 0)                 // 检测按键是否按下（低电平有效）
        {
            delay_ms(10);           // 延时10ms（消抖）

            if(K1 == 0)             // 再次确认按键仍为按下状态
            {
                if(key_flag == 0)   // 防止重复触发
                {
                    key_flag = 1;   // 标志置1，表示已处理此次按下
                    count++;        // 计数加1

                    if(count > 99)  // 超过99则归0
                        count = 0;

                    lcd_show_num(1, 0, count);  // 在第一行第0列显示计数值
                }
            }
        }
        else
        {
            key_flag = 0;           // 按键松开，清除标志
        }
    }
}

// 显示两位数（0-99），指定起始位置
void lcd_show_num(unsigned char row, unsigned char col, unsigned int num)
{
    unsigned char shi, ge;
    
    shi = num / 10;             // 十位
    ge = num % 10;              // 个位
    
    lcd_show_char(row, col, shi + '0');      // 十位显示
    lcd_show_char(row, col + 1, ge + '0');   // 个位显示
}