# collect-alpha API 목록

## create table

1. Hbase에 새로운 table을 추가한다. ( [http://(서버ip):2000/create-table](http://ip:2000/create-table) )
2. 상세
    - POST method
    - body Datagram

    ```jsx
    {
    	table_name : 'table_name',
    	column_family_name : {
    		"column_family1 name": {},
    		"column_family2 name" : {},	
    	}
    }
    ```

    - table_name을 이름으로, column_family_name의 column_family들을 가지는 table을 생성한다,
3. 결과
    - 유효하지 않은 Datagram 입력 시
        1. table_name이 없음 : "There is no table name (table_name)"
        2. column_family_name이 없음 : 해당 부분을 "cf1"으로 초기화 하여 테이블 생성
    - 테이블 생성 성공 시
        1. "Creating the 'table_name' table"

## table list

1. Hbase의 table 목록을 반환한다. ( [http://(서버ip):2000/](http://ip:2000/create-table)table-list)
2. 상세
    - GET method
    - argument 불필요
3. 결과
    - 반환 실패 시
        1. Hbase의 오류 내용을 반환
    - 테이블 생성 성공 시
        1. table list를 반환

## put-rows

1. Hbase의 특정 table에 row들을 추가한다. ( [http://(서버ip):2000/](http://ip:2000/create-table)put-rows)
2. 상세
    - POST method
    - body Datagram

    ```jsx
    {
    	table_name : 'table_name',
    	datalist : [
    		{rowkey: '1',{'cf1:col1': '1', 'cf1:col2': '2'}},
        {rowkey: '2',{'cf1:col1': '3', 'cf1:col2': '4'}},
    			. . . 
    	],
    }
    ```

    - table_name에 해당하는 table에 datalist들을 추가한다.
3. 결과
    - 해당 요청을 처리하는 server의 ip를 반환한다.

## delete table

1. Hbase의 특정 table을 삭제한다 ( [http://(서버ip):2000/](http://ip:2000/create-table)delete-table?table_name="테이블 이름")
2. 상세
    - GET method
    - arguments
        1. delete-table : 삭제하고자하는 table 이름
3. 결과
    - 유효하지 않은 arguments
        1. table_name이 없음 : "There is no table name(table_name)"
    - Hbase에서 처리 실패
        1. 해당 table_name 미존재 : "There is no table name corresponding to hbase."
    - 삭제 성공 시
        1. "Deleting the 'table_name' table"

## scan

1. Hbase의 특정 table에서 Scanning을 수행한다 ( [http://(서버ip):2000/](http://ip:2000/create-table)scan)
2. 상세
    - POST method
    - body Datagram

    ```jsx
    {
    			table_name : 'table_name',
    			filter : "filter string",
    			row_start : 'row_start'
    			row_stop : 'row_stop',
    }
    ```

    - table_name에 해당하는 table에서 filter에 해당하는 row들을 Scan. 그 범위는 row_start에서 row_stop까지 해당된다.
    - filter string
        1. Hbase Scanner를 생성하는 Pseudo string
        2. Reference site : [https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/admin_hbase_filtering.html](https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/admin_hbase_filtering.html)
        3. 예시 : "SingleColumnValueFilter('ID','BLD_NM',=,'regexstring:경북대학교',true,true)"

            해당 필터는 Column family = ID, Column = BLD_NM인 칼럼의 값이 경북대를 포함하고 있는 row들을 반환한다.

3. 결과
    - Scanning 결과를 반환
    - 결과 datagram

        ```jsx
        {
        			row_key: String,
        			row_data: Object,
        }
        ```
