const mysql = require('mysql2');

const dbPoolConfig = {
    debug: 0,
    enableKeepAlive: true,
    connectionLimit : 10,
    host: 'deploy-sample-auroranest-bmtauroraclusterb2799f1e-165v0e9hvurh7.cluster-crt3boedqse3.ap-northeast-2.rds.amazonaws.com',
    user: 'admin',
    password: '_mjT=Q63D5dPl,ie_jSrmcNU8fj82=',
    database: 'mysql'
}
const connPool = mysql.createPool(dbPoolConfig);

const init = async () => {
    while (true){
        dbTest();
        await sleep(1000);  
    }
}

const sleep = (ms) => {
  return new Promise(resolve=>{
      setTimeout(resolve,ms)
  })
}

const dbTest = () => {
    return connPool.getConnection(function(err, conn) {
        if(err) {
            console.log(err);
            if (conn){
                conn.destroy();
            }
            return false;
        } else if(conn){
            conn.query(
                'SELECT now(), @@read_only, @@innodb_read_only, @@hostname',
                (err, rows, fields) => {
                    if(err) {
                        console.log(err);
                    }
                    if(rows) {
                        console.log(rows);
                    }
                }
            );
            conn.release();
            return true;
        } 
    })

};

init();

/*
    https://github.com/sidorares/node-mysql2/issues/1103
    https://github.com/sidorares/node-mysql2/blob/07a429d9765dcbb24af4264654e973847236e0de/lib/pool_cluster.js

*/