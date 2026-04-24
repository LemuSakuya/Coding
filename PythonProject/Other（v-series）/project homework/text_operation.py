#text_operation.py
def text_operation():
    while True:
        try:
            filename = input("请输入文件名(输入q退出): ")
            if filename.lower() == 'q':
                break
                
            content = input("请输入文件内容: ")
            
            try:
                with open(filename, 'r') as file:
                    print("\n文件已存在，当前内容为:")
                    print(file.read())
                    
                action = input("\n请选择操作: [a]追加 [o]覆盖 [c]取消: ").lower()
                if action == 'a':
                    with open(filename, 'a') as file:
                        file.write('\n' + content)
                    print("内容已追加到文件末尾。")
                elif action == 'o':
                    with open(filename, 'w') as file:
                        file.write(content)
                    print("文件内容已被覆盖。")
                else:
                    print("操作已取消。")
                    
            except FileNotFoundError:
                with open(filename, 'w') as file:
                    file.write(content)
                print(f"文件 {filename} 已创建并写入内容。")
                
        except PermissionError:
            print("错误: 没有文件操作权限。")
        except IOError as e:
            print(f"IO错误: {e}")
        except Exception as e:
            print(f"发生未知错误: {e}")
            
        print("-" * 40)

if __name__ == "__main__":
    text_operation()