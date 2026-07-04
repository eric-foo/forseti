# fixture_expected: pass -- non-strict is a coverage note only; CI --strict must fail an unresolved lane arg.
def write(data_root, lane):
    data_root.append_record(
        subtree="derived",
        raw_anchor="anchor",
        lane=lane,
        record_id="r.json",
        data=b"{}\n",
    )
