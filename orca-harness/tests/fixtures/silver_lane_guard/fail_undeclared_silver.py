# fixture_expected: fail -- a silver-named lane not declared in the registry (G1).
def write(data_root):
    data_root.append_record(
        subtree="derived",
        raw_anchor="anchor",
        lane="experiments_silver",
        record_id="r.json",
        data=b"{}\n",
    )
