import os, re

# 任务一：加载知识库并分块（chunk）
def load_kb(kb="step3", size=320, overlap=60):
    docs=[]
    for fn in sorted(os.listdir(kb)):
        if not fn.endswith(".txt"):
            continue
        txt=open(os.path.join(kb,fn),encoding="utf-8").read()
        i=0
        cid=0
        while i < len(txt):
            # ##########   Begin   ##########
            # 1. 计算本次 chunk 的结束位置
            end = i + size
            if end > len(txt):
                end = len(txt)

            # 2. 保存 (来源文件名, chunk编号, chunk文本)
            docs.append((fn, cid, txt[i:end]))

            # 3. 为当前 chunk 编号递增一次，并把指针 i 移到下一段的起点
            cid += 1
            if end == len(txt):
                break
            i += size - overlap
            # ##########   End   ##########
    return docs

# 任务二：实现 TopK 检索（按关键词重叠度排序）
def retrieve(question, docs, k=3):
    tok=r"[A-Za-z0-9]+|[\u4e00-\u9fff]"  # 英文按词，中文按字（入门演示够用）
    q=set(re.findall(tok, question.lower()))
    scored=[]
    for src, cid, text in docs:
        s=len(q & set(re.findall(tok, text.lower())))
        if s>0:
            scored.append((s, src, cid, text))
    # ##########   Begin   ##########
    # 分数从高到低排序，取 TopK
    scored.sort(key=lambda x: (x[0], x[2]), reverse=True)
    return scored[:k]
    # ##########   End   ##########

# 任务三：把检索结果拼成【资料】，让模型只根据资料回答
def rag_answer(question, docs, chat_func):
    hits=retrieve(question, docs, k=3)
    ctx="\n\n".join([f"[{src}#{cid} score={s}]\n{text}" for s,src,cid,text in hits]) or "(空)"
    msgs=[
        # ##########   Begin   ##########
        # 构造发给模型的 msgs，要求模型只能根据【资料】回答
        {"role":"system","content":"你是一个只能根据资料回答的助手。请严格只根据【资料】中的信息回答问题。如果资料中没有相关信息，请直接说「我不知道」，不要编造或使用你自己的知识。"},
        # ##########   End   ##########
        {"role":"user","content":f"问题：{question}\n\n【资料】\n{ctx}"}
    ]
    return chat_func(msgs), hits