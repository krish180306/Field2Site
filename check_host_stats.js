import mysql from 'mysql2/promise';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.join(__dirname, 'server', '.env') });

async function check() {
    const pool = mysql.createPool({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME
    });

    try {
        const [p] = await pool.execute('SELECT COUNT(*) as count FROM BOOKING WHERE Host_ID = 6 AND Status = "Pending"');
        const [r1] = await pool.execute('SELECT COUNT(*) as count FROM FARM_EQUIPMENT WHERE Host_ID = 6 AND Availability_Status = "Rented"');
        const [r2] = await pool.execute('SELECT COUNT(*) as count FROM CONSTRUCTION_EQUIPMENT WHERE Host_ID = 6 AND Availability_Status = "Rented"');

        console.log(`JSON_START:{"pending":${p[0].count},"rentedFarm":${r1[0].count},"rentedConst":${r2[0].count}}:JSON_END`);
    } catch (err) {
        console.error(err);
    } finally {
        await pool.end();
    }
}

check();
