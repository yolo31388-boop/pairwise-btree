# Pair-wise GSB 基线：B+ 树索引引擎

题目（feature 迭代）：实现 B+ 树索引引擎（插入分裂 / 查找 / 范围扫描 / 删除合并）。

- 骨架：`btree.py`（方法均 `raise NotImplementedError`）
- 验收：`python -m pytest tests/test_btree.py -q` 全绿
- 约束：只 import 标准库；必须真实维护 B+ 树结构（不能退化成排序 list）
