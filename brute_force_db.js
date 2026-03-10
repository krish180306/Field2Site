import mysql from 'mysql2/promise';

const passwords = ['123456', '', 'root', 'admin', 'password', '12345678', 'mysql'];

async function bruteForce() {
    for (const pwd of passwords) {
        console.log(`Trying password: "${pwd}"`);
        try {
            const connection = await mysql.createConnection({
                host: 'localhost',
                user: 'root',
                password: pwd,
                database: 'rental_system'
            });
            console.log(`SUCCESS! Password is: "${pwd}"`);
            await connection.end();
            process.exit(0);
        } catch (err) {
            console.log(`Failed: ${err.message}`);
        }
    }

    // Also try without database name (maybe it doesn't exist yet)
    for (const pwd of passwords) {
        console.log(`Trying password (no DB): "${pwd}"`);
        try {
            const connection = await mysql.createConnection({
                host: 'localhost',
                user: 'root',
                password: pwd
            });
            console.log(`SUCCESS (no DB)! Password is: "${pwd}"`);
            await connection.end();
            process.exit(0);
        } catch (err) {
            console.log(`Failed (no DB): ${err.message}`);
        }
    }

    console.log('All attempts failed.');
}

bruteForce();
