import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from btree import BPlusTree  # noqa: E402


def test_insert_and_search():
    t = BPlusTree(order=4)
    for i in range(1, 11):
        t.insert(i, i * 10)
    for i in range(1, 11):
        assert t.search(i) == i * 10
    assert t.search(99) is None
    assert t.search(0) is None


def test_overwrite_same_key():
    t = BPlusTree(order=4)
    t.insert(5, "a")
    t.insert(5, "b")
    assert t.search(5) == "b"


def test_range_scan_ordered():
    t = BPlusTree(order=4)
    for i in [5, 1, 4, 2, 6, 3]:
        t.insert(i, i)
    assert t.range_query(2, 5) == [(2, 2), (3, 3), (4, 4), (5, 5)]
    assert t.range_query(1, 1) == [(1, 1)]
    assert t.range_query(0, 100) == [(i, i) for i in range(1, 7)]


def test_split_promotes_and_heights():
    t = BPlusTree(order=4)
    for i in range(1, 9):
        t.insert(i, i)
    st = t.stats()
    assert st["entries"] == 8
    assert st["height"] >= 2          # 叶子满分裂 -> 内部节点出现
    assert st["internal_nodes"] >= 1
    for i in range(1, 9):
        assert t.search(i) == i


def test_many_inserts_balanced():
    t = BPlusTree(order=4)
    for i in range(1, 501):
        t.insert(i, i)
    st = t.stats()
    assert st["entries"] == 500
    assert st["height"] <= 6
    for i in (1, 250, 500):
        assert t.search(i) == i
    assert len(t.range_query(1, 500)) == 500


def test_delete_rebalances():
    t = BPlusTree(order=4)
    for i in range(1, 13):
        t.insert(i, i)
    for i in (6, 7, 8):
        t.delete(i)
    assert t.search(6) is None
    assert t.search(8) is None
    assert t.search(5) == 5
    assert t.search(9) == 9
    expect = [(i, i) for i in range(1, 13) if i not in (6, 7, 8)]
    assert t.range_query(1, 12) == expect


def test_delete_borrow_or_merge_keeps_consistency():
    t = BPlusTree(order=4)
    for i in range(1, 21):
        t.insert(i, i)
    # 逐个删掉一半，始终保证可查、范围有序
    for i in range(1, 11):
        t.delete(i)
    assert t.stats()["entries"] == 10
    for i in range(1, 11):
        assert t.search(i) is None
    expect = [(i, i) for i in range(11, 21)]
    assert t.range_query(1, 30) == expect


def test_delete_all_shrinks():
    t = BPlusTree(order=4)
    for i in range(1, 9):
        t.insert(i, i)
    for i in range(1, 9):
        t.delete(i)
    st = t.stats()
    assert st["entries"] == 0
    assert t.search(3) is None
    assert t.range_query(1, 9) == []


def test_root_shrinks_after_heavy_delete():
    t = BPlusTree(order=4)
    for i in range(1, 33):
        t.insert(i, i)
    h_before = t.stats()["height"]
    assert h_before >= 3
    for i in range(1, 29):
        t.delete(i)
    st = t.stats()
    assert st["entries"] == 4
    assert st["height"] < h_before     # 大量删除后树降层
    assert t.search(32) == 32


def test_stats_fields():
    t = BPlusTree(order=4)
    t.insert(1, "x")
    st = t.stats()
    assert set(st.keys()) >= {"height", "nodes", "internal_nodes",
                              "leaf_nodes", "entries"}
    assert st["entries"] == 1
    assert st["leaf_nodes"] >= 1
    assert st["nodes"] == st["internal_nodes"] + st["leaf_nodes"]
