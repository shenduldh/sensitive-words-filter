import jieba


class DFA:
    def __init__(self):
        self.chains = {}
        self.end = "\x00"

    def add(self, chunks):
        chunks = [i.strip().lower() for i in chunks]

        level = self.chains
        for i, c in enumerate(chunks):
            if c in level:
                level = level[c]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chunks)):
                    level[chunks[j]] = {}
                    last_level, last_char = level, chunks[j]
                    level = level[chunks[j]]
                last_level[last_char] = {self.end: 0}
                break
        if i == len(chunks) - 1:
            level[self.end] = 0

    def filter(self, chunks, replace_char="*"):
        lower_chunks = [i.lower() for i in chunks]
        results = []
        start = 0
        is_sensitive = False
        dirty_chunks = []

        while start < len(lower_chunks):
            level = self.chains
            step = 0
            local_chunks = []

            for chunk in lower_chunks[start:]:
                if chunk in level:
                    step += 1
                    local_chunks.append(chunk)

                    if self.end not in level[chunk]:
                        level = level[chunk]
                    else:
                        is_sensitive = True
                        dirty_chunks.append("".join(local_chunks))
                        results.append(replace_char * len(dirty_chunks[-1]))
                        start += step - 1
                        break
                else:
                    results.append(chunks[start])
                    break
            else:
                results.append(chunks[start])

            start += 1

        return is_sensitive, "".join(results), dirty_chunks


class SensitiveFilter:
    def __init__(self, sensitive_words_path, tokenized_words_path) -> None:
        self.jieba = jieba
        self.dfa = DFA()
        self.add_sensitive_words(sensitive_words_path)
        self.add_tokenized_words(tokenized_words_path)

    def cut(self, text):
        return list(self.jieba.cut(text, cut_all=False, HMM=True))

    def add_sensitive_words(self, path):
        with open(path, "r", encoding="utf-8") as f:
            for i in f:
                i = i.strip()
                if i:
                    self.dfa.add(i)
                    self.dfa.add(self.cut(i))

    def add_tokenized_words(self, path):
        with open(path, "r", encoding="utf-8") as f:
            for i in f:
                i = i.strip()
                if i:
                    jieba.add_word(i, freq=999)

    def filter(self, text, replace_char="*"):
        return self.dfa.filter(self.cut(text), replace_char)


if __name__ == "__main__":
    sstft = SensitiveFilter("assets/sensitive_words.txt", "assets/tokenized_words.txt")

    text = "天性爱玩"
    filtered = sstft.filter(text)
    print(filtered)
