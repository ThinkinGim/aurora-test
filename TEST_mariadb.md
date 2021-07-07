// npm install --save mariadb

const mariadb = require('mariadb');

const pool = mariadb.createPool({
    host: 'deploy-sample-auroranest-bmtauroraclusterb2799f1e-165v0e9hvurh7.cluster-crt3boedqse3.ap-northeast-2.rds.amazonaws.com',
    port: 3306,
    user: 'admin',
    password: '_mjT=Q63D5dPl,ie_jSrmcNU8fj82=',
    connectionLimit: 5
});

const init = async () => {
  console.log(pool.config)
  while (true){
    test();
    await sleep(1000);
  }
}

const sleep = (ms) => {
  return new Promise(resolve=>{
          setTimeout(resolve,ms)
  })
}

const test = async () => {
  try{
      conn = await pool.getConnection();
      const [rows] = await conn.query('SELECT now(), @@read_only, @@innodb_read_only, @@hostname');
      console.log(rows)
  }
  catch(err){
      console.log(err)
  }
  finally{
      if (conn) conn.end();
  }
}

init();