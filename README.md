# kafka-hbase

kubectl exec alpha-collect-alpha-0 -- python3 /modules/app.py 'alpha-kafka' 'alpha-hbase-master'

1. create table

post 방식
post('/create-table',{
     'table_name' : 'Daegue',
     'column_family_name' : {
         'ID': {},
         'data': {},
     }
})

ex) http://ip:2000/create-table

table_name 없을 시 : There is no table name(table_name). 반환 ,
column_family_name 없을 시 : column_family_name 을 cf1 으로 초기화 하여 테이블 생성
성공 시 : Creating the 테이블 명 table 반환

2. table list

get 방식
쿼리인자 - 필요 없음
ex)  http://ip:2000/table-list
http://34.64.100.75:2000/table-list

성공 시 테이블 리스트 반환
실패 시 fail 반환

3. put-rows

post 방식
{
"table_name" : "my-topic11",
 "datalist" : 
[
{"rowkey":"1", "data": {"cf1:col1" : "1","cf1:col2" : "2",}},
{"rowkey":"2", "data": {"cf1:col1" : "3","cf1:col2" : "4",}}
]
}

table_name으로 Hbase table을 연 뒤
datalist 의 값으로 데이터 insert 수행

ex) http://ip:2000/put-rows

4.delete table
get 방식
쿼리인자 -  - table_name : 필수

table_name 없을 시 : There is no table name(table_name). 반환 ,
table_name 이 hbase table 명이랑 일치하지 않으면 'There is no table name corresponding to hbase.' 반환,
성공 시 : ‘Deleting the 테이블 명 table’ 반환

ex)  http://34.64.94.147:2000/delete-table?table_name=aaa

5.scan
post 방식
body // 사용하지 않으면 안넣으면 됨
table(str) - 테이블 이름 필수
row_start (str) – the row key to start at (inclusive)
row_stop (str) – the row key to stop at (exclusive)
filter (str) – a filter string (optional)
return
Returns:	generator yielding the rows matching the scan
Return type:	iterable of (row_key, row_data) tuples
https://blog.voidmainvoid.net/236
https://nabillera.tistory.com/entry/HBase-%EA%B3%B5%EB%B6%80-Scan-Filter
https://madist.github.io/2018/06/06/Hbase-Shell/

