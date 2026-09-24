"""B+ 树索引引擎（插入分裂 / 查找 / 范围扫描 / 删除合并）。

模型：
- BPlusTree(order)：order 为节点最大键数（默认 4）。
- 内部节点：keys + children（children 长度 = keys+1，
  children[i] 指向键 < keys[i] 的子树）。
- 叶子节点：keys + values + next（叶子链，支持范围扫描）。
- 插入：叶子满（> order）分裂，中间键上提，根满则树高 +1。
- 删除：叶子下溢（< ceil(order/2)）先借兄弟，借不到合并。
"""
from __future__ import annotations


class BNode:
    """统一节点。leaf=True 时用 values/next；否则用 children。"""

    def __init__(self, leaf: bool):
        self.leaf = leaf
        self.keys: list = []
        self.values: list | None = [] if leaf else None
        self.children: list | None = None if leaf else []
        self.next: "BNode | None" = None


class BPlusTree:
    def __init__(self, order: int = 4):
        self.order = order
        self.root = BNode(leaf=True)

    # -------------------------------------------------- 公开接口
    def insert(self, key, value) -> None:
        """插入 (key, value)；同 key 覆盖写。满节点沿路径分裂。"""
        raise NotImplementedError

    def search(self, key):
        """返回 key 对应的 value；不存在返回 None。"""
        raise NotImplementedError

    def range_query(self, k1, k2) -> list:
        """返回 [(key, value)...] 按 key 升序。"""
        raise NotImplementedError

    def delete(self, key) -> None:
        """删除 key（不存在则忽略）。必要时借兄弟或合并。"""
        raise NotImplementedError

    def stats(self) -> dict:
        """返回 {height, nodes, internal_nodes, leaf_nodes, entries}。
        height：从根到叶子的层数（空树 0，只有根叶子 1）。"""
        raise NotImplementedError
