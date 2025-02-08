# Filter Sensitive Words Simply and Quickly for Chinese

The repository is used to create an simple API for filtering sensitive words. I implement sensitive word filtering by deterministic finite automaton (DFA) and [jieba](https://github.com/fxsjy/jieba) segmentation. Specifically, I perform a text segmentation and then execute DFA on a chunk level. As a result, it avoids incorrect filtering of words like “天性爱玩”.

## Usage

1. Install the dependencies;
    ```bash
    pip install -r requirements.txt
    ```
2. Set your environment config in the file `.env`;
3. Start up the server;
    ```bash
    sh start.sh
    ```
4. Visit the local url `0.0.0.0:12223/docs` (default setting) to see how to use the API.
