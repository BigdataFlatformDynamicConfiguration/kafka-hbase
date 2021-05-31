import happybase
    connection = happybase.Connection(host="test-hbase-master", port=9090)
    connection.open()
    table = connection.table('Daegue')