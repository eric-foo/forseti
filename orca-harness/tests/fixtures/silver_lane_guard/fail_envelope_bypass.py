# fixture_expected: fail -- raw append to a silver_envelope lane that is NOT pending; must use the front-door (G2).
def write(data_root):
    data_root.append_record(
        subtree="derived",
        raw_anchor="anchor",
        lane="cleaning_fragrantica_silver",
        record_id="r.json",
        data=b"{}\n",
    )
