const mysql = require('mysql2');

const dbPoolConfig = {
    connectionLimit : 10,
    host: 'deploy-sample-auroranest-bmtauroraclusterb2799f1e-165v0e9hvurh7.cluster-crt3boedqse3.ap-northeast-2.rds.amazonaws.com',
    user: 'admin',
    password: '_mjT=Q63D5dPl,ie_jSrmcNU8fj82=',
    database: 'mysql'
}
const poolCluster = mysql.createPoolCluster();
var offsetPrimary = 0;

const init = async () => {
    poolCluster.add(offsetPrimary.toString(), dbPoolConfig);
    console.log('initialized  connection pool for Primary database')

    console.log('Starting loop...')
    while (true){
        result = dbTest();
        console.log(result);

        await sleep(1000);  
    }
}

const sleep = (ms) => {
  return new Promise(resolve=>{
          setTimeout(resolve,ms)
  })
}

const nextPool = () => {
  return new Promise(resolve=>{
      offsetPrimary++;
      console.log('Offset: '+offsetPrimary)
      poolCluster.add(offsetPrimary.toString(), dbPoolConfig);
  })
}


const dbTest = () => {
    
	try {
        console.log('offset: '+offsetPrimary.toString())
        return poolCluster.getConnection(offsetPrimary.toString(), function (err, connection) {
            if(err){
                console.log(err);
                return false;
            }

            try {
                return connection.query(
                    'SELECT now(), @@read_only, @@innodb_read_only, @@hostname', 
                    function (error, results, fields) {
                        if(error) {
                            console.log(error);
                            return false;
                        } else {
                            console.log(results);
                            return true;
                        }
                    }
                );
            } catch (err) {
                console.log(err);
                return false;
            } finally {
                if (connection) connection.release();
            }
        });
    } 
    catch(err) {
        console.log('Error from getting connection');
        console.log(err);

		return false;
	}
};

init();

/*
    https://github.com/sidorares/node-mysql2/issues/1103
*/