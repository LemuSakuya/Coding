#(5)
print("(5):")
Dic1 = {"苹果":5.8, "香蕉":3.2, "橙子":4.5, "葡萄":6.7, "梨子":1.5}
Dic2 = {"苹果":120, "香蕉":200, "橙子":150, "梨子":80}

merged = {}
for fruit in Dic1:
    merged[fruit] = {
        "价格": Dic1[fruit],
        "库存": Dic2.get(fruit, 0)
    }

total_value = sum(info["价格"] * info["库存"] for info in merged.values())

min_stock = min(info["库存"] for info in merged.values())
min_fruits = [(fruit, info) for fruit, info in merged.items() if info["库存"] == min_stock]

print("合并后的字典：")
for fruit, info in merged.items():
    print(f"{fruit}: 价格={info['价格']}元，库存={info['库存']}斤")

print("\n总库存价值:", round(total_value, 2), "元")

print("\n库存最少的商品:")
for fruit, info in min_fruits:
    print(f"名称：{fruit}，价格：{info['价格']}元，库存：{info['库存']}斤")