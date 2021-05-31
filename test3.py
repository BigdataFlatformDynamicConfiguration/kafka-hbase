import happybase
    connection = happybase.Connection(host="test-hbase-master", port=9090)
    connection.open()
    table = connection.table('Daegue')
    rse = table.scan(filter="SingleColumnValueFilter('ID','BLD_NM',=,'binary:경북대학교',true,true)")